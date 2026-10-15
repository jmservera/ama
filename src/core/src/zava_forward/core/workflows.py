"""Return and reopen, handoff states and safety referral workflows.

Each step is a small, checked state change by a named person with a reason, and
each is written to the audit ledger. None of them decides anything for a
person: the system records, enforces who may do what, and refuses steps that
skip a state.
"""
from copy import deepcopy
from datetime import UTC, date, datetime

from . import controls, insights, projection

MANAGER_ROLES = ("Retrofit Programme Manager", "Programme Support Officer")
HAZARD_PRIORITIES = ("Emergency", "Significant", "Routine")
HAZARD_CATEGORIES = ("Damp and mould", "Structural", "Electrical", "Other")
SAFETY_ROLES = ("Building Safety Liaison",) + MANAGER_ROLES
HANDOFF_OPEN = "Offered"
HANDOFF_PENDING = (HANDOFF_OPEN, "Received", "Escalated")
HANDOFF_ACTIVE = HANDOFF_PENDING + ("Accepted",)
HANDOFF_STATUS = {"Offered": "Sent", "Declined": "Rejected"}


def _today():
    return date.today().isoformat()


def _now():
    return datetime.now(UTC).isoformat(timespec="minutes")


def _due(value):
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError("Enter a due date with a time and timezone.") from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Enter a due date with a time and timezone.")
    return parsed.astimezone(UTC).isoformat(timespec="minutes")


def handoff_view(c):
    """Project accountability separately from an offer or receipt; never mutate stored history."""
    if not c.get("handoff"):
        return None
    h = deepcopy(c["handoff"])
    accepted = h["state"] in ("Accepted", "Completed")
    h.update(status=HANDOFF_STATUS.get(h["state"], h["state"]),
             accountable_owner=c["owner"], accountable_owner_code=c["owner_code"],
             destination=h.get("to_role"), proposed_receiver=h.get("to_name"),
             confirmed_receiver=h.get("to_name") if accepted else None,
             chase_owner=c["owner"] if accepted else h.get("from_name"),
             chase_owner_code=c["owner_code"] if accepted else h.get("from_code"))
    for key in ("due_at", "urgency", "next_action", "resident_update_owner", "resident_update_due_at"):
        h.setdefault(key, None)
    return h


def hazard_state(h):
    if h["released"]:
        return "Released"
    if h.get("repaired"):
        return "Repaired, awaiting release"
    if h.get("referred"):
        return "Referred"
    return "Raised"


class WorkflowMixin:
    # ---- return and reopen
    def _disposition(self, c, user, was, to, reason, metadata, reopened=False):
        metadata = metadata if metadata is not None else {}
        source = controls.text(metadata.get("source"), "the source reference")
        next_action = controls.text(metadata.get("next_action"), "the next action")
        return dict(version=len(c.get("returns", [])) + 1, at=_now(), by=user["name"],
                    from_stage=was, to_stage=to, reason=reason, reopened=reopened,
                    source=source or None, next_action=next_action or None,
                    initiating_authority=dict(email=user["email"], code=user["code"], role=user["role"]),
                    receiving_owner=dict(code=c["owner_code"], name=c["owner"], role=c["owner_role"]))

    def return_case(self, user, case_id, to_stage, reason, metadata=None):
        controls.require_role(user, projection.STAFF_ROLES, "an authorised staff reviewer can return a case")
        reason = controls.text(reason, "why the case is being returned")
        with self.lock:
            c = self._case(case_id)
            self.guard_case_event(c)
            if c["closed"]:
                raise ValueError("This case is closed. A manager can reopen it.")
            order = insights.STAGE_ORDER
            if c["stage"] not in order or to_stage not in order or order.index(to_stage) >= order.index(c["stage"]):
                raise ValueError("A case can only be returned to an earlier stage.")
            was = c["stage"]
            rec = self._disposition(c, user, was, to_stage, reason, metadata)
            for a in c["appointments"]:
                if was == "Install booked" and a["outcome"] == "Booked":
                    a["outcome"] = "Cancelled"
            c["decision"] = c["decision"] if to_stage not in ("Contacting resident", "Waiting for resident decision") \
                else dict(status="Waiting" if to_stage == "Waiting for resident decision" else "Not yet asked", by=user["name"], at=_today())
            c.update(stage=to_stage, stage_since=_today(), days_in_stage=0, reason="after being returned", waiting_on=c["owner"])
            c.setdefault("returns", []).append(rec)
            self.audit(user["email"], "return_case", case_id, f"{was} -> {to_stage}: {reason}")
            self.save()

    def reopen_case(self, user, case_id, reason, metadata=None):
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError("Only a manager can reopen a closed case.")
        reason = controls.text(reason, "why the case is being reopened")
        with self.lock:
            c = self._case(case_id)
            if not c["closed"]:
                raise ValueError("This case is already open.")
            was = c["stage"]
            to = "Aftercare issue" if was == "Completed" else "Contacting resident"
            rec = self._disposition(c, user, was, to, reason, metadata, reopened=True)
            if to == "Contacting resident":
                c["decision"] = dict(status="Not yet asked", by=user["name"], at=_today())
            c.update(closed=False, stage=to, stage_since=_today(), days_in_stage=0, reason="after being reopened", waiting_on=c["owner"])
            c.setdefault("returns", []).append(rec)
            self.audit(user["email"], "reopen_case", case_id, f"{was} -> {to}: {reason}")
            self.save()

    # ---- receipt is not acceptance; only acceptance transfers case ownership
    def _staff_person(self, email):
        if not isinstance(email, str):
            raise ValueError("Choose a colleague to take this over.")
        p = self.staff.get((email or "").lower())
        if not p or p["role"] not in projection.STAFF_ROLES:
            raise ValueError("Choose a colleague to take this over.")
        return p

    def offer_handoff(self, user, case_id, to_email, note="", metadata=None):
        controls.require_role(user, projection.STAFF_ROLES, "a staff owner or manager can offer a handoff")
        to = self._staff_person(to_email)
        metadata = metadata or {}
        due_at = _due(metadata.get("due_at"))
        update_due = _due(metadata.get("resident_update_due_at"))
        urgency = metadata.get("urgency") or None
        if urgency not in (None, "Routine", "Urgent"):
            raise ValueError("Choose Routine or Urgent for handoff urgency.")
        update_owner = self._staff_person(metadata["resident_update_to"]) if metadata.get("resident_update_to") else None
        with self.lock:
            c = self._case(case_id)
            if c["closed"]:
                raise ValueError("This case is closed.")
            if c["owner_code"] != user["code"] and user["role"] not in MANAGER_ROLES:
                raise PermissionError("Only the owner or a manager can offer this case to someone else.")
            if to["code"] == c["owner_code"]:
                raise ValueError("That colleague already owns this case.")
            cur = c.get("handoff")
            if cur and cur["state"] in HANDOFF_ACTIVE:
                raise ValueError("A handoff is already waiting for an answer.")
            previous_update = c.get("resident_update") or {}
            if previous_update and (
                (update_owner and update_owner["name"] != previous_update.get("owner"))
                or (update_due and update_due != previous_update.get("due_at"))
            ):
                raise ValueError("A resident-update commitment already exists. Preserve it during handoff.")
            resident_update = previous_update or dict(owner=update_owner["name"] if update_owner else None,
                                                      due_at=update_due)
            c["handoff"] = dict(state=HANDOFF_OPEN, from_code=c["owner_code"], from_name=c["owner"], to_code=to["code"], to_name=to["name"],
                                to_role=to["role"], offered_by=user["name"], offered_at=_now(), note=(note or "")[:300],
                                answered_at=None, answer_note="", due_at=due_at, urgency=urgency,
                                next_action=controls.text(metadata.get("next_action"), "", required=False) or None,
                                resident_update_owner=resident_update.get("owner"),
                                resident_update_due_at=resident_update.get("due_at"))
            if not previous_update and (update_owner or update_due):
                c["resident_update"] = resident_update
            self._handoff_event(c, user)
            self.audit(user["email"], "handoff_offered", case_id, f"to {to['name']} {note or ''}".strip())
            self.save()

    def _open_offer(self, c, user, who):
        controls.require_role(user, projection.STAFF_ROLES, "authorised staff can act on handoffs")
        h = c.get("handoff")
        if not h or h["state"] not in HANDOFF_PENDING:
            raise ValueError("There is no handoff waiting for an answer.")
        if who == "recipient" and h["to_code"] != user["code"]:
            raise PermissionError("This handoff was offered to someone else.")
        if who == "offerer" and h["from_code"] != user["code"] and user["role"] not in MANAGER_ROLES:
            raise PermissionError("Only the person who offered it, or a manager, can withdraw it.")
        return h

    def _handoff_event(self, c, user):
        events = c.setdefault("handoff_history", [])
        events.append(dict(handoff_view(c), version=len(events) + 1, at=_now(),
                           by=user["email"], authority=user["role"]))

    def receive_handoff(self, user, case_id):
        with self.lock:
            c = self._case(case_id)
            h = self._open_offer(c, user, "recipient")
            if h["state"] != HANDOFF_OPEN:
                raise ValueError("Only a sent handoff can be marked received.")
            h.update(state="Received", received_at=_now(), received_by=user["email"])
            self._handoff_event(c, user)
            self.audit(user["email"], "handoff_received", case_id, "Receipt recorded; ownership unchanged")
            self.save()

    def accept_handoff(self, user, case_id):
        with self.lock:
            c = self._case(case_id)
            h = self._open_offer(c, user, "recipient")
            c.update(owner=user["name"], owner_code=user["code"], owner_role=user["role"], waiting_on=user["name"])
            h.update(state="Accepted", answered_at=_now())
            c.setdefault("handoff_log", []).append(dict(h))
            self._handoff_event(c, user)
            self.audit(user["email"], "handoff_accepted", case_id, f"from {h['from_name']}")
            self.save()

    def decline_handoff(self, user, case_id, reason):
        reason = controls.text(reason, "why you cannot take this on")
        with self.lock:
            c = self._case(case_id)
            h = self._open_offer(c, user, "recipient")
            h.update(state="Declined", answered_at=_now(), answer_note=reason)
            c.setdefault("handoff_log", []).append(dict(h))
            self._handoff_event(c, user)
            self.audit(user["email"], "handoff_declined", case_id, reason)
            self.save()

    def withdraw_handoff(self, user, case_id):
        with self.lock:
            c = self._case(case_id)
            h = self._open_offer(c, user, "offerer")
            h.update(state="Withdrawn", answered_at=_now())
            c.setdefault("handoff_log", []).append(dict(h))
            self._handoff_event(c, user)
            self.audit(user["email"], "handoff_withdrawn", case_id, f"offer to {h['to_name']}")
            self.save()

    def escalate_handoff(self, user, case_id, to_email, reason):
        reason = controls.text(reason, "why this handoff needs escalation")
        to = self._staff_person(to_email)
        if to["role"] not in MANAGER_ROLES:
            raise ValueError("Choose a manager for the escalation.")
        with self.lock:
            c = self._case(case_id)
            h = self._open_offer(c, user, "offerer")
            if h["state"] == "Escalated":
                raise ValueError("This handoff has already been escalated.")
            h.update(state="Escalated", escalated_at=_now(), escalation_owner=to["name"],
                     escalation_owner_code=to["code"], answer_note=reason)
            self._handoff_event(c, user)
            self.audit(user["email"], "handoff_escalated", case_id, f"to {to['code']}: {reason}")
            self.save()

    def complete_handoff(self, user, case_id, note):
        note = controls.text(note, "the completed action")
        with self.lock:
            c = self._case(case_id)
            controls.require_role(user, projection.STAFF_ROLES, "the accepting case owner can complete a handoff")
            h = c.get("handoff")
            if not h or h["state"] != "Accepted":
                raise ValueError("Accept the handoff before completing it.")
            if h["to_code"] != user["code"] or c["owner_code"] != user["code"]:
                raise PermissionError("Only the accepting case owner can complete this handoff.")
            h.update(state="Completed", completed_at=_now(), completion_note=note)
            self._handoff_event(c, user)
            self.audit(user["email"], "handoff_completed", case_id, note)
            self.save()

    def pending_handoffs(self, user):
        controls.require_role(user, projection.STAFF_ROLES, "authorised staff can view handoffs")
        with self.lock:
            rows = []
            for c in self.cases.values():
                h = handoff_view(c)
                if h and h["state"] in HANDOFF_PENDING and (
                    user["code"] in (h.get("from_code"), h.get("to_code"))
                    or user["role"] in MANAGER_ROLES
                ):
                    rows.append(dict(case_id=c["id"], resident=c["resident"]["name"],
                                     address=c["home"]["address"], **h))
            return rows if projection.can_see_reason(user) else projection.hold_notes(rows)

    # ---- safety referral: raised, referred, repaired, then released by someone else
    def _hazard(self, c, idx):
        try:
            return c["hazards"][int(idx)]
        except (IndexError, ValueError, TypeError):
            raise ValueError("Choose one of this case's safety issues.")

    def raise_hazard(self, user, case_id, category, priority, note=""):
        if category not in HAZARD_CATEGORIES or priority not in HAZARD_PRIORITIES:
            raise ValueError("Choose a category and a priority from the lists.")
        with self.lock:
            c = self._case(case_id)
            if c["closed"]:
                raise ValueError("This case is closed.")
            c["hazards"].append(dict(category=category, priority=priority, noticed=_today(), referred=None, repaired=None, released=False,
                                     job="", owner=c["owner"], raised_by=user["name"], note=(note or "")[:300]))
            self.audit(user["email"], "safety_raised", case_id, f"{category} {priority} {note or ''}".strip())
            if priority == "Emergency":
                self.audit(user["email"], "safety_emergency", case_id, "Emergency safety issue: refer to Building Safety Liaison the same day")
            self.save()
            return len(c["hazards"]) - 1

    def refer_hazard(self, user, case_id, idx, to_email, job):
        job = (job or "").strip()[:40]
        if not job:
            raise ValueError("Enter the repair job reference.")
        to = self._staff_person(to_email)
        if to["role"] not in SAFETY_ROLES:
            raise ValueError("Refer a safety issue to the Building Safety Liaison or a manager.")
        with self.lock:
            c = self._case(case_id)
            h = self._hazard(c, idx)
            if h["released"] or h.get("referred"):
                raise ValueError("This safety issue has already been referred.")
            h.update(referred=_today(), job=job, owner=to["name"], referred_by=user["name"])
            self.audit(user["email"], "safety_referred", case_id, f"{h['category']} to {to['name']} job {job}")
            self.save()

    def record_repair(self, user, case_id, idx):
        with self.lock:
            c = self._case(case_id)
            h = self._hazard(c, idx)
            if h["released"] or h.get("repaired"):
                raise ValueError("This repair is already recorded.")
            if not h.get("referred"):
                raise ValueError("Refer the safety issue before recording a repair.")
            h.update(repaired=_today(), repaired_by=user["name"])
            self.audit(user["email"], "safety_repaired", case_id, f"{h['category']} job {h['job']}")
            self.save()

    def release_hazard(self, user, case_id, idx, note=""):
        if user["role"] not in SAFETY_ROLES:
            raise PermissionError("Only the Building Safety Liaison or a manager can release a safety issue.")
        with self.lock:
            c = self._case(case_id)
            h = self._hazard(c, idx)
            if h["released"]:
                raise ValueError("This safety issue is already released.")
            if not h.get("repaired"):
                raise ValueError("The repair must be recorded before release.")
            if user["name"] in (h.get("raised_by"), h.get("repaired_by")):
                raise PermissionError("Someone else must confirm the release: a safety issue is not released by the person who raised or repaired it.")
            h.update(released=True, released_by=user["name"], released_at=_today(), release_note=(note or "")[:300])
            self.audit(user["email"], "safety_released", case_id, f"{h['category']} job {h['job']} {note or ''}".strip())
            self.save()

    def hazard_states(self, case_id):
        with self.lock:
            return [dict(index=i, category=h["category"], priority=h["priority"], state=hazard_state(h)) for i, h in enumerate(self._case(case_id)["hazards"])]
