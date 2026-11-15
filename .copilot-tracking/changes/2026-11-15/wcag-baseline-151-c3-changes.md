<!-- markdownlint-disable-file -->
# RPI Changes: Focused Cycle 3 Safety-Screen Table Header Remediation for PR #1802 (#151)

## Metadata

* Task ID: 2026-11-15-wcag-baseline-151-c3
* Related plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-c3-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete (full plan)
* Declared invocation scope: Full plan (`P01`, `P01-T01`, `P01-T02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`
* All remaining active-plan markers: none
* Status basis: Both `P01-T01` (`src/api/tests/test_safety_screens.py` table header and alignment assertions) and `P01-T02` (`65` unit tests across `6` modules, `ruff check .`, `ruff format --check .`, and strict `mypy`) completed and exited `0` with Cycle 1 and Cycle 2 tracking files untouched.

## Execution Summary

Implemented Option 2 across `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` so `<thead>` `<th scope="col">` column headers and `<tbody>` leading `<th scope="row">` row headers plus `<td>` data cells are verified across both `safety-lead` and `hazard-triage` home and cross-home summary views. All `65` tests across the six required `unittest` suites passed, and `ruff check .`, `ruff format --check .` (`214` files), and `mypy` (`298` source files) passed with zero diagnostics.

## Completed Work

### Update SafetyScreens Table Header and Column Alignment Assertions

* Related phase or task: `P01-T01` (within `P01`)
* Files: `src/api/tests/test_safety_screens.py`
* What changed and why: Replaced the table-wide `find_all(table, "th")` query in `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` with separate `(thead,) = find_all(table, "thead")` (`heads = find_all(thead, "th")`, `scope == "col"`) and `(tbody,) = find_all(table, "tbody")` (`rows = find_all(tbody, "tr")`) checks asserting each `<tbody>` row starts with a single `<th scope="row">` carrying non-empty stripped `string_leaves` text followed by `<td>` cells (`row["kids"][1:] == tds`) summing to `len(heads)`. This aligns the safety-screen unit suite with `screenTable(..., rowHeader = true)` (`role-screens.js`), WCAG 2.2 SC 1.3.1, `test_wcag_workbench_baseline_151.py`, and `docs/reference/research/ux/wcag-conformance-baseline.md`.
* Completion evidence: Surgical update in `src/api/tests/test_safety_screens.py` (`test_rendered_tables_are_labelled_focusable_and_aligned`).
* Validation: Passed (`python3 -m unittest tests/test_safety_screens.py -q` ran `14` tests in `0.983s`, `OK`; `python3 -m ruff format --check tests/test_safety_screens.py` reported `1 file already formatted`).

### Execute Focused Unittest, Ruff, and Mypy Validation

* Related phase or task: `P01-T02` (completing `P01`)
* Files: `src/api/tests/test_safety_screens.py` (verified alongside `src/api`)
* What changed and why: Executed the full caller-specified Focused validation tier (`6` `unittest` modules plus `ruff check .`, `ruff format --check .`, and strict `mypy` in `src/api`) without running `tools/rpi-checks.py`, and verified `git status --short` leaves historical Cycle 1 and Cycle 2 `.copilot-tracking/` artifacts untouched.
* Completion evidence: Validation Record below.
* Validation: Passed (`65` unit tests `OK`; `ruff check .` `All checks passed!`; `ruff format --check .` `214 files already formatted`; `mypy` `Success: no issues found in 298 source files`).

## Implementation-Time Plan and Detail Updates

### Clarify Exact Test Count in Phase Details Validation Expectation

* Affected plan area or markers: `P01-T01` in `.copilot-tracking/details/2026-11-15/wcag-baseline-151-c3-phase-details.md`
* What changed: Updated `P01-T01` validation expectation wording from `12 tests` to `14 tests` in `test_safety_screens.py`.
* Why: Direct execution of `python3 -m unittest tests/test_safety_screens.py -q` runs `14` test methods (`65` total across the `6` suites remains exact).
* Triggering evidence: `Ran 14 tests in 0.983s — OK`.
* User answer or decision: none (factual target clarification under immediately relevant update rule)
* Reconciliation performed: Updated `P01-T01` in `wcag-baseline-151-c3-phase-details.md` and `P01` status to `completed`; plan sections already cited the exact `65`-test aggregate.
* Planning and critique state: Not needed (preserves approved intent and locked test bounds).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m unittest tests/test_safety_screens.py -q` | `src/api/tests/test_safety_screens.py` | Passed | `Ran 14 tests in 0.983s — OK` |
| Focused `unittest` (`test_safety_screens.py`, `test_wcag_workbench_baseline_151.py`, `test_accessibility_baseline.py`, `test_epic149_landmarks_skip_link_focus_order.py`, `test_housing_resident_wcag_232.py`, `test_role_screens.py`) | `src/api/tests/` (`6` modules) | Passed | `Ran 65 tests in 3.746s — OK` |
| `python3 -m ruff check .` | `src/api` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/api` | Passed | `214 files already formatted` |
| `python3 -m mypy` | `src/api` (`src`, `tests`, `checks`) | Passed | `Success: no issues found in 298 source files` |
| `tools/rpi-checks.py` | Repository gate | Skipped | Explicitly prohibited by caller instructions (`Focused` validation tier) |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, and `P01-T02` marked `[x]` in `wcag-baseline-151-c3-plan.md`; `P01` marked `completed` in `wcag-baseline-151-c3-phase-details.md`)
* Completed-work evidence and handoff prose: Current
* Validation, blockers, remaining work, and follow-up items: Current (`0` blockers, `0` remaining active-plan markers, `3` canonical follow-ups preserved)
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* None.

## Remaining Work

* None within declared full-plan scope (`P01`, `P01-T01`, `P01-T02` all complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md, `## Follow-Up Items`
* Add a `.skip-link` bypass anchor and polite status region to standalone `/law.html` (and shrink `NO_SKIP_LINK` to `set()`) if `/law.html` enters workbench conformance scope (outside immediate `c3` remediation scope; owner: follow-up UX cycle).
* Apply optional Web Interface Guidelines typography and locale polish (`RV-001` from Cycle 1: `tabular-nums`, `Intl.NumberFormat` in `bars()`, `<meta name="theme-color">`) (outside immediate `c3` remediation scope; owner: follow-up UX polish task).
* Execute human assistive-technology and browser zoom walkthroughs (`NVDA`, `VoiceOver`, `200%` text resize, `400%` reflow), record owner confirmation `O-1`, and integrate rendered Playwright / axe-core CI probes (`#155`, `#619`) (human-owned and CI probe follow-up).

## Return-to-Caller State

* Implementation execution status: Complete (full plan)
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P01-T02`; remaining: `none`
* Validation coverage: Focused `unittest` (`65` tests across `6` suites `OK`), `ruff check .` (`Passed`), `ruff format --check .` (`214` files `Passed`), and strict `mypy` (`298` files `Passed`); `tools/rpi-checks.py` skipped per caller constraint
* Blockers: none
* Current plan and detail updates: Clarified `14` tests in `test_safety_screens.py` in `P01-T01` phase details (`65` aggregate unchanged)
* Planning and critique state: Ready (`Pass` in `.copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-c3-plan-critique.md`)
* Follow-up items: 3 canonical items mirrored from plan
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: Parent confirmed automatic RPI Agent (`c3`)
