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

CONTRACTOR = "Contractor"
DEFAULT_REASON_ROLES = ("Resident Liaison Officer", "Building Safety Liaison", "Retrofit Programme Manager")
REDACTED = "Extra support noted"
NOTE_HELD = "Held for roles with a recorded need"
NOTE_KEYS = ("note", "release_note", "answer_note")

STAFF_ROLES = ("Retrofit Coordinator", "Resident Liaison Officer", "Building Safety Liaison", "Grants and Evidence Officer",
               "Quality Inspector", "Retrofit Programme Manager", "Programme Support Officer")
FINANCE_VIEW = ("Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer")
STAFF_GET = ("finance_queue", "me", "cases", "cases.csv", "case", "ranking", "ai_priority", "facets", "stats", "map", "visits",
             "funding", "briefing", "doc", "audit", "handoffs", "time", "packages", "workorders", "checklists", "ai_report", "assistants", "law", "retention", "chat", "building")
CONTRACTOR_GET = ("me", "cases", "case", "workorders")
CONTRACTOR_POST = ("logout",)

SUMMARY_FIELDS = ("id", "address", "town", "postcode", "stage", "status", "next_visit", "needs_notice", "named_contact",
                  "closed")
DETAIL_FIELDS = ("id", "stage", "status", "measures", "needs_notice", "named_contact")


def reason_roles():
    raw = os.environ.get("ZF_REASON_ROLES")
    return tuple(r.strip() for r in raw.split(",") if r.strip()) if raw is not None else DEFAULT_REASON_ROLES


def is_contractor(user):
    return user.get("role") == CONTRACTOR


def can_see_reason(user):
    return user.get("role") in reason_roles()


def allowed(user, kind, method="GET"):
    """Default deny: contractors get a short list, staff roles the staff list, unknown roles nothing."""
    if is_contractor(user):
        return kind in (CONTRACTOR_GET if method == "GET" else CONTRACTOR_POST)
    return user.get("role") in STAFF_ROLES and (kind in STAFF_GET if method == "GET" else True)


def needs_notice(c):
    return bool(c["resident"]["priority_support"] or c["resident"]["adjustment"] != "None")


def own_case(user, c):
    return is_contractor(user) and c["contractor"]["name"] == user.get("contractor")


def contractor_summary(c, s):
    out = dict(s, needs_notice=needs_notice(c), named_contact=c["owner"])
    return {k: out[k] for k in SUMMARY_FIELDS if k in out}


def contractor_detail(c, d):
    out = dict(d, needs_notice=needs_notice(c), named_contact=c["owner"])
    keep = {k: out[k] for k in DETAIL_FIELDS if k in out}
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
        for k, v in c.items():
            if k in NOTE_KEYS and v:
                c[k] = NOTE_HELD
            else:
                hold_notes(v)
        if c.get("channel") and c.get("outcome"):
            c["outcome"] = NOTE_HELD
        elif c.get("date") and c.get("outcome") and c["outcome"] not in APPOINTMENT_STATUS:
            c["outcome"] = NOTE_HELD
    return c


def redact_staff_detail(user, d):
    if not can_see_reason(user):
        hold_notes(d)
        d["resident"]["adjustment"] = REDACTED if d["resident"]["adjustment"] != "None" else "None"
    if user.get("role") not in FINANCE_VIEW:
        d.pop("finance", None)
        d.pop("grants", None)
        d.pop("cost_allocation", None)
    return d


def me_payload(user, counts, staff):
    if is_contractor(user):
        return dict(user=dict(name=user["name"], role=user["role"], contractor=user.get("contractor")), counts={}, staff=[])
    return dict(user=user, counts=counts, staff=staff)
