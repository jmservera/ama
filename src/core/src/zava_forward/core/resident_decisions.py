"""Resident decision per measure and a separate service/complaint route (FR-014, AC-017, AC-037, SA-008).

The decision is a resident-owned field. It starts as "Not recorded" for every
measure and changes only when a person records what the resident said, with how
they said it. It is never worked out from calls, visits, access or other
measures, and one measure's pause or withdrawal does not touch another's.
Service and complaint requests have their own route, desired outcome and a
named redress owner. Contact needs are held as short coded entries so only the
minimum necessary is shown.
"""
import json
import hashlib
import logging
import os
import re
import uuid
import weakref
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, date, datetime
from typing import Any

from . import challenges, complaints_route, identity, nomination_route
from . import controls as k

DECISION_STATUSES = ("Waiting", "Accepted", "Declined", "Paused", "Withdrawn")
ANSWERED_BY = ("The resident", "Their representative")
ROUTES = ("Service request", "Complaint", "Independent review", "Repair", "Defect", "Hazard",
          "Charge query", "Household dispute")
REQUEST_STATUSES = ("Open", "In progress", "Resolved")
ACCESS_CODES = ("None", "Unknown", "Large print", "Phone only", "Plain language", "Interpreter", "Representative contact", "Safe route needed")
RESIDENT_ACTIONS = ("scope_record", "safe_contact_record", "representative_record", "disclosure_check",
                    "decision_record", "service_open", "service_update", "service_close",
                    "service_reopen", "service_reassign", "update_record", "remedy_confirm", "remedy_update",
                    "challenge_open", "challenge_resolve", "service_forward", "service_supersede_authorize",
                    "nomination_record", "nomination_acknowledge", "nomination_correct", "nomination_review",
                    "tenure_intake", "tenure_legal_position", "tenure_verify", "tenure_question_pack",
                    "tenure_question_pack_review",
                    "tenure_review_trigger", "tenure_trigger_resolve", "tenure_inventory_record")
NOT_RECORDED = "Not recorded"
AUTHORITY_TASKS = ("Receive information", "Communicate", "Attend", "Works decision")
AUTHORITY_STATUSES = ("Confirmed", "Unclear", "Disputed", "Revoked")
RESIDENT_RETENTION_YEARS = 5
RESIDENT_RETENTION_ID = "resident-decisions"
RESIDENT_FIELDS = ("resident_scopes", "measure_decisions", "representative_authorities",
                   "authorised_works_exceptions",
                   "resident_safe_contact", "resident_contact_history", "resident_reviews",
                   "nomination_records", "tenure_reports", "tenure_household_inventories")
AUTHORISED_EXCEPTION_ROLES = frozenset({"Building Safety Liaison", "Retrofit Programme Manager"})
AUTHORISED_EXCEPTION_RULE_ID = "RULE-002; BRD FR-008; BRD FR-011; BRD FR-014"
_AUTOMATED_APPROVER_TOKENS = frozenset(
    {
        "ai",
        "agent",
        "assistant",
        "auto",
        "automated",
        "bot",
        "copilot",
        "llm",
        "model",
        "system",
    }
)
INTAKE_ACTIONS = ("nomination_record", "nomination_acknowledge", "nomination_correct", "nomination_review",
                  "tenure_intake", "tenure_legal_position",
                  "tenure_verify", "tenure_question_pack", "tenure_question_pack_review",
                  "tenure_review_trigger", "tenure_trigger_resolve", "tenure_inventory_record")
REVIEW_TRIGGERS = ("Changed scope", "Dispute", "Defect", "Charge query", "Ambiguous lease identity")
TENURE_ROUTES = {
    "Tenant": "Tenant",
    "Shared owner": "Shared owner",
    "Right to buy leaseholder": "Right to buy",
    "Preserved right to buy leaseholder": "Right to buy",
    "Leaseholder": "Leaseholder",
    "Mixed block": "Mixed block: set a route per household",
}
NOMINATION_OUTCOMES = ("Accepted for human eligibility review", "More evidence needed",
                       "Not progressed; resident may challenge")
INTAKE_FIELDS = ("nomination_records", "tenure_reports", "tenure_household_inventories",
                 "tenure_inventory_view")
# Transport safety bound for one caller-supplied list. It is not a policy limit on households.
INVENTORY_MAX_ROWS = 100
_IDENTITY_UNRESOLVED = ("Unknown", "Ambiguous")
_KNOWN_ROUTES = frozenset(TENURE_ROUTES.values())
INVENTORY_QUALIFICATION = (
    "Caller supplied. Completeness, household identity and authority are not verified here; "
    "this is not a roster, an approval or a release."
)
HAZARD_INTAKE_ROUTE = nomination_route.HAZARD_INTAKE
HAZARD_ROUTING_MESSAGE = nomination_route.HAZARD_ROUTING_MESSAGE
CORRECTION_RAISERS = ("Resident", "Representative", "Officer")
INTAKE_CHANNELS = ("Digital", "Phone", "Letter", "In person", "Trusted intermediary")
TENURE_HOLD = (
    "Tenure and lease identity are unverified. Owner: Home Ownership data owner and Legal "
    "(appointment required). Next action: verify all affected households and obtain a "
    "Legal-reviewed decision route; no measure offer or work release."
)
UNSET_TENURE_REASON = (
    "Tenure and lease interest are not recorded for this home. Owner: Home Ownership data owner. "
    "Next action: record and verify the tenure and decision route (tenant, shared owner, right to buy "
    "or leaseholder) before any measure is offered."
)
MANAGERS = ("Retrofit Programme Manager", "Programme Support Officer")
FORMAL_ROUTES = ("Complaint", "Independent review")
FOLLOWUP_ACTIONS = ("service_open", "service_update", "service_close", "service_reopen", "service_reassign",
                    "update_record", "remedy_confirm", "remedy_update", "challenge_open",
                    "challenge_resolve", "service_supersede_authorize")
CHALLENGE_CHANNELS = ("Digital", "Phone", "Letter", "In person", "Assisted visit",
                      "Trusted intermediary")
CHALLENGE_SUBMITTERS = ("The resident", "Their representative", "Nominee")
NON_RETALIATION_ACTIONS = frozenset({
    "challenge_open", "challenge_resolve", "nomination_record", "nomination_correct", "nomination_review",
    "service_open", "service_reopen",
    "service_update", "service_close", "service_reassign", "service_supersede_authorize",
    "remedy_confirm", "remedy_update",
})
SERVICE_ROUTE_GUARDED_ACTIONS = frozenset({
    "service_update", "service_close", "service_reassign", "service_supersede_authorize",
    "remedy_confirm", "remedy_update",
})


class ResidentCommittedError(RuntimeError):
    """A resident write persisted, but its acknowledgement needs reconciliation."""


def _time():
    return datetime.now(UTC).isoformat()


def _actor(store, user):
    from .change_provenance import _actor as current_actor
    return current_actor(store, user)


def _identity(actor):
    return {key: actor.get(key) for key in ("email", "code", "name", "role", "oid")}


def _identity_value(identity, key):
    value = identity.get(key) if isinstance(identity, dict) else None
    return value.strip().casefold() if isinstance(value, str) else ""


def _same_person(first, second):
    return any(_identity_value(first, key) and _identity_value(first, key) == _identity_value(second, key)
               for key in ("email", "code", "oid"))


def _same_signed_in_person(actor, roster_person):
    """Email and code must match; oid must match only when the roster row records one.

    Display claims and tenant metadata on an Entra principal differ from the roster row, and a row keyed
    by the derived code and email may store no oid. The verified principal already ties code and email
    to its object id.
    """
    if any(_identity_value(actor, key) != _identity_value(roster_person, key) for key in ("email", "code")):
        return False
    recorded_oid = _identity_value(roster_person, "oid")
    return not recorded_oid or recorded_oid == _identity_value(actor, "oid")


def _identity_status(identity):
    return "Known" if any(_identity_value(identity, key) for key in ("code", "oid")) else "Unknown"


def _require_independent_reviewer(reviewer, historical):
    if (_identity_status(historical) == "Unknown"
            or not any(_identity_value(historical, key) and _identity_value(reviewer, key)
                       for key in ("code", "oid"))):
        raise PermissionError("The historical recorder identity is Unknown. Resolve the original evidence before assigning independent review.")
    if _same_person(reviewer, historical):
        raise PermissionError("Choose a reviewer who did not make the contested decision.")


_BINDING_ROLES = ("control_owner", "reviewer")


class SupersessionBinding:
    """Immutable, explicit approval-role binding for manual_verified supersession (issue 1238, Q6).

    Set by trusted composition as ``store.supersession_binding``; unset by default, so supersession
    fails closed. It is never derived from staff roles, requests, stored rows or request bodies. Its
    actual named content is a human gate; changing it withdraws approvals given under the old value.
    """

    __slots__ = ("_binding_id", "_roles", "_digest")

    def __init__(self, binding_id, control_owner, reviewer):
        if not isinstance(binding_id, str) or not 1 <= len(binding_id.strip()) <= 60:
            raise ValueError("A binding needs an identifier of at most 60 characters.")
        roles = []
        for name, given in zip(_BINDING_ROLES, (control_owner, reviewer)):
            identity = {key: given.get(key).strip() for key in ("email", "code", "oid")
                        if isinstance(given, dict) and isinstance(given.get(key), str) and given.get(key).strip()}
            if "email" not in identity or not (identity.get("code") or identity.get("oid")):
                raise ValueError(f"The {name.replace('_', ' ')} needs a known identity: an email and a code or oid.")
            roles.append(tuple(sorted(identity.items())))
        if _same_person(dict(roles[0]), dict(roles[1])):
            raise ValueError("The control owner and reviewer must be different people.")
        object.__setattr__(self, "_binding_id", binding_id.strip())
        object.__setattr__(self, "_roles", dict(zip(_BINDING_ROLES, roles)))
        object.__setattr__(self, "_digest", hashlib.sha256(
            json.dumps([self._binding_id, roles], separators=(",", ":")).encode()).hexdigest())

    def __setattr__(self, name, value):
        raise AttributeError("An approval-role binding is immutable.")

    @property
    def binding_id(self):
        return self._binding_id

    @property
    def digest(self):
        return self._digest

    def identity(self, role):
        return {key: dict(self._roles[role]).get(key) for key in ("email", "code", "oid")}


def _supersession_binding(store):
    binding = getattr(store, "supersession_binding", None)
    if not isinstance(binding, SupersessionBinding):
        raise PermissionError("No approval-role binding is configured, so no one can authorize this supersession. "
                              "A governed configuration step is required first.")
    context = getattr(getattr(store, "local", store), "resident_validation", None)
    if context is not None:
        if context["validating"] and context.get("binding_digest") != binding.digest:
            raise PermissionError("The approval-role binding changed. Reload before continuing.")
        context["binding_digest"] = binding.digest
    return binding


def _same_owner(recorded, current):
    keys = [key for key in ("code", "oid") if _identity_value(recorded, key)]
    return bool(keys) and all(_identity_value(recorded, key) == _identity_value(current, key) for key in keys)


def _approval_detail(binding, case_id, req_id, reservation_id, number, role, evidence_ref):
    """Audit detail carrying a digest of the exact approval payload; the evidence text is never logged."""
    payload = dict(case=case_id, request=req_id, reservation=reservation_id, attempt=number, role=role,
                   identity=binding.identity(role), binding_id=binding.binding_id, binding_digest=binding.digest,
                   evidence_sha256=hashlib.sha256(str(evidence_ref).encode()).hexdigest())
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return f"{req_id} formal-route attempt {number} supersession authorized by the {role.replace('_', ' ')} [approval {digest}]"


def _authorization_holds(store, binding, case_id, req, number, evidence_ref, given):
    """A stored approval counts only under this binding, for the bound person, if the audit holds its exact payload."""
    if not isinstance(given, dict) or given.get("role") not in _BINDING_ROLES or not isinstance(given.get("identity"), dict):
        return False
    role = given["role"]
    bound = binding.identity(role)
    detail = _approval_detail(binding, case_id, req["id"], req["formal_route"]["attempts"][number - 1].get("reservation_id"),
                              number, role, evidence_ref)
    return (given.get("binding_digest") == binding.digest
            and _identity_value(given["identity"], "email") == _identity_value(bound, "email")
            and _same_owner(bound, given["identity"])
            and any(entry.get("who", "").casefold() == _identity_value(bound, "email")
                    and entry.get("action") == "resident_service_supersede_authorize"
                    and entry.get("case") == case_id and entry.get("detail") == detail
                    for entry in store.audit_entries()))


def _day(value):
    try:
        if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("Enter the next update date as a valid YYYY-MM-DD date.") from None
    return value


def _intake_text(value, label, limit=500):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"Supply {label}, at most {limit} characters; the original is never truncated.")
    return value


HazardRouted = nomination_route.HazardRouted


def _refuse_hazard(c, body, *, required=False):
    if required or "hazard_concern" in body:
        if nomination_route.hazard_routing(body.get("hazard_concern"), case_id=c.get("id")) is not None:
            raise HazardRouted(HAZARD_ROUTING_MESSAGE, case_id=c.get("id"))


def _split_optional(body, optional):
    return ({key: value for key, value in body.items() if key not in optional},
            {key: body[key] for key in optional if key in body})


def _raiser(c, extras):
    """Who raised a challenge or correction; a representative needs current confirmed authority to communicate."""
    raised_by = k.choice(extras.get("raised_by", "Officer"), CORRECTION_RAISERS, "who raised the correction")
    raw_ref = extras.get("representative_ref")
    if raised_by != "Representative":
        if raw_ref is not None:
            raise ValueError("A representative reference applies only when a representative raised the correction.")
        return dict(raised_by=raised_by, representative_ref=None)
    if not isinstance(raw_ref, str) or not raw_ref.strip():
        raise ValueError("Representative authority needs human confirmation through the safe contact route.")
    if retention_schedule(c)["expired"]:
        raise ValueError("Resident records are past retention. Obtain current human-reviewed evidence.")
    ref = raw_ref.strip()
    versions = c.get("representative_authorities", {}).get(ref, [])
    today = k.today()
    safe_ref = c.get("resident_safe_contact")
    safe_rev = len(c.get("resident_contact_history", []))
    for measure in case_measures(c):
        for_measure = [v for v in versions if v.get("measure") == measure]
        if not for_measure:
            continue
        a = for_measure[-1]
        context = current_context(c, measure)
        if (context and a["status"] == "Confirmed" and "Communicate" in a["tasks"]
                and a["context_revision"] == context["revision"]
                and a["safe_contact_ref"] == safe_ref
                and a["safe_contact_revision"] == safe_rev
                and a["authority_date"] <= today < a["review_date"]):
            return dict(raised_by=raised_by, representative_ref=ref)
    raise ValueError("Representative authority needs human confirmation through the safe contact route.")


def _intake_fields(user, c, body, fields):
    from . import projection
    if not projection.appointment_evidence_visible(user):
        raise PermissionError("Intake evidence needs current resident-workflow and recorded-reason rights.")
    if set(body) != {"action", *fields}:
        raise ValueError("Supply only the intake fields. Verification and approvals cannot be supplied here.")
    if body["case_id"] != c["id"]:
        raise ValueError("The reported home does not match this case. Ask the data owner to reconcile identity; do not transfer the account.")


def _tenure_report(c, body):
    reports = c.get("tenure_reports", [])
    number = body["report_version"]
    if type(number) is not int or not 1 <= number <= len(reports):
        raise ValueError("Choose an existing tenure report version for this case.")
    return reports[number - 1]


def _open_triggers(report):
    return [t for t in report.get("review_triggers", []) if t["resolution"] is None]


def _inventory_managed(c):
    """Presence, not truthiness, so a null or corrupted field cannot opt a case out."""
    reports = c.get("tenure_reports")
    return bool("tenure_household_inventories" in c or c.get("tenure_review_required") or reports
                or ("tenure_reports" in c and not isinstance(reports, list)))


def _household_ref_ok(ref):
    return isinstance(ref, str) and bool(ref.strip()) and ref == ref.strip() and len(ref) <= 100


def _history_rows_ok(rows):
    if rows is None:
        return True
    if not isinstance(rows, list) or not 1 <= len(rows) <= INVENTORY_MAX_ROWS:
        return False
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"household_ref", "report_version", "report_digest"}:
            return False
        ref, link, digest = row["household_ref"], row["report_version"], row["report_digest"]
        if not _household_ref_ok(ref) or ref.casefold() in seen:
            return False
        seen.add(ref.casefold())
        if link is None:
            if digest is not None:
                return False
        elif type(link) is not int or link < 1 or not isinstance(digest, str):
            return False
    return True


def _inventory_history_ok(inventories, case_id):
    """Non-mutating check of every stored revision. Old digests may differ from current reports."""
    if not isinstance(inventories, list) or not inventories:
        return False
    for number, revision in enumerate(inventories, 1):
        if (not isinstance(revision, dict) or type(revision.get("version")) is not int
                or revision["version"] != number or revision.get("case_id") != case_id
                or "households" not in revision or not _history_rows_ok(revision["households"])):
            return False
    return True


def _inventory_fill(view, case):
    reports = case.get("tenure_reports", [])
    if not isinstance(reports, list) or not all(isinstance(r, dict) for r in reports):
        raise TypeError("reports")
    if "tenure_household_inventories" not in case:
        view["reasons"].append("No expected-household inventory has been recorded for this case.")
        return
    inventories = case["tenure_household_inventories"]
    if not _inventory_history_ok(inventories, case.get("id")):
        raise ValueError("history")
    latest = inventories[-1]
    view["version"] = latest["version"]
    households = latest["households"]
    if households is None:
        view.update(status="Unknown")
        view["reasons"].append("The expected-household inventory is Unknown.")
        return
    view.update(status="Declared", expected_count=len(households))
    entries = []
    for row in households:
        ref, link, digest = row["household_ref"], row["report_version"], row["report_digest"]
        entry = dict(household_ref=ref, report_version=link, linkage="Not linked", binding="Not linked")
        if link is not None:
            report = reports[link - 1] if 1 <= link <= len(reports) else None
            entry["linkage"] = "Linked"
            if report is None or report["household_ref"] != ref:
                entry["binding"] = "Stale: linked report is missing"
            elif any(r["household_ref"] == ref for r in reports[link:]):
                entry["binding"] = "Stale: a newer report exists for this reference"
            elif _digest(report) != digest:
                entry["binding"] = "Stale: the linked report changed"
            else:
                entry["binding"] = "Current"
            if report is not None and report["household_ref"] == ref:
                entry.update(verification=report["verification"], identity_state=report["identity_state"],
                             decision_route=report["decision_route"], open_triggers=len(_open_triggers(report)))
        entries.append(entry)
    view["households"] = entries
    unlinked = sum(e["linkage"] == "Not linked" for e in entries)
    stale = sum(e["binding"].startswith("Stale") for e in entries)
    unverified = sum(e["linkage"] == "Linked" and not str(e.get("verification")).startswith("Verified")
                     for e in entries)
    triggers = sum(bool(e.get("open_triggers")) for e in entries)
    # No existing action changes identity_state, so the intake value stands; a later verification is not
    # inferred to supersede it. Counts only: no reference, owner, source or digest enters a reason.
    identity = sum("identity_state" in e and (not isinstance(e["identity_state"], str)
                                              or e["identity_state"] in _IDENTITY_UNRESOLVED)
                   for e in entries)
    routes = sum("decision_route" in e and not (isinstance(e["decision_route"], str)
                                                and e["decision_route"] in _KNOWN_ROUTES)
                 for e in entries)
    view.update(linked=len(entries) - unlinked, not_linked=unlinked, stale=stale)
    for count, text in (
        (unlinked, f"{unlinked} of {len(entries)} expected households have no linked tenure report."),
        (stale, f"{stale} linked tenure reports changed or were replaced since this inventory. Record a new inventory version."),
        (unverified, f"{unverified} linked tenure reports are not verified by the data owner."),
        (identity, f"{identity} linked tenure reports still have an unresolved or ambiguous household identity."),
        (routes, f"{routes} linked tenure reports have no recorded decision route or an invalid one."),
        (triggers, f"{triggers} linked tenure reports have an open review trigger."),
    ):
        if count:
            view["reasons"].append(text)


def tenure_inventory_view(case):
    """Pure read of the caller-declared inventory. It never mutates, permits or releases."""
    view = dict(status="Missing", version=None, expected_count="Unknown", households=[], linked=0,
                not_linked=0, stale=0, reasons=[], qualification=INVENTORY_QUALIFICATION,
                release="Not available here: the case-wide tenure hold remains")
    try:
        _inventory_fill(view, case)
    except (AttributeError, KeyError, TypeError, ValueError):
        view.update(status="Malformed", version=None, expected_count="Unknown", households=[],
                    linked=0, not_linked=0, stale=0,
                    reasons=["The stored expected-household inventory is malformed. Ask the data owner to reconcile it."])
    return view


def _inventory_rows(households, reports):
    if households is None:
        return None
    if not isinstance(households, list) or not households:
        raise ValueError("List the expected households, or record the inventory as Unknown with null. An empty list is not accepted.")
    if len(households) > INVENTORY_MAX_ROWS:
        raise ValueError(f"The list is over the {INVENTORY_MAX_ROWS} household transport limit and is never truncated. Record the inventory as Unknown and ask the data owner how to proceed.")
    rows, seen = [], set()
    for row in households:
        if not isinstance(row, dict) or set(row) != {"household_ref", "report_version"}:
            raise ValueError("Each household needs exactly household_ref and report_version, which is null when no report is linked.")
        ref = row["household_ref"]
        if not _household_ref_ok(ref):
            raise ValueError("Supply each household reference as reported: not blank, no surrounding spaces, at most 100 characters.")
        if ref.casefold() in seen:
            raise ValueError("Each household reference may appear once. Duplicates are ambiguous and are never merged.")
        seen.add(ref.casefold())
        link, digest = row["report_version"], None
        if link is not None:
            if type(link) is not int or not 1 <= link <= len(reports) or reports[link - 1]["household_ref"] != ref:
                raise ValueError("Link only an existing tenure report version of this case with exactly the same household reference, or null.")
            if any(r["household_ref"] == ref for r in reports[link:]):
                raise ValueError("Link the latest tenure report for that household reference. A later report never closes an earlier dispute.")
            digest = _digest(reports[link - 1])
        rows.append(dict(household_ref=ref, report_version=link, report_digest=digest))
    return rows


def _inventory_refusal(c):
    """Specific refusal reasons only once an inventory field exists; the hold itself is separate."""
    if not _inventory_managed(c):
        return []
    view = tenure_inventory_view(c)
    return [] if view["status"] == "Missing" else view["reasons"]


def _pack_is_current(report, pack):
    if _open_triggers(report):
        return False
    if pack.get("trigger_version", 0) != len(report.get("review_triggers", [])):
        return False
    verifications = report.get("verifications", [])
    positions = report.get("legal_positions", [])
    return bool(verifications and positions
                and verifications[-1]["version"] == pack["verification_version"]
                and verifications[-1]["outcome"] == "Verified"
                and positions[-1]["version"] == pack["legal_position_version"])


def _intake_owner(store, email):
    from . import projection
    owner = _person(store, email)
    if not projection.appointment_evidence_visible(owner):
        raise ValueError("Choose a named follow-up owner with resident-workflow and recorded-reason rights.")
    return _identity(owner)


def _version(body, record):
    from .store import ConflictError
    value = body.get("expected_version")
    if type(value) is not int or value < 0:
        raise ValueError("Reload and supply the current record version.")
    if value != (record or {}).get("version", 0):
        raise ConflictError("The resident record changed. Reload before recording this step.")


def _person(store, email):
    if not isinstance(email, str) or not email.strip():
        raise ValueError("Choose a named resident-workflow colleague from the staff list.")
    if hasattr(store, "db"):
        row = store.db.execute("SELECT body FROM staff WHERE email=?", (email.lower(),)).fetchone()
        candidate = json.loads(row[0]) if row else {}
    else:
        candidate = store.staff.get(email.lower(), {})
    if not candidate or candidate.get("role") not in k.RESIDENT_VIEW_ROLES:
        raise ValueError("Choose a current named resident-workflow colleague from the staff list.")
    actor = _actor(store, candidate)
    k.require_role(actor, k.RESIDENT_VIEW_ROLES, "current resident-workflow staff")
    if not actor.get("code") or actor["name"].strip().casefold() == actor["role"].casefold():
        raise PermissionError("Choose a registered named person, not a role or unresolved identity.")
    context = getattr(getattr(store, "local", store), "resident_validation", None)
    if context is not None and not context["validating"]:
        context["subjects"].append(deepcopy(actor))
    return actor


def _require_named_reviewer(actor, identity):
    """Persisted identity continuity: every recorded code/oid must match; no manager bypass."""
    if _identity_status(identity) == "Unknown":
        raise PermissionError("The named reviewer's identity is Unknown. Resolve it before forwarding this review.")
    compared = [(_identity_value(identity, key), _identity_value(actor, key)) for key in ("code", "oid")
                if _identity_value(identity, key)]
    if not compared or any(recorded != current for recorded, current in compared):
        raise PermissionError("Only the named independent reviewer can send this review.")


def _owner_rights(store, actor, identity, email=None):
    if actor["role"] in MANAGERS:
        return
    # Legacy lookup authorizes the present action only, never reconstructs history.
    owner = _actor(store, identity) if identity else _person(store, email)
    if not _same_signed_in_person(actor, owner):
        raise PermissionError("Only the named current owner or a resident-workflow manager can record this step.")


def _review_current(record):
    reviews = record.get("reviews") or []
    return bool(reviews) and reviews[-1].get("record_version") == record.get("version")


def nomination_follow_up(record, today=None):
    """Read-only readiness view: never a decision, priority, consent or hazard change."""
    missing = nomination_route.missing_before_review(record)
    due = record.get("next_update")
    try:
        overdue = date.fromisoformat(due) < (today or datetime.now(UTC).date()) if due else "Unknown"
    except (TypeError, ValueError):
        overdue = "Unknown"
    return dict(
        route_ready=not missing,
        missing=missing or [],
        next_update_overdue=overdue,
        re_review_pending=bool(record.get("corrections")) and not _review_current(record),
        dependent_review_versions_stale=[r["record_version"] for r in record.get("reviews") or []
                                         if r.get("stale_from_version")],
        automatic_acceptance=False,
        automatic_sanction=False,
        review_current=_review_current(record),
        review_owner="Human identity and eligibility review; policy owner not yet appointed (OD-41/42)",
        not_inferred=["priority change", "consent or refusal", "vulnerability", "sanction",
                      "hazard clock change", "eligibility"],
    )


def confirmed_communicate_representatives(c):
    """Return sorted representative references with confirmed, in-date Communicate authority."""
    if retention_schedule(c)["expired"]:
        return []
    today = k.today()
    safe_ref = c.get("resident_safe_contact")
    safe_rev = len(c.get("resident_contact_history", []))
    measures = case_measures(c)
    confirmed = []
    for ref, versions in sorted((c.get("representative_authorities") or {}).items()):
        if not isinstance(ref, str) or not ref.strip() or not isinstance(versions, list):
            continue
        for measure in measures:
            for_measure = [v for v in versions if isinstance(v, dict) and v.get("measure") == measure]
            if not for_measure:
                continue
            a = for_measure[-1]
            context = current_context(c, measure)
            if (context and a.get("status") == "Confirmed" and "Communicate" in (a.get("tasks") or ())
                    and a.get("context_revision") == context["revision"]
                    and a.get("safe_contact_ref") == safe_ref
                    and a.get("safe_contact_revision") == safe_rev
                    and a.get("authority_date", "") <= today < a.get("review_date", "")):
                confirmed.append(ref.strip())
                break
    return confirmed


def nomination_permissions(store, user, case):
    """Describe role-gated field permissions for nomination, acknowledgement, correction and challenge forms."""
    from . import projection
    if user is None or not challenge_references_visible(store, user):
        return None
    can_write = bool(projection.appointment_evidence_visible(user))
    is_manager = user.get("role") in MANAGERS
    acknowledgeable_ids = []
    correctable_ids = []
    editable_ids = []
    for rec in case.get("nomination_records", []):
        rec_id = rec.get("id")
        if not isinstance(rec_id, str) or not rec_id:
            continue
        known_owner = _identity_status(rec.get("owner")) == "Known"
        owns_or_manager = is_manager or (known_owner and _same_person(user, rec.get("owner")))
        can_ack = can_write and not _review_current(rec) and (not known_owner or owns_or_manager)
        can_corr = can_write and owns_or_manager
        if can_ack:
            acknowledgeable_ids.append(rec_id)
        if can_corr:
            correctable_ids.append(rec_id)
        if can_ack or can_corr:
            editable_ids.append(rec_id)
    staff_owners = []
    for person in store.data.get("staff", ()):
        if not isinstance(person, dict) or not person.get("code") or not projection.appointment_evidence_visible(person):
            continue
        if is_manager or _same_person(user, person):
            staff_owners.append(dict(
                email=person.get("email"),
                name=person.get("name"),
                role=person.get("role"),
            ))
    staff_owners.sort(key=lambda owner: str(owner.get("email") or "").lower())
    return dict(
        can_view=True,
        can_write=can_write,
        can_submit_digital=can_write,
        can_submit_staff_recorded_non_digital=can_write,
        can_assign_third_party_owner=can_write and is_manager,
        can_reassign_owner=is_manager,
        acknowledgeable_nomination_ids=acknowledgeable_ids,
        correctable_nomination_ids=correctable_ids,
        editable_nomination_ids=editable_ids,
        staff_owners=staff_owners,
        representative_authorities=confirmed_communicate_representatives(case),
        channels=["digital", "staff_recorded_non_digital", *INTAKE_CHANNELS],
        challenge_channels=["digital", "staff_recorded_non_digital", "Digital", "Phone", "Letter", "In person"],
        assisted_channels=[
            dict(value="phone", label="Phone"),
            dict(value="paper", label="Paper"),
            dict(value="letter", label="Letter"),
            dict(value="in_person", label="In person"),
            dict(value="trusted_intermediary", label="Trusted intermediary"),
        ],
    )


def followup_view(case, *, recommendations=(), can_view_intake=True, can_view_reason=True):
    """Expose missing legacy provenance without mutating or inventing it."""
    for record in case.get("nomination_records", []):
        cleaned = nomination_route.scrub_nomination_restricted_fields(record)
        record.clear()
        record.update(cleaned)
        fu = nomination_follow_up(record)
        expl = nomination_route.filter_explanation_for_viewer(
            nomination_route.nomination_explanation(
                record,
                follow_up=fu,
                recommendations=recommendations,
                can_view_intake=can_view_intake,
                can_view_reason=can_view_reason,
            ),
            can_view_intake=can_view_intake,
            can_view_reason=can_view_reason,
        )
        if expl is not None:
            fu["plain_language_explanation"] = expl
            record["plain_language_explanation"] = deepcopy(expl)
        record["follow_up"] = fu
        record["challenge_trail"] = nomination_route.challenge_trail(
            record, case.get("affected_challenges", ())
        )
    for req in case.get("service_requests", []):
        if req.get("route") == "Independent review":
            req["reviewed_identity_status"] = _identity_status(req.get("reviewed_identity"))
        req.setdefault("status_owner", None)
        req.setdefault("status_at", None)
        req.setdefault("version", 0)
        req.setdefault("remedy", dict(status="Unknown", owner=None, at=None,
                                      opened_at=None, version=0, history=[]))
    update = case.get("resident_update")
    if update:
        for key in ("purpose", "basis", "owner_identity", "at", "opened_at"):
            update.setdefault(key, None)
        update.setdefault("version", 0)
        update.setdefault("status", "Unknown")
        update.setdefault("safe_contact_ref", "Unknown")
    if _inventory_managed(case):
        case["tenure_inventory_view"] = tenure_inventory_view(case)
    return case


def validate_sql(store):
    context = getattr(store.local, "resident_validation", None)
    if context is None:
        return
    context["validating"] = True
    try:
        actor = _actor(store, context["actor"])
        for subject in context["subjects"]:
            try:
                current = _person(store, subject["email"])
            except ValueError:
                raise PermissionError("Resident-workflow responsibility changed. Reload before continuing.") from None
            if current != subject:
                raise PermissionError("Resident-workflow responsibility changed. Reload before continuing.")
        row = store.db.execute("SELECT rowversion, body FROM cases WHERE id=?", (context["case_id"],)).fetchone()
        if not row or row[0] != context["rowversion"]:
            from .store import ConflictError
            raise ConflictError(context["case_id"])
        # Replay validation on a detached current input, never on the persisted record.
        getattr(store, "_res_" + context["body"]["action"])(actor, json.loads(row[1]), context["body"])
    finally:
        context["validating"] = False


def mark_committed(store):
    context = getattr(store.local, "resident_validation", None)
    if context is not None:
        context["persisted"] = True
    mark_priority_committed(store)


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _is_replaying_sql(store):
    holder = getattr(store, "local", None)
    ctx = getattr(holder, "resident_validation", None) if holder is not None else None
    return bool(ctx and ctx.get("validating"))


def _challenge_has_correction(record):
    return ((record.get("resolution") or {}).get("outcome") == "Correction recorded"
            or record.get("prior_correction_preserved") is True)


def priority_binding(rec):
    """Bind original suggestion inputs separately from the retained human disposition."""
    kind = rec.get("kind")
    if kind == "ai_task":
        prov = rec.get("provenance")
        raw_hashes = prov.get("source_hashes") if isinstance(prov, dict) else None
        original = {key: rec.get(key) for key in (
            "id", "kind", "task", "created", "source", "model", "prompt_version",
            "policy_version", "case_ids", "ai_output", "workflow_output", "sources", "release",
        )}
        original["source_hashes"] = deepcopy(raw_hashes if isinstance(raw_hashes, dict) else {})
        decision = {
            "status": deepcopy(rec.get("status")),
            "resolved_by": deepcopy(rec.get("resolved_by")),
            "resolved_at": deepcopy(rec.get("resolved_at")),
            "reason": deepcopy(rec.get("reviewer_reason")
                               if "reviewer_reason" in rec else rec.get("reason")),
            "reviewer_action": deepcopy(rec.get("reviewer_action")),
            "override_text": deepcopy(rec.get("override_text")),
        }
        return _digest(original), _digest(decision), decision
    if kind == "form_staging":
        original = {key: deepcopy(rec.get(key)) for key in (
            "id", "kind", "case_id", "schema_id", "schema_version",
            "schema_digest", "source", "candidates",
        )}
        decision = deepcopy(rec.get("human_decision") or {
            "status": "Proposed", "resolved_by": None, "resolved_at": None, "reason": None,
        })
        return _digest(original), _digest(decision), decision
    original = {key: rec.get(key) for key in (
        "id", "created", "source", "model", "prompt_version", "policy_version",
        "source_versions", "case_ids", "items", "workflow_items", "ai_output", "release",
    )}
    decision = {key: deepcopy(rec.get(key)) for key in (
        "status", "resolved_by", "resolved_at", "reason", "final_items",
    )}
    return _digest(original), _digest(decision), decision


def _form_staging_records(case, catalog_only=False):
    out = []
    if not isinstance(case, dict):
        return out
    case_id = case.get("id")
    drafts = case.get("form_reviews") or case.get("form_drafts") or []
    held_drafts = {
        hold.get("draft_id")
        for hold in (case.get("finance_decision_holds") or [])
        if isinstance(hold, dict)
        and hold.get("status") == "Held"
        and isinstance(hold.get("draft_id"), str)
    }
    linked_batches = set()
    for draft in drafts:
        if not isinstance(draft, dict) or draft.get("id") in held_drafts:
            continue
        for row in (draft.get("fields") or {}).values():
            ev = (row or {}).get("evidence") or {}
            if isinstance(ev.get("batch_id"), str):
                linked_batches.add(ev["batch_id"])
    challenged_ids = {
        (ch.get("target") or {}).get("id")
        for ch in (case.get("affected_challenges") or [])
        if isinstance(ch, dict)
    } | {
        ch.get("proposal_id")
        for ch in (case.get("affected_challenges") or [])
        if isinstance(ch, dict)
    }
    for batch in case.get("form_staging") or []:
        if not isinstance(batch, dict) or not isinstance(batch.get("id"), str):
            continue
        batch_id = batch["id"]
        prop_id = f"form:{batch_id}"
        if catalog_only and batch_id not in linked_batches and prop_id not in challenged_ids:
            continue
        verified_by = None
        verified_at = None
        for draft in drafts:
            if not isinstance(draft, dict) or draft.get("id") in held_drafts:
                continue
            for row in (draft.get("fields") or {}).values():
                ev = (row or {}).get("evidence") or {}
                if ev.get("batch_id") == batch_id:
                    ver = ev.get("verification") or {}
                    verified_by = ver.get("verified_by") or row.get("updated_by") or draft.get("recorded_by")
                    verified_at = ver.get("verified_at") or row.get("updated_at") or draft.get("recorded_at")
                    break
            if verified_by:
                break
        src = batch.get("source") or {}
        src_ver = (f"{src.get('id')}:{src.get('version')}:{src.get('content_sha256')}"
                   if src.get("id") else None)
        pol_ver = (f"{batch.get('schema_id')}@{batch.get('schema_version')}:{batch.get('schema_digest')}"
                   if batch.get("schema_id") else None)
        proc = batch.get("processing") or {}
        out.append(dict(
            id=prop_id, kind="form_staging", case_id=case_id,
            case_ids=[case_id] if case_id else [], schema_id=batch.get("schema_id"),
            schema_version=batch.get("schema_version"), schema_digest=batch.get("schema_digest"),
            source=proc.get("mode") or "ai", model=proc.get("model"),
            prompt_version=proc.get("prompt_version"), policy_version=pol_ver,
            source_versions={case_id: src_ver} if case_id and src_ver else {},
            candidates=deepcopy(batch.get("candidates") or []),
            resolved_by=verified_by,
            human_decision=dict(
                status="Accepted" if verified_by else "Proposed",
                resolved_by=verified_by, resolved_at=verified_at, reason=None,
            ),
        ))
    return out


def _priority_record(store, rec_id, case=None):
    if not isinstance(rec_id, str) or not rec_id or len(rec_id) > 64:
        raise ValueError("Choose a recorded suggestion for this case.")
    if case is not None and rec_id.startswith("form:"):
        found = next((r for r in _form_staging_records(case) if r["id"] == rec_id), None)
        if not found:
            raise ValueError("Choose a recorded suggestion for this case.")
        return found
    if hasattr(store, "db"):
        with store.dblock:
            row = store.db.execute("SELECT body FROM recommendations WHERE id=?", (rec_id,)).fetchone()
        rec = json.loads(row[0]) if row else None
    else:
        rec = next((r for r in store.data["recommendations"] if r["id"] == rec_id), None)
    if not rec:
        raise ValueError("Choose a recorded suggestion for this case.")
    return rec


def _source_version_for(rec, case_id):
    if rec.get("kind") == "ai_task":
        prov = rec.get("provenance")
        hashes = prov.get("source_hashes") if isinstance(prov, dict) else None
        return hashes.get(case_id) if isinstance(hashes, dict) else None
    sv = rec.get("source_versions")
    return sv.get(case_id) if isinstance(sv, dict) else None


def _policy_version_for(rec):
    if rec.get("kind") == "ai_task":
        return rec.get("policy_version") or rec.get("prompt_version")
    return rec.get("policy_version")


def _policy_id_for(rec):
    if rec.get("kind") == "ai_task":
        return f"ai-task:{rec.get('task') or 'task'}"
    if rec.get("kind") == "form_staging":
        return f"form-schema:{rec.get('schema_id') or 'form'}"
    return "priority-ranking"


def _dependency(rec, kind, case_id):
    if kind == "proposal":
        return dict(kind=kind, id=rec["id"], version=priority_binding(rec)[0])
    if kind == "human_decision":
        if not rec.get("resolved_by"):
            raise ValueError("This suggestion has no recorded human decision yet. Challenge the suggestion instead.")
        return dict(kind=kind, id=rec["id"], version=priority_binding(rec)[1])
    if kind == "source":
        version = _source_version_for(rec, case_id)
        if not version:
            raise ValueError("This older suggestion has no recorded source version. Challenge the suggestion instead.")
        return dict(kind=kind, id=case_id, version=version)
    if kind == "policy":
        pol_version = _policy_version_for(rec)
        if not pol_version:
            raise ValueError("This suggestion has no recorded policy version. Challenge the suggestion instead.")
        return dict(kind=kind, id=_policy_id_for(rec), version=pol_version)
    raise ValueError("Choose proposal, source, policy or human_decision.")


def priority_correction_lookup(store, sql_current=False):
    """Index correction dependencies once, without loading SQL case bodies in a writer."""
    if sql_current:
        rows = store._priority_correction_rows()
    else:
        rows = ((case["id"], record["id"], record["target"])
                for case in store.cases.values()
                for record in case.get("affected_challenges", [])
                if _challenge_has_correction(record))
    lookup = {}
    for case_id, record_id, target in rows:
        key = (target["kind"], target["id"], target["version"])
        lookup.setdefault(key, set()).add(f"{case_id}/{record_id}")
    return lookup


def challenge_references_visible(store, user):
    """Recheck both evidence rights against the current registered reader."""
    from . import projection
    if not user:
        return False
    email = user.get("email")
    if not isinstance(email, str):
        return False
    if identity.is_entra(user):
        current = identity.verified(user) or {}
    elif hasattr(store, "db"):
        with store.dblock:
            row = store.db.execute("SELECT body FROM staff WHERE email=?", (email.lower(),)).fetchone()
        current = json.loads(row[0]) if row else {}
    else:
        current = store.staff.get(email.lower(), {})
    return (projection.appointment_evidence_visible(current)
            and all(current.get(key) == user.get(key) for key in ("email", "code", "name", "role", "oid")))


def priority_challenge_state(store, rec, corrections=None):
    """Derive correction effects without rewriting original proposals or human decisions."""
    dependencies = [_dependency(rec, "proposal", None)]
    if rec.get("kind") == "ai_task":
        prov = rec.get("provenance")
        raw_hashes = prov.get("source_hashes") if isinstance(prov, dict) else None
        source_map = raw_hashes if isinstance(raw_hashes, dict) else {}
    else:
        sv = rec.get("source_versions")
        source_map = sv if isinstance(sv, dict) else {}
    dependencies += [dict(kind="source", id=cid, version=version)
                     for cid, version in source_map.items() if version]
    if _policy_version_for(rec):
        dependencies.append(_dependency(rec, "policy", None))
    if rec.get("resolved_by"):
        dependencies.append(_dependency(rec, "human_decision", None))
    if corrections is None:
        corrections = priority_correction_lookup(store)
    causes = set().union(*(corrections.get((d["kind"], d["id"], d["version"]), set())
                           for d in dependencies))
    return dict(stale=bool(causes), review_stale=bool(causes and rec.get("resolved_by")),
                challenge_ids=sorted(causes))


def _priority_includes_case(rec, case_id):
    return (case_id in rec.get("case_ids", [])
            or any(item["case_id"] == case_id for item in rec.get("final_items") or []))


def challenge_catalog(store, case_id, *, can_view_intake=True, can_view_reason=True):
    out = []
    corrections = priority_correction_lookup(store)
    ai_rows = []
    for rec in store.data["recommendations"]:
        if not _priority_includes_case(rec, case_id):
            continue
        original, decision_version, decision = priority_binding(rec)
        entry = dict(proposal_id=rec["id"], proposal_version=original,
                     decision_version=decision_version, human_decision=decision,
                     source_version=(rec.get("source_versions") or {}).get(case_id),
                     policy_version=rec.get("policy_version"), model=rec.get("model"),
                     prompt_version=rec.get("prompt_version"), source=rec.get("source"),
                     **priority_challenge_state(store, rec, corrections))
        expl = nomination_route.filter_explanation_for_viewer(
            nomination_route.challenge_explanation(
                entry,
                can_view_intake=can_view_intake,
                can_view_reason=can_view_reason,
            ),
            can_view_intake=can_view_intake,
            can_view_reason=can_view_reason,
        )
        if expl is not None:
            entry["plain_language_explanation"] = expl
        out.append(entry)
    return out


def validate_priority_sql(store):
    context = getattr(store.local, "priority_challenge_validation", None)
    if context is not None:
        _actor(store, context["actor"])
        if context["action"] != "reject" and priority_challenge_state(
                store, context["record"], priority_correction_lookup(store, sql_current=True))["stale"]:
            raise PermissionError("A supplied correction affects this suggestion. Owner: its reviewer. Create a fresh suggestion or use the manual route.")


def mark_priority_committed(store):
    holder = getattr(store, "local", store)
    context = getattr(holder, "priority_challenge_validation", None)
    if context is not None:
        context["persisted"] = True


@contextmanager
def priority_review(store, user, rec_id, action):
    """Fence the reverse race: a correction may commit while a reviewer is saving."""
    actor = _actor(store, user)
    rec = next((r for r in store.data["recommendations"] if r["id"] == rec_id), None)
    if not rec:
        raise KeyError(rec_id)
    if action != "reject" and priority_challenge_state(store, rec)["stale"]:
        raise PermissionError("A supplied correction affects this suggestion. Owner: its reviewer. Create a fresh suggestion or use the manual route.")
    holder = getattr(store, "local", store)
    previous = getattr(holder, "priority_challenge_validation", None)
    context = dict(actor=actor, record=deepcopy(rec), action=action, persisted=False)
    holder.priority_challenge_validation = context
    before = deepcopy(rec)
    sql = hasattr(store, "db")
    if sql:
        store._touched()
    pending = list(store.local.pending) if sql else []
    audit_size = None if sql else (os.path.getsize(store.audit_path) if os.path.exists(store.audit_path) else 0)
    audit_head = None if sql else store.last_hash
    try:
        yield
    except BaseException as error:
        if context["persisted"]:
            logging.getLogger(__name__).exception("Priority review committed; acknowledgement failed")
            raise ResidentCommittedError("The draft review was recorded, but confirmation failed. Reload its history before another action.") from error
        if sql:
            with store.dblock:
                store._discard(pending)
        else:
            rec.clear()
            rec.update(before)
            if os.path.exists(store.audit_path):
                with open(store.audit_path, "r+b") as audit:
                    audit.truncate(audit_size)
            store.last_hash = audit_head
            from .store import Store
            Store.save(store)
        raise
    finally:
        holder.priority_challenge_validation = previous


@contextmanager
def _operation(store, user, case_id, body):
    with store.lock:
        sql = hasattr(store, "db")
        holder = getattr(store, "local", store)
        previous = getattr(holder, "resident_validation", None)
        if sql:
            store._touched()
        pending = list(store.local.pending) if sql else []
        audit_size = None if sql else (os.path.getsize(store.audit_path) if os.path.exists(store.audit_path) else 0)
        audit_head = None if sql else store.last_hash
        before = None
        saving = False
        context = dict(actor=deepcopy(user), body=deepcopy(body), case_id=case_id, subjects=[],
                       validating=False, persisted=False)
        holder.resident_validation = context
        try:
            actor = _actor(store, user)
            k.require_role(actor, k.RESIDENT_VIEW_ROLES, "current resident-workflow staff")
            if not _same_signed_in_person(actor, _person(store, user.get("email"))):
                raise PermissionError("Reload your current staff identity before recording this step.")
            c = store._case(case_id)
            before = deepcopy(c)
            before_ranking = store._ranking() if body["action"] in NON_RETALIATION_ACTIONS else None
            if sql:
                context["rowversion"] = store._rv[case_id]
            detail = getattr(store, "_res_" + body["action"])(actor, c, context["body"])
            if body["action"] in SERVICE_ROUTE_GUARDED_ACTIONS:
                challenges.assert_no_retaliation(before, c)
            if before_ranking is not None:
                store._ranks = None
                after_ranking = store._ranking()
                added_hazard = len(c.get("hazards", [])) > len(before.get("hazards", []))
                before_entry = before_ranking.get(case_id)
                after_entry = after_ranking.get(case_id)
                lowered = (
                    before_entry is not None
                    and after_entry is not None
                    and after_entry["rank"] > before_entry["rank"]
                )
                if lowered or (not added_hazard and after_ranking != before_ranking):
                    raise challenges.ChallengeSafeguardError(
                        "Challenge or correction operation lowered or altered case priority ranking."
                    )
            store.audit(actor["email"], f"resident_{body['action']}", case_id, detail)
            saving = True
            store.save()
            context["persisted"] = True
            yield
        except BaseException as error:
            if sql:
                try:
                    with store.dblock:
                        store._discard(() if context["persisted"] else pending)
                except Exception:
                    error.add_note("Resident record recovery failed; reload to establish the outcome.")
                    logging.getLogger(__name__).exception("Resident record SQL recovery failed")
            elif not context["persisted"] and before is not None:
                c.clear()
                c.update(before)
                try:
                    if os.path.exists(store.audit_path):
                        with open(store.audit_path, "r+b") as audit:
                            audit.truncate(audit_size)
                    store.last_hash = audit_head
                finally:
                    if saving:
                        from .store import Store
                        try:
                            Store.save(store)
                        except Exception:
                            error.add_note("Resident state restoration failed; durable outcome may be unknown. Reload before retrying.")
                            logging.getLogger(__name__).exception("Resident record JSON recovery failed")
            if context["persisted"]:
                logging.getLogger(__name__).exception("Resident record committed; acknowledgement failed")
                raise ResidentCommittedError(
                    "The resident change was recorded, but confirmation failed. Reload and reconcile its history before another action."
                ) from error
            raise
        finally:
            holder.resident_validation = previous


def _receiver(store):
    return getattr(store, "complaints_receiver", None) or complaints_route.receiver_from_env(os.environ)


_IN_FLIGHT: "weakref.WeakKeyDictionary[object, set[tuple[str, str, int]]]" = weakref.WeakKeyDictionary()


def in_flight(store, case_id, request_id):
    return {attempt for case, request, attempt in _IN_FLIGHT.get(store, ()) if (case, request) == (case_id, request_id)}


def _forward(store, user, case_id, body):
    """Reserve, send outside the store lock, then record the outcome; each record is its own committed step."""
    receiver = _receiver(store)
    reservation = uuid.uuid4().hex
    with store.lock:
        with _operation(store, user, case_id, dict(body, action="service_forward", reservation_id=reservation)):
            pass
        req = k.find(store.cases[case_id].get("service_requests", []), body.get("id"), "request")
        route = req["formal_route"]
        matches = [a for a in route["attempts"] if a.get("reservation_id") == reservation]
        if len(matches) != 1:
            raise ResidentCommittedError(
                "The formal-route send was reserved, but its attempt could not be identified. Reload: check with the receiver before retrying."
            )
        attempt = matches[0]["attempt"]
        # Point-in-time guard under the lock; a change after this point is not detected.
        stale = req["status"] == "Closed" or req.get("version", 0) != matches[0]["request_version"]
        envelope = None if stale else complaints_route.build_envelope(case_id, req, route["route_key"], attempt)
        key = (case_id, req["id"], attempt)
        _IN_FLIGHT.setdefault(store, set()).add(key)
    try:
        if envelope is None:
            outcome = dict(status="Failed", reason=complaints_route.NOT_SENT_REASON, not_sent=True)
        else:
            outcome = _send(receiver, envelope)
        outcome.update(action="service_forward_outcome", id=req["id"], attempt=attempt, reservation_id=reservation)
        _record_outcome(store, user, case_id, outcome)
    finally:
        _IN_FLIGHT.get(store, set()).discard(key)


def _record_outcome(store, user, case_id, outcome):
    """Record a send outcome with one bounded retry of the same write; the receiver is never contacted again."""
    last = None
    for _ in range(2):
        try:
            with _operation(store, user, case_id, outcome):
                pass
            return
        except ResidentCommittedError:
            raise
        except Exception as error:
            last = error
            if any(mark in note.lower() for note in getattr(error, "__notes__", ()) for mark in _UNVERIFIED):
                break
            try:
                if _outcome_recorded(store, case_id, outcome):
                    return
            except Exception:
                break
    logging.getLogger(__name__).warning(
        "Formal-route outcome not recorded: %s; case %s request %s attempt %s status %s receipt_ref %r",
        type(last).__name__, case_id, outcome["id"], outcome["attempt"], outcome["status"], outcome.get("receipt_ref"))
    raise ResidentCommittedError(
        "The formal-route send was reserved, but its outcome may not be recorded. Reload to establish the attempt's "
        "state and check with the receiver before retrying."
    ) from last


_UNVERIFIED = ("recovery failed", "restoration failed")


def _outcome_recorded(store, case_id, outcome):
    """True when a lost commit acknowledgement already left this exact outcome on its reserved attempt."""
    with store.lock:
        req = k.find(store.cases[case_id].get("service_requests", []), outcome["id"], "request")
        attempts = (req.get("formal_route") or {}).get("attempts", [])
        found = attempts[outcome["attempt"] - 1] if 1 <= outcome["attempt"] <= len(attempts) else {}
    return (found.get("reservation_id") == outcome["reservation_id"] and found.get("status") == outcome["status"]
            and found.get("receipt_ref") == outcome.get("receipt_ref"))


def _send(receiver, envelope):
    try:
        raw = receiver.submit(envelope)
    except complaints_route.NotConfigured:
        return dict(status="Unconfigured", reason=complaints_route.UNCONFIGURED_REASON)
    except complaints_route.NotSent:
        return dict(status="Failed", reason=complaints_route.NOT_SENT_REASON, not_sent=True)
    except Exception as error:
        logging.getLogger(__name__).warning("Formal-route receiver failed: %s", type(error).__name__)
        return dict(status="Unconfirmed", reason=complaints_route.UNCONFIRMED_REASON)
    try:
        ack = complaints_route.parse_acknowledgement(raw)
    except ValueError:
        return dict(status="Unconfirmed", reason=complaints_route.MALFORMED_REASON)
    return dict(status="Acknowledged", reason="The receiver acknowledged this request.", **ack)


def first_contact(c, today=None):
    """Only actual contact evidence can establish the resident's first interaction."""
    today = date.fromisoformat(today or k.today())
    deleted = c.get("resident_retention_deleted_at")
    tombstone = c.get("resident_retention_tombstone")
    offset = tombstone["contacts_before_deletion"] if tombstone else 0
    legacy = bool(deleted and not tombstone)
    candidates = [((c.get("resident") or {}).get("first_contact_at"), legacy)]
    candidates += [(r.get("at"), legacy) for r in c.get("contacts", [])[offset:]]
    candidates += [(r.get("at"), False) for r in c.get("resident_contact_history", [])]
    days = []
    for raw, legacy_contact in candidates:
        try:
            day = date.fromisoformat(str(raw)[:10])
        except ValueError:
            continue
        if deleted and (day.isoformat() < deleted or
                        (legacy_contact and day.isoformat() == deleted)):
            continue
        if day <= today:
            days.append(day)
    return min(days) if days else None


def remember_first_contact(c):
    day = first_contact(c)
    if day:
        c["resident"]["first_contact_at"] = day.isoformat()


def retention_schedule(c, today=None):
    today = today or k.today()
    start = first_contact(c, today)
    due = None
    if start:
        try:
            due = start.replace(year=start.year + RESIDENT_RETENTION_YEARS)
        except ValueError:
            due = start.replace(year=start.year + RESIDENT_RETENTION_YEARS, day=28)
    return dict(years=RESIDENT_RETENTION_YEARS, trigger="First recorded resident contact",
                first_contact=start.isoformat() if start else None,
                due=due.isoformat() if due else None,
                expired=bool(due and due.isoformat() <= today),
                status="Known" if start else "Unknown: first recorded contact needs evidence")


def current_context(c, measure):
    versions = c.get("resident_scopes", {}).get(measure, [])
    context = versions[-1] if versions else None
    design = (c.get("technical") or {}).get("design_version")
    return context if context and context["design_version"] == design else None


def require_context(c, body):
    measure = body.get("measure")
    if not isinstance(measure, str) or measure not in case_measures(c):
        raise ValueError("Choose one of this home's measures.")
    context = current_context(c, measure)
    revision = body.get("context_revision")
    if (not context or type(revision) is not int
            or revision != context["revision"]):
        raise ValueError("Confirm the current measure scope and design before recording this step.")
    return measure, context


def _resolve_gate_clock(now: Any) -> tuple[datetime, str, str | None]:
    from . import resident_journey_design

    if now is None:
        return datetime.now(UTC), k.today(), None
    if isinstance(now, datetime):
        parsed_dt = resident_journey_design.parse_iso_utc(now)
        if parsed_dt is None:
            raise ValueError("Invalid naive datetime reference clock.")
        return parsed_dt, parsed_dt.date().isoformat(), parsed_dt.isoformat()
    if not isinstance(now, str) or not now.strip():
        raise ValueError("Invalid reference clock.")
    raw = now.strip()
    if len(raw) == 10:
        day = date.fromisoformat(raw)
        if day.isoformat() != raw:
            raise ValueError("Invalid ISO reference date.")
        dt = datetime(day.year, day.month, day.day, 12, 0, 0, tzinfo=UTC)
        return dt, day.isoformat(), dt.isoformat()
    parsed = resident_journey_design.parse_iso_utc(raw)
    if parsed is None:
        raise ValueError("Invalid ISO UTC reference timestamp.")
    return parsed, parsed.date().isoformat(), parsed.isoformat()


def _iso_day(value: object) -> str | None:
    if not isinstance(value, str) or len(value) != 10:
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return None
    return value if parsed.isoformat() == value else None


def _clean_exception_field(value: object, *, limit: int = 300) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    if not cleaned or len(cleaned) > limit:
        return None
    if k.is_memory_reference(cleaned) or k.is_sensor_reference(cleaned):
        return None
    return cleaned


def validate_authorised_works_exception(
    c: Any,
    measure: Any,
    context: Any,
    *,
    now: str | None = None,
) -> dict[str, Any]:
    """Fail-closed validator for an explicitly authorised works exception (RULE-002, FR-008, FR-014)."""
    from . import resident_journey_design

    def deny(reason: str) -> dict[str, Any]:
        return dict(
            permitted=False,
            reason=reason,
            rule_id=AUTHORISED_EXCEPTION_RULE_ID,
            exception=None,
        )

    if not isinstance(c, dict):
        return deny("Case record is missing or malformed.")
    if not isinstance(measure, str) or measure not in case_measures(c):
        return deny("Exception measure does not belong to this home.")
    if (
        not isinstance(context, dict)
        or type(context.get("revision")) is not int
        or type(context.get("design_version")) is not int
    ):
        return deny("Current measure scope and design context are unverified.")
    try:
        now_utc, check_day, _ = _resolve_gate_clock(now)
    except ValueError:
        return deny("Reference clock is missing or malformed.")
    raw_map = c.get("authorised_works_exceptions")
    if not isinstance(raw_map, dict):
        return deny("No authorised works exception is recorded for this measure.")
    versions = raw_map.get(measure)
    if not isinstance(versions, list) or not versions or any(not isinstance(v, dict) for v in versions):
        return deny("No valid authorised works exception list is recorded for this measure.")
    exc = versions[-1]
    if exc.get("status") != "Authorised":
        return deny("Latest works exception is not in 'Authorised' status.")
    if (
        exc.get("measure") != measure
        or type(exc.get("context_revision")) is not int
        or exc["context_revision"] != context["revision"]
        or type(exc.get("design_version")) is not int
        or exc["design_version"] != context["design_version"]
    ):
        return deny("Works exception does not match the active scope revision and design version.")
    for field_name in ("reference", "rule_source", "reason", "notification_ref"):
        if _clean_exception_field(exc.get(field_name)) is None:
            return deny(f"Works exception {field_name} is missing, out of bounds, or cites prohibited telemetry/memory.")
    approver = _clean_exception_field(exc.get("approved_by"), limit=120)
    if approver is None:
        return deny("Works exception requires a named human approver.")
    tokens = [tok for tok in re.split(r"[^a-z0-9]+", approver.casefold()) if tok]
    if not tokens or any(tok in _AUTOMATED_APPROVER_TOKENS for tok in tokens):
        return deny("Works exception cannot be approved by an automated or AI actor.")
    role = exc.get("approved_by_role")
    if not isinstance(role, str) or role.strip() not in AUTHORISED_EXCEPTION_ROLES:
        return deny("Works exception requires Building Safety Liaison or Retrofit Programme Manager authority.")
    effective_day = _iso_day(exc.get("effective_date"))
    review_day = _iso_day(exc.get("review_date"))
    if effective_day is None or review_day is None or not (effective_day <= check_day < review_day):
        return deny("Works exception is outside its effective/review date window.")
    if "expires_at" in exc and exc.get("expires_at") is not None:
        parsed_exp = resident_journey_design.parse_iso_utc(exc.get("expires_at"))
        if parsed_exp is None or now_utc >= parsed_exp:
            return deny("Works exception has expired or has a malformed expiry timestamp.")
    if type(exc.get("resident_notified")) is not bool or exc.get("resident_notified") is not True:
        return deny("Works exception requires confirmed resident notification before work starts.")
    return dict(
        permitted=True,
        reason="Valid human-authorised, resident-notified works exception is active for the current scope and design.",
        rule_id=AUTHORISED_EXCEPTION_RULE_ID,
        exception=deepcopy(exc),
    )


def authority_for(c, ref, task, measure, context, version=None, *, now=None):
    from . import resident_journey_design

    try:
        now_utc, check_day, _ = _resolve_gate_clock(now)
    except ValueError as err:
        raise ValueError("Representative authority needs human confirmation through the safe contact route.") from err
    if retention_schedule(c, today=check_day)["expired"]:
        raise ValueError("Resident records are past retention. Obtain current human-reviewed evidence.")
    clean_ref = resident_journey_design.valid_representative_ref(ref)
    versions = c.get("representative_authorities", {}).get(clean_ref, []) if clean_ref else []
    a = versions[-1] if versions else None
    if not a or (version is not None and a["version"] != version):
        raise ValueError("Representative authority needs human confirmation through the safe contact route.")
    if (a["status"] != "Confirmed" or task not in a["tasks"]
            or a["measure"] != measure or a["context_revision"] != context["revision"]
            or a["safe_contact_ref"] != c.get("resident_safe_contact")
            or a["safe_contact_revision"] != len(c.get("resident_contact_history", []))
            or not a["authority_date"] <= check_day < a["review_date"]):
        raise ValueError("Representative authority needs human confirmation through the safe contact route.")
    if "expires_at" in a:
        parsed_exp = resident_journey_design.parse_iso_utc(a.get("expires_at"))
        if parsed_exp is None or now_utc >= parsed_exp:
            raise ValueError("Representative authority needs human confirmation through the safe contact route.")
    return a


def resident_gate(c, bindings=None, *, now=None):
    """Case advance checks all measures; scoped work checks only explicit bindings."""
    if _inventory_managed(c):
        return [*_inventory_refusal(c), TENURE_HOLD]
    if not _home_tenure_recorded(c):
        return [UNSET_TENURE_REASON]
    return _resident_decision_gate(c, bindings, now=now)


def _home_tenure_recorded(c):
    home = c.get("home")
    tenure = home.get("tenure") if isinstance(home, dict) else None
    return isinstance(tenure, str) and tenure.strip().casefold() not in ("", "unknown")


def _resident_decision_gate(c, bindings=None, *, now=None):
    try:
        _, check_day, now_iso = _resolve_gate_clock(now)
    except ValueError:
        return ["Resident decision or authority needs confirmation. Owner: Resident Liaison Officer. "
                "Next action: review the affected measure's current scope, supplied answer and authority."]
    if retention_schedule(c, today=check_day)["expired"]:
        return ["Resident records are past retention. Owner: Resident Liaison Officer. Next action: obtain current human-reviewed evidence."]
    if bindings is None:
        bindings = [dict(measure=m, context_revision=(current_context(c, m) or {}).get("revision"))
                    for m in case_measures(c)]
    if not isinstance(bindings, list) or not bindings:
        return ["Resident scope is unknown. Owner: Resident Liaison Officer. Next action: bind the work to its measure and current scope."]
    why, seen = [], set()
    for binding in bindings:
        try:
            if not isinstance(binding, dict):
                raise ValueError("Invalid resident scope binding.")
            measure, context = require_context(c, binding)
            if measure in seen:
                raise ValueError("Choose each measure once.")
            seen.add(measure)
            if c.get("resident_reviews", {}).get(measure, {}).get("status") == "Needs human review":
                raise ValueError("Human review is needed.")
            versions = c.get("measure_decisions", {}).get(measure, [])
            answer = versions[-1] if versions else {}
            if answer.get("context_revision") == context["revision"] and answer.get("status") == "Accepted":
                if answer.get("answered_by") == ANSWERED_BY[1]:
                    authority_for(c, answer.get("representative_ref"), "Works decision", measure, context,
                                  answer.get("authority_version"), now=now_iso)
            else:
                exc_check = validate_authorised_works_exception(c, measure, context, now=now_iso)
                if not exc_check["permitted"]:
                    raise ValueError("A current supplied resident acceptance is needed.")
        except ValueError:
            why.append("Resident decision or authority needs confirmation. Owner: Resident Liaison Officer. "
                       "Next action: review the affected measure's current scope, supplied answer and authority.")
    return why


def resident_status(c):
    """Conservative list/prompt status; a legacy case-wide answer is not scoped evidence."""
    if not _resident_decision_gate(c):
        return "Accepted"
    measures = case_measures(c)
    if measures and all(current_context(c, m) and c.get("measure_decisions", {}).get(m)
                        and c["measure_decisions"][m][-1].get("context_revision") == current_context(c, m)["revision"]
                        and c["measure_decisions"][m][-1]["status"] == "Declined" for m in measures):
        return "Declined"
    return NOT_RECORDED


def case_measures(c):
    m = c.get("measures", [])
    parts = m if isinstance(m, list) else [p.strip() for p in str(m).replace(";", ",").split(",")]
    return [p for p in parts if p]


def measure_decision_view(c):
    """Every measure with its latest recorded answer, or 'Not recorded'. Nothing is filled in."""
    recorded = c.get("measure_decisions") or {}
    out = []
    for measure in case_measures(c):
        context = current_context(c, measure)
        versions = deepcopy(recorded.get(measure, []))
        for version in versions:
            version["recorder_identity_status"] = _identity_status(version.get("recorder_identity"))
        answer = versions[-1] if versions else {}
        status = answer.get("status", NOT_RECORDED) if context and answer.get("context_revision") == context["revision"] else NOT_RECORDED
        out.append(dict(measure=measure, status=status, context=deepcopy(context),
                        versions=deepcopy(versions), readiness="Needs human review" if resident_gate(c, [
                            dict(measure=measure, context_revision=(context or {}).get("revision"))]) else "Resident decision current",
                        review=deepcopy(c.get("resident_reviews", {}).get(measure))))
    return out


NON_DETRIMENT_COMMITMENTS = (
    "Programme place: asking for a review or making a complaint does not remove or delay the household's place in the programme.",
    "Repairs: repairs and defect work continue and are not held back because of a review or complaint.",
    "Safety duties: hazard and safety duties stay in force and are never waived or paused by a review or complaint.",
    "Measures: a pause or withdrawal stays limited to its own measure.",
)
REDRESS_ROUTES = (
    dict(route="Independent review",
         who="The resident, their representative, or frontline staff on their behalf.",
         how="Choose the recorded measure decision to review. A named reviewer who did not record that decision does the review."),
    dict(route="Complaint",
         who="The resident, their representative, or frontline staff on their behalf.",
         how="Record the complaint and the outcome wanted. A different named person owns the redress."),
)


def redress_route_view(c):
    """Read-only route to independent human review and the formal complaints route, with what is preserved."""
    formal = []
    for req in c.get("service_requests", []):
        if req.get("route") not in FORMAL_ROUTES:
            continue
        attempts = (req.get("formal_route") or {}).get("attempts", [])
        sent = attempts[-1]["status"] if attempts else "Not sent"
        formal.append(dict(id=req["id"], route=req["route"], status=req.get("status"),
                           next_update=req.get("next_update"), formal_route_status=sent,
                           review_measure=req.get("review_measure"),
                           review_decision_version=req.get("review_decision_version")))
    recorded = c.get("measure_decisions") or {}
    reviewable = [dict(measure=m, version=n, status=v.get("status"),
                       recorder_identity_status=_identity_status(v.get("recorder_identity")))
                  for m in case_measures(c) for n, v in enumerate(recorded.get(m, []), 1)
                  if _identity_status(v.get("recorder_identity")) != "Unknown"]
    return dict(commitments=list(NON_DETRIMENT_COMMITMENTS), routes=deepcopy(list(REDRESS_ROUTES)),
                reviewable_decisions=reviewable, formal_requests=formal,
                send_note="Recording a request here does not send it. Nothing has reached the formal complaints route unless its status is Acknowledged.")


class ResidentDecisionMixin:
    def resident_recorder(self, user, service=False):
        roles = k.RESIDENT_VIEW_ROLES if service else k.RESIDENT_ROLES
        k.require_role(user, roles, "authorised resident-workflow staff")
        actor = identity.verified(user) if identity.is_entra(user) else self.staff.get(user.get("email", "").lower())
        if not actor or any(actor.get(key) != user.get(key) for key in ("role", "name", "code")):
            raise PermissionError("Resident records require a registered named human staff identity.")
        return actor

    def delete_resident_records(self, user, case_id, today=None):
        self._manager(user, "approve resident record deletion")
        with self.lock:
            c = self._case(case_id)
            if (c.get("legal_hold") or {}).get("active"):
                raise PermissionError("A legal hold blocks deletion on this case.")
            if not retention_schedule(c, today)["expired"]:
                raise ValueError("Resident records are not past their first-contact retention period.")
            c["resident"].pop("first_contact_at", None)
            # Contacts have a separate purpose; count their retained prefix without copying content.
            c["resident_retention_tombstone"] = dict(contacts_before_deletion=len(c.get("contacts", [])))
            for key in RESIDENT_FIELDS:
                c.pop(key, None)
            c["decision"] = dict(status=NOT_RECORDED, by=None, at=None)
            c["resident"]["representative"] = None
            for request in c.get("service_requests", []):
                request.pop("representative_ref", None)
                for attempt in (request.get("formal_route") or {}).get("attempts", []):
                    attempt.pop("resident_request_ref", None)
                    attempt.pop("requested_by", None)
            for challenge in c.get("affected_challenges", []):
                challenge.pop("representative_ref", None)
            c["resident_retention_deleted_at"] = today or k.today()
            self.audit(user["email"], "resident_retention_deleted", case_id, "resident decision payload removed")
            self.save()

    def resident_action(self, user, case_id, body):
        k.refuse_bulk(body)
        action = body.get("action")
        if action not in RESIDENT_ACTIONS:
            raise ValueError("Unknown step.")
        if action == "service_forward":
            return _forward(self, user, case_id, body)
        if action in FOLLOWUP_ACTIONS + INTAKE_ACTIONS or action == "decision_record":
            with _operation(self, user, case_id, body):
                return
        with self.lock:
            self.resident_recorder(user, service=action in ("service_open", "service_update", "service_close"))
            c = self._case(case_id)
            detail = getattr(self, "_res_" + action)(user, c, body)
            self.audit(user["email"], f"resident_{action}", case_id, detail)
            self.save()

    def _res_nomination_record(self, user, c, body):
        body, extras = _split_optional(body, ("assisted_channel",))
        _intake_fields(user, c, body, {
            "case_id", "kind", "reported_subject_ref", "account", "source", "channel",
            "owner", "acknowledgement_ref", "next_update", "non_digital_route", "hazard_concern",
        })
        _refuse_hazard(c, body, required=True)
        stored_channel, route_mode, assisted_channel = nomination_route.normalize_route_channel(
            body["channel"],
            assisted_channel=extras.get("assisted_channel"),
            allow_intermediary=True,
            label="the supplied channel",
        )
        guard = challenges.protected_snapshot(c)
        record = dict(
            id=f"NOM-{uuid.uuid4().hex}", version=1,
            case_id=c["id"], kind=k.choice(body["kind"], ("Officer nomination", "Self-referral"), "the referral kind"),
            original=dict(
                reported_subject_ref=_intake_text(body["reported_subject_ref"], "the unverified subject reference", 100),
                account=_intake_text(body["account"], "the original account", 4000),
                source=_intake_text(body["source"], "the supplied source"),
                channel=stored_channel,
                route_mode=route_mode,
                assisted_channel=assisted_channel,
                recorded_by=_identity(user), at=_time(),
            ),
            identity_status="Unknown", support_needs="Unknown", risk_flags="Unknown",
            owner=_intake_owner(self, body["owner"]),
            acknowledgement=dict(
                reference=_intake_text(body["acknowledgement_ref"], "the staff-recorded acknowledgement evidence"),
                channel=stored_channel,
                route_mode=route_mode,
                assisted_channel=assisted_channel,
                recorded_by=_identity(user), at=_time(), delivery="Not verified by this system",
            ),
            next_update=_day(body["next_update"]),
            non_digital_route=_intake_text(body["non_digital_route"], "the staffed non-digital route"),
            review_status="Human identity and eligibility review required",
            corrections=[],
        )
        c.setdefault("nomination_records", []).append(record)
        challenges.assert_no_retaliation(guard, c)
        return f"{record['id']} unverified intake recorded"

    def _res_nomination_acknowledge(self, user, c, body):
        body, extras = _split_optional(
            body, ("hazard_concern", "channel", "assisted_channel", "owner_reassignment_reason")
        )
        _intake_fields(user, c, body, {
            "case_id", "id", "expected_version", "owner",
            "acknowledgement_ref", "non_digital_route", "next_update",
        })
        _refuse_hazard(c, extras)
        guard = challenges.protected_snapshot(c)
        record = k.find(c.get("nomination_records", []), body["id"], "nomination")
        _version(body, record)
        if _review_current(record):
            raise ValueError("This referral version already has its human review. Record a correction before changing route ownership.")
        if _identity_status(record.get("owner")) == "Known":
            _owner_rights(self, user, record["owner"])
        owner = _intake_owner(self, body["owner"])
        if user["role"] not in MANAGERS and not _same_person(user, owner):
            raise PermissionError("Only a resident-workflow manager can assign another colleague as owner.")
        reassignment_reason = (
            _intake_text(extras["owner_reassignment_reason"], "the owner reassignment reason")
            if extras.get("owner_reassignment_reason") is not None
            else None
        )
        raw_channel = (
            extras["channel"]
            if "channel" in extras
            else ((record.get("original") or {}).get("channel") or "digital")
        )
        stored_channel, route_mode, assisted_channel = nomination_route.normalize_route_channel(
            raw_channel,
            assisted_channel=extras.get("assisted_channel"),
            allow_intermediary=True,
            label="the acknowledgement channel",
        )
        ack_ref = _intake_text(body["acknowledgement_ref"], "the staff-recorded acknowledgement evidence")
        route = _intake_text(body["non_digital_route"], "the staffed non-digital route")
        next_update = _day(body["next_update"])
        if any(record.get(key) is not None for key in ("owner", "acknowledgement", "non_digital_route")):
            record.setdefault("acknowledgement_history", []).append(dict(
                record_version=record["version"],
                owner=deepcopy(record.get("owner")),
                acknowledgement=deepcopy(record.get("acknowledgement")),
                non_digital_route=record.get("non_digital_route"),
            ))
        ack_payload = dict(
            reference=ack_ref,
            channel=stored_channel,
            route_mode=route_mode,
            assisted_channel=assisted_channel,
            recorded_by=_identity(user),
            at=_time(),
            delivery="Not verified by this system",
        )
        if reassignment_reason is not None:
            ack_payload["reassignment_reason"] = reassignment_reason
        record.update(
            version=record["version"] + 1,
            owner=owner,
            acknowledgement=ack_payload,
            non_digital_route=route,
            next_update=next_update,
        )
        challenges.assert_no_retaliation(guard, c)
        return f"{record['id']} route acknowledgement version {record['version']} recorded"

    def _res_nomination_correct(self, user, c, body):
        body, extras = _split_optional(
            body, ("hazard_concern", "raised_by", "representative_ref", "dependencies", "assisted_channel")
        )
        _intake_fields(user, c, body, {
            "case_id", "id", "expected_version", "reported_subject_ref", "account",
            "source", "channel", "next_update", "challenge_id",
        })
        _refuse_hazard(c, extras)
        raiser = _raiser(c, extras)
        stored_channel, route_mode, assisted_channel = nomination_route.normalize_route_channel(
            body["channel"],
            assisted_channel=extras.get("assisted_channel"),
            allow_intermediary=True,
            label="the supplied channel",
        )
        has_deps = "dependencies" in extras
        parsed_deps = nomination_route.parse_dependencies(extras["dependencies"]) if has_deps else {}
        guard = challenges.protected_snapshot(c)
        record = k.find(c.get("nomination_records", []), body["id"], "nomination")
        _version(body, record)
        _owner_rights(self, user, record["owner"])
        challenge = None
        if body["challenge_id"] is not None:
            challenge = deepcopy(k.find(c.get("affected_challenges", []), body["challenge_id"], "this case's challenge"))
        correction = dict(
            version=record["version"] + 1,
            reported_subject_ref=_intake_text(body["reported_subject_ref"], "the corrected unverified subject reference", 100),
            account=_intake_text(body["account"], "the competing corrected account", 4000),
            source=_intake_text(body["source"], "the supplied correction evidence"),
            channel=stored_channel,
            route_mode=route_mode,
            assisted_channel=assisted_channel,
            recorded_by=_identity(user), at=_time(),
            challenge=challenge, **raiser,
        )
        next_update = _day(body["next_update"])
        reviews = record.get("reviews", [])
        correction["challenged_review"] = deepcopy(reviews[-1]) if reviews else None
        re_review_info = nomination_route.re_review_set(
            ("nomination", record["id"], f"v{record['version']}"), parsed_deps, record
        )
        record["corrections"].append(correction)
        for review in reviews:
            review.setdefault("stale_from_version", correction["version"])
        re_review_payload = dict(
            required=True,
            automatic_acceptance=False,
            automatic_sanction=False,
            dependent_review_versions=re_review_info["dependent_review_versions"],
        )
        if has_deps:
            re_review_payload["dependents"] = [
                dict(kind=nk, id=ni, version=nv) for nk, ni, nv in re_review_info["dependents"]
            ]
        correction["re_review"] = re_review_payload
        record.update(version=correction["version"], next_update=next_update,
                      review_status="Re-review required; no priority or consent change")
        challenges.stamp_assurance(guard, c, record)
        return f"{record['id']} correction version {record['version']} recorded"

    def _res_nomination_review(self, user, c, body):
        body, extras = _split_optional(body, ("hazard_concern",))
        _intake_fields(user, c, body, {
            "case_id", "id", "expected_version", "outcome", "rationale", "evidence_ref", "next_update",
        })
        _refuse_hazard(c, extras)
        guard = challenges.protected_snapshot(c)
        record = k.find(c.get("nomination_records", []), body["id"], "nomination")
        _version(body, record)
        nomination_route.require_ready_for_review(record)
        if _identity_status(record.get("owner")) != "Known":
            raise ValueError("Human review cannot start until the referral has a registered named owner.")
        reviews = record.setdefault("reviews", [])
        if reviews and reviews[-1]["record_version"] == record["version"]:
            raise ValueError("This version already has its human review. Record a correction to request another.")
        latest = record["corrections"][-1] if record.get("corrections") else record["original"]
        _require_independent_reviewer(user, latest.get("recorded_by"))
        outcome = k.choice(body["outcome"], NOMINATION_OUTCOMES, "the human review outcome")
        reviews.append(dict(
            record_version=record["version"], outcome=outcome,
            rationale=_intake_text(body["rationale"], "the reviewer's plain-language reasons", 1000),
            evidence_ref=_intake_text(body["evidence_ref"], "the evidence the reviewer considered"),
            competing_evidence_versions=[c_["version"] for c_ in record.get("corrections", [])],
            reviewer=_identity(user), at=_time(),
        ))
        record.update(next_update=_day(body["next_update"]),
                      review_status=f"Human review recorded: {outcome}; no priority, consent or sanction change")
        challenges.assert_no_retaliation(guard, c)
        return f"{record['id']} version {record['version']} human review recorded"

    def _res_tenure_intake(self, user, c, body):
        _intake_fields(user, c, body, {
            "case_id", "household_ref", "expected_version", "reported_tenure",
            "reported_lease_interest", "identity_state", "source", "owner", "next_update",
        })
        reports = c.get("tenure_reports", [])
        _version(body, reports[-1] if reports else None)
        report = dict(
            version=len(reports) + 1, case_id=c["id"],
            household_ref=_intake_text(body["household_ref"], "the reported household reference", 100),
            reported_tenure=k.choice(body["reported_tenure"], (
                "Tenant", "Shared owner", "Right to buy leaseholder",
                "Preserved right to buy leaseholder", "Leaseholder", "Mixed block", "Unknown",
            ), "the reported tenure"),
            reported_lease_interest=_intake_text(body["reported_lease_interest"], "the reported lease-interest status or Unknown"),
            identity_state=k.choice(body["identity_state"], ("Unknown", "Ambiguous"), "the unresolved identity state"),
            source=_intake_text(body["source"], "the tenure source reference"),
            verification="Unknown", decision_route="Unknown", legal_position="Unknown",
            cost_position="Unknown", review_status="Open; human data-owner and Legal review required",
            owner=_intake_owner(self, body["owner"]), next_update=_day(body["next_update"]),
            recorded_by=_identity(user), at=_time(),
            responsibility_questions=[
                "Which home, household and lease are verified by the data owner?",
                "What is the current approved measure scope?",
                "Who decides and is landlord permission needed?",
                "What is the Legal-reviewed responsibility position and its version?",
                "What cost position has Finance approved?",
                "Has Legal recorded the consultation requirement and status?",
                "Which disputes, defects or charge queries remain open?",
            ],
        )
        c.setdefault("tenure_reports", []).append(report)
        c["tenure_review_required"] = True
        return f"tenure intake version {report['version']} recorded; case-wide hold remains"

    def _res_tenure_inventory_record(self, user, c, body):
        _intake_fields(user, c, body, {
            "case_id", "expected_version", "source", "source_version", "owner", "next_update", "households",
        })
        inventories = c.get("tenure_household_inventories", [])
        reports = c.get("tenure_reports", [])
        if (("tenure_household_inventories" in c and not _inventory_history_ok(inventories, c["id"]))
                or not isinstance(reports, list) or not all(isinstance(r, dict) for r in reports)):
            raise ValueError("The stored tenure records are malformed. Ask the data owner to reconcile them; nothing was recorded.")
        _version(body, inventories[-1] if inventories else None)
        record = dict(
            version=len(inventories) + 1, case_id=c["id"],
            source=_intake_text(body["source"], "the household list source reference"),
            source_version=_intake_text(body["source_version"], "the household list version", 100),
            owner=_intake_owner(self, body["owner"]), next_update=_day(body["next_update"]),
            households=_inventory_rows(body["households"], reports),
        )
        record.update(status="Unknown" if record["households"] is None else "Declared",
                      qualification=INVENTORY_QUALIFICATION, recorded_by=_identity(user), at=_time())
        c.setdefault("tenure_household_inventories", []).append(record)
        c["tenure_review_required"] = True
        count = "Unknown" if record["households"] is None else len(record["households"])
        return f"household inventory version {record['version']} recorded; expected {count}; caller supplied; case-wide hold remains"

    def _res_tenure_legal_position(self, user, c, body):
        _intake_fields(user, c, body, {
            "case_id", "report_version", "expected_version", "reviewer_name", "reviewer_role",
            "position_ref", "position_version", "reviewed_on",
        })
        reports = c.get("tenure_reports", [])
        number = body["report_version"]
        if type(number) is not int or not 1 <= number <= len(reports):
            raise ValueError("Choose an existing tenure report version for this case.")
        report = reports[number - 1]
        positions = report.setdefault("legal_positions", [])
        _version(body, positions[-1] if positions else None)
        reviewer = _intake_text(body["reviewer_name"], "the named Legal reviewer", 100)
        role = _intake_text(body["reviewer_role"], "the Legal reviewer's role", 100)
        if "legal" not in role.casefold():
            raise ValueError("The reviewer's role must be a Legal role. Name the Legal reviewer; staff cannot approve a position here.")
        if reviewer.strip().casefold() in {_identity_value(user, "name"), _identity_value(user, "email")}:
            raise ValueError("Choose a Legal reviewer other than the person recording this reference.")
        reviewed_on = _day(body["reviewed_on"])
        if reviewed_on > k.today():
            raise ValueError("The Legal review date cannot be in the future.")
        position = dict(
            version=len(positions) + 1, report_version=number,
            reviewer_name=reviewer, reviewer_role=role,
            position_ref=_intake_text(body["position_ref"], "the Legal position document reference", 300),
            position_version=_intake_text(body["position_version"], "the Legal position version", 50),
            reviewed_on=reviewed_on, recorded_by=_identity(user), at=_time(),
            interpretation="None: reference only; lease terms are not read or interpreted here",
            status="Attached; verification, decision route and Finance cost remain open",
        )
        positions.append(position)
        report["legal_position"] = f"Reference attached (version {position['version']}); not verified or interpreted here"
        return f"tenure report {number} Legal position reference {position['version']} attached; case-wide hold remains"

    def _res_tenure_verify(self, user, c, body):
        _intake_fields(user, c, body, {
            "case_id", "report_version", "expected_version", "outcome", "verified_tenure",
            "identity_confirmed", "verifier_name", "verifier_role", "evidence_ref", "verified_on",
        })
        reports = c.get("tenure_reports", [])
        number = body["report_version"]
        if type(number) is not int or not 1 <= number <= len(reports):
            raise ValueError("Choose an existing tenure report version for this case.")
        report = reports[number - 1]
        verifications = report.setdefault("verifications", [])
        _version(body, verifications[-1] if verifications else None)
        outcome = k.choice(body["outcome"], ("Verified", "Not verified"), "the data-owner outcome")
        tenure = k.choice(body["verified_tenure"], (*TENURE_ROUTES, "Unknown"), "the verified tenure")
        confirmed = body["identity_confirmed"]
        if type(confirmed) is not bool:
            raise ValueError("State whether the data owner confirmed home, household and lease identity.")
        verifier = _intake_text(body["verifier_name"], "the named data owner", 100)
        role = _intake_text(body["verifier_role"], "the data owner's role", 100)
        if not any(word in role.casefold() for word in ("data owner", "home ownership")):
            raise ValueError("The verifier must be the Home Ownership data owner. Staff cannot verify tenure here.")
        if verifier.strip().casefold() in {_identity_value(user, "name"), _identity_value(user, "email")}:
            raise ValueError("Choose a data owner other than the person recording this verification.")
        verified_on = _day(body["verified_on"])
        if verified_on > k.today():
            raise ValueError("The verification date cannot be in the future.")
        if outcome == "Verified":
            if _open_triggers(report):
                raise ValueError("Resolve the open review trigger first. Owner: Home Ownership data owner.")
            if tenure == "Unknown" or not confirmed:
                raise ValueError("A verified outcome needs a known tenure and confirmed identity. Otherwise record Not verified.")
            if not report.get("legal_positions"):
                raise ValueError("Attach the Legal position reference before a decision route is set. Owner: Legal.")
            route = TENURE_ROUTES[tenure]
        elif tenure != "Unknown" or confirmed:
            raise ValueError("A Not verified outcome keeps tenure Unknown and identity unconfirmed.")
        else:
            route = "Unknown"
        record = dict(
            version=len(verifications) + 1, report_version=number, outcome=outcome,
            verified_tenure=tenure, identity_confirmed=confirmed, decision_route=route,
            verifier_name=verifier, verifier_role=role,
            evidence_ref=_intake_text(body["evidence_ref"], "the data-owner evidence reference", 300),
            verified_on=verified_on, recorded_by=_identity(user), at=_time(),
            interpretation="None: route label only; lease terms, payer and landlord permission are not decided here",
        )
        verifications.append(record)
        if outcome == "Verified":
            report["verification"] = f"Verified by data owner (version {record['version']}); Legal and Finance positions remain separate"
        else:
            report["verification"] = "Unknown"
        report["decision_route"] = route
        return (f"tenure report {number} verification {record['version']} {outcome.lower()}; "
                f"decision route {route}; case-wide hold remains")

    def _res_tenure_question_pack(self, user, c, body):
        _intake_fields(user, c, body, {"case_id", "report_version", "expected_version"})
        report = _tenure_report(c, body)
        packs = report.setdefault("question_packs", [])
        _version(body, packs[-1] if packs else None)
        verifications = report.get("verifications", [])
        positions = report.get("legal_positions", [])
        if not verifications or verifications[-1]["outcome"] != "Verified" or not positions:
            raise ValueError("Draft a question pack only from a data-owner-verified report with an attached Legal position reference.")
        if _open_triggers(report):
            raise ValueError("A review trigger is open on this report. Resolve it before drafting a question pack.")
        verified, position = verifications[-1], positions[-1]
        if packs and _pack_is_current(report, packs[-1]) and packs[-1]["review"] is None:
            raise ValueError("The current question pack is awaiting human approval. Review it first.")
        route = verified["decision_route"]
        refs = (f"verification {verified['version']} (evidence {verified['evidence_ref']}); "
                f"Legal position {position['position_ref']} {position['position_version']}")
        pack = dict(
            version=len(packs) + 1, report_version=body["report_version"],
            verification_version=verified["version"], legal_position_version=position["version"],
            trigger_version=len(report.get("review_triggers", [])),
            route=route, source="Template from reviewed record references; no AI used and no lease terms read",
            questions=[
                dict(owner="Home Ownership data owner",
                     question=f"Confirm home, household and lease identity for route {route}, using {refs}."),
                dict(owner="Legal", question="What is the responsibility position for each proposed measure, and is landlord permission needed? Legal interprets the lease; this pack does not."),
                dict(owner="Legal", question="What consultation requirement and status apply, and where is it recorded?"),
                dict(owner="Finance", question="Who bears the cost, and what cost position does Finance approve? Finance retains cost."),
                dict(owner="Home Ownership team", question="Which disputes, defects or charge queries are open and affect this package?"),
            ],
            status="Draft; awaiting human approval", review=None,
            drafted_by=_identity(user), at=_time(),
        )
        packs.append(pack)
        return f"tenure report {body['report_version']} question pack {pack['version']} drafted; awaiting human approval; case-wide hold remains"

    def _res_tenure_question_pack_review(self, user, c, body):
        _intake_fields(user, c, body, {
            "case_id", "report_version", "expected_version", "outcome", "reviewer_name",
            "reviewer_role", "reviewed_on", "note",
        })
        report = _tenure_report(c, body)
        packs = report.get("question_packs", [])
        if not packs:
            raise ValueError("Draft a question pack before reviewing it.")
        pack = packs[-1]
        _version(body, pack)
        if pack["review"] is not None:
            raise ValueError("This question pack already has its human review. Draft a new pack to change it.")
        if not _pack_is_current(report, pack):
            raise ValueError("The verification or Legal position changed. Draft a new question pack.")
        outcome = k.choice(body["outcome"], ("Approved", "Returned"), "the human review outcome")
        reviewer = _intake_text(body["reviewer_name"], "the named human reviewer", 100)
        role = _intake_text(body["reviewer_role"], "the reviewer's role", 100)
        if not any(word in role.casefold() for word in ("home ownership", "leasehold", "data owner")):
            raise ValueError("The reviewer must be in the home ownership and leasehold team. Name the person; no agent approves a pack.")
        own = {_identity_value(pack["drafted_by"], key) for key in ("name", "email")} - {""}
        if reviewer.strip().casefold() in {_identity_value(user, "name"), _identity_value(user, "email"), *own}:
            raise ValueError("Choose a reviewer other than the person who drafted or records this pack.")
        reviewed_on = _day(body["reviewed_on"])
        if reviewed_on > k.today():
            raise ValueError("The review date cannot be in the future.")
        pack["review"] = dict(
            outcome=outcome, reviewer_name=reviewer, reviewer_role=role, reviewed_on=reviewed_on,
            note=_intake_text(body["note"], "the review note", 300), recorded_by=_identity(user), at=_time(),
        )
        pack["status"] = ("Approved as questions only; Legal keeps interpretation and Finance keeps cost"
                          if outcome == "Approved" else "Returned; draft a new pack")
        return f"tenure report {body['report_version']} question pack {pack['version']} {outcome.lower()}; case-wide hold remains"

    def _res_tenure_review_trigger(self, user, c, body):
        _intake_fields(user, c, body, {
            "case_id", "report_version", "expected_version", "trigger", "source", "owner", "next_update",
        })
        report = _tenure_report(c, body)
        triggers = report.setdefault("review_triggers", [])
        _version(body, triggers[-1] if triggers else None)
        kind = k.choice(body["trigger"], REVIEW_TRIGGERS, "the review trigger")
        ambiguous = kind == "Ambiguous lease identity"
        record = dict(
            version=len(triggers) + 1, report_version=body["report_version"], trigger=kind,
            source=_intake_text(body["source"], "the trigger source reference"),
            owner=_intake_owner(self, body["owner"]), next_update=_day(body["next_update"]),
            route_to=("Home Ownership data owner (appointment required); do not reuse this lease record"
                      if ambiguous else "Home Ownership team and Legal (appointment required)"),
            recorded_by=_identity(user), at=_time(), resolution=None,
        )
        triggers.append(record)
        report["review_status"] = f"Open; review reopened by {kind.lower()}"
        c["tenure_review_required"] = True
        if ambiguous:
            report.update(identity_state="Ambiguous", verification="Unknown", decision_route="Unknown",
                          reuse_blocked=True)
            verifications = report.setdefault("verifications", [])
            verifications.append(dict(
                version=len(verifications) + 1, report_version=body["report_version"],
                outcome="Not verified", verified_tenure="Unknown", identity_confirmed=False,
                decision_route="Unknown", verifier_name="Not applicable: system-recorded",
                verifier_role="Superseded by ambiguous lease identity trigger",
                evidence_ref=f"review trigger {record['version']}", verified_on=k.today(),
                recorded_by=_identity(user), at=_time(),
                interpretation="None: earlier verification withdrawn until the data owner re-verifies",
            ))
        return (f"tenure report {body['report_version']} review trigger {record['version']} recorded; "
                "package review stays open; case-wide hold remains")

    def _res_tenure_trigger_resolve(self, user, c, body):
        _intake_fields(user, c, body, {
            "case_id", "report_version", "expected_version", "trigger_version", "resolver_name",
            "resolver_role", "resolved_on", "note",
        })
        report = _tenure_report(c, body)
        triggers = report.get("review_triggers", [])
        _version(body, triggers[-1] if triggers else None)
        number = body["trigger_version"]
        if type(number) is not int or not 1 <= number <= len(triggers):
            raise ValueError("Choose an existing review trigger version for this report.")
        trigger = triggers[number - 1]
        if trigger["resolution"] is not None:
            raise ValueError("This review trigger is already resolved.")
        resolver = _intake_text(body["resolver_name"], "the named resolver", 100)
        role = _intake_text(body["resolver_role"], "the resolver's role", 100)
        words = ("data owner", "home ownership", "leasehold")
        if trigger["trigger"] == "Ambiguous lease identity":
            words = ("data owner",)
        if not any(word in role.casefold() for word in words):
            raise ValueError("The resolver must be in the home ownership and leasehold team; ambiguous lease identity needs the data owner.")
        if resolver.strip().casefold() in {_identity_value(user, "name"), _identity_value(user, "email")}:
            raise ValueError("Choose a resolver other than the person recording this step.")
        resolved_on = _day(body["resolved_on"])
        if resolved_on > k.today():
            raise ValueError("The resolution date cannot be in the future.")
        trigger["resolution"] = dict(
            resolver_name=resolver, resolver_role=role, resolved_on=resolved_on,
            note=_intake_text(body["note"], "the resolution note", 300),
            recorded_by=_identity(user), at=_time(),
        )
        if not _open_triggers(report):
            report["review_status"] = "Open; human data-owner and Legal review required"
            report.pop("reuse_blocked", None)
        return (f"tenure report {body['report_version']} review trigger {number} resolved; "
                "re-verify and redraft any question pack; case-wide hold remains")

    def _res_challenge_open(self, user, c, body):
        from . import projection
        body, extras = _split_optional(
            body, ("hazard_concern", "raised_by", "representative_ref", "assisted_channel")
        )
        if not projection.appointment_evidence_visible(user):
            raise PermissionError("Challenge records need current resident-workflow and recorded-reason rights.")
        fields = {"action", "proposal_id", "proposal_version", "decision_version", "target_kind",
                  "channel", "source", "request", "explanation", "owner", "non_digital_route", "next_update"}
        if set(body) != fields:
            raise ValueError("Supply only the challenge fields. Identity, time, decisions and dependencies are recorded by the server.")
        _refuse_hazard(c, extras)
        raiser = _raiser(c, extras)
        stored_channel, route_mode, assisted_channel = nomination_route.normalize_route_channel(
            body["channel"],
            assisted_channel=extras.get("assisted_channel"),
            allow_intermediary=False,
            label="the supplied challenge channel",
        )
        guard = challenges.protected_snapshot(c)
        rec = _priority_record(self, body.get("proposal_id"))
        if not _priority_includes_case(rec, c["id"]):
            raise ValueError("Choose a priority suggestion that includes this case.")
        original, decision_version, decision = priority_binding(rec)
        if body["proposal_version"] != original or body["decision_version"] != decision_version:
            raise ValueError("The suggestion or its human review changed. Reload before recording the challenge.")
        target = _dependency(rec, body["target_kind"], c["id"])
        owner = _person(self, body["owner"])
        if not projection.appointment_evidence_visible(owner):
            raise ValueError("Choose a named owner with resident-workflow and recorded-reason rights.")
        if user["role"] not in MANAGERS and not _same_person(user, owner):
            raise PermissionError("Only a resident-workflow manager can assign another colleague as owner.")
        record = dict(id=k.next_id(c.get("affected_challenges", []), "CH"),
                      version=1, status="Open", target=target, proposal_id=rec["id"],
                      proposal_version=original, human_decision=decision,
                      decision_version=decision_version, owner=_identity(owner),
                      channel=stored_channel, route_mode=route_mode, assisted_channel=assisted_channel,
                      source=k.text(body["source"], "the supplied challenge reference", 300),
                      request=k.text(body["request"], "the person's supplied request", 300),
                      explanation=k.text(body["explanation"], "the permitted plain-language explanation", 300),
                      non_digital_route=k.text(body["non_digital_route"], "an accessible phone, letter or in-person route", 300),
                      next_update=_day(body["next_update"]), recorded_by=_identity(user), at=_time(),
                      ai_details={key: deepcopy(rec.get(key)) for key in ("source", "model", "prompt_version", "policy_version", "source_versions")},
                      resolution=None, **raiser)
        c.setdefault("affected_challenges", []).append(record)
        challenges.stamp_assurance(guard, c, record)
        return f"{record['id']} supplied challenge recorded"

    def _res_challenge_resolve(self, user, c, body):
        from . import projection
        if not projection.appointment_evidence_visible(user):
            raise PermissionError("Challenge records need current resident-workflow and recorded-reason rights.")
        if set(body) != {"action", "id", "expected_version", "resolution", "resolution_ref", "explanation", "next_update"}:
            raise ValueError("Supply only the resolution fields. A person must supply the resolution evidence.")
        guard = challenges.protected_snapshot(c)
        record = k.find(c.get("affected_challenges", []), body["id"], "challenge")
        _version(body, record)
        if record["status"] != "Open":
            raise ValueError("This challenge already has its recorded resolution. Its evidence cannot be replaced.")
        _owner_rights(self, user, record["owner"])
        resolution = dict(outcome=k.choice(body["resolution"], ("Correction recorded", "Explanation recorded"), "the supplied resolution"),
                          reference=k.text(body["resolution_ref"], "the supplied human resolution evidence", 300),
                          explanation=k.text(body["explanation"], "the permitted resolution explanation", 300),
                          next_update=_day(body["next_update"]), recorded_by=_identity(user), at=_time())
        record.update(status="Resolved", version=2, resolution=resolution)
        challenges.stamp_assurance(guard, c, record)
        return f"{record['id']} supplied resolution recorded"

    def _res_scope_record(self, user, c, body):
        if _inventory_managed(c):
            raise ValueError(" ".join([*_inventory_refusal(c), TENURE_HOLD]))
        measure = body.get("measure")
        if not isinstance(measure, str) or measure not in case_measures(c):
            raise ValueError("Choose one of this home's measures.")
        design = body.get("design_version")
        if type(design) is not int or design < 1 or design != (c.get("technical") or {}).get("design_version"):
            raise ValueError("Use the current recorded technical design version.")
        scope = k.text(body.get("scope"), "the measure scope reference", 100)
        source = k.text(body.get("source"), "the supplied scope source reference", 100)
        versions = c.get("resident_scopes", {}).get(measure, [])
        rec = dict(revision=len(versions) + 1, case_id=c["id"], measure=measure, scope=scope,
                   design_version=design, source=source, recorded_by=user["email"], at=k.now())
        c.setdefault("resident_scopes", {}).setdefault(measure, []).append(rec)
        return f"scope revision {rec['revision']} recorded"

    def _res_safe_contact_record(self, user, c, body):
        ref = k.text(body.get("safe_contact_ref"), "the resident-confirmed safe contact reference", 80)
        source = k.text(body.get("source"), "the supplied contact confirmation source", 100)
        c["resident_safe_contact"] = ref
        c.setdefault("resident_contact_history", []).append(
            dict(reference=ref, source=source, recorded_by=user["email"], at=k.now()))
        remember_first_contact(c)
        return f"safe contact revision {len(c['resident_contact_history'])} recorded"

    def _res_representative_record(self, user, c, body):
        from . import resident_journey_design

        measure, context = require_context(c, body)
        ref = k.text(body.get("representative_ref"), "the representative reference", 80)
        if resident_journey_design.valid_representative_ref(ref) is None:
            raise ValueError("Enter a specific representative reference, not Unknown.")
        status = k.choice(body.get("status"), AUTHORITY_STATUSES, "the authority status")
        tasks = body.get("tasks")
        if not isinstance(tasks, list) or not tasks or any(t not in AUTHORITY_TASKS for t in tasks):
            raise ValueError("Choose the representative's evidenced tasks.")
        try:
            start_day = date.fromisoformat(body.get("authority_date", ""))
            review_day = date.fromisoformat(body.get("review_date", ""))
            start = start_day.isoformat()
            review = review_day.isoformat()
        except (TypeError, ValueError):
            raise ValueError("Enter the authority and review dates as YYYY-MM-DD.")
        if start > k.today() or review <= start:
            raise ValueError("Authority cannot start in the future and review must follow its source date.")
        expires_iso = None
        if "expires_at" in body:
            parsed_exp = resident_journey_design.parse_iso_utc(body.get("expires_at"))
            if parsed_exp is None:
                raise ValueError("Enter the authority expiry timestamp with a time and timezone.")
            start_utc = datetime(start_day.year, start_day.month, start_day.day, 0, 0, 0, tzinfo=UTC)
            review_utc = datetime(review_day.year, review_day.month, review_day.day, 0, 0, 0, tzinfo=UTC)
            if parsed_exp <= start_utc or parsed_exp > review_utc:
                raise ValueError("Authority expiry must fall after its start date and within its review date.")
            expires_iso = resident_journey_design.format_iso_utc(parsed_exp)
        safe = k.text(body.get("safe_contact_ref"), "the resident-confirmed safe contact reference", 80)
        if safe != c.get("resident_safe_contact"):
            raise ValueError("Confirm the resident's current safe contact route first.")
        source = k.text(body.get("source"), "the authority evidence reference", 100)
        wishes = k.text(body.get("resident_wishes"), "the resident's own stated wishes", 300)
        versions = c.get("representative_authorities", {}).get(ref, [])
        rec = dict(version=len(versions) + 1, representative_ref=ref, status=status, tasks=list(tasks),
                   case_id=c["id"], measure=measure, scope=context["scope"], design_version=context["design_version"],
                   context_revision=context["revision"], authority_date=start, review_date=review,
                   safe_contact_ref=safe, safe_contact_revision=len(c.get("resident_contact_history", [])),
                   source=source, resident_wishes=wishes,
                   recorded_by=user["email"], at=k.now())
        if expires_iso is not None:
            rec["expires_at"] = expires_iso
        c.setdefault("representative_authorities", {}).setdefault(ref, []).append(rec)
        return f"representative authority version {rec['version']} recorded"

    def _res_disclosure_check(self, user, c, body):
        measure, context = require_context(c, body)
        task = k.choice(body.get("task"), AUTHORITY_TASKS, "the representative task")
        authority_for(c, body.get("representative_ref"), task, measure, context)
        return "representative task checked; nothing sent"

    def _res_decision_record(self, user, c, body):
        k.require_role(user, k.RESIDENT_ROLES, "authorised resident-workflow staff")
        measure, context = require_context(c, body)
        status = k.choice(body.get("status"), DECISION_STATUSES, "what the resident said")
        by = k.choice(body.get("answered_by"), ANSWERED_BY, "who gave the answer")
        note = k.text(body.get("note"), "what they said, in their words" if status in ("Paused", "Withdrawn", "Declined") else "", 300,
                      required=status in ("Paused", "Withdrawn", "Declined"))
        rep = k.text(body.get("representative_ref"), "the reference for their representative", 80, required=by == ANSWERED_BY[1])
        authority = authority_for(c, rep, "Works decision", measure, context) if by == ANSWERED_BY[1] else None
        source = k.text(body.get("source"), "the supplied resident answer source reference", 100)
        review = c.get("resident_reviews", {}).get(measure)
        review_ref = k.text(body.get("review_ref"), "the human review evidence reference", 100,
                            required=status == "Accepted" and bool(review and review["status"] == "Needs human review"))
        versions = c.setdefault("measure_decisions", {}).setdefault(measure, [])
        versions.append(dict(version=len(versions) + 1, case_id=c["id"], measure=measure,
                             scope=context["scope"], design_version=context["design_version"],
                             context_revision=context["revision"], source=source,
                             authority_version=authority["version"] if authority else None,
                             status=status, answered_by=by, representative_ref=rep if authority else "", note=note,
                             recorded_by_email=user["email"], recorder_identity=_identity(user), review_ref=review_ref,
                             next_update=k.text(body.get("next_update"), "", 10, False), recorded_by=user["name"], at=k.now()))
        if status in ("Paused", "Withdrawn", "Declined"):
            c.setdefault("resident_reviews", {})[measure] = dict(status="Needs human review", decision_version=len(versions),
                                                                context_revision=context["revision"], owner=c["owner"],
                                                                recorded_by=user["email"], at=k.now())
        elif status == "Accepted" and review:
            review.update(status="Reviewed with supplied acceptance", review_ref=review_ref,
                          reviewed_by=user["email"], at=k.now())
        return f"scope revision {context['revision']}: {status} decision v{len(versions)}"

    def _res_service_open(self, user, c, body):
        before_srv = deepcopy(c)
        route = k.choice(body.get("route"), ROUTES, "the route")
        owners = []
        for key, label in (("service_owner", "who deals with it"), ("redress_owner", "who owns the redress")):
            s = _person(self, body.get(key))
            owners.append(s)
        if route in ("Complaint", "Independent review") and _same_person(owners[0], owners[1]):
            raise ValueError("A complaint or independent review needs a different redress owner.")
        subject = None
        historical = None
        if route == "Independent review":
            review_measure = body.get("review_measure")
            if not isinstance(review_measure, str) or review_measure not in case_measures(c):
                raise ValueError("Choose the recorded measure decision to review.")
            decisions = c.get("measure_decisions", {}).get(review_measure, [])
            version = body.get("review_decision_version")
            if type(version) is not int or not 1 <= version <= len(decisions):
                raise ValueError("Choose the recorded measure decision version to review.")
            decision = decisions[version - 1]
            if decision.get("version") != version:
                raise ValueError("Choose the recorded measure decision version to review.")
            historical = deepcopy(decision.get("recorder_identity"))
            _require_independent_reviewer(owners[1], historical)
            subject = decision.get("recorded_by_email")
        review_reference = k.text(body.get("review_reference"), "the contested decision reference", 100,
                                  required=route == "Independent review")
        codes = body.get("accessibility") or ["Unknown"]
        if not isinstance(codes, list) or not codes or any(x not in ACCESS_CODES for x in codes):
            raise ValueError("Choose contact needs from the list.")
        reqs = c.get("service_requests", [])
        req = dict(id=k.next_id(reqs, "SR"), route=route, summary=k.text(body.get("summary"), "a short summary", 200),
                   desired_outcome=k.text(body.get("desired_outcome"), "the outcome the resident wants", 300),
                   service_owner=owners[0]["name"], service_owner_email=owners[0]["email"], redress_owner=owners[1]["name"],
                   redress_owner_email=owners[1]["email"], accessibility=codes, representative_ref=k.text(body.get("representative_ref"), "", 80, False) or "Unknown",
                   status="Open", next_update=_day(body.get("next_update")), opened_by=user["name"], opened_at=_time(),
                   service_identity=_identity(owners[0]), redress_identity=_identity(owners[1]),
                   version=1, status_owner=_identity(owners[0]), status_at=_time(),
                   remedy=dict(status="Open", owner=_identity(owners[1]), at=_time(),
                               opened_at=_time(), version=1, basis="Supplied desired outcome",
                               history=[]),
                   reviewed_actor=subject, reviewed_identity=historical, review_reference=review_reference,
                   review_measure=body.get("review_measure") if route == "Independent review" else None,
                   review_decision_version=body.get("review_decision_version") if route == "Independent review" else None,
                   history=[])
        c.setdefault("service_requests", []).append(req)
        challenges.assert_no_adverse_challenge_effects(
            before_srv, c, allowed_case_keys=("service_requests",)
        )
        return f"{req['id']} {route} opened"

    def _res_service_forward(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        _version(body, req)
        if req["route"] not in FORMAL_ROUTES:
            raise ValueError("Only a complaint or an independent review can be sent to the formal route.")
        if req["status"] == "Closed":
            raise ValueError("This request is closed.")
        route = req.get("formal_route") or dict(route_key=uuid.uuid4().hex, attempts=[])
        attempts = route["attempts"]
        if any(a["status"] == "Acknowledged" for a in attempts):
            raise ValueError("The formal route has already acknowledged this request.")
        # A legacy Failed attempt has no not_sent evidence, so its "not received" claim is not trusted.
        unresolved = [a for a in attempts if a["status"] in ("Pending", "Unconfirmed", "Superseded")
                      or (a["status"] == "Failed" and a.get("not_sent") is not True)]
        if unresolved and body.get("retry_unresolved") is not True:
            raise ValueError("An earlier send has no confirmed outcome. Check with the receiver, then retry explicitly.")
        if unresolved and in_flight(self, c.get("id"), req["id"]):
            raise ValueError("A send for this request is still in progress on this system. Wait for its outcome.")
        if req["route"] == "Independent review":
            if user["email"].lower() != req["redress_owner_email"].lower():
                raise PermissionError("Only the named independent reviewer can send this review.")
            _require_named_reviewer(user, req.get("redress_identity"))
            _require_independent_reviewer(user, req.get("reviewed_identity"))
        else:
            _owner_rights(self, user, req.get("redress_identity"), req.get("redress_owner_email"))
        ref = k.text(body.get("resident_request_ref"), "the reference showing the resident asked for this to be sent", 100)
        attempt = len(route["attempts"]) + 1
        route["attempts"].append(dict(attempt=attempt, status="Pending", request_id=req["id"],
                                      request_version=req.get("version", 0), resident_request_ref=ref,
                                      reservation_id=body.get("reservation_id"),
                                      requested_by=_identity(user), reserved_at=_time(),
                                      reason="Sending. No outcome is recorded yet."))
        req["formal_route"] = route
        return f"{req['id']} formal-route attempt {attempt} reserved; no outcome recorded"

    def _res_service_forward_outcome(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        attempts = (req.get("formal_route") or {}).get("attempts", [])
        attempt = body.get("attempt")
        if (type(attempt) is not int or not 1 <= attempt <= len(attempts) or attempts[attempt - 1]["status"] != "Pending"
                or attempts[attempt - 1].get("reservation_id") != body.get("reservation_id")):
            raise ValueError("There is no pending formal-route attempt to record.")
        if body.get("status") not in complaints_route.STATUSES[1:]:
            raise ValueError("Unknown formal-route outcome.")
        attempts[attempt - 1].update(status=body["status"], reason=body["reason"], outcome_at=_time())
        if body.get("not_sent") is True and body["status"] == "Failed":
            attempts[attempt - 1]["not_sent"] = True
        if body["status"] == "Acknowledged":
            attempts[attempt - 1].update(receipt_ref=body["receipt_ref"], received_at=body.get("received_at"))
            self._flag_stale_pending(c, req, attempts, attempt)
        return f"{req['id']} formal-route attempt {attempt}: {body['status']}"

    def _flag_stale_pending(self, c, req, attempts, acknowledged):
        """Flag earlier idle Pending attempts for the manual_verified review; never change their status."""
        busy = in_flight(self, c.get("id"), req["id"])
        route = req["formal_route"]
        route["supersession_eligible_attempts"] = [
            a["attempt"] for a in attempts[:acknowledged - 1] if a["status"] == "Pending" and a["attempt"] not in busy]
        route["stale_pending_supersession_required"] = bool(route["supersession_eligible_attempts"])
        route["supersession_evidence_ref"] = attempts[acknowledged - 1]["receipt_ref"]

    def _res_service_supersede_authorize(self, user, c, body):
        """Owner-approved manual_verified step (issue 1238 Q6): two explicitly bound people, never age, never a resend."""
        binding = _supersession_binding(self)
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        attempts = (req.get("formal_route") or {}).get("attempts", [])
        number = body.get("attempt")
        if (type(number) is not int or not 1 <= number <= len(attempts) or attempts[number - 1]["status"] != "Pending"
                or attempts[number - 1].get("reservation_id") != body.get("reservation_id")):
            raise ValueError("There is no pending formal-route attempt to supersede.")
        if in_flight(self, c.get("id"), req["id"]):
            raise ValueError("A send for this request is still in progress on this system. Wait for its outcome.")
        role = k.choice(body.get("authorize_as"), _BINDING_ROLES, "the authorizing role")
        evidence = k.text(body.get("evidence_ref"), "the reference to the verified outcome evidence", 100)
        bound = binding.identity(role)
        if _identity_value(user, "email") != _identity_value(bound, "email") or not _same_owner(bound, user):
            raise PermissionError(f"Only the configured {role.replace('_', ' ')} can authorize this supersession.")
        _require_named_reviewer(user, bound)
        if role == "reviewer" and req["route"] == "Independent review":
            _require_independent_reviewer(user, req.get("reviewed_identity"))
        attempt = attempts[number - 1]
        record = attempt.setdefault("supersession", dict(evidence_ref=evidence, authorizations=[], withdrawn=[]))
        if (not isinstance(record, dict) or not isinstance(record.get("authorizations"), list)
                or not isinstance(record.get("withdrawn"), list)):
            raise ValueError("The recorded supersession is not in a usable state. Resolve it before authorizing.")
        for given in list(record["authorizations"]):
            if not _authorization_holds(self, binding, c.get("id"), req, number, record.get("evidence_ref"), given):
                record["authorizations"].remove(given)
                record["withdrawn"].append(given)
        if not record["authorizations"]:
            record["evidence_ref"] = evidence
        if any(a["role"] == role for a in record["authorizations"]):
            raise ValueError("This role has already authorized the supersession. Reload to see its state.")
        if record["evidence_ref"] != evidence:
            raise ValueError("Both authorizers must authorize the same verified outcome evidence reference.")
        if any(_same_person(user, a["identity"]) for a in record["authorizations"]):
            raise PermissionError("A different named person must give the other authorization.")
        record["authorizations"].append(dict(role=role, identity=_identity(user), at=_time(),
                                             binding_id=binding.binding_id, binding_digest=binding.digest))
        if len(record["authorizations"]) == 2:
            attempt.update(status="Superseded", superseded_from="Pending", superseded_at=_time())
            route = req["formal_route"]
            if number in route.get("supersession_eligible_attempts", []):
                route["supersession_eligible_attempts"].remove(number)
                route["stale_pending_supersession_required"] = bool(route["supersession_eligible_attempts"])
            detail = _approval_detail(binding, c.get("id"), req["id"], attempt.get("reservation_id"), number, role, evidence)
            return f"{detail}; attempt superseded, receipt, key and history kept"
        return _approval_detail(binding, c.get("id"), req["id"], attempt.get("reservation_id"), number, role, evidence)

    def _res_service_update(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        if req["status"] == "Closed":
            raise ValueError("This request is closed.")
        if req["route"] == "Independent review" and user["email"].lower() != req["redress_owner_email"].lower():
            raise PermissionError("Only the named independent reviewer can update this review.")
        identity_key = "redress" if req["route"] == "Independent review" or user["email"] == req["redress_owner_email"] else "service"
        _owner_rights(self, user, req.get(identity_key + "_identity"), req.get(identity_key + "_owner_email"))
        status = k.choice(body.get("status"), REQUEST_STATUSES, "the status")
        next_update = _day(body.get("next_update"))
        req.update(status=status, next_update=next_update)
        self._response_event(req, user, k.text(body.get("note"), "a note", 300, False))
        return f"{req['id']} {req['status']}"

    def _res_service_close(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        if req["status"] != "Resolved":
            raise ValueError("Mark it resolved before closing it.")
        if req["route"] in ("Complaint", "Independent review"):
            if user["email"].lower() != req["redress_owner_email"].lower():
                raise PermissionError("Only the redress owner can close a complaint.")
            k.different_person(user, req["service_owner_email"], "close a complaint")
            _owner_rights(self, user, req.get("redress_identity"), req["redress_owner_email"])
            other = req.get("service_identity") or _person(self, req["service_owner_email"])
            if any(user.get(key) and user.get(key) == other.get(key) for key in ("email", "code", "oid")):
                raise PermissionError("A different named person must close the complaint response.")
        elif user["email"].lower() not in (req["service_owner_email"].lower(), req["redress_owner_email"].lower()):
            raise PermissionError("Only the person dealing with it or the redress owner can close this.")
        else:
            key = "service" if user["email"] == req["service_owner_email"] else "redress"
            _owner_rights(self, user, req.get(key + "_identity"), req[key + "_owner_email"])
        req.update(status="Closed", closed_by=user["name"], closed_at=_time(), outcome=k.text(body.get("note"), "the outcome for the resident", 300))
        self._response_event(req, user, req["outcome"])
        return f"{req['id']} closed"

    def _response_event(self, req, user, note):
        key = "redress" if req["status"] == "Closed" or req["route"] == "Independent review" else "service"
        owner = _person(self, req.get(key + "_owner_email"))
        if req.get(key + "_identity"):
            _actor(self, req[key + "_identity"])
        req.update(version=req.get("version", 0) + 1, status_owner=_identity(owner), status_at=_time())
        req.setdefault("history", []).append(dict(status=req["status"], actor=_identity(user),
                                                 by=user["name"], at=req["status_at"], note=note))

    def _res_service_reassign(self, user, c, body):
        k.require_role(user, MANAGERS, "a resident-workflow manager")
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        _version(body, req)
        key = k.choice(body.get("responsibility"), ("service", "redress"), "the response responsibility")
        owner = _person(self, body.get("owner"))
        identity = _identity(owner)
        old = deepcopy(req.get(key + "_identity"))
        if old == identity:
            raise ValueError("Choose a different named owner for this responsibility.")
        if req["route"] in ("Complaint", "Independent review"):
            other_key = "redress" if key == "service" else "service"
            other = req.get(other_key + "_identity") or _person(self, req.get(other_key + "_owner_email"))
            if _same_person(owner, other):
                raise PermissionError("A complaint or independent review needs different service and redress owners.")
        if key == "redress" and req["route"] == "Independent review":
            # An unbound legacy ordinal may refer to history deleted and recreated since opening.
            _require_independent_reviewer(owner, req.get("reviewed_identity"))
        note = k.text(body.get("note"), "the reason for reassigning response responsibility")
        at = _time()
        status_key = "redress" if req["status"] == "Closed" or req["route"] == "Independent review" else "service"
        event = dict(kind="Response owner reassigned", responsibility=key,
                     changes=dict(old=old, new=identity), old_owner_email=req.get(key + "_owner_email"),
                     old_owner_name=req.get(key + "_owner"), old_status_owner=deepcopy(req.get("status_owner")),
                     old_status_at=req.get("status_at"), status=req["status"],
                     actor=_identity(user), by=user["name"], note=note, at=at,
                     version=req.get("version", 0) + 1)
        req.update({key + "_identity": identity, key + "_owner": owner["name"],
                    key + "_owner_email": owner["email"], "version": event["version"]})
        if key == status_key:
            req.update(status_owner=identity, status_at=at)
        req.setdefault("history", []).append(event)
        return f"{req['id']} {key} response responsibility reassigned; remedy unchanged"

    def _res_service_reopen(self, user, c, body):
        before_srv = deepcopy(c)
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        _version(body, req)
        if req["status"] != "Closed":
            raise ValueError("Only a closed response can be reopened.")
        if req["route"] == "Independent review" and user["email"] != req["redress_owner_email"]:
            raise PermissionError("Only the named independent reviewer can reopen this review.")
        key = "redress" if user["email"] == req["redress_owner_email"] else "service"
        _owner_rights(self, user, req.get(key + "_identity"), req.get(key + "_owner_email"))
        note = k.text(body.get("note"), "why the response is reopened")
        req["status"] = "Open"
        self._response_event(req, user, note)
        challenges.assert_no_adverse_challenge_effects(
            before_srv, c, allowed_case_keys=("service_requests",)
        )
        return f"{req['id']} response reopened; remedy unchanged"

    def _res_update_record(self, user, c, body):
        previous = c.get("resident_update")
        _version(body, previous)
        if previous and previous.get("version"):
            _owner_rights(self, user, previous.get("owner_identity"))
        elif previous and user["role"] not in MANAGERS and c["owner_code"] != user["code"]:
            raise PermissionError("The case owner or a resident-workflow manager must confirm this legacy commitment.")
        elif not previous and user["role"] not in MANAGERS and c["owner_code"] != user["code"]:
            raise PermissionError("The case owner or a resident-workflow manager must create this commitment.")
        owner = _person(self, body.get("owner"))
        due = body.get("due_at")
        try:
            parsed = datetime.fromisoformat(due) if isinstance(due, str) else None
            if parsed is None or parsed.tzinfo is None or parsed.utcoffset() is None:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Enter the commitment due date with a time and timezone.") from None
        rec = dict(
            purpose=k.text(body.get("purpose"), "the update purpose or linked issue"),
            owner=owner["name"], owner_identity=_identity(owner),
            due_at=parsed.astimezone(UTC).isoformat(),
            basis=k.text(body.get("basis"), "the human-selected due date basis"),
            safe_contact_ref=k.text(body.get("safe_contact_ref"), "", 80, False) or "Unknown",
            status=k.choice(body.get("status"), ("Outstanding", "Proposed"), "the commitment status"),
            version=(previous or {}).get("version", 0) + 1,
            at=_time(), opened_at=previous.get("opened_at") if previous else _time(),
            history=deepcopy((previous or {}).get("history", [])),
        )
        old = deepcopy(previous)
        if old:
            old.pop("history", None)
        rec["history"].append(dict(old=old, actor=_identity(user), at=rec["at"], version=rec["version"]))
        c["resident_update"] = rec
        return f"Resident-update commitment v{rec['version']} recorded; no message sent"

    def _res_remedy_confirm(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        _version(body, req.get("remedy"))
        if req.get("remedy"):
            raise ValueError("This remedy is already recorded. Use its current version.")
        _owner_rights(self, user, req.get("redress_identity"), req.get("redress_owner_email"))
        owner = _person(self, body.get("owner"))
        req["remedy"] = dict(
            status="Open", owner=_identity(owner), version=1, at=_time(), opened_at=None,
            basis=k.text(body.get("basis"), "the supplied remedy responsibility basis"),
            history=[dict(old=None, actor=_identity(user), at=_time(), status="Open", version=1)],
        )
        return f"{req['id']} legacy remedy responsibility confirmed; original provenance unknown"

    def _res_remedy_update(self, user, c, body):
        req = k.find(c.get("service_requests", []), body.get("id"), "request")
        remedy = req.get("remedy")
        if not remedy:
            raise ValueError("Confirm the legacy remedy responsibility before recording progress.")
        _version(body, remedy)
        _owner_rights(self, user, remedy.get("owner"))
        owner = _person(self, body["owner"]) if body.get("owner") else _actor(self, remedy["owner"])
        k.require_role(owner, k.RESIDENT_VIEW_ROLES, "current resident-workflow staff")
        status = k.choice(body.get("status"), ("Open", "In progress", "Resolved", "Closed"), "the remedy status")
        allowed = {"Open": ("In progress", "Resolved"), "In progress": ("Open", "Resolved"),
                   "Resolved": ("Open", "Closed"), "Closed": ("Open",)}
        if status not in allowed.get(remedy["status"], ()):
            raise ValueError("Resolve the remedy before closing it; reopen a closed remedy explicitly.")
        note = k.text(body.get("note"), "the supplied remedy progress or reopening evidence")
        old = {key: deepcopy(value) for key, value in remedy.items() if key != "history"}
        remedy.update(status=status, owner=_identity(owner), version=remedy["version"] + 1, at=_time())
        remedy["history"].append(dict(old=old, status=status, actor=_identity(user),
                                       at=remedy["at"], note=note, version=remedy["version"]))
        return f"{req['id']} remedy {status}; response unchanged"

    def _representative_sessions(self):
        from . import resident_journey_design

        sessions = getattr(self, "_rep_session_store", None)
        if sessions is None:
            sessions = resident_journey_design.RepresentativeSessionStore()
            self._rep_session_store = sessions
        return sessions

    def representative_view(self, user, cid, representative_ref, *, now=None, session_id=None):
        from . import resident_journey_design

        with self.lock:
            k.require_role(user, k.RESIDENT_VIEW_ROLES, "current resident-workflow staff")
            c = self._case(cid)
            orders = getattr(self, "work_orders", ())
            if isinstance(session_id, str) and session_id.strip():
                sid = session_id.strip()
                sessions = self._representative_sessions()
                if sessions.get(sid) is not None:
                    return sessions.session_view(
                        sid,
                        c,
                        now=now,
                        work_orders=orders,
                        include_case_id=True,
                    )
                _, view = sessions.open_session(
                    c,
                    representative_ref,
                    now=now,
                    work_orders=orders,
                    session_id=sid,
                    include_case_id=True,
                )
                return view
            return resident_journey_design.project_representative_view(
                c,
                representative_ref,
                now=now,
                work_orders=orders,
                include_case_id=True,
            )

    def representative_action_check(self, user, cid, body, *, now=None):
        from . import resident_journey_design

        if not isinstance(body, dict):
            raise ValueError("Supply the representative action check payload.")
        with self.lock:
            k.require_role(user, k.RESIDENT_VIEW_ROLES, "current resident-workflow staff")
            c = self._case(cid)
            orders = getattr(self, "work_orders", ())
            rep_ref = body.get("representative_ref")
            act = body.get("action")
            measure = body.get("measure")
            assistant_topic = body.get("assistant_topic")
            session_id = body.get("session_id")
            if isinstance(session_id, str) and session_id.strip():
                sid = session_id.strip()
                sessions = self._representative_sessions()
                if sessions.get(sid) is None and rep_ref is not None:
                    sessions.open_session(
                        c,
                        rep_ref,
                        now=now,
                        work_orders=orders,
                        session_id=sid,
                        include_case_id=False,
                    )
                return sessions.session_action(
                    sid,
                    c,
                    act,
                    measure=measure,
                    assistant_topic=assistant_topic,
                    now=now,
                    work_orders=orders,
                )
            return resident_journey_design.enforce_representative_action(
                c,
                rep_ref,
                act,
                measure=measure,
                assistant_topic=assistant_topic,
                now=now,
                work_orders=orders,
            )

