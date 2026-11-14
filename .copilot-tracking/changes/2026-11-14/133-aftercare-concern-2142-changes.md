<!-- markdownlint-disable-file -->
# RPI Changes: Issue #133 Aftercare Accessible Concern Routes and Neutral-Text Enforcement in src/core

## Metadata

* Task ID: 133-aftercare-concern-2142
* Related plan: .copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/133-aftercare-concern-2142-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: none
* Status basis: Full plan (`P01` through `P03`) completed, reconciled, and verified by Focused-tier checks including bare `mypy`, `ruff`, and `unittest discover` in `src/core`.

## Execution Summary

Delivered the two locally verifiable acceptance criteria for Issue #133 in `src/core`:
1. Accessible concern raising for households and representatives across both self-service digital routes (`household_form`, `submit_household_concern`, `household_receipt` on `/api/aftercare/household-*`) and staff-recorded non-digital channels (`phone`, `in_person`, `paper`, `assisted_visit`), with optional non-gatekept `support_needed` communication/visit adjustments (`SUPPORT_OPTION_CODES`), plain-language per-field and summary error messages (`intake_error_summary`), cross-UTC-midnight idempotent replay, and full legacy `zf-aftercare-intake/1` snapshot and SHA-256 fingerprint compatibility.
2. End-to-end neutral-text enforcement across `aftercare.py`, `aftercare_intake.py`, and `aftercare_store.py`, blocking literal phrases, invisible/full-width/hyphen/newline evasions, causal/blame/savings paraphrases, and second-clause injections after uncertainty or negation clauses without echoing rejected text, while preserving resident and representative verbatim `statement` and `representative_basis` unchanged.

## Completed Work

### P01: Harden Neutral-Text Guard and Accessible Register Contract in aftercare.py

* `P01-T01`: Hardened `_variants`, `_UNCERTAIN`, `_NEGATED_CLAIM`, `PARAPHRASE_PATTERNS`, `neutral_text` (non-echoing `ValueError` with `@lru_cache(maxsize=512)` on `_check_neutral`), `strip_unsafe_sentences` (splitting across newlines and punctuation), `assert_templates_neutral` over all module templates, and `neutral_text` checks on `owner` and `sensor_context` keys and values in `raise_concern`, `record_closure`, and `from_state`.
* `P01-T02`: Added `SUPPORT_OPTIONS` (`SUPPORT_OPTION_CODES`), `normalize_support_needed` (accepting `None`, comma-separated strings, and sequences), optional `support_needed` field in `intake_form()` and `intake_errors()`, `intake_error_summary()`, and backward-compatible `support_needed` storage and `from_state()` restoration on `AftercareRegister`.

### P02: Add Accessible Household Digital Intake, Support Adjustments, and Template Guards in aftercare_intake.py and aftercare_store.py

* `P02-T01`: Added `household_form()`, `submit_household_concern()`, and `household_receipt()` plus `/api/aftercare/household-form`, `POST /api/aftercare/household-concerns`, and `GET /api/aftercare/household-concerns/<cid>?request_id=...` routes to `AftercareService`, with cross-UTC-midnight replay resolution (`PC-001`), safe legacy snapshot defaults (`PC-003`), verbatim household statement/representative-basis preservation, and household-safe readback omitting sensor context and audit history.
* `P02-T02`: Registered all fixed service and store strings across `aftercare_intake.py` and `aftercare_store.py` with `assert_templates_neutral(...)` at import time and wrapped dynamic formatted strings and error messages with `neutral_text(...)` at runtime.

### P03: Worktree Test Resolution, Focused AC1/AC5 Tests, Documentation, and Bare Verification

* `P03-T01`: Created `src/core/tests/aftercare_fixture.py` (`CORE_SRC`, `ensure_worktree_src`) so bare `unittest discover` in `src/core` deterministically resolves worktree `src/core/src` ahead of any external `.pth` install (`PC-004`). Added 9 focused test methods (within the locked `<= 14` budget, `0` removals): 4 in `src/core/tests/test_aftercare.py`, 4 in `src/core/tests/test_aftercare_intake.py`, and 1 in `src/core/tests/test_aftercare_store.py`.
* `P03-T02`: Updated `## Aftercare concern route and evaluator view (#133)` in `src/core/README.md` with accurate module capabilities and explicit "Not delivered" human/UI/governance boundaries, and executed Focused-tier local checks.

## Implementation-Time Plan and Detail Updates

* Local judgment (`aftercare.py`): Added `@lru_cache(maxsize=512)` on internal pure helper `_check_neutral(text: str) -> None` so repeated `AftercareRegister.from_state` owner/template neutrality checks run without redundant regex overhead during 1000-record snapshot and store contract tests. Preserved `SUPPORT_OPTIONS` union (`large_print`, `easy_read`, `interpreter`, `bsl`, `callback_window`, `paper_letter`, `support_person`) so both communication formats and trusted-person visit support are available.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` (bare in `src/core`) | 308 source files in `src/core` | Passed | `Success: no issues found in 308 source files` |
| `python3 -m ruff check .` (in `src/core`) | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` (in `src/core`) | `src/core` | Passed | `255 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*aftercare*.py' -v` (bare in `src/core`) | `test_aftercare.py` (39), `test_aftercare_intake.py` (50), `test_aftercare_store.py` (43 incl. 15 opt-in MSSQL skips) | Passed | `Ran 132 tests in 170.196s — OK (skipped=15)` |
| `python3 -m unittest discover -s tests -p 'test_dependency_rule.py' -q` (in `src/core`) | `src/core` dependency boundary | Passed | `Ran 2 tests in 2.559s — OK` |
| `PYTHONPATH=../core/src:../agents/src:src python3 -m unittest discover -s tests -p 'test_aftercare_screen.py' -q` (in `src/api`) | Downstream `aftercare.js` screen compatibility | Passed | `Ran 17 tests in 0.892s — OK` |
| Hosted CI workflows | GitHub Actions | Unavailable locally | Local-only task commit (`Do NOT push`); hosted CI runs only after push/PR |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P02`, `P03` and all `P01-T01`..`P03-T02` markers checked with matching evidence)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled (Focused validation tier per repository D4/#1294 rules: pure `src/core` Python logic, tests, and README with zero SQL schema, infra, workflow, Dockerfile, or dependency-manifest changes)
* Review readiness: ready for single-pass `rpi-review`

## Blockers

* none

## Remaining Work

* none (all active plan items `P01`, `P02`, and `P03` complete)

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/133-aftercare-concern-2142-plan.md, `## Follow-Up Items`
* Obtain assistive-technology and WCAG 2.2 AA acceptance evidence on a served resident-facing UI wired to `/api/aftercare/household-form` and `/api/aftercare/household-concerns` (outside `src/core`-only scope; owned by follow-up UI/UX slice on #133).
* Resolve evaluator role authorization and Data Protection Officer lawful-basis sign-off on outcome data (open governance dependencies on Issue #133).
* Deliver a served human-review screen and approved release evidence before enabling any model binding for `aftercare-concern-pack` (`FR-036`, Issue #133 AC6).

## Return-to-Caller State

* Implementation execution status: Complete (full plan `P01`–`P03`)
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`; remaining: none
* Validation coverage: Focused tier passed (`mypy`, `ruff check`, `ruff format --check`, 132 bare `test_*aftercare*.py` unit/contract tests with 15 opt-in MSSQL skips, `test_dependency_rule.py`, and `src/api/tests/test_aftercare_screen.py`)
* Blockers: none
* Current plan and detail updates: Local `@lru_cache` judgment on `_check_neutral` recorded above; review-ready for automatic parent transition to `Review`
* Planning and critique state: implementation-ready (`PC-001` through `PC-004` applied)
* Follow-up items: 3 external governance/UI follow-ups tracked in plan
* Review readiness or no-handoff reason: not ready; implementation starting at `P01-T01`
* Continuation owner: confirmed automatic RPI Agent parent
