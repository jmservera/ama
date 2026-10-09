"""Return and reopen, handoff states and safety referral workflows.

Each step is a small, checked state change by a named person with a reason, and
each is written to the audit ledger. None of them decides anything for a
person: the system records, enforces who may do what, and refuses steps that
skip a state.
"""
from datetime import date, datetime

from . import insights

MANAGER_ROLES = ("Retrofit Programme Manager", "Programme Support Officer")
HAZARD_PRIORITIES = ("Emergency", "Significant", "Routine")
HAZARD_CATEGORIES = ("Damp and mould", "Structural", "Electrical", "Other")
SAFETY_ROLES = ("Building Safety Liaison",) + MANAGER_ROLES
HANDOFF_OPEN = "Offered"


def _today():
    return date.today().isoformat()


def _now():
    return datetime.now().isoformat(timespec="minutes")


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
    def return_case(self, user, case_id, to_stage, reason):
        reason = (reason or "").strip()[:300]
        if not reason:
            raise ValueError("Say why the case is being returned.")
        with self.lock:
            c = self._case(case_id)
            if c["closed"]:
                raise ValueError("This case is closed. A manager can reopen it.")
            order = insights.STAGE_ORDER
            if c["stage"] not in order or to_stage not in order or order.index(to_stage) >= order.index(c["stage"]):
                raise ValueError("A case can only be returned to an earlier stage.")
            was = c["stage"]
            for a in c["appointments"]:
                if was == "Install booked" and a["outcome"] == "Booked":
                    a["outcome"] = "Cancelled"
            c["decision"] = c["decision"] if to_stage not in ("Contacting resident", "Waiting for resident decision") \
                else dict(status="Waiting" if to_stage == "Waiting for resident decision" else "Not yet asked", by=user["name"], at=_today())
            c.update(stage=to_stage, stage_since=_today(), days_in_stage=0, reason="after being returned", waiting_on=c["owner"])
            c.setdefault("returns", []).append(dict(at=_now(), by=user["name"], from_stage=was, to_stage=to_stage, reason=reason))
            self.audit(user["email"], "return_case", case_id, f"{was} -> {to_stage}: {reason}")
            self.save()

    def reopen_case(self, user, case_id, reason):
        if user["role"] not in MANAGER_ROLES:
            raise PermissionError("Only a manager can reopen a closed case.")
        reason = (reason or "").strip()[:300]
        if not reason:
            raise ValueError("Say why the case is being reopened.")
        with self.lock:
            c = self._case(case_id)
            if not c["closed"]:
                raise ValueError("This case is already open.")
            was = c["stage"]
            to = "Aftercare issue" if was == "Completed" else "Contacting resident"
            if to == "Contacting resident":
                c["decision"] = dict(status="Not yet asked", by=user["name"], at=_today())
            c.update(closed=False, stage=to, stage_since=_today(), days_in_stage=0, reason="after being reopened", waiting_on=c["owner"])
            c.setdefault("returns", []).append(dict(at=_now(), by=user["name"], from_stage=was, to_stage=to, reason=reason, reopened=True))
            self.audit(user["email"], "reopen_case", case_id, f"{was} -> {to}: {reason}")
            self.save()

    # ---- handoff: offered, then accepted or declined by the person receiving it
    def _staff_person(self, email):
        p = self.staff.get((email or "").lower())
        if not p or p["role"] == "Contractor":
            raise ValueError("Choose a colleague to take this over.")
        return p

    def offer_handoff(self, user, case_id, to_email, note=""):
        to = self._staff_person(to_email)
        with self.lock:
            c = self._case(case_id)
            if c["closed"]:
                raise ValueError("This case is closed.")
            if c["owner_code"] != user["code"] and user["role"] not in MANAGER_ROLES:
                raise PermissionError("Only the owner or a manager can offer this case to someone else.")
            if to["code"] == c["owner_code"]:
                raise ValueError("That colleague already owns this case.")
            cur = c.get("handoff")
            if cur and cur["state"] == HANDOFF_OPEN:
                raise ValueError("A handoff is already waiting for an answer.")
            c["handoff"] = dict(state=HANDOFF_OPEN, from_code=c["owner_code"], from_name=c["owner"], to_code=to["code"], to_name=to["name"],
                                offered_by=user["name"], offered_at=_now(), note=(note or "")[:300], answered_at=None, answer_note="")
            self.audit(user["email"], "handoff_offered", case_id, f"to {to['name']} {note or ''}".strip())
            self.save()

    def _open_offer(self, c, user, who):
        h = c.get("handoff")
        if not h or h["state"] != HANDOFF_OPEN:
            raise ValueError("There is no handoff waiting for an answer.")
        if who == "recipient" and h["to_code"] != user["code"]:
            raise PermissionError("This handoff was offered to someone else.")
        if who == "offerer" and h["from_code"] != user["code"] and user["role"] not in MANAGER_ROLES:
            raise PermissionError("Only the person who offered it, or a manager, can withdraw it.")
        return h

    def accept_handoff(self, user, case_id):
        with self.lock:
            c = self._case(case_id)
            h = self._open_offer(c, user, "recipient")
            c.update(owner=user["name"], owner_code=user["code"], owner_role=user["role"], waiting_on=user["name"])
            h.update(state="Accepted", answered_at=_now())
            c.setdefault("handoff_log", []).append(dict(h))
            self.audit(user["email"], "handoff_accepted", case_id, f"from {h['from_name']}")
            self.save()

    def decline_handoff(self, user, case_id, reason):
        reason = (reason or "").strip()[:300]
        if not reason:
            raise ValueError("Say why you cannot take this on.")
        with self.lock:
            c = self._case(case_id)
            h = self._open_offer(c, user, "recipient")
            h.update(state="Declined", answered_at=_now(), answer_note=reason)
            c.setdefault("handoff_log", []).append(dict(h))
            self.audit(user["email"], "handoff_declined", case_id, reason)
            self.save()

    def withdraw_handoff(self, user, case_id):
        with self.lock:
            c = self._case(case_id)
            h = self._open_offer(c, user, "offerer")
            h.update(state="Withdrawn", answered_at=_now())
            c.setdefault("handoff_log", []).append(dict(h))
            self.audit(user["email"], "handoff_withdrawn", case_id, f"offer to {h['to_name']}")
            self.save()

    def pending_handoffs(self, user):
        with self.lock:
            return [dict(case_id=c["id"], resident=c["resident"]["name"], address=c["home"]["address"], **{k: c["handoff"][k] for k in
                    ("from_name", "offered_at", "note")}) for c in self.cases.values()
                    if c.get("handoff") and c["handoff"]["state"] == HANDOFF_OPEN and c["handoff"]["to_code"] == user["code"]]

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
