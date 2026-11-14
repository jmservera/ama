"""Pure journey ownership register check and human-review routing (NFR-008, NFR-009, #128).

Each material journey needs an accountable human owner, escalation route, service-time measures
with thresholds set by that owner, and a manual alternative that a person has tested. This module
only checks a supplied register and never invents owners, thresholds or test results; with no
supplied approval the result is blocked. It performs no store, clock or network access.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

from zava_forward.core.rai_release import digest, named, named_human

RECORD_VERSION = "journey-ownership-register-v1"
MEASURES = (
    "intake_to_owner",
    "hazard_action",
    "professional_review",
    "resident_contact_and_adjustment",
    "appointment_recovery",
    "evidence_review",
    "defect_resolution",
    "external_query_response",
)
JOURNEYS = {
    "J1": "Choose each proposed measure",
    "J2": "Pause, withdraw or ask for more time",
    "J3": "Compare appointment offers and confirmations",
    "J4": "Know who will update you and when",
    "J5": "Handover, practise controls and get aftercare",
    "J6": "Challenge, complain and follow a remedy",
    "R1": "Task-limited representative briefing and actions",
}
DESIGN_DOC = "docs/reference/research/ux/customer-journeys/residents.md"
REVIEW_REASONS = ("source_missing", "sensor_missing", "support_unknown", "appointment_incomplete")
OBSERVATION_FIELDS = frozenset({"measure", "value"})
MIN_CELL_FLOOR = 5
INCOMPLETE_APPOINTMENT = {"unconfirmed", "no_response", "prior_no_access", "unknown", "missed"}
IDENTITY_FIELDS = frozenset(
    {"staff_id", "staff", "user_id", "user", "employee", "operator", "handler", "officer", "name"}
    | {"email", "resident_id", "case_id", "session_id", "device_id"}
)
GAP = (
    "Owners, thresholds and the manual-alternative tests are human decisions (OD-09, OD-25); "
    "this check does not make them and a blocked record is not a finding about any resident."
)


def draft() -> dict[str, Any]:
    """Draft register: every journey listed; none has an owner, threshold or tested alternative."""
    return {
        "version": RECORD_VERSION,
        "synthetic": True,
        "journeys": [
            {
                "id": code,
                "name": name,
                "design_ref": f"{DESIGN_DOC}#{code.lower()}",
                "owner": None,
                "escalation": None,
                "measures": {m: {"threshold": None, "approved_by": None} for m in MEASURES},
                "manual_alternative": {"documented": True, "tested_by": None, "tested_on": None},
            }
            for code, name in JOURNEYS.items()
        ],
    }


def _journey_blockers(journey: Mapping[str, Any]) -> list[str]:
    code = str(journey.get("id"))
    out: list[str] = []
    if not named(journey.get("owner")):
        out.append(f"{code}:owner_missing")
    if not named(journey.get("escalation")):
        out.append(f"{code}:escalation_missing")
    measures = journey.get("measures")
    measures = measures if isinstance(measures, Mapping) else {}
    for key in MEASURES:
        entry = measures.get(key)
        entry = entry if isinstance(entry, Mapping) else {}
        if not named(entry.get("threshold")) or not named(entry.get("approved_by")):
            out.append(f"{code}:{key}:threshold_unapproved")
    manual = journey.get("manual_alternative")
    manual = manual if isinstance(manual, Mapping) else {}
    if manual.get("documented") is not True:
        out.append(f"{code}:manual_alternative_undocumented")
    if not (named(manual.get("tested_by")) and named(manual.get("tested_on"))):
        out.append(f"{code}:manual_alternative_untested")
    return out


def evaluate(register: Mapping[str, Any]) -> dict[str, Any]:
    """Return a hash-bound readiness record; a gap blocks the journey, never a resident."""
    journeys = register.get("journeys")
    items = [j for j in journeys if isinstance(j, Mapping)] if isinstance(journeys, list) else []
    seen = {str(j.get("id")) for j in items}
    blockers = [f"{code}:journey_missing" for code in JOURNEYS if code not in seen]
    per_journey = {}
    for journey in items:
        found = _journey_blockers(journey)
        per_journey[str(journey.get("id"))] = {"ready": not found, "blockers": found}
        blockers += found
    record = {
        "version": RECORD_VERSION,
        "register_digest": digest(register),
        "journeys": per_journey,
        "blockers": blockers,
        "status": "ready" if not blockers else "blocked",
        "activation_allowed": not blockers,
        "usability_evidence": False,
        "gap": GAP,
    }
    record["record_hash"] = digest(record)
    return record


def human_review_route(case: Mapping[str, Any], reviewer: str | None = None) -> dict[str, Any]:
    """Route missing data or an incomplete appointment to a named person, with no rank effect.

    The result carries reasons and a human route only. It has no score, never lowers priority or
    service, never drops the case, and does not infer vulnerability or refusal from absent data.
    An unassigned reviewer is reported as a blocker on the route, not a reason to skip review.
    """
    reasons = []
    if case.get("source_record") in (None, "missing", "stale", "partial"):
        reasons.append("source_missing")
    if case.get("sensor_data") in (None, "missing", "declined"):
        reasons.append("sensor_missing")
    resident = case.get("resident")
    if not isinstance(resident, Mapping) or resident.get("priority_support") is None:
        reasons.append("support_unknown")
    history = case.get("appointment_history", "unknown")
    if (
        not isinstance(history, str)
        or not history.strip()
        or history.strip().lower() in INCOMPLETE_APPOINTMENT
    ):
        reasons.append("appointment_incomplete")
    assigned = bool(reasons) and named_human(reviewer)
    return {
        "case_id": case.get("id"),
        "route": "human_review" if reasons else "none",
        "reasons": reasons,
        "reviewer": reviewer.strip() if assigned and isinstance(reviewer, str) else None,
        "assignment_blocker": "named_reviewer_missing" if reasons and not assigned else None,
        "rank_effect": "none",
    }


def route_cases(cases: Sequence[Mapping[str, Any]], reviewer: str | None = None) -> dict[str, Any]:
    """Route every case and count review burden by reason; counts are aggregate only."""
    routes = [human_review_route(c, reviewer) for c in cases]
    counts = {r: sum(r in x["reasons"] for x in routes) for r in REVIEW_REASONS}
    return {
        "routes": routes,
        "tested": len(routes),
        "routed_to_human": sum(x["route"] == "human_review" for x in routes),
        "unassigned": sum(x["assignment_blocker"] is not None for x in routes),
        "dropped": 0,
        "reason_counts": counts,
    }


def _finite_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def aggregate_usability(
    observations: Sequence[Mapping[str, Any]], min_cell: int | None = None
) -> dict[str, Any]:
    """Report usability measures as aggregates only; reject individual-level records.

    Any observation carrying a staff or person identifier blocks the whole report with no figures.
    Cells smaller than the owner-approved minimum are suppressed; with no approved minimum nothing
    is reported. This invents no threshold and is not usability evidence.
    """
    rejected = sorted(
        {
            str(k)
            for o in observations
            if isinstance(o, Mapping)
            for k in o
            if str(k).casefold() in IDENTITY_FIELDS
        }
    )
    malformed = not observations or any(
        not isinstance(o, Mapping)
        or o.get("measure") not in MEASURES
        or not set(o) <= OBSERVATION_FIELDS
        or not _finite_number(o.get("value"))
        for o in observations
    )
    approved = (
        isinstance(min_cell, int) and not isinstance(min_cell, bool) and min_cell >= MIN_CELL_FLOOR
    )
    blockers = []
    if rejected:
        blockers.append("individual_identifiers_rejected")
    if malformed:
        blockers.append("unknown_measure_or_malformed")
    if not approved:
        blockers.append("min_cell_unapproved")
    cells: dict[str, dict[str, Any]] = {}
    if not blockers:
        for measure in MEASURES:
            values = [o["value"] for o in observations if o["measure"] == measure]
            if not values:
                continue
            if len(values) < (min_cell or 0):
                cells[measure] = {"n": None, "mean": None, "suppressed": True}
            else:
                cells[measure] = {
                    "n": len(values),
                    "mean": sum(values) / len(values),
                    "suppressed": False,
                }
    return {
        "level": "aggregate",
        "status": "blocked" if blockers else "reported",
        "blockers": blockers,
        "rejected_fields": rejected,
        "measures": cells,
        "staff_surveillance": False,
    }
