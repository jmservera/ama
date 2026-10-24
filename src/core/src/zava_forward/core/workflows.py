"""Return and reopen, handoff states and safety referral workflows.

Each step is a small, checked state change by a named person with a reason, and
each is written to the audit ledger. None of them decides anything for a
person: the system records, enforces who may do what, and refuses steps that
skip a state.
"""
from copy import deepcopy
from datetime import UTC, date, datetime

from . import change_provenance, controls, hazard, identity, insights, projection

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


def _now(timespec="minutes"):
    return datetime.now(UTC).isoformat(timespec=timespec)


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
        return "Retrofit hold released"
    if h.get("repaired"):
        return "Repair evidenced, hold active"
    if h.get("accepted_at"):
        return "Accepted"
    if h.get("received_at"):
        return "Received"
    if h.get("referred"):
        return "Sent" if h.get("referral_version") else "Legacy referral, evidence needed"
    return "Raised"


def hazard_view(h, case_id):
    out = deepcopy(h)
    out["state"] = hazard_state(h)
    out["service_authority"] = "Existing hazard and repairs service"
    out["classification"] = "Unverified report; service categorisation not recorded here"
    for key in ("source", "aware_at", "sent_at", "received_at", "accepted_at",
                "response_due_at", "responded_at", "resident_update_due_at", "resident_updated_at"):
        out.setdefault(key, None)
    out.setdefault("hold", dict(scope="Home", case_id=case_id, status="Released" if h["released"] else "Active",
                                accountable_role=None, legacy=True))
    out["follow_up"] = deepcopy(h.get("accepted_by") or h.get("sender"))
    return out


def _hazard_time(value, label, actual=False):
    result = _due(value)
    if result is None:
        raise ValueError(f"Add {label} with a time and timezone.")
    if actual and datetime.fromisoformat(value) > datetime.now(UTC):
        raise ValueError(f"{label} cannot be in the future.")
    return result


class WorkflowMixin:
    # ---- return and reopen
    def _disposition(self, c, user, was, to, reason, metadata, reopened=False):
        metadata = metadata if metadata is not None else {}
        source = controls.text(metadata.get("source"), "the source reference")
        next_action = controls.text(metadata.get("next_action"), "the next action")
        return dict(version=len(c.get("returns", [])) + 1, at=_now("microseconds"), by=user["name"],
                    from_stage=was, to_stage=to, reason=reason, reopened=reopened,
                    source=source or None, next_action=next_action or None,
                    source_version=controls.text(metadata.get("source_version"), "source version", required=False) or None,
                    schema="controlled-event/v1", event_type="reopen" if reopened else "return",
                    actor={k: user.get(k) for k in ("email", "code", "name", "role", "oid")},
                    initiating_authority=dict(email=user["email"], code=user["code"], role=user["role"]),
                    receiving_owner=dict(code=c["owner_code"], name=c["owner"], role=c["owner_role"]))

    def return_case(self, user, case_id, to_stage, reason, metadata=None):
        controls.require_role(user, projection.STAFF_ROLES, "an authorised staff reviewer can return a case")
        reason = controls.text(reason, "why the case is being returned")
        with change_provenance.controlled(self, user, case_id) as (c, user):
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
            self._save_workflow(user, "return_case", case_id, f"{was} -> {to_stage}: {reason}")

    def reopen_case(self, user, case_id, reason, metadata=None):
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError("Only a manager can reopen a closed case.")
        reason = controls.text(reason, "why the case is being reopened")
        with change_provenance.controlled(self, user, case_id) as (c, user):
            if not c["closed"]:
                raise ValueError("This case is already open.")
            was = c["stage"]
            to = "Aftercare issue" if was == "Completed" else "Contacting resident"
            rec = self._disposition(c, user, was, to, reason, metadata, reopened=True)
            if to == "Contacting resident":
                c["decision"] = dict(status="Not yet asked", by=user["name"], at=_today())
            c.update(closed=False, stage=to, stage_since=_today(), days_in_stage=0, reason="after being reopened", waiting_on=c["owner"])
            c.setdefault("returns", []).append(rec)
            self._save_workflow(user, "reopen_case", case_id, f"{was} -> {to}: {reason}")

    # ---- receipt is not acceptance; only acceptance transfers case ownership
    def _staff_person(self, email):
        if not isinstance(email, str):
            raise ValueError("Choose a colleague to take this over.")
        p = self.staff.get((email or "").lower()) or identity.person(self, email)
        if not p or p["role"] not in projection.STAFF_ROLES:
            raise ValueError("Choose a colleague to take this over.")
        return p

    def offer_handoff(self, user, case_id, to_email, note="", metadata=None):
        controls.require_role(user, projection.STAFF_ROLES, "a staff owner or manager can offer a handoff")
        to = self._staff_person(to_email)
        metadata = metadata if isinstance(metadata, dict) else {}
        due_at = _due(metadata.get("due_at"))
        update_due = _due(metadata.get("resident_update_due_at"))
        urgency = metadata.get("urgency") or None
        if urgency not in (None, "Routine", "Urgent"):
            raise ValueError("Choose Routine or Urgent for handoff urgency.")
        update_owner = self._staff_person(metadata["resident_update_to"]) if metadata.get("resident_update_to") else None
        with change_provenance.operation(self, user, case_id, "handoff_offered", metadata, "handoff_history") as (c, event):
            old_handoff = deepcopy(c.get("handoff"))
            old_owner = change_provenance.ownership(c)
            old_update = deepcopy(c.get("resident_update"))
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
            if not previous_update and (update_owner or update_due):
                raise ValueError("Record a complete resident-update commitment in the resident panel before referencing it in a handoff.")
            if previous_update and (
                (update_owner and update_owner["name"] != previous_update.get("owner"))
                or (update_due and update_due != _due(previous_update.get("due_at")))
            ):
                raise ValueError("A resident-update commitment already exists. Preserve it during handoff.")
            resident_update = previous_update or dict(owner=update_owner["name"] if update_owner else None,
                                                      due_at=update_due)
            c["handoff"] = dict(state=HANDOFF_OPEN, from_code=c["owner_code"], from_name=c["owner"], to_code=to["code"], to_name=to["name"],
                                to_role=to["role"], offered_by=user["name"], offered_at=event["at"], note=(note or "")[:300],
                                answered_at=None, answer_note="", due_at=due_at, urgency=urgency,
                                next_action=controls.text(metadata.get("next_action"), "", required=False) or None,
                                resident_update_owner=resident_update.get("owner"),
                                resident_update_due_at=resident_update.get("due_at"))
            event.update(handoff_view(c), by=user["email"], authority=user["role"])
            event["changes"] = dict(
                handoff=dict(old=old_handoff, new=deepcopy(c["handoff"])),
                ownership=dict(old=old_owner, new=change_provenance.ownership(c)),
                resident_update=dict(old=old_update, new=deepcopy(c.get("resident_update"))))

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
        field = {"Received": "received_at", "Escalated": "escalated_at",
                 "Declined": "answered_at", "Withdrawn": "answered_at",
                 "Completed": "completed_at"}[c["handoff"]["state"]]
        change_provenance.append_event(c, "handoff_history", user,
                                       "handoff_" + c["handoff"]["state"].lower(),
                                       "controlled/handoff", **handoff_view(c),
                                       at=c["handoff"][field], by=user["email"], authority=user["role"])

    def _save_workflow(self, user, action, case_id, detail):
        if not hasattr(self, "db"):
            self.save()
        self.audit(user["email"], action, case_id, detail)
        if hasattr(self, "db"):
            self.save()

    def receive_handoff(self, user, case_id):
        with change_provenance.controlled(self, user, case_id) as (c, user):
            h = self._open_offer(c, user, "recipient")
            if h["state"] != HANDOFF_OPEN:
                raise ValueError("Only a sent handoff can be marked received.")
            h.update(state="Received", received_at=_now("microseconds"), received_by=user["email"])
            self._handoff_event(c, user)
            self._save_workflow(user, "handoff_received", case_id, "Receipt recorded; ownership unchanged")

    def accept_handoff(self, user, case_id, metadata=None):
        with change_provenance.operation(self, user, case_id, "handoff_accepted", metadata, "handoff_history") as (c, event):
            h = self._open_offer(c, user, "recipient")
            old_handoff, old_owner = deepcopy(h), change_provenance.ownership(c)
            c.update(owner=user["name"], owner_code=user["code"], owner_role=user["role"], waiting_on=user["name"])
            h.update(state="Accepted", answered_at=event["at"])
            c.setdefault("handoff_log", []).append(dict(h))
            event.update(handoff_view(c), by=user["email"], authority=user["role"])
            event["changes"] = dict(
                handoff=dict(old=old_handoff, new=deepcopy(h)),
                ownership=dict(old=old_owner, new=change_provenance.ownership(c)))

    def decline_handoff(self, user, case_id, reason):
        reason = controls.text(reason, "why you cannot take this on")
        with change_provenance.controlled(self, user, case_id) as (c, user):
            h = self._open_offer(c, user, "recipient")
            h.update(state="Declined", answered_at=_now("microseconds"), answer_note=reason)
            c.setdefault("handoff_log", []).append(dict(h))
            self._handoff_event(c, user)
            self._save_workflow(user, "handoff_declined", case_id, reason)

    def withdraw_handoff(self, user, case_id):
        with change_provenance.controlled(self, user, case_id) as (c, user):
            h = self._open_offer(c, user, "offerer")
            h.update(state="Withdrawn", answered_at=_now("microseconds"))
            c.setdefault("handoff_log", []).append(dict(h))
            self._handoff_event(c, user)
            self._save_workflow(user, "handoff_withdrawn", case_id, f"offer to {h['to_name']}")

    def escalate_handoff(self, user, case_id, to_email, reason):
        reason = controls.text(reason, "why this handoff needs escalation")
        to = self._staff_person(to_email)
        if to["role"] not in MANAGER_ROLES:
            raise ValueError("Choose a manager for the escalation.")
        with change_provenance.controlled(self, user, case_id) as (c, user):
            h = self._open_offer(c, user, "offerer")
            if h["state"] == "Escalated":
                raise ValueError("This handoff has already been escalated.")
            h.update(state="Escalated", escalated_at=_now("microseconds"), escalation_owner=to["name"],
                     escalation_owner_code=to["code"], answer_note=reason)
            self._handoff_event(c, user)
            self._save_workflow(user, "handoff_escalated", case_id, f"to {to['code']}: {reason}")

    def complete_handoff(self, user, case_id, note):
        note = controls.text(note, "the completed action")
        with change_provenance.controlled(self, user, case_id) as (c, user):
            controls.require_role(user, projection.STAFF_ROLES, "the accepting case owner can complete a handoff")
            h = c.get("handoff")
            if not h or h["state"] != "Accepted":
                raise ValueError("Accept the handoff before completing it.")
            if h["to_code"] != user["code"] or c["owner_code"] != user["code"]:
                raise PermissionError("Only the accepting case owner can complete this handoff.")
            h.update(state="Completed", completed_at=_now("microseconds"), completion_note=note)
            self._handoff_event(c, user)
            self._save_workflow(user, "handoff_completed", case_id, note)

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

    # ---- external hazard referral; only the linked home's retrofit hold is controlled here
    def _hazard(self, c, idx):
        if isinstance(idx, bool) or not isinstance(idx, (str, int)) or (
            isinstance(idx, str) and not idx.isdecimal()
        ):
            raise ValueError("Choose one of this case's safety issues.")
        try:
            if int(idx) < 0:
                raise ValueError
            return c["hazards"][int(idx)]
        except (IndexError, ValueError, TypeError):
            raise ValueError("Choose one of this case's safety issues.") from None

    @staticmethod
    def _hazard_actor(user):
        return hazard.identity(user)

    def _hazard_event(self, c, h, user, action, evidence):
        events = h.setdefault("history", [])
        snapshot = deepcopy({k: v for k, v in h.items() if k != "history"})
        events.append(dict(version=len(events) + 1, action=action, at=_now(),
                           actor=self._hazard_actor(user), evidence=evidence, snapshot=snapshot))
        hazard.persist_event(self, user, c["id"], action,
                             f"Home retrofit hold; {h.get('job', '')}; {evidence}",
                             emergency=action == "safety_raised" and h["priority"] == "Emergency")

    def raise_hazard(self, user, case_id, category, priority, note="", metadata=None):
        controls.require_role(user, projection.STAFF_ROLES, "authorised staff")
        if category not in HAZARD_CATEGORIES or priority not in HAZARD_PRIORITIES:
            raise ValueError("Choose the reported observation and urgency from the lists.")
        metadata = metadata or {}
        source = controls.text(metadata.get("source"), "the report source")
        aware = _hazard_time(metadata.get("aware_at"), "the awareness time", actual=True)
        with hazard.decision_scope(self, user, case_id) as (c, user):
            h = dict(category=category, priority=priority, noticed=aware[:10], aware_at=aware,
                     source=source, recorded_at=_now(), referred=None, repaired=None, released=False,
                     job="", owner=user["name"], sender=self._hazard_actor(user),
                     raised_by=user["name"], raised_by_email=user["email"],
                     raised_identity=self._hazard_actor(user),
                     note=controls.text(note, "", required=False),
                     hold=dict(scope="Home", case_id=case_id, status="Active",
                               accountable_role="Building Safety Liaison", decision=None))
            c["hazards"].append(h)
            self._hazard_event(c, h, user, "safety_raised", source)
            return len(c["hazards"]) - 1

    def refer_hazard(self, user, case_id, idx, to_email, job, metadata=None):
        controls.require_role(user, projection.STAFF_ROLES, "authorised staff")
        job = controls.text(job, "the external hazard or repair case reference", 40)
        evidence = controls.text((metadata or {}).get("evidence"), "evidence of sending the referral")
        with hazard.decision_scope(self, user, case_id) as (c, user):
            to = hazard.subject(self, self._staff_person(to_email))
            if to["role"] not in SAFETY_ROLES:
                raise ValueError("Refer a safety issue to the Building Safety Liaison or a manager.")
            h = self._hazard(c, idx)
            if h["released"] or h.get("referral_version"):
                raise ValueError("This safety issue has already been referred.")
            if h.get("referred") or h.get("repaired"):
                h["legacy_record"] = deepcopy(h)
                h.update(repaired=None, repaired_by=None)
            h.update(referral_version=1, referred=_today(), sent_at=_now(), job=job,
                     destination=self._hazard_actor(to), sender=self._hazard_actor(user),
                     owner=user["name"], referred_by=user["name"], sent_evidence=evidence,
                     hold=dict(scope="Home", case_id=case_id, status="Active",
                               accountable_role=to["role"], decision=None))
            self._hazard_event(c, h, user, "safety_referred", evidence)

    def _hazard_receiver(self, c, idx, user, allow_released=False):
        controls.require_role(user, SAFETY_ROLES, "the designated safety receiver")
        h = self._hazard(c, idx)
        if (h["released"] and not allow_released) or not h.get("referral_version"):
            raise ValueError("Record a prospective evidenced referral before continuing.")
        if hazard.identity(h["destination"]) != self._hazard_actor(user):
            raise PermissionError("Only the designated safety receiver can record this event.")
        return h

    def receive_hazard(self, user, case_id, idx, evidence):
        evidence = controls.text(evidence, "the external receipt evidence")
        with hazard.decision_scope(self, user, case_id) as (c, user):
            h = self._hazard_receiver(c, idx, user)
            if h.get("received_at"):
                raise ValueError("Receipt has already been recorded.")
            h.update(received_at=_now(), received_by=self._hazard_actor(user), receipt_evidence=evidence)
            self._hazard_event(c, h, user, "safety_received", evidence)

    def accept_hazard(self, user, case_id, idx, evidence):
        evidence = controls.text(evidence, "the external acceptance evidence")
        with hazard.decision_scope(self, user, case_id) as (c, user):
            h = self._hazard_receiver(c, idx, user)
            if not h.get("received_at") or h.get("accepted_at"):
                raise ValueError("Record receipt first; acceptance can only be recorded once.")
            h.update(accepted_at=_now(), accepted_by=self._hazard_actor(user),
                     acceptance_evidence=evidence, owner=user["name"])
            self._hazard_event(c, h, user, "safety_accepted", evidence)

    def observe_hazard_times(self, user, case_id, idx, metadata):
        evidence = controls.text(metadata.get("evidence"), "the external service timing evidence")
        fields = ("response_due_at", "responded_at", "resident_update_due_at", "resident_updated_at")
        times = {k: _hazard_time(metadata[k], k, actual=k in ("responded_at", "resident_updated_at"))
                 for k in fields if metadata.get(k) not in (None, "")}
        if not times:
            raise ValueError("Add at least one externally recorded response or resident-update time.")
        with hazard.decision_scope(self, user, case_id) as (c, user):
            h = self._hazard_receiver(c, idx, user, allow_released=True)
            if not h.get("accepted_at"):
                raise ValueError("Record acceptance before observing service times.")
            if any(h.get(k) is not None for k in times):
                raise ValueError("Recorded service times cannot be overwritten here; retain the external service record.")
            if h.get("aware_at") and any(times[k] < h["aware_at"] for k in times):
                raise ValueError("Service times cannot precede recorded awareness.")
            h.update(times)
            self._hazard_event(c, h, user, "safety_times_observed", evidence)

    def record_repair(self, user, case_id, idx, evidence=None):
        evidence = controls.text(evidence, "the external repair evidence")
        with hazard.decision_scope(self, user, case_id) as (c, user):
            h = self._hazard_receiver(c, idx, user)
            if h["released"] or h.get("repaired"):
                raise ValueError("This repair is already recorded.")
            if not h.get("accepted_at"):
                raise ValueError("Record acceptance before observing repair evidence.")
            h.update(repaired=_today(), repaired_by=user["name"], repaired_by_email=user["email"],
                     repaired_identity=self._hazard_actor(user),
                     repair_evidence=evidence)
            self._hazard_event(c, h, user, "safety_repaired", evidence)

    def release_hazard(self, user, case_id, idx, note="", evidence=None):
        if user["role"] not in SAFETY_ROLES:
            raise PermissionError("Only the Building Safety Liaison or a manager can release a retrofit hold.")
        note = controls.text(note, "the retrofit hold release reason")
        evidence = controls.text(evidence, "the external evidence supporting hold release")
        with hazard.decision_scope(self, user, case_id) as (c, user):
            h = self._hazard(c, idx)
            if h["released"]:
                raise ValueError("This retrofit hold is already released.")
            if not h.get("repair_evidence") or not h.get("accepted_at"):
                raise ValueError("Record receipt, acceptance and external repair evidence before hold release.")
            hazard.require_independent(user, h)
            h.update(released=True, released_by=user["name"], released_at=_now(), release_note=note)
            h["hold"].update(status="Released", decision=dict(at=_now(), actor=self._hazard_actor(user),
                                                            reason=note, evidence=evidence))
            self._hazard_event(c, h, user, "safety_released", evidence)

    def hazard_states(self, case_id):
        with self.lock:
            return [dict(index=i, **hazard_view(h, case_id)) for i, h in enumerate(self._case(case_id)["hazards"])]
