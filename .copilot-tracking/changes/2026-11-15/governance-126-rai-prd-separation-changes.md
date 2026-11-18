<!-- markdownlint-disable-file -->
# RPI Changes: Issue #126 RAI Closure and PRD Separation Slice

## Metadata

* Task ID: issue-126-rai-prd-separation
* Task slug: governance-126-rai-prd-separation
* Related plan: .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/governance-126-rai-prd-separation-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: none
* Status basis: All declared-scope phases and tasks (`P01`-`P03`) completed, reconciled, and verified against the focused validation suite with zero blockers.

## Execution Summary

Implemented the bounded Issue #126 RAI closure and PRD separation slice on `feat/governance-126-rai-prd-separation` (targeting `feat/demo-164-chat-grounding-provenance-0900`, PR #1641). Extended `src/core/src/zava_forward/core/governance.py` (`_rai_view` and `governance_view`) with detached, immutable `prd_quality_review` and `prd_owner_acceptance` projections plus structured `affected_dispatch`, `conditional_eu_assurance`, and `RAI_EU_CONDITIONAL` (`EU-COND-01`, `EU-COND-02`, `EU-COND-04`) applicability guards alongside `live_use`. Reconciled `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, and append-only `docs/reference/log.md` while preserving all historical versions and negative/insufficient outcomes. Proved all three contracts with focused JSON, SQLite, and repository documentation invariant tests in `src/core/tests/test_governance.py`.

## Completed Work

### Core Governance Register PRD Separation and Dispatch/EU Boundaries

* Related phase or task: `P01` (`P01-T01`, `P01-T02`)
* Files: `src/core/src/zava_forward/core/governance.py`
* What changed and why: Defined `RAI_EU_CONDITIONAL = ("EU-COND-01", "EU-COND-02", "EU-COND-04")`, `RAI_AFFECTED_DISPATCH`, `RAI_CONDITIONAL_EU_ASSURANCE`, `PRD_QUALITY_REVIEW`, and `PRD_OWNER_ACCEPTANCE` constants. Projected detached copies of `prd_quality_review` and `prd_owner_acceptance` in both `_rai_view` and `governance_view` without reading stored register overrides, exposed `affected_dispatch` and `conditional_eu_assurance` alongside `live_use` in `_rai_view`, and annotated each finding row with `conditional_eu` and `applicability_review` while preserving `NOT_ASSESSED` / `UNCHANGED` / `Open` / `Unknown` / `Not independently established` guards.
* Completion evidence: Direct source edits in `src/core/src/zava_forward/core/governance.py`.
* Validation: Passed JSON (`EvidenceRegister`), SQLite (`SqlEvidenceRegister`), and downstream HTTP API (`GovernanceEvidenceApi`, `JsonGovernanceEvidenceApi`) unit tests, plus `ruff check .`, `ruff format --check .`, and `python3 -m mypy` in `src/core`.

### Canonical Documentation, ADR 0002, Core Guide, and Knowledge Base Reconciliation

* Related phase or task: `P02` (`P02-T01`, `P02-T02`)
* Files: `docs/case_study_48_addendum.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `src/core/README.md`, `docs/reference/README.md`, `docs/reference/log.md`
* What changed and why: Added concise, dated (`2026-11-15`) Issue #126 reconciliation paragraphs across the addendum, unsigned `0.21.0` PRD, ADR 0002, `src/core/README.md`, and `docs/reference/README.md`, and appended one chronological `[2026-11-15] update` entry to `docs/reference/log.md`. Preserved all historical versions (`0.12.0`, `0.14.0`, `0.16.0`, unsigned `0.21.0`, baseline `1cb398c7b90bec05a5700008a97d0cfac494144a`) and negative/insufficient outcomes (`FAIL / Validate BLOCKED / Finalize NOT_EVALUATED`, `PARTIAL`, `NOT_ASSESSED`, `DOWNGRADED`, `INVALID_PAYLOAD`) with zero added tracking-directory strings.
* Completion evidence: Direct edits verified across all six target Markdown files; `docs/reference/log.md` diff confirmed strictly append-only at EOF.
* Validation: Passed `GovernanceDocumentationContractTests` (3 methods), `test_live_doc_links.py` (2 methods), `python3 tools/check-legacy-references.py` (`links: 0 violation(s) in 819 document(s)`), and `git diff` tracking-reference audit.

### Focused Runtime and Repository Documentation Invariant Tests and Validation

* Related phase or task: `P03` (`P03-T01`, `P03-T02`)
* Files: `src/core/tests/test_governance.py`, `src/core/README.md`
* What changed and why: Added 2 runtime contract test methods on `EvidenceRegister` (inherited by `SqlEvidenceRegister` and `MssqlEvidenceRegister`) verifying PRD review/owner-acceptance separation across 22/22 claims, closed-schema validation, governance actions, and raw stored-dict overrides, plus blocked live use, disabled affected dispatch, and conditional EU applicability guards across `EU-COND-01`, `EU-COND-02`, and `EU-COND-04`. Added `GovernanceDocumentationContractTests` (3 container-safe methods, 5 total added methods <= 8 ceiling, 0 removals) verifying synchronized contracts, preserved historical versions and negative/insufficient outcomes, append-only log structure, relative links and heading anchors, and absence of tracking-directory strings. During `P03-T02`, added explicit `report_acceptance_scope="baseline-assessment-and-remediation-planning only"` prose in `src/core/README.md` (local judgment / current-state reconciliation) so all four governance doc surfaces carry the exact acceptance-scope string.
* Completion evidence: 82 tests discovered in `test_governance.py` (`64` executed across JSON, SQLite, and repository doc suites, `18` opt-in MSSQL loopback tests skipped as expected in focused tier, `0` failures).
* Validation: All focused validation commands passed cleanly (recorded in `## Validation Record`).

## Implementation-Time Plan and Detail Updates

* Local judgment (`P03-T02`): Included explicit `report_acceptance_scope="baseline-assessment-and-remediation-planning only"` field prose in `src/core/README.md` alongside `separate_from_report_acceptance=True` so `core_readme` matches the addendum, PRD, and ADR 0002 contract wording directly; no plan structure, task scope, or acceptance criteria changed.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|---|---|---|---|
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_governance.py" -v` | `src/core` JSON, SQLite, and repository doc contracts | Passed | `Ran 82 tests in 13.867s — OK (skipped=18)` (18 opt-in MSSQL loopback tests skipped in focused tier) |
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p "test_live_doc_links.py" -v` | Live documentation relative links | Passed | `Ran 2 tests in 1.864s — OK` |
| `PYTHONPATH=src/api/src:src/api/tests:src/core/src:src/agents/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_governance_evidence_api.py" -v` | Downstream API payload compatibility | Passed | `Ran 10 tests in 10.084s — OK` |
| `cd src/core && python3 -m ruff check .` | `src/core` lint | Passed | `All checks passed!` |
| `cd src/core && python3 -m ruff format --check .` | `src/core` format check | Passed | `314 files already formatted` |
| `cd src/core && python3 -m mypy` | `src/core` type check | Passed | `Success: no issues found in 367 source files` |
| `python3 tools/check-legacy-references.py` & `git diff` audit | Repository links & diff hygiene | Passed | `links: 0 violation(s) in 819 document(s)`; zero added tracking-path references in `src/` or `docs/`; `docs/reference/log.md` strictly append-only at EOF |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02` all `[x]`)
* Completed-work evidence and handoff prose: Reconciled across `plan.md`, `changes.md`, and `state.json`
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active-plan markers)
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None in declared full-plan scope (`P01`-`P03` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/governance-126-rai-prd-separation-plan.md, `## Follow-Up Items`
* Remaining non-engineering human/live prerequisites on Issue #126 (real OD-18 definitions/MDE, real OD-36 DPIA/lawful-basis approval, real OD-35 restart authority appointment, real OD-51 budget-owner confirmation, fresh independent PRD quality review and human owner acceptance of PRD `0.21.0`, qualified EU applicability review, and live pilot phase release gates) remain outside engineering scope.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`-`P03`), completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`; remaining: none
* Validation coverage: Focused tier passed (`test_governance.py` 82 tests / 18 opt-in MSSQL skipped, `test_live_doc_links.py` 2 tests, `test_governance_evidence_api.py` 10 tests, `ruff check .`, `ruff format --check .`, `python3 -m mypy`, `check-legacy-references.py` 0 link violations, `git diff` hygiene audit)
* Blockers: None
* Current plan and detail updates: Local judgment prose alignment in `src/core/README.md` (`report_acceptance_scope`); no plan/detail structural change
* Planning and critique state: Ready (`PC-001`-`PC-004` directly resolved in plan/details)
* Follow-up items: Non-engineering Issue #126 human/live prerequisites retained outside scope
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Parent confirmed automatic RPI Agent
