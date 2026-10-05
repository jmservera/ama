from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DEFAULT_THRESHOLD = 5
MAX_THRESHOLD = 100

EVENT_OUTCOMES = {
    "resident_no_access_verified": "Verified resident no-access",
    "provider_no_show": "Provider or contractor no-show",
    "cancelled": "Cancelled",
    "rescheduled": "Rescheduled",
    "attended": "Attended",
}

ACTOR_LABELS = frozenset({"Local reviewer", "Synthetic scenario runner"})
CLOSURE_REASONS = frozenset(
    {"human_review_completed", "scenario_complete", "synthetic_test_reset"}
)

CASE_STAGES = [
    "01 Identified",
    "02 Contacting resident",
    "03 Survey booked",
    "04 Survey complete",
    "05 In design",
    "06 Awaiting resident decision",
    "07 Ready to order",
    "08 Ordered",
    "09 On site",
    "10 Practical completion",
    "11 Handed over",
    "12 Closed",
]

SOURCE_STATUSES = frozenset(
    CASE_STAGES
    + [
        "Closed",
        "Complete",
        "Design",
        "Excluded",
        "Hold",
        "On hold",
        "Reopened",
        "Withdrawn",
    ]
)

STAGE_GATES = {
    1: ("named_owner",),
    2: ("contact_plan", "adjustment_reviewed"),
    3: ("assessment_evidence", "professional_review"),
    4: ("design_evidence", "professional_approval"),
    5: ("resident_decision",),
    6: ("funding_confirmed", "safety_clear"),
    7: ("supplier_capacity", "human_release"),
    8: ("work_started_evidence", "safety_clear"),
    9: ("completion_evidence",),
    10: ("quality_pass", "evidence_accepted"),
    11: ("handover_recorded", "human_close_approval"),
}

GATE_LABELS = {
    "named_owner": "Named owner",
    "contact_plan": "Synthetic contact plan",
    "adjustment_reviewed": "Accessibility adjustments checked",
    "assessment_evidence": "Assessment evidence",
    "professional_review": "Professional review",
    "design_evidence": "Design evidence",
    "professional_approval": "Professional approval",
    "resident_decision": "Resident decision recorded",
    "funding_confirmed": "Funding confirmed",
    "safety_clear": "No active safety hold",
    "supplier_capacity": "Supplier capacity committed",
    "human_release": "Human release approval",
    "work_started_evidence": "Work-start evidence",
    "completion_evidence": "Completion evidence",
    "quality_pass": "Quality pass",
    "evidence_accepted": "Evidence accepted",
    "handover_recorded": "Resident handover recorded",
    "human_close_approval": "Human closure approval",
}


@dataclass(frozen=True)
class Escalation:
    eligible_count: int
    threshold: int
    required: bool
    message: str


def validate_threshold(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError("Threshold must be an integer between 0 and 100.")
    try:
        threshold = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Threshold must be an integer between 0 and 100.") from exc
    if str(value).strip() != str(threshold) or not 0 <= threshold <= MAX_THRESHOLD:
        raise ValueError("Threshold must be an integer between 0 and 100.")
    return threshold


def is_eligible_no_access(outcome: str, appointment_confirmed: bool) -> bool:
    return outcome == "resident_no_access_verified" and appointment_confirmed is True


def active_event_slice(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    last_closed = max(
        (index for index, event in enumerate(events) if event["outcome"] == "case_closed"),
        default=-1,
    )
    return events[last_closed + 1 :]


def escalation_status(
    events: list[dict[str, Any]], threshold: int, active: bool = True
) -> Escalation:
    eligible_count = sum(
        is_eligible_no_access(
            event["outcome"], bool(event["appointment_confirmed"])
        )
        for event in active_event_slice(events)
    ) if active else 0
    required = active and eligible_count > validate_threshold(threshold)
    message = (
        "Human investigation required. The count alone is not a finding of refusal or non-cooperation."
        if required
        else "No escalation. Only verified resident no-access at a confirmed appointment counts."
    )
    return Escalation(eligible_count, threshold, required, message)


def normalize_scenario_stage(status: str) -> str | None:
    normalized = status.strip()
    if normalized in CASE_STAGES:
        return normalized
    legacy_stage = {"complete": CASE_STAGES[9], "design": CASE_STAGES[4]}
    if normalized.casefold() in legacy_stage:
        return legacy_stage[normalized.casefold()]
    terminal = {"closed", "withdrawn", "excluded"}
    if normalized.casefold() in terminal:
        return CASE_STAGES[-1]
    if normalized.casefold() == "reopened":
        return CASE_STAGES[0]
    if normalized.casefold() in {"hold", "on hold"}:
        return "On hold"
    return None


def check_transition(
    stage: str, controls: dict[str, bool], safety_hold_active: bool
) -> tuple[str | None, list[str]]:
    normalized_stage = normalize_scenario_stage(stage)
    if normalized_stage is None:
        return None, ["Current source status is not mapped to a supported lifecycle stage."]
    if normalized_stage not in CASE_STAGES:
        return None, ["Case is on hold or has no supported next stage."]
    current_index = CASE_STAGES.index(normalized_stage)
    if current_index >= len(CASE_STAGES) - 1:
        return None, ["Case is already at the final stage."]
    target_index = current_index + 1
    required_gates = STAGE_GATES.get(target_index, ())
    missing = [
        GATE_LABELS[gate]
        for gate in required_gates
        if not controls.get(gate, False)
    ]
    if safety_hold_active:
        missing = [
            label for label in missing
            if label != GATE_LABELS["safety_clear"]
        ]
        missing.append("Active safety hold")
    if missing:
        return None, missing
    return CASE_STAGES[target_index], []
