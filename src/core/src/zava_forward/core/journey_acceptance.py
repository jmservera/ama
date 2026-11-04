"""Acceptance register for PRD AC-034 to AC-043 (Refs #134, slice 2).

Each criterion is recorded as `partial` (existing constructed-fixture evidence is named but the
full Given/When/Then is not proven) or `deferred` (with a reason). Nothing is recorded as passing
and nothing here is user validation or owner approval. `check` reads only the repository files it
is pointed at and changes nothing.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

PRD = "docs/prds/zava-forward-retrofit-programme-demonstrator.md"
CRITERIA = tuple(f"AC-{n:03d}" for n in range(34, 44))
NOTICE = (
    "Constructed-fixture evidence, not user validation. No criterion is recorded as passing; "
    "partial means related evidence exists but the full criterion is not proven."
)
BROWSER = "No browser run in this slice; live reset, focus and announcement are unverified."
CORE = "src/core/src/zava_forward/core/"

REGISTER: dict[str, dict[str, Any]] = {
    "AC-034": dict(
        status="partial",
        reason=BROWSER,
        evidence=[
            "src/api/checks/workbench_browser_check.py",
            "src/api/checks/workbench-manifest.json",
        ],
    ),
    "AC-035": dict(
        status="deferred",
        reason="No constructed commitment and rejected-handoff evidence is mapped yet.",
        evidence=[],
    ),
    "AC-036": dict(
        status="deferred",
        reason="Owner, destination, receiver and chase-owner label agreement is not mapped yet.",
        evidence=[],
    ),
    "AC-037": dict(
        status="partial",
        reason="Per-measure decisions exist; pause isolation and consent checks are not mapped.",
        evidence=[CORE + "resident_decisions.py", "src/core/tests/test_resident_decisions.py"],
    ),
    "AC-038": dict(
        status="deferred",
        reason="Referral with unconfirmed receipt and read-only hold evidence is not mapped yet.",
        evidence=[],
    ),
    "AC-039": dict(
        status="partial",
        reason="Capacity and package records exist; draft-package readiness display is not mapped.",
        evidence=[CORE + "procurement.py", "src/core/tests/test_quality_procurement.py"],
    ),
    "AC-040": dict(
        status="partial",
        reason="Source-conflict queue exists; per-case rationale on switching is not mapped.",
        evidence=[CORE + "exception_queue.py", "src/core/tests/test_exception_queue.py"],
    ),
    "AC-041": dict(
        status="deferred",
        reason="Portfolio figures with denominator and filter-impact display are not mapped yet.",
        evidence=[],
    ),
    "AC-042": dict(
        status="partial",
        reason="Quality and invoice records; the mismatch and incomplete-pack view is not mapped.",
        evidence=[CORE + "quality.py", CORE + "procurement.py"],
    ),
    "AC-043": dict(
        status="partial",
        reason="Manifest lists 11 profiles and 9 workflows, all unavailable; Slice C is deferred.",
        evidence=[
            "docs/reference/research/retrofit-synthetic-data/scenario-manifest.json",
            "src/core/tests/test_scenario_manifest.py",
            CORE + "journey_trace.py",
            "src/core/tests/test_journey_store.py",
            "src/core/tests/test_journey_building.py",
        ],
    ),
}


def check(root: Path, register: Mapping[str, Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """Return blockers: missing or unknown IDs, invalid status, no reason, absent evidence files."""
    reg = REGISTER if register is None else register
    prd = (root / PRD).read_text(encoding="utf-8")
    blockers: list[str] = []
    for ac in CRITERIA:
        if f"| {ac} |" not in prd:
            blockers.append(f"{ac}:not_in_prd")
        entry = reg.get(ac)
        if entry is None:
            blockers.append(f"{ac}:missing")
            continue
        status = entry.get("status")
        if status not in ("partial", "deferred"):
            blockers.append(f"{ac}:status_invalid")
        if not str(entry.get("reason") or "").strip():
            blockers.append(f"{ac}:reason_missing")
        evidence = entry.get("evidence")
        if not isinstance(evidence, list) or (status == "partial" and not evidence):
            blockers.append(f"{ac}:evidence_missing")
            continue
        blockers += [f"{ac}:evidence_not_found:{p}" for p in evidence if not (root / p).is_file()]
    blockers += [f"{ac}:unknown_criterion" for ac in reg if ac not in CRITERIA]
    return dict(
        status="blocked" if blockers else "recorded",
        blockers=blockers,
        passed=[],
        partial=[a for a in CRITERIA if reg.get(a, {}).get("status") == "partial"],
        deferred=[a for a in CRITERIA if reg.get(a, {}).get("status") == "deferred"],
        notice=NOTICE,
    )
