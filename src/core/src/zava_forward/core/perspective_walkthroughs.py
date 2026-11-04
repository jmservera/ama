"""Perspective walkthrough coverage register for the eleven PRD perspectives (Refs #134, slice 4).

For each perspective the PRD "Profile Journey Contract" needs five elements: entry, evidence
inspection, safe endpoint, recovery route and accountable handoff over linked records. This
register records each element as `partial` (a named constructed-fixture record module exists but no
screen walkthrough is proven) or `unmet`. Nothing is recorded as met, and nothing here is user
validation or owner approval. `check` reads only the repository files it is pointed at.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

PRD = "docs/prds/zava-forward-retrofit-programme-demonstrator.md"
MANIFEST = "docs/reference/research/retrofit-synthetic-data/scenario-manifest.json"
ELEMENTS = ("entry", "evidence", "safe_endpoint", "recovery", "handoff")
NOTICE = (
    "Constructed-fixture evidence, not user validation. No element is recorded as met; partial "
    "means a record module exists but no screen walkthrough, keyboard or announcement run "
    "proves it."
)
CORE = "src/core/src/zava_forward/core/"
TESTS = "src/core/tests/"
UNMET = "No linked-record walkthrough is mapped for this element yet."

# perspective id -> element -> evidence files; an empty list means unmet.
EVIDENCE: dict[str, dict[str, list[str]]] = {
    "asset-investment": {
        "entry": [CORE + "taskqueues.py", TESTS + "test_taskqueues.py"],
        "evidence": [CORE + "stock.py", TESTS + "test_stock_reconciliation.py"],
        "safe_endpoint": [],
        "recovery": [],
        "handoff": [],
    },
    "programme-coordinator": {
        "entry": [CORE + "taskqueues.py", TESTS + "test_taskqueues.py"],
        "evidence": [CORE + "exception_queue.py", TESTS + "test_exception_queue.py"],
        "safe_endpoint": [],
        "recovery": ["src/api/checks/workbench_browser_check.py"],
        "handoff": [CORE + "coordinator.py"],
    },
    "retrofit-case-team": {
        "entry": [CORE + "home_case.py", TESTS + "test_home_case.py"],
        "evidence": [
            CORE + "buildings.py",
            CORE + "journey_trace.py",
            TESTS + "test_journey_building.py",
        ],
        "safe_endpoint": [CORE + "gates.py"],
        "recovery": [],
        "handoff": [CORE + "signoffs.py"],
    },
    "assessor-designer": {
        "entry": [CORE + "taskqueues.py"],
        "evidence": [CORE + "signoffs.py"],
        "safe_endpoint": [CORE + "signoffs.py"],
        "recovery": [],
        "handoff": [CORE + "signoffs.py"],
    },
    "housing-resident-engagement": {
        "entry": [CORE + "resident_decisions.py", TESTS + "test_resident_decisions.py"],
        "evidence": [CORE + "resident_decisions.py"],
        "safe_endpoint": [CORE + "resident_decisions.py"],
        "recovery": [],
        "handoff": [],
    },
    "repairs-building-safety": {
        "entry": [CORE + "hazard.py", TESTS + "test_hazard_referral.py"],
        "evidence": [CORE + "hazard.py"],
        "safe_endpoint": [CORE + "hazard.py"],
        "recovery": [],
        "handoff": [CORE + "hazard.py"],
    },
    "procurement-contracts": {
        "entry": [CORE + "procurement.py", TESTS + "test_quality_procurement.py"],
        "evidence": [CORE + "procurement.py"],
        "safe_endpoint": [CORE + "procurement.py"],
        "recovery": [],
        "handoff": [],
    },
    "provider-contractor": {
        "entry": [CORE + "job_pack.py"],
        "evidence": [],
        "safe_endpoint": [],
        "recovery": [],
        "handoff": [],
    },
    "quality-assurance": {
        "entry": [CORE + "quality.py", TESTS + "test_quality_procurement.py"],
        "evidence": [CORE + "quality.py"],
        "safe_endpoint": [CORE + "quality.py"],
        "recovery": [],
        "handoff": [CORE + "journey_trace.py", TESTS + "test_journey_store.py"],
    },
    "finance-grants": {
        "entry": [CORE + "finance.py", TESTS + "test_finance_match_controls.py"],
        "evidence": [CORE + "finance.py", CORE + "grants.py"],
        "safe_endpoint": [CORE + "form_review.py", TESTS + "test_form_review.py"],
        "recovery": [],
        "handoff": [TESTS + "test_finance_signoffs.py"],
    },
    "digital-auditor": {
        "entry": [CORE + "exception_queue.py"],
        "evidence": [CORE + "change_provenance.py", TESTS + "test_change_provenance.py"],
        "safe_endpoint": [CORE + "ledger.py"],
        "recovery": [CORE + "recovery.py", TESTS + "test_recovery.py"],
        "handoff": [],
    },
}


def register() -> dict[str, dict[str, dict[str, Any]]]:
    """Build the per-element register: partial where evidence is named, otherwise unmet."""
    return {
        pid: {
            el: dict(
                status="partial" if files else "unmet",
                evidence=list(files),
                reason=NOTICE if files else UNMET,
            )
            for el, files in ((e, elements.get(e, [])) for e in ELEMENTS)
        }
        for pid, elements in EVIDENCE.items()
    }


def check(
    root: Path, reg: Mapping[str, Mapping[str, Mapping[str, Any]]] | None = None
) -> dict[str, Any]:
    """Return blockers: profile mismatch with the manifest, bad status, missing evidence files."""
    reg = register() if reg is None else reg
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    prd = (root / PRD).read_text(encoding="utf-8")
    profiles = {p["id"]: p["perspective"] for p in manifest["profiles"]}
    blockers: list[str] = []
    for pid, name in profiles.items():
        if f"| {name} |" not in prd:
            blockers.append(f"{pid}:not_in_prd")
        if pid not in reg:
            blockers.append(f"{pid}:missing")
    blockers += [f"{pid}:unknown_profile" for pid in reg if pid not in profiles]
    for pid, cells in reg.items():
        if pid not in profiles:
            continue
        for el in ELEMENTS:
            cell = cells.get(el)
            if cell is None:
                blockers.append(f"{pid}.{el}:missing")
                continue
            status, files = cell.get("status"), cell.get("evidence")
            if status not in ("partial", "unmet"):
                blockers.append(f"{pid}.{el}:status_invalid")
            if not str(cell.get("reason") or "").strip():
                blockers.append(f"{pid}.{el}:reason_missing")
            if not isinstance(files, list) or (status == "partial" and not files):
                blockers.append(f"{pid}.{el}:evidence_missing")
                continue
            blockers += [
                f"{pid}.{el}:evidence_not_found:{p}" for p in files if not (root / p).is_file()
            ]
    cells_all = [c for cells in reg.values() for c in cells.values()]
    return dict(
        status="blocked" if blockers else "recorded",
        blockers=blockers,
        perspectives=len(profiles),
        elements_met=0,
        elements_partial=sum(c.get("status") == "partial" for c in cells_all),
        elements_unmet=sum(c.get("status") == "unmet" for c in cells_all),
        notice=NOTICE,
    )
