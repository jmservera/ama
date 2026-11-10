"""Fixed credential-free synthetic discovery demonstration (Refs #125).

Composes the delivered discovery assistant helpers over one explicitly fictional in-module fixture.
It reads no environment, path, store, clock, network, company dataset or model, dispatches no tool
and manufactures no readiness report. The output is a design-hypothesis illustration: the expected
figures are constructed from the fixture, not an analyst's observed results, and the conventional
table reuses the same calculation rather than an independent reporting engine.
"""

import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from typing import Any

from zava_forward.core import discovery_assistant_boundary as boundary
from zava_forward.core import discovery_assistant_drafting as drafting
from zava_forward.core import discovery_assistant_evaluation as evaluation
from zava_forward.core.version import __version__

DEMO_VERSION = "discovery-assistant-demo-v1"
FIXTURE_ID = "zava-synthetic-discovery-demo-v1"
DESIGN_HYPOTHESIS_STATUS = "UNAPPROVED_DESIGN_HYPOTHESIS"

FIXTURE: tuple[drafting.StageEvent, ...] = (
    drafting.StageEvent("SYN-P1", "survey", "2026-03-02T09:00:00+00:00", "SYN-EVT-001"),
    drafting.StageEvent("SYN-P1", "design", "2026-03-03T09:00:00+00:00", "SYN-EVT-002"),
    drafting.StageEvent("SYN-P1", "install", "2026-03-05T21:00:00+00:00", "SYN-EVT-003"),
    drafting.StageEvent("SYN-P1", "handover", "2026-03-06T09:00:00+00:00", "SYN-EVT-004"),
    drafting.StageEvent("SYN-P2", "survey", "2026-03-09T10:00:00+01:00", "SYN-EVT-005"),
    drafting.StageEvent("SYN-P2", "design", "2026-03-09T21:30:00+00:00", "SYN-EVT-006"),
    drafting.StageEvent("SYN-P2", "install", "not-recorded", "SYN-EVT-007"),
)

# Hand-derived from the fixture above, independently of the calculation under test.
EXPECTED_HOURS: dict[str, float] = {"design": 60.0, "install": 12.0, "survey": 36.5}
EXPECTED_REFERENCES: tuple[str, ...] = (
    "SYN-EVT-001",
    "SYN-EVT-002",
    "SYN-EVT-003",
    "SYN-EVT-004",
    "SYN-EVT-005",
    "SYN-EVT-006",
)
EXPECTED_GAPS: tuple[str, ...] = ("unusable-timestamp:SYN-P2/install",)
EXPECTED_DRAFT_TEXT = (
    "design: 60 hours; install: 12 hours; survey: 36.5 hours. "
    "Sources: SYN-EVT-001, SYN-EVT-002, SYN-EVT-003, SYN-EVT-004, SYN-EVT-005, SYN-EVT-006."
)

# Policy decisions only: nothing is registered, dispatched or attempted.
DECISION_NAMES: tuple[str, ...] = (
    "query_approved_analytical_store",
    "write_source_system",
    "contact_resident",
    "rank_properties",
    "read_company_dataset",
)


def _calculate(events: Sequence[drafting.StageEvent]) -> dict[str, Any]:
    durations = drafting.calculate_stage_durations(events)
    return {
        "hours": durations.hours,
        "source_references": list(durations.source_references),
        "gaps": list(durations.gaps),
    }


def _expected_check(calculated: Mapping[str, Any], draft_text: str) -> dict[str, Any]:
    mismatches: list[str] = []
    if calculated["hours"] != EXPECTED_HOURS:
        mismatches.append("hours")
    if tuple(calculated["source_references"]) != EXPECTED_REFERENCES:
        mismatches.append("source_references")
    if tuple(calculated["gaps"]) != EXPECTED_GAPS:
        mismatches.append("gaps")
    if draft_text != EXPECTED_DRAFT_TEXT:
        mismatches.append("draft_text")
    return {
        "basis": "constructed expectation for this fictional fixture, not an observed result",
        "expected_hours": EXPECTED_HOURS,
        "expected_source_references": list(EXPECTED_REFERENCES),
        "expected_gaps": list(EXPECTED_GAPS),
        "mismatches": mismatches,
        "passed": not mismatches,
    }


def run_demo() -> dict[str, Any]:
    readiness = boundary.assess_readiness([])
    connection_denied = (
        readiness.status != boundary.READY_FOR_OWNER_DECISION
        and not readiness.connection_to_company_data_permitted
    )
    decisions = [asdict(boundary.authorise_tool(name)) for name in DECISION_NAMES]
    for decision in decisions:
        decision["dispatched"] = False
        decision["attempted"] = False
        decision["note"] = "policy decision only; no tool is registered, dispatched or attempted"
    calculated = _calculate(FIXTURE)
    durations = drafting.calculate_stage_durations(FIXTURE)
    draft = drafting.draft_evidence(durations)
    expected = _expected_check(calculated, draft.text)
    repeat = evaluation.check_repeatability(_calculate, FIXTURE, runs=3)
    comparison = evaluation.compare_methods([])
    return {
        "demo_version": DEMO_VERSION,
        "core_version": __version__,
        "helper_versions": {
            "boundary": boundary.BOUNDARY_VERSION,
            "drafting": drafting.DRAFTING_VERSION,
            "evaluation": evaluation.EVALUATION_VERSION,
        },
        "design_hypothesis_status": DESIGN_HYPOTHESIS_STATUS,
        "approved_solution": False,
        "fixture": {
            "id": FIXTURE_ID,
            "explicitly_fictional": True,
            "events": [
                {
                    "event_id": e.source_reference,
                    "property_id": e.property_id,
                    "stage": e.stage,
                    "timestamp": e.timestamp,
                }
                for e in FIXTURE
            ],
        },
        "readiness": {
            "status": readiness.status,
            "satisfied": list(readiness.satisfied),
            "missing": list(readiness.missing),
            "missing_count": len(readiness.missing),
            "invalid": list(readiness.invalid),
            "connection_to_company_data_permitted": readiness.connection_to_company_data_permitted,
            "next_step": readiness.next_step,
        },
        "company_connection": "DENY" if connection_denied else "UNEXPECTED_NOT_DENIED",
        "authority_decisions": decisions,
        "calculation": calculated,
        "conventional_table": {
            "basis": "same calculation as the draft; not an independent reporting engine",
            "rows": [
                {"stage": stage, "hours": hours} for stage, hours in calculated["hours"].items()
            ],
        },
        "draft": {
            "status": draft.status,
            "text": draft.text,
            "model_used": draft.model_used,
            "fallback_reason": draft.rejected_reason,
            "validated_finding": draft.validated_finding,
            "source_references": list(draft.source_references),
        },
        "expected_arithmetic": expected,
        "repeatability": {
            "runs": repeat.runs,
            "identical": repeat.identical,
            "digests": list(repeat.digests),
        },
        "comparison": {
            "criterion_met": comparison.criterion_met,
            "assistant_preferred": comparison.assistant_preferred,
            "human_result_pointers": [],
            "comparable_measures": list(comparison.comparable),
            "missing_by_measure": {k: list(v) for k, v in comparison.incomplete.items()},
            "invalid": list(comparison.invalid),
        },
        "evidence_boundary": [
            "Fictional fixture only: no company, resident or property data is read.",
            "Expected figures are constructed, not observed by any analyst.",
            "No participant, elapsed effort, benefit, preference or model evaluation exists.",
            "Fallback text is deterministic code output, not an AI result.",
            "Phase 0, access, privacy and human approvals remain unproven and are not replaced.",
        ],
        "manual_path": boundary.MANUAL_PATH,
        "overall_passed": (
            connection_denied
            and expected["passed"]
            and repeat.identical
            and not draft.model_used
            and not comparison.criterion_met
        ),
    }


def render(report: Mapping[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True)


def main(args: Sequence[str]) -> int:
    import sys

    if args:
        print(f"discovery-demo takes no arguments: {' '.join(args)}", file=sys.stderr)
        return 2
    report = run_demo()
    print(render(report))
    if not report["overall_passed"]:
        print(
            "discovery-demo failed: expectation mismatch or repeatability failure", file=sys.stderr
        )
        return 1
    return 0
