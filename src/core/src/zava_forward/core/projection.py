"""Server-side field projection and endpoint access by role (PR-002), default deny.

Every response that leaves the service passes through here for the signed-in
role. A field that is not on a role's allow-list is not returned, and a new
field stays hidden until it is added. The vulnerability reason (the
resident's adjustment text) is shown only to roles with a recorded need; a
contractor sees only "needs notice" and a named contact, never the reason.

The set of roles with a need is confirmed for the synthetic demo by the owner
decision of 2026-11-18 (OD-14, OD-19); DPO and Legal approval stays a
production gate. Override it with ZF_REASON_ROLES (comma separated). The
override can never grant the contractor the reason.

Free-text notes (decided for the exercise, issue 116): no pattern-based
redaction, because a reason can be typed in any words and a filter would give
false assurance. Instead the default-deny allow-lists keep every free-text
field out of contractor responses and AI prompts, and roles without a recorded
need see a "held" marker in place of staff-written notes and contact outcomes.
"""

import os
import re
import unicodedata
from collections.abc import Iterable, Mapping
from copy import deepcopy
from typing import Any

from . import taskqueues
from .doc_controls import is_available_case_document
from .controls import RESIDENT_ROLES, RESIDENT_VIEW_ROLES
from .resident_decisions import (
    INTAKE_FIELDS,
    RESIDENT_FIELDS,
    case_measures,
    current_context,
    resident_gate,
)
from .stock import support_status
from .taskqueues import raw_safeguarding_items

CONTRACTOR = "Contractor"
RESIDENT_RECORD_ROLES = RESIDENT_ROLES
DEFAULT_REASON_ROLES = (
    "Resident Liaison Officer",
    "Building Safety Liaison",
    "Retrofit Programme Manager",
)
REDACTED = "Extra support noted"
NOTE_HELD = "Held for roles with a recorded need"
NOTE_KEYS = (
    "note",
    "release_note",
    "answer_note",
    "next_action",
    "completion_note",
    "sent_evidence",
    "receipt_evidence",
    "acceptance_evidence",
    "repair_evidence",
)

STAFF_ROLES = (
    "Retrofit Coordinator",
    "Resident Liaison Officer",
    "Building Safety Liaison",
    "Grants and Evidence Officer",
    "Quality Inspector",
    "Retrofit Programme Manager",
    "Programme Support Officer",
)
FINANCE_VIEW = (
    "Grants and Evidence Officer",
    "Retrofit Programme Manager",
    "Programme Support Officer",
)
STAFF_GET = (
    "coordinator",
    "finance_queue",
    "me",
    "cases",
    "cases.csv",
    "case",
    "ranking",
    "ai_priority",
    "facets",
    "stats",
    "map",
    "visits",
    "funding",
    "briefing",
    "doc",
    "audit",
    "handoffs",
    "time",
    "packages",
    "workorders",
    "job_pack",
    "field_intake",
    "checklists",
    "ai_report",
    "assistants",
    "law",
    "retention",
    "data_protection",
    "chat",
    "building",
    "forms",
    "continuity",
    "continuity_export",
    "stock_queue",
    "resident_choice_queue",
    "exceptions",
    "aftercare",
    "packages.csv",
    "workorders.csv",
    "handoffs.csv",
    "visits.csv",
    "funding.csv",
    "checklists.csv",
)
CONTRACTOR_GET = ("me", "cases", "case", "workorders")
CONTRACTOR_POST = ("logout",)

SUMMARY_FIELDS = (
    "id",
    "address",
    "town",
    "postcode",
    "stage",
    "status",
    "next_visit",
    "needs_notice",
    "named_contact",
    "closed",
)
DETAIL_FIELDS = ("id", "stage", "status", "measures", "needs_notice", "named_contact")


def reason_roles() -> tuple[str, ...]:
    raw = os.environ.get("ZF_REASON_ROLES")
    if raw is None:
        return DEFAULT_REASON_ROLES
    return tuple(r.strip() for r in raw.split(",") if r.strip() and r.strip() != CONTRACTOR)


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
    if user.get("role") == "Application Administrator":
        # Option visibility only: no case, resident, finance or export data, and no action.
        return method == "GET" and kind == "me"
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
        dict(
            measure=m,
            flag="Hold"
            if resident_gate(
                c, [dict(measure=m, context_revision=(current_context(c, m) or {}).get("revision"))]
            )
            else "Proceed",
        )
        for m in case_measures(c)
    ]
    keep["home"] = {k: c["home"][k] for k in ("address", "town", "postcode", "type")}
    keep["contractor"] = {"name": c["contractor"]["name"], "contact": c["contractor"]["contact"]}
    keep["appointments"] = [
        {k: a[k] for k in ("type", "date", "slot")} | {"outcome": status_only(a["outcome"])}
        for a in c["appointments"]
    ]
    return keep


APPOINTMENT_STATUS = (
    "Booked",
    "Planned",
    "Completed",
    "No access",
    "Missed",
    "Cancelled",
    "Rescheduled",
)


def status_only(outcome):
    return outcome if outcome in (None, "") + APPOINTMENT_STATUS else NOTE_HELD


def hold_notes(c):
    """Replace staff-written free text anywhere in a case-shaped dict for roles without a need."""
    if isinstance(c, list):
        for item in c:
            hold_notes(item)
    elif isinstance(c, dict):
        c.pop("safeguarding_items", None)
        if "document_history" in c:
            c["document_history"] = [
                dict(
                    version=event["version"], at=event["at"], actor=event["actor"], detail=NOTE_HELD
                )
                for event in c["document_history"]
            ]
        if "source_version" in c and "reason" in c:
            for key in ("source", "source_version", "reason", "changes"):
                if c.get(key):
                    c[key] = NOTE_HELD
        if "edit_history" in c:
            c["edit_history"] = [
                dict(
                    version=event["version"],
                    at=event["at"],
                    actor=event["actor"],
                    preview_id=event["preview_id"],
                    detail=NOTE_HELD,
                )
                for event in c["edit_history"]
            ]
        if "from_stage" in c and "to_stage" in c:
            for key in ("reason", "source"):
                if c.get(key):
                    c[key] = NOTE_HELD
        advisory = (
            (c.get("contract_instruction") is False or "acts_as_contract_instruction" in c)
            and "summary" in c
            and ("kind" in c or "escalation_kind" in c)
        )
        if advisory and c.get("summary"):
            c["summary"] = NOTE_HELD
        for sg_item in raw_safeguarding_items(c):
            for key in ("source", "job", "summary", "reason"):
                if sg_item.get(key):
                    sg_item[key] = NOTE_HELD
        for k, v in c.items():
            if advisory and k in ("note", "contract_notice"):
                continue
            is_safety_dict = ("category" in c and "released" in c) or c.get("item_kind") in (
                "hazard",
                "safeguarding",
            )
            private_hazard = (is_safety_dict and k in ("source", "job", "summary", "reason")) or (
                "actor" in c and k in ("reason", "evidence")
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


_HIGH_SENSITIVITY_LEAF_KEYS = frozenset(
    NOTE_KEYS
    + (
        "adjustment",
        "phone",
        "email",
        "representative",
        "unavailable",
        "reason",
        "outcome",
        "source",
        "job",
        "evidence",
        "detail",
        "reference",
        "representative_ref",
        "review_ref",
        "recorder_identity",
        "account",
        "uprn",
        "ni_number",
    )
)
_HIGH_SENSITIVITY_SEGMENTS = frozenset(
    (
        "finance",
        "grants",
        "cost_allocation",
        "representative_authorities",
        "resident_safe_contact",
        "resident_contact_history",
        "resident_scopes",
        "resident_update",
        "service_requests",
    )
    + tuple(INTAKE_FIELDS)
)
_ISO_DATE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}(?:[t ]\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:z|[+-]\d{2}:?\d{2})?)?$"
)


def normalize_visibility_text(value: Any) -> str:
    if value is None:
        return ""
    raw = unicodedata.normalize("NFKC", str(value))
    cleaned = "".join(ch for ch in raw if unicodedata.category(ch) != "Cf")
    return " ".join(cleaned.split()).casefold()


_BENIGN_VISIBILITY_TOKENS = frozenset(
    normalize_visibility_text(token)
    for token in (
        "",
        "none",
        "unknown",
        REDACTED,
        NOTE_HELD,
        "yes",
        "no",
        "true",
        "false",
        "hold",
        "proceed",
        "completed",
        "ready",
        "proposed",
        "draft",
        "draft ready",
        "approved",
        "accepted",
        "rejected",
        "not reviewed",
        "not yet asked",
        "given",
        "refused",
        "withdrawn",
        "phone",
        "email",
        "post",
        "letter",
        "sms",
        "in person",
        "waiting for the recorded next step",
    )
    + APPOINTMENT_STATUS
)


def _skip_ai_generated_path(path: tuple[str, ...]) -> bool:
    if len(path) >= 2 and path[0] == "funding" and path[1] == "draft":
        return True
    if (
        len(path) >= 3
        and path[0] == "documents"
        and path[2] in ("summary", "derivative_text", "necessity_exception")
    ):
        return True
    return path == ("sensor_review_drafts",)


def _collect_case_strings(
    obj: Any,
    *,
    skip_ai_fields: bool = True,
    path: tuple[str, ...] = (),
) -> list[tuple[tuple[str, ...], str]]:
    if skip_ai_fields and _skip_ai_generated_path(path):
        return []
    if isinstance(obj, str):
        return [(path, obj)]
    if isinstance(obj, Mapping):
        out: list[tuple[tuple[str, ...], str]] = []
        for k, v in obj.items():
            out.extend(
                _collect_case_strings(v, skip_ai_fields=skip_ai_fields, path=path + (str(k),))
            )
        return out
    if isinstance(obj, list | tuple):
        out = []
        for item in obj:
            out.extend(
                _collect_case_strings(item, skip_ai_fields=skip_ai_fields, path=path + ("*",))
            )
        return out
    return []


def _is_high_sensitivity_path(path: tuple[str, ...]) -> bool:
    if not path:
        return False
    if path[-1] in _HIGH_SENSITIVITY_LEAF_KEYS:
        return True
    if path[-1] == "summary" and any(
        seg in ("hazards", "safeguarding_items", "safeguarding") for seg in path
    ):
        return True
    return any(seg in _HIGH_SENSITIVITY_SEGMENTS for seg in path)


def _is_plain_iso_date(norm_val: str, path: tuple[str, ...]) -> bool:
    if path and path[-1] in ("unavailable", "dob", "date_of_birth"):
        return False
    return bool(_ISO_DATE_RE.match(norm_val))


def withheld_case_values(
    raw_detail: Mapping[str, Any] | None,
    projected_detail: Mapping[str, Any] | None,
) -> tuple[str, ...]:
    """Return normalized case strings present in raw_detail that are absent from projected_detail."""
    if raw_detail is None:
        return ()
    raw_items = _collect_case_strings(raw_detail, skip_ai_fields=True)
    visible_items = (
        _collect_case_strings(projected_detail, skip_ai_fields=True)
        if projected_detail is not None
        else []
    )
    visible_norm = {normalize_visibility_text(val) for _, val in visible_items}
    visible_norm.discard("")
    found: set[str] = set()
    for path, val in raw_items:
        nv = normalize_visibility_text(val)
        if not nv or nv in _BENIGN_VISIBILITY_TOKENS or _is_plain_iso_date(nv, path):
            continue
        high_sens = _is_high_sensitivity_path(path)
        min_len = 3 if high_sens else 5
        if len(nv) < min_len or (nv.isdigit() and len(nv) < 5):
            continue
        if nv in visible_norm or any(nv in vis for vis in visible_norm):
            continue
        found.add(nv)
    return tuple(sorted(found, key=len, reverse=True))


def project_case_visibility(
    user: Mapping[str, Any] | None,
    raw_case: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    """Project raw_case for user's live role and case scope without running queue or handover queries."""
    if not isinstance(raw_case, Mapping):
        return None
    if user is None:
        return deepcopy(dict(raw_case))
    user_dict = dict(user)
    if is_contractor(user_dict):
        if not own_case(user_dict, raw_case):
            return None
        return contractor_detail(raw_case, deepcopy(dict(raw_case)))
    if user_dict.get("role") in STAFF_ROLES:
        return redact_staff_detail(user_dict, deepcopy(dict(raw_case)))
    return None


def withheld_scope_values(
    store: Any,
    user: Mapping[str, Any] | None,
    case_ids: Iterable[str] = (),
) -> tuple[str, ...]:
    """Return normalized values withheld from user across scoped cases plus out-of-scope sensitive case values."""
    if user is None:
        return ()
    user_dict = dict(user)
    scoped = list(dict.fromkeys(str(cid) for cid in case_ids if cid))
    found: set[str] = set()
    scoped_visible: set[str] = set()
    cases_map: Mapping[str, Any] = getattr(store, "cases", {}) or {}
    detail_fn = getattr(store, "detail", None)
    for cid in scoped:
        raw_case = cases_map.get(cid)
        proj: Mapping[str, Any] | None = None
        if isinstance(raw_case, Mapping):
            proj = project_case_visibility(user_dict, raw_case)
            if proj is not None:
                for _, val in _collect_case_strings(proj, skip_ai_fields=True):
                    nv = normalize_visibility_text(val)
                    if nv:
                        scoped_visible.add(nv)
            found.update(withheld_case_values(raw_case, proj))
        elif callable(detail_fn):
            raw: Mapping[str, Any] | None = None
            try:
                raw = detail_fn(cid)
            except KeyError:
                raw = None
            try:
                proj = detail_fn(cid, user_dict)
            except (KeyError, PermissionError):
                proj = None
            if proj is not None:
                for _, val in _collect_case_strings(proj, skip_ai_fields=True):
                    nv = normalize_visibility_text(val)
                    if nv:
                        scoped_visible.add(nv)
            found.update(withheld_case_values(raw, proj))
    for other_id, other_case in cases_map.items():
        if other_id in scoped or not isinstance(other_case, Mapping):
            continue
        for path, val in _collect_case_strings(other_case, skip_ai_fields=True):
            if not (
                _is_high_sensitivity_path(path)
                or (is_contractor(user_dict) and path == ("resident", "name"))
            ):
                continue
            nv = normalize_visibility_text(val)
            if not nv or nv in _BENIGN_VISIBILITY_TOKENS or _is_plain_iso_date(nv, path):
                continue
            if not is_contractor(user_dict) and re.match(r"^zf-\d+$", nv):
                continue
            if len(nv) < 4 or (nv.isdigit() and len(nv) < 5):
                continue
            if nv in scoped_visible or any(nv in vis for vis in scoped_visible):
                continue
            found.add(nv)
    return tuple(sorted(found, key=len, reverse=True))


def contains_withheld_value(text: Any, withheld: Iterable[str]) -> bool:
    """True when text contains any normalized withheld string under boundary-safe matching."""
    nt = normalize_visibility_text(text)
    if not nt:
        return False
    for w in withheld:
        if not w:
            continue
        if len(w) <= 7 and w[0].isalnum() and w[-1].isalnum():
            if re.search(rf"(?<![0-9a-z]){re.escape(w)}(?![0-9a-z])", nt):
                return True
        elif w in nt:
            return True
    return False


def redact_staff_detail(user, d):
    d.pop("sensor_review_drafts", None)
    raw_snapshot = deepcopy(d)
    d.pop("safeguarding_items", None)
    resident_view = user.get("role") in RESIDENT_VIEW_ROLES
    resident_data = (
        {key: deepcopy(d[key]) for key in RESIDENT_FIELDS + ("decision",) if key in d}
        if resident_view
        else {}
    )
    if not resident_view:
        d.pop("resident_update", None)
        d.pop("service_requests", None)
        d.pop("redress_route", None)
        for event in d.get("handoff_history", []):
            if isinstance(event.get("changes"), dict):
                event["changes"].pop("resident_update", None)
        for key in (
            "representative_authorities",
            "resident_safe_contact",
            "resident_contact_history",
            "resident_scopes",
        ):
            d.pop(key, None)
        raw_measures = d.get("measure_decisions", [])
        measures_iter = raw_measures.values() if isinstance(raw_measures, Mapping) else raw_measures
        for measure in measures_iter:
            if not isinstance(measure, dict):
                continue
            if measure.get("context"):
                measure["context"].pop("source", None)
            for answer in measure.get("versions", []):
                if isinstance(answer, dict):
                    for key in (
                        "source",
                        "note",
                        "representative_ref",
                        "review_ref",
                        "recorder_identity",
                    ):
                        answer.pop(key, None)
            if isinstance(measure.get("review"), dict):
                measure["review"].pop("review_ref", None)
        for review in d.get("resident_reviews", {}).values():
            if isinstance(review, dict):
                review.pop("review_ref", None)
        for request in d.get("service_requests", []):
            if isinstance(request, dict):
                request.pop("representative_ref", None)
    if not can_see_reason(user):
        work = d.pop("work", None)  # Already projected by the shared queue read model.
        hold_notes(d)
        for item in d.get("hazards", []):
            if taskqueues.is_safeguarding(item.get("category")):
                item["category"] = "Safety review"
                item["clock_text"] = str(item.get("clock_text", "")).replace(
                    "Safeguarding clock", "Safety clock")
            for entry in (*item.get("history", []), item.get("legacy_record")):
                for node in (entry, (entry or {}).get("snapshot")):
                    if isinstance(node, dict) and taskqueues.is_safeguarding(node.get("category")):
                        node["category"] = "Safety review"
        if work is not None:
            d["work"] = work
        if d.get("status", "").startswith("Waiting on "):
            d["status"] = "Waiting for the recorded next step"
        if d.get("reason"):
            d["reason"] = NOTE_HELD
        adjustment = d["resident"].get("adjustment")
        d["resident"]["adjustment"] = (
            "Unknown"
            if adjustment in (None, "", "Unknown")
            else REDACTED
            if adjustment != "None"
            else "None"
        )
    d.update(resident_data)
    if not appointment_evidence_visible(user):
        for key in INTAKE_FIELDS:
            d.pop(key, None)
        d.pop("affected_challenges", None)
        d.pop("challenge_targets", None)
        d.pop("challenge_guarantees", None)
        d.pop("challenge_assurance", None)
        d.pop("nomination_permissions", None)
    else:
        from . import nomination_route
        for key in ("nomination_records", "affected_challenges", "challenge_targets"):
            if key in d:
                d[key] = nomination_route.scrub_nomination_restricted_fields(d[key])
    if user.get("role") not in FINANCE_VIEW:
        d.pop("finance", None)
        d.pop("grants", None)
        d.pop("cost_allocation", None)
        if isinstance(d.get("funding"), dict) and d["funding"].get("draft"):
            d["funding"]["draft"] = NOTE_HELD
    reason_ok = can_see_reason(user)
    for doc in d.get("documents", []):
        if isinstance(doc, dict):
            doc.pop("derivative_text", None)
            if (
                not reason_ok
                and isinstance(doc.get("necessity_exception"), dict)
                and doc["necessity_exception"].get("reason")
            ):
                doc["necessity_exception"]["reason"] = NOTE_HELD
    withheld = withheld_case_values(raw_snapshot, d)
    if (
        isinstance(d.get("funding"), dict)
        and d["funding"].get("draft")
        and d["funding"]["draft"] != NOTE_HELD
    ):
        if contains_withheld_value(d["funding"]["draft"], withheld):
            d["funding"]["draft"] = NOTE_HELD
    for doc in d.get("documents", []):
        if isinstance(doc, dict) and doc.get("summary") and doc["summary"] != NOTE_HELD:
            if (
                not is_available_case_document(doc)
                or (doc.get("summary_from_exception") and not reason_ok)
                or contains_withheld_value(doc["summary"], withheld)
            ):
                doc["summary"] = NOTE_HELD
    return d


def me_payload(user, counts, staff):
    if is_contractor(user):
        return dict(
            user=dict(name=user["name"], role=user["role"], contractor=user.get("contractor")),
            counts={},
            staff=[],
        )
    if user.get("role") == "Application Administrator":
        return dict(user=user, counts={}, staff=[])
    return dict(user=user, counts=counts, staff=staff)
