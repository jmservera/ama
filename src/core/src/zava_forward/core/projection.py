"""Server-side field projection and endpoint access by role (PR-002), default deny.

Every response that leaves the service passes through here for the signed-in
role. A field that is not on a role's allow-list is not returned, and a new
field stays hidden until it is added. The vulnerability reason (the
resident's adjustment text) is shown only to roles with a recorded need; a
contractor sees only "needs notice" and a named contact, never the reason.

The set of roles with a need is a proposal for the control owners (OD-14,
OD-19). Override it with ZF_REASON_ROLES (comma separated) once decided.

Free-text notes (decided for the exercise, issue 116): no pattern-based
redaction, because a reason can be typed in any words and a filter would give
false assurance. Instead the default-deny allow-lists keep every free-text
field out of contractor responses and AI prompts, and roles without a recorded
need see a "held" marker in place of staff-written notes and contact outcomes.
"""
import os
from copy import deepcopy
from typing import Any

from .controls import RESIDENT_ROLES, RESIDENT_VIEW_ROLES
from .resident_decisions import RESIDENT_FIELDS, case_measures, current_context, resident_gate
from .stock import support_status

CONTRACTOR = "Contractor"
RESIDENT_RECORD_ROLES = RESIDENT_ROLES
DEFAULT_REASON_ROLES = ("Resident Liaison Officer", "Building Safety Liaison", "Retrofit Programme Manager")
REDACTED = "Extra support noted"
NOTE_HELD = "Held for roles with a recorded need"
NOTE_KEYS = ("note", "release_note", "answer_note", "next_action", "completion_note",
             "sent_evidence", "receipt_evidence", "acceptance_evidence", "repair_evidence")

STAFF_ROLES = ("Retrofit Coordinator", "Resident Liaison Officer", "Building Safety Liaison", "Grants and Evidence Officer",
               "Quality Inspector", "Retrofit Programme Manager", "Programme Support Officer")
FINANCE_VIEW = ("Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer")
STAFF_GET = ("coordinator", "finance_queue", "me", "cases", "cases.csv", "case", "ranking", "ai_priority", "facets", "stats", "map", "visits",
             "funding", "briefing", "doc", "audit", "handoffs", "time", "packages", "workorders", "checklists", "ai_report", "assistants", "law", "retention", "chat", "building", "forms")
CONTRACTOR_GET = ("me", "cases", "case", "workorders")
CONTRACTOR_POST = ("logout",)

SUMMARY_FIELDS = ("id", "address", "town", "postcode", "stage", "status", "next_visit", "needs_notice", "named_contact",
                  "closed")
DETAIL_FIELDS = ("id", "stage", "status", "measures", "needs_notice", "named_contact")


def reason_roles() -> tuple[str, ...]:
    raw = os.environ.get("ZF_REASON_ROLES")
    return tuple(r.strip() for r in raw.split(",") if r.strip()) if raw is not None else DEFAULT_REASON_ROLES


def is_contractor(user: dict[str, Any]) -> bool:
    return user.get("role") == CONTRACTOR


def can_see_reason(user: dict[str, Any]) -> bool:
    return user.get("role") in reason_roles()

def appointment_evidence_visible(user: dict[str, Any]) -> bool:
    """Appointment sources and human histories retain both existing evidence boundaries."""
    return user.get("role") in RESIDENT_VIEW_ROLES and can_see_reason(user)


def allowed(user, kind, method="GET"):
    """Default deny: contractors get a short list, staff roles the staff list, unknown roles nothing."""
    if is_contractor(user):
        return kind in (CONTRACTOR_GET if method == "GET" else CONTRACTOR_POST)
    return user.get("role") in STAFF_ROLES and (kind in STAFF_GET if method == "GET" else True)


def needs_notice(c):
    return support_status(c["resident"]) == "Yes"


def own_case(user, c):
    return is_contractor(user) and c["contractor"]["name"] == user.get("contractor")


def contractor_summary(c, s):
    out = dict(s, needs_notice=needs_notice(c), named_contact=c["owner"])
    out["status"] = "Completed" if c["closed"] else c["stage"]
    return {k: out[k] for k in SUMMARY_FIELDS if k in out}


def contractor_detail(c, d):
    out = dict(d, needs_notice=needs_notice(c), named_contact=c["owner"])
    keep = {k: out[k] for k in DETAIL_FIELDS if k in out}
    keep["status"] = "Completed" if c["closed"] else c["stage"]
    keep["resident_readiness"] = [
        dict(measure=m, flag="Hold" if resident_gate(c, [
            dict(measure=m, context_revision=(current_context(c, m) or {}).get("revision"))
        ]) else "Proceed") for m in case_measures(c)]
    keep["home"] = {k: c["home"][k] for k in ("address", "town", "postcode", "type")}
    keep["contractor"] = {"name": c["contractor"]["name"], "contact": c["contractor"]["contact"]}
    keep["appointments"] = [{k: a[k] for k in ("type", "date", "slot")} | {"outcome": status_only(a["outcome"])} for a in c["appointments"]]
    return keep


APPOINTMENT_STATUS = ("Booked", "Planned", "Completed", "No access", "Missed", "Cancelled", "Rescheduled")


def status_only(outcome):
    return outcome if outcome in (None, "") + APPOINTMENT_STATUS else NOTE_HELD


def hold_notes(c):
    """Replace staff-written free text anywhere in a case-shaped dict for roles without a need."""
    if isinstance(c, list):
        for item in c:
            hold_notes(item)
    elif isinstance(c, dict):
        if "document_history" in c:
            c["document_history"] = [dict(version=event["version"], at=event["at"],
                                          actor=event["actor"], detail=NOTE_HELD)
                                     for event in c["document_history"]]
        if "source_version" in c and "reason" in c:
            for key in ("source", "source_version", "reason", "changes"):
                if c.get(key):
                    c[key] = NOTE_HELD
        if "edit_history" in c:
            c["edit_history"] = [dict(version=event["version"], at=event["at"],
                                      actor=event["actor"], preview_id=event["preview_id"],
                                      detail=NOTE_HELD) for event in c["edit_history"]]
        if "from_stage" in c and "to_stage" in c:
            for key in ("reason", "source"):
                if c.get(key):
                    c[key] = NOTE_HELD
        for k, v in c.items():
            private_hazard = (
                ("category" in c and "released" in c and k in ("source", "job"))
                or ("actor" in c and k in ("reason", "evidence"))
            )
            if (k in NOTE_KEYS or private_hazard) and v:
                c[k] = NOTE_HELD
            else:
                hold_notes(v)
        if c.get("channel") and c.get("outcome"):
            c["outcome"] = NOTE_HELD
        elif c.get("date") and c.get("outcome") and c["outcome"] not in APPOINTMENT_STATUS:
            c["outcome"] = NOTE_HELD
    return c


def redact_staff_detail(user, d):
    resident_view = user.get("role") in RESIDENT_VIEW_ROLES
    resident_data = {key: deepcopy(d[key]) for key in RESIDENT_FIELDS + ("decision",)
                     if key in d} if resident_view else {}
    if not resident_view:
        d.pop("resident_update", None)
        d.pop("service_requests", None)
        for event in d.get("handoff_history", []):
            if isinstance(event.get("changes"), dict):
                event["changes"].pop("resident_update", None)
        for key in ("representative_authorities", "resident_safe_contact", "resident_contact_history", "resident_scopes"):
            d.pop(key, None)
        for measure in d.get("measure_decisions", []):
            if measure.get("context"):
                measure["context"].pop("source", None)
            for answer in measure.get("versions", []):
                for key in ("source", "note", "representative_ref", "review_ref"):
                    answer.pop(key, None)
            if measure.get("review"):
                measure["review"].pop("review_ref", None)
        for review in d.get("resident_reviews", {}).values():
            review.pop("review_ref", None)
        for request in d.get("service_requests", []):
            request.pop("representative_ref", None)
    if not can_see_reason(user):
        work = d.pop("work", None)  # Already projected by the shared queue read model.
        hold_notes(d)
        if work is not None:
            d["work"] = work
        if d.get("status", "").startswith("Waiting on "):
            d["status"] = "Waiting for the recorded next step"
        if d.get("reason"):
            d["reason"] = NOTE_HELD
        adjustment = d["resident"].get("adjustment")
        d["resident"]["adjustment"] = (
            "Unknown" if adjustment in (None, "", "Unknown") else
            REDACTED if adjustment != "None" else "None")
    d.update(resident_data)
    if user.get("role") not in FINANCE_VIEW:
        d.pop("finance", None)
        d.pop("grants", None)
        d.pop("cost_allocation", None)
    return d


def me_payload(user, counts, staff):
    if is_contractor(user):
        return dict(user=dict(name=user["name"], role=user["role"], contractor=user.get("contractor")), counts={}, staff=[])
    return dict(user=user, counts=counts, staff=staff)
