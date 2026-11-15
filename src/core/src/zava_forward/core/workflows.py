"""Return and reopen, handoff states and safety referral workflows.

Each step is a small, checked state change by a named person with a reason, and
each is written to the audit ledger. None of them decides anything for a
person: the system records, enforces who may do what, and refuses steps that
skip a state.
"""
from copy import deepcopy
from datetime import UTC, date, datetime, time, timedelta
import math

from . import change_provenance, controls, gates, hazard, identity, insights, projection

MANAGER_ROLES = ("Retrofit Programme Manager", "Programme Support Officer")
DEFAULT_ESCALATION_ROLE = "Retrofit Programme Manager"
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


def _valid_hours(value):
    if value is None or value == "" or isinstance(value, bool):
        return None
    try:
        hours = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(hours) or not 0 < hours < 1e6:
        return None
    return hours


def _validate_max_age_hours(max_age_hours):
    if max_age_hours is None:
        return None
    hours = _valid_hours(max_age_hours)
    if hours is None:
        raise ValueError("max_age_hours must be a positive number of hours.")
    return hours


def approved_handoff_policy(policy):
    """Return a validated approved BG-010 handoff SLA policy dict, or None when unapproved/unset."""
    if not isinstance(policy, dict) or policy.get("status") != "Approved":
        return None
    owner = policy.get("owner")
    if not isinstance(owner, str) or not owner.strip() or owner.strip() in ("Unknown", "to be named"):
        return None
    acceptance_hours = _valid_hours(policy.get("acceptance_hours"))
    if acceptance_hours is None:
        return None
    urgent_raw = policy.get("urgent_acceptance_hours")
    urgent_hours = None
    if urgent_raw is not None:
        urgent_hours = _valid_hours(urgent_raw)
        if urgent_hours is None:
            return None
    role_raw = policy.get("escalation_role")
    escalation_role = (
        role_raw.strip()
        if isinstance(role_raw, str) and role_raw.strip() in MANAGER_ROLES
        else DEFAULT_ESCALATION_ROLE
    )
    esc_owner = policy.get("escalation_owner")
    esc_code = policy.get("escalation_owner_code")
    esc_to = policy.get("escalation_to")
    policy_id = str(policy.get("policy_id") or policy.get("version") or "BG-010").strip() or "BG-010"
    return dict(
        status="Approved",
        owner=owner.strip(),
        policy_id=policy_id,
        acceptance_hours=acceptance_hours,
        urgent_acceptance_hours=urgent_hours,
        escalation_role=escalation_role,
        escalation_owner=esc_owner.strip() if isinstance(esc_owner, str) and esc_owner.strip() else None,
        escalation_owner_code=esc_code.strip() if isinstance(esc_code, str) and esc_code.strip() else None,
        escalation_to=esc_to.strip().lower() if isinstance(esc_to, str) and esc_to.strip() else None,
    )


def approved_handoff_limit_hours(policy, *, urgency=None):
    """Return the approved BG-010 acceptance limit in hours for the handoff urgency, or None."""
    approved = approved_handoff_policy(policy)
    if approved is None:
        return None
    if urgency == "Urgent" and approved["urgent_acceptance_hours"] is not None:
        return approved["urgent_acceptance_hours"]
    return approved["acceptance_hours"]


def _parse_sla_as_of(as_of):
    if as_of in (None, ""):
        return None
    if not isinstance(as_of, str):
        raise ValueError("Ageing needs an as-of time with a timezone.")
    text = as_of.strip()
    if len(text) == 10:
        return datetime.combine(date.fromisoformat(text), time(), UTC)
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Ageing needs an as-of time with a timezone.")
    return parsed.astimezone(UTC)


def _optional_tz_instant(value):
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        if len(text) == 10:
            return datetime.combine(date.fromisoformat(text), time(), UTC)
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(UTC)


def _resolve_escalation_target(h, *, policy=None, staff=None):
    staff_rows = [s for s in (staff or ()) if isinstance(s, dict)]
    if h.get("escalation_owner"):
        code = h.get("escalation_owner_code")
        role = h.get("escalation_owner_role")
        matched = next((s for s in staff_rows if code and s.get("code") == code), None)
        if matched and not role:
            role = matched.get("role")
        return h["escalation_owner"], code, role or DEFAULT_ESCALATION_ROLE, matched
    approved = approved_handoff_policy(policy)
    preferred_role = approved["escalation_role"] if approved else DEFAULT_ESCALATION_ROLE
    if approved:
        for s in staff_rows:
            if s.get("role") not in MANAGER_ROLES:
                continue
            if (
                (approved["escalation_to"] and str(s.get("email") or "").lower() == approved["escalation_to"])
                or (approved["escalation_owner_code"] and s.get("code") == approved["escalation_owner_code"])
                or (approved["escalation_owner"] and s.get("name") == approved["escalation_owner"])
            ):
                return s["name"], s["code"], s["role"], s
        if approved["escalation_owner"]:
            return (
                approved["escalation_owner"],
                approved["escalation_owner_code"],
                preferred_role,
                None,
            )
    for s in staff_rows:
        if s.get("role") == preferred_role:
            return s["name"], s["code"], s["role"], s
    for s in staff_rows:
        if s.get("role") in MANAGER_ROLES:
            return s["name"], s["code"], s["role"], s
    return preferred_role, None, preferred_role, None


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


def handoff_sla(c, *, as_of=None, policy=None, max_age_hours=None, staff=None):
    """Deterministic BG-010 SLA and escalation evaluation for a case handoff."""
    if not c.get("handoff"):
        return None
    h = c["handoff"]
    state = h.get("state")
    explicit_limit = _validate_max_age_hours(max_age_hours)
    approved = approved_handoff_policy(policy)
    limit_hours = (
        explicit_limit
        if explicit_limit is not None
        else approved_handoff_limit_hours(approved, urgency=h.get("urgency"))
    )
    offered = _optional_tz_instant(h.get("offered_at"))
    sla_due_dt = (
        (offered + timedelta(hours=limit_hours)).astimezone(UTC)
        if offered is not None and limit_hours is not None
        else None
    )
    sla_due_at = sla_due_dt.isoformat() if sla_due_dt is not None else None
    due_raw = h.get("due_at")
    due_dt = _optional_tz_instant(due_raw)
    if due_dt is not None and sla_due_dt is not None:
        effective_due_at = due_raw if due_dt <= sla_due_dt else sla_due_at
    else:
        effective_due_at = due_raw if due_dt is not None else sla_due_at

    now = _parse_sla_as_of(as_of)
    ref_end = (
        now
        if state in HANDOFF_PENDING
        else (_optional_tz_instant(h.get("completed_at") or h.get("answered_at")) or now)
    )
    if offered is not None and ref_end is not None:
        raw_seconds = (ref_end - offered).total_seconds()
        elapsed_hours = max(0.0, round(raw_seconds / 3600, 2))
    else:
        raw_seconds = None
        elapsed_hours = None

    if state in HANDOFF_PENDING and now is not None:
        due_over = max(0.0, (now - due_dt).total_seconds()) if due_dt is not None and due_dt < now else 0.0
        sla_over = (
            max(0.0, raw_seconds - limit_hours * 3600)
            if raw_seconds is not None and limit_hours is not None and raw_seconds > limit_hours * 3600
            else 0.0
        )
        over_seconds = max(due_over, sla_over)
        overdue = over_seconds > 0.0
        overdue_hours = round(over_seconds / 3600, 2) if overdue else 0.0
    else:
        overdue = False
        overdue_hours = 0.0 if state not in HANDOFF_PENDING else None

    needs_escalation = bool(overdue and state in (HANDOFF_OPEN, "Received"))
    target, target_code, target_role, _ = _resolve_escalation_target(h, policy=approved, staff=staff)

    if state == "Escalated":
        escalation_status = "Escalated"
    elif state in (HANDOFF_OPEN, "Received"):
        if overdue:
            escalation_status = "Overdue - escalation required"
        elif limit_hours is not None or due_dt is not None:
            escalation_status = "Within approved window"
        else:
            escalation_status = "Pending acceptance (unbounded - OD-09)"
    elif state == "Accepted":
        escalation_status = "Accepted"
    elif state == "Completed":
        escalation_status = "Completed"
    else:
        escalation_status = "Closed without acceptance"

    accountable = c.get("owner") or "Unknown"
    proposed = h.get("to_name") or h.get("to_role") or "the proposed receiver"
    if state == "Escalated":
        escalation_next_action = (
            f"Escalated to {target}: confirm acceptance with {proposed} or reassign; "
            f"{accountable} remains accountable owner."
        )
    elif needs_escalation:
        escalation_next_action = (
            f"Escalate overdue handoff to {target}; {accountable} remains accountable owner "
            f"and must keep chasing {proposed}."
        )
    elif state in (HANDOFF_OPEN, "Received"):
        if limit_hours is not None or due_dt is not None:
            escalation_next_action = (
                f"Ask {proposed} to accept or decline within the approved window; "
                f"{accountable} remains accountable owner and chase owner."
            )
        else:
            escalation_next_action = (
                f"Ask {proposed} to accept or decline; "
                f"{accountable} remains accountable owner and must keep chasing."
            )
    elif state == "Accepted":
        escalation_next_action = (
            f"Complete the accepted handoff action; {accountable} is now the accountable owner."
        )
    else:
        escalation_next_action = None

    return dict(
        approved_limit_hours=limit_hours,
        sla_due_at=sla_due_at,
        effective_due_at=effective_due_at,
        elapsed_hours=elapsed_hours,
        overdue_hours=overdue_hours,
        overdue=overdue,
        needs_escalation=needs_escalation,
        escalation_status=escalation_status,
        escalation_target=target,
        escalation_target_code=target_code,
        escalation_target_role=target_role,
        escalation_next_action=escalation_next_action,
        auto_escalated=bool(h.get("auto_escalated")),
    )


def handoff_view(c, *, as_of=None, policy=None, max_age_hours=None, staff=None):
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
    sla = handoff_sla(c, as_of=as_of, policy=policy, max_age_hours=max_age_hours, staff=staff)
    if sla is not None:
        h.update(sla)
    return h


def handoff_ageing(c, as_of, max_age_hours=None, *, policy=None):
    """Read-only ageing of one unaccepted handoff against its own due time and an approved limit.

    The approved limit is an operational decision (BG-010, OD-09) and is never defaulted: without
    one, ageing is shown but no handoff is flagged for escalation by age alone.
    """
    h = handoff_view(c)
    if not h or h["state"] not in HANDOFF_PENDING:
        return None
    now = datetime.fromisoformat(as_of)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Ageing needs an as-of time with a timezone.")
    offered = datetime.fromisoformat(h["offered_at"])
    if offered.tzinfo is None or offered.utcoffset() is None:
        raise ValueError("Handoff offered_at needs a timezone.")
    explicit_limit = _validate_max_age_hours(max_age_hours)
    approved = approved_handoff_policy(policy)
    limit = (
        explicit_limit
        if explicit_limit is not None
        else approved_handoff_limit_hours(approved, urgency=h.get("urgency"))
    )
    raw_seconds = (now - offered).total_seconds()
    age = round(raw_seconds / 3600, 2)
    reasons = []
    if h["due_at"] and datetime.fromisoformat(h["due_at"]) < now:
        reasons.append("Handoff due time has passed")
    if limit is not None and raw_seconds > limit * 3600:
        shown_limit = max_age_hours if explicit_limit is not None else limit
        reasons.append(f"Unaccepted for more than the approved {shown_limit} hours")
    if limit is None:
        limit_note = "Approved escalation time not set (OD-09)"
    elif explicit_limit is not None:
        limit_note = None
    else:
        limit_note = f"Approved escalation limit: {limit}h ({approved['policy_id']})"
    return dict(case_id=c["id"], status=h["status"], age_hours=age, due_at=h["due_at"],
                chase_owner=h["chase_owner"], chase_owner_code=h["chase_owner_code"],
                proposed_receiver=h["proposed_receiver"], escalated=h["state"] == "Escalated",
                needs_escalation=bool(reasons) and h["state"] != "Escalated", reasons=reasons,
                approved_limit_hours=max_age_hours if explicit_limit is not None else limit,
                limit_note=limit_note,
                as_of=as_of)


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
        source = controls.evidence_text(metadata.get("source"), "the source reference")
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
                     escalation_owner_code=to["code"], escalation_owner_role=to["role"],
                     auto_escalated=False, answer_note=reason)
            self._handoff_event(c, user)
            self._save_workflow(user, "handoff_escalated", case_id, f"to {to['code']}: {reason}")

    def escalate_overdue_handoffs(self, user, *, as_of=None, max_age_hours=None, reason=None):
        """Controlled manager sweep transitioning overdue Offered/Received handoffs to Escalated."""
        controls.require_role(user, MANAGER_ROLES, "a programme manager can escalate overdue handoffs")
        as_of = as_of or _now()
        _parse_sla_as_of(as_of)
        _validate_max_age_hours(max_age_hours)
        custom_note = (
            controls.text(reason, "why this handoff needs escalation")
            if reason not in (None, "")
            else None
        )
        with self.lock:
            policy = self.data.get("handoff_policy")
            staff_rows = self.data.get("staff")
            evaluated_count = 0
            already_escalated_count = 0
            candidates = []
            for cid in sorted(self.cases):
                c = self.cases[cid]
                if c.get("closed"):
                    continue
                raw_h = c.get("handoff")
                if not raw_h or raw_h.get("state") not in HANDOFF_PENDING:
                    continue
                if raw_h["state"] == "Escalated":
                    already_escalated_count += 1
                    continue
                evaluated_count += 1
                sla = handoff_sla(
                    c, as_of=as_of, policy=policy, max_age_hours=max_age_hours, staff=staff_rows
                )
                if sla and sla["overdue"]:
                    _, _, _, matched = _resolve_escalation_target(
                        raw_h, policy=policy, staff=staff_rows
                    )
                    target = matched or user
                    candidates.append((cid, sla, target))

            escalated_case_ids = []
            items = []
            for cid, sla, target in candidates:
                with change_provenance.controlled(self, user, cid) as (c, actor):
                    h = c.get("handoff")
                    if not h or h.get("state") not in (HANDOFF_OPEN, "Received"):
                        continue
                    note = (
                        custom_note
                        if custom_note is not None
                        else f"Auto-escalated past approved window ({sla['overdue_hours']}h overdue as of {as_of})"
                    )
                    h.update(
                        state="Escalated",
                        escalated_at=_now("microseconds"),
                        escalation_owner=target["name"],
                        escalation_owner_code=target["code"],
                        escalation_owner_role=target["role"],
                        auto_escalated=True,
                        answer_note=note,
                    )
                    self._handoff_event(c, actor)
                    self._save_workflow(
                        actor, "handoff_escalated", cid, f"to {target['code']}: {note}"
                    )
                    escalated_case_ids.append(cid)
                    projected = handoff_view(
                        c,
                        as_of=as_of,
                        policy=policy,
                        max_age_hours=max_age_hours,
                        staff=staff_rows,
                    )
                    items.append(self._shared_handoff_row(c, projected, as_of))
            visible_items = (
                items if projection.can_see_reason(user) else projection.hold_notes(items)
            )
            return dict(
                as_of=as_of,
                evaluated_count=evaluated_count,
                escalated_count=len(escalated_case_ids),
                already_escalated_count=already_escalated_count,
                escalated_case_ids=escalated_case_ids,
                items=visible_items,
            )

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

    @staticmethod
    def _direct_handoff_visible(user, h):
        return (
            user["code"] in (h.get("from_code"), h.get("to_code"), h.get("escalation_owner_code"))
            or (not h.get("to_code") and h.get("to_role") == user.get("role"))
            or user["role"] in MANAGER_ROLES
        )

    @staticmethod
    def _shared_handoff_row(c, h, as_of):
        row = dict(case_id=c["id"], stage=c.get("stage"), as_of=as_of)
        for key in (
            "state",
            "status",
            "from_code",
            "from_name",
            "to_code",
            "to_name",
            "to_role",
            "destination",
            "proposed_receiver",
            "confirmed_receiver",
            "accountable_owner",
            "accountable_owner_code",
            "chase_owner",
            "chase_owner_code",
            "offered_at",
            "received_at",
            "escalated_at",
            "due_at",
            "sla_due_at",
            "effective_due_at",
            "urgency",
            "approved_limit_hours",
            "elapsed_hours",
            "overdue_hours",
            "overdue",
            "needs_escalation",
            "escalation_status",
            "escalation_target",
            "escalation_target_code",
            "escalation_target_role",
            "escalation_owner",
            "escalation_owner_code",
            "escalation_next_action",
            "auto_escalated",
            "note",
            "answer_note",
            "next_action",
            "resident_update_owner",
            "resident_update_due_at",
        ):
            row[key] = h.get(key)
        return row

    @staticmethod
    def _handoff_queue_sort_key(row):
        return (
            not bool(row.get("overdue")),
            -(row.get("overdue_hours") or 0.0),
            -(row.get("elapsed_hours") or 0.0),
            row["case_id"],
        )

    def pending_handoffs(self, user):
        controls.require_role(user, projection.STAFF_ROLES, "authorised staff can view handoffs")
        with self.lock:
            policy = self.data.get("handoff_policy")
            staff_rows = self.data.get("staff")
            rows = []
            for c in self.cases.values():
                if c.get("closed"):
                    continue
                h = handoff_view(c, as_of=self.as_of, policy=policy, staff=staff_rows)
                if h and h["state"] in HANDOFF_PENDING and self._direct_handoff_visible(user, h):
                    rows.append(dict(case_id=c["id"], resident=c["resident"]["name"],
                                     address=c["home"]["address"], **h))
            return rows if projection.can_see_reason(user) else projection.hold_notes(rows)

    def unaccepted_handoffs(self, user, as_of=None, max_age_hours=None):
        """Visible unaccepted handoffs with ageing; escalation stays a named manager's act."""
        controls.require_role(user, projection.STAFF_ROLES, "authorised staff can view handoffs")
        as_of = as_of or _now()
        now = datetime.fromisoformat(as_of)
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Ageing needs an as-of time with a timezone.")
        _validate_max_age_hours(max_age_hours)
        with self.lock:
            policy = self.data.get("handoff_policy")
            rows = []
            for c in self.cases.values():
                if c.get("closed"):
                    continue
                row = handoff_ageing(c, as_of, max_age_hours, policy=policy)
                h = c.get("handoff") or {}
                if row and self._direct_handoff_visible(user, h):
                    rows.append(row)
            return sorted(rows, key=lambda r: (-r["age_hours"], r["case_id"]))

    def unowned_handoffs(self, user, as_of=None, max_age_hours=None):
        """Shared role-visible queue of handoffs without a confirmed accepting receiver."""
        controls.require_role(user, projection.STAFF_ROLES, "authorised staff can view handoffs")
        as_of = as_of or _now()
        _parse_sla_as_of(as_of)
        _validate_max_age_hours(max_age_hours)
        with self.lock:
            policy = self.data.get("handoff_policy")
            staff_rows = self.data.get("staff")
            rows = []
            for c in self.cases.values():
                if c.get("closed"):
                    continue
                h = handoff_view(
                    c, as_of=as_of, policy=policy, max_age_hours=max_age_hours, staff=staff_rows
                )
                if (
                    h
                    and h["state"] in HANDOFF_PENDING
                    and h.get("confirmed_receiver") is None
                    and (
                        self._direct_handoff_visible(user, h)
                        or h.get("to_role") == user.get("role")
                    )
                ):
                    rows.append(self._shared_handoff_row(c, h, as_of))
            rows.sort(key=self._handoff_queue_sort_key)
            return rows if projection.can_see_reason(user) else projection.hold_notes(rows)

    def escalated_handoffs(self, user, as_of=None, max_age_hours=None):
        """Shared role- and manager-visible queue of escalated or overdue unaccepted handoffs."""
        controls.require_role(user, projection.STAFF_ROLES, "authorised staff can view handoffs")
        as_of = as_of or _now()
        _parse_sla_as_of(as_of)
        _validate_max_age_hours(max_age_hours)
        with self.lock:
            policy = self.data.get("handoff_policy")
            staff_rows = self.data.get("staff")
            rows = []
            for c in self.cases.values():
                if c.get("closed"):
                    continue
                h = handoff_view(
                    c, as_of=as_of, policy=policy, max_age_hours=max_age_hours, staff=staff_rows
                )
                if (
                    h
                    and h["state"] in HANDOFF_PENDING
                    and (h["state"] == "Escalated" or h.get("overdue"))
                    and (
                        self._direct_handoff_visible(user, h)
                        or h.get("to_role") == user.get("role")
                        or h.get("escalation_target_role") == user.get("role")
                    )
                ):
                    rows.append(self._shared_handoff_row(c, h, as_of))
            rows.sort(key=self._handoff_queue_sort_key)
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
        source = controls.evidence_text(metadata.get("source"), "the report source")
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
        evidence = controls.evidence_text((metadata or {}).get("evidence"), "evidence of sending the referral")
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
        if h["released"] and not allow_released:
            raise ValueError("Retrofit work on this safety issue has already been restarted. Nothing more to do.")
        if not h.get("referral_version"):
            raise ValueError("Record a prospective evidenced referral before continuing.")
        if hazard.identity(h["destination"]) != self._hazard_actor(user):
            raise PermissionError("Only the designated safety receiver can record this event.")
        return h

    def receive_hazard(self, user, case_id, idx, evidence):
        evidence = controls.evidence_text(evidence, "the external receipt evidence")
        with hazard.decision_scope(self, user, case_id) as (c, user):
            h = self._hazard_receiver(c, idx, user)
            if h.get("received_at"):
                raise ValueError("Receipt has already been recorded.")
            h.update(received_at=_now(), received_by=self._hazard_actor(user), receipt_evidence=evidence)
            self._hazard_event(c, h, user, "safety_received", evidence)

    def accept_hazard(self, user, case_id, idx, evidence):
        evidence = controls.evidence_text(evidence, "the external acceptance evidence")
        with hazard.decision_scope(self, user, case_id) as (c, user):
            h = self._hazard_receiver(c, idx, user)
            if not h.get("received_at") or h.get("accepted_at"):
                raise ValueError("Record receipt first; acceptance can only be recorded once.")
            h.update(accepted_at=_now(), accepted_by=self._hazard_actor(user),
                     acceptance_evidence=evidence, owner=user["name"])
            self._hazard_event(c, h, user, "safety_accepted", evidence)

    def observe_hazard_times(self, user, case_id, idx, metadata):
        evidence = controls.evidence_text(metadata.get("evidence"), "the external service timing evidence")
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
        evidence = controls.evidence_text(evidence, "the external repair evidence")
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
            raise PermissionError("Only the Building Safety Liaison or a manager can restart stopped retrofit work. Ask one of them to record the restart.")
        note = controls.text(note, "the reason for restarting retrofit work")
        evidence = controls.evidence_text(evidence, "the external evidence supporting the restart")
        with hazard.decision_scope(self, user, case_id) as (c, user):
            h = self._hazard(c, idx)
            if h["released"]:
                raise ValueError("Retrofit work on this safety issue has already been restarted. Nothing more to do.")
            if any(controls.is_memory_reference(h.get(k)) for k in ("receipt_evidence", "acceptance_evidence", "repair_evidence")):
                raise ValueError(controls.MEMORY_REFUSAL)
            if not h.get("repair_evidence") or not h.get("accepted_at"):
                raise ValueError(
                    "Retrofit work cannot restart yet. Receipt, acceptance and external repair "
                    "evidence must be recorded first.")
            if h["hold"].get("accountable_role") and not h["hold"].get("legacy"):
                verdict = gates.safety_release_gate(h["hold"], user, [])
                if verdict.outcome != gates.PASS:
                    raise PermissionError(verdict.reason)
            hazard.require_independent(user, h)
            h.update(released=True, released_by=user["name"], released_at=_now(), release_note=note)
            h["hold"].update(status="Released", decision=dict(at=_now(), actor=self._hazard_actor(user),
                                                            reason=note, evidence=evidence))
            self._hazard_event(c, h, user, "safety_released", evidence)

    def hazard_states(self, case_id):
        with self.lock:
            return [dict(index=i, **hazard_view(h, case_id)) for i, h in enumerate(self._case(case_id)["hazards"])]
