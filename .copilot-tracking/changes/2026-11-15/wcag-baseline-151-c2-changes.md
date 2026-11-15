<!-- markdownlint-disable-file -->
# RPI Changes: Focused Cycle 2 Correction for Workbench WCAG 2.2 Baseline (#151)

## Metadata

* Task ID: 2026-11-15-wcag-baseline-151-c2
* Related plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-c2-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`
* All remaining active-plan markers: none
* Status basis: Completed shrink-only `NO_SKIP_LINK` update in `test_epic149_landmarks_skip_link_focus_order.py`, formatted `test_accessibility_baseline.py` and `test_wcag_workbench_baseline_151.py` with `ruff format --isolated --line-length 100` while preserving `"self.assertEqual(sites, 9,"`, and verified all targeted and coupled `unittest`, `ruff`, and `mypy` checks.

## Execution Summary

Delivered the focused Cycle 2 (`c2`) correction for issue `#151` (`rev-151-wcag` finding) on `feat/ux-151-wcag-baseline`. Shrank `NO_SKIP_LINK` from `{"/", "/law.html"}` to `{"/law.html"}` in `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` so `SkipLink.test_skip_link_gaps_are_recorded_and_shrink_only` enforces the `/` welcome page `.skip-link` added in Cycle 1 (`d15acc57a`). Bound `invalid_msg` in `src/api/tests/test_accessibility_baseline.py` so `"self.assertEqual(sites, 9,"` stays on one line under `100` columns (preserving `test_epic149_form_error_summary_associations.py`), formatted `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py` with `python3 -m ruff format --isolated --line-length 100`, and confirmed green execution across all targeted `unittest`, `ruff`, and `mypy` suites.

## Completed Work

### Shrink-Only NO_SKIP_LINK Alignment and Isolated 100-Column Formatting

* Related phase or task: `P01-T01`
* Files: `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_wcag_workbench_baseline_151.py`
* What changed and why: Updated `NO_SKIP_LINK = {"/law.html"}` in `test_epic149_landmarks_skip_link_focus_order.py` now that `welcome.html` (`/`) serves `<a class="skip-link" href="#welcome-main">Skip to main content</a>`; assigned `invalid_msg` before `self.assertEqual(sites, 9, invalid_msg)` in `test_accessibility_baseline.py` so `test_epic149_form_error_summary_associations.py` continues to match `"self.assertEqual(sites, 9,"`; ran `python3 -m ruff format --isolated --line-length 100` on `test_accessibility_baseline.py` and `test_wcag_workbench_baseline_151.py`.
* Completion evidence: `ruff format --isolated --line-length 100 --check` reports `3 files already formatted`.
* Validation: Passed (`test_epic149_landmarks_skip_link_focus_order.py`, `test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`, `test_epic149_form_error_summary_associations.py`).

### Targeted and Coupled Validation Verification

* Related phase or task: `P01-T02`
* Files: `src/api/tests/` and `src/api/src/`
* What changed and why: Executed all four caller-requested commands alongside coupled `test_epic149_*.py` modules, `ruff format --isolated --line-length 100 --check`, and `mypy`, and verified Cycle 1 `.copilot-tracking/` artifacts remain unmodified.
* Completion evidence: Zero failures or errors across all commands.
* Validation: Passed (`14` + `6` + `14` + `55` unit tests, `ruff check`, `ruff format --check`, `mypy`).

## Implementation-Time Plan and Detail Updates

* none

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m ruff format --isolated --line-length 100 --check` | `test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`, `test_epic149_landmarks_skip_link_focus_order.py` | Passed | `3 files already formatted` (exit `0`) |
| `unittest` (`test_epic149_landmarks_skip_link_focus_order.py`) | Landmarks, shrink-only `NO_SKIP_LINK`, focus, reduced motion, forced colours | Passed | `Ran 14 tests in 2.773s - OK` |
| `unittest` (`test_wcag_workbench_baseline_151.py`) | `#151` Node-VM DOM accessible equivalents and 8-dimension baseline invariants | Passed | `Ran 6 tests in 0.164s - OK` |
| `unittest` (`test_accessibility_baseline.py`) | `#151` static token contrast, target-size, table, and error-site invariants | Passed | `Ran 14 tests in 0.068s - OK` |
| `unittest` (`test_epic149_*.py`) | All Epic `#149` suites including `test_epic149_form_error_summary_associations.py` | Passed | `Ran 55 tests in 85.715s - OK` |
| `(cd src/api && python3 -m ruff check src tests)` | `src/api` source and test lint | Passed | `All checks passed!` (exit `0`) |
| `(cd src/api && python3 -m mypy src tests/test_epic149_landmarks_skip_link_focus_order.py tests/test_wcag_workbench_baseline_151.py tests/test_accessibility_baseline.py)` | Static type checking | Passed | `Success: no issues found in 31 source files` (exit `0`) |

## Pre-Review Reconciliation

* Plan markers and phase details: aligned (`P01`, `P01-T01`, `P01-T02` checked `[x]`; Phase Index `completed`)
* Completed-work evidence and handoff prose: aligned
* Validation, blockers, remaining work, and follow-up items: aligned
* Review readiness: ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c2-plan.md, `## Follow-Up Items`
* Add a `.skip-link` bypass anchor and polite status region to standalone `/law.html` (and shrink `NO_SKIP_LINK` to `set()`) if `/law.html` enters workbench conformance scope.
* Apply optional Web Interface Guidelines typography and locale polish (`RV-001` from Cycle 1: `tabular-nums`, `Intl.NumberFormat` in `bars()`, `<meta name="theme-color">`).
* Execute human assistive-technology and browser zoom walkthroughs (`NVDA`, `VoiceOver`, `200%` text resize, `400%` reflow), record owner confirmation `O-1`, and integrate rendered Playwright / axe-core CI probes (`#155`, `#619`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`); completed: `P01`, `P01-T01`, `P01-T02`; remaining: none
* Validation coverage: `ruff format --isolated --line-length 100 --check`, `test_epic149_landmarks_skip_link_focus_order.py` (14), `test_wcag_workbench_baseline_151.py` (6), `test_accessibility_baseline.py` (14), `test_epic149_*.py` (55), `ruff check src tests`, and `mypy` (31 files) all passed
* Blockers: none
* Current plan and detail updates: Checked `P01`, `P01-T01`, `P01-T02` and marked Phase Index `completed`
* Planning and critique state: ready (`Pass` critique with `0` findings)
* Follow-up items: standalone `/law.html` skip link, Web Interface Guidelines polish (`RV-001`), and human AT/zoom walkthroughs + CI live-browser probes (`#155`)
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
