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

### Post-Rebase Reconciliation onto `origin/feat/demo-233-same-home-tensions-0825` (`f52679aff`)

* Related phase or task: `P01-T01`, `P01-T02`
* Files: `docs/reference/README.md`, `docs/reference/log.md`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `src/api/src/zava_forward/api/web/panels.js`, `src/api/tests/test_housing_resident_wcag_232.py`
* What changed and why: Rebased `feat/ux-151-wcag-baseline` onto `origin/feat/demo-233-same-home-tensions-0825` (`f52679affff4b15b4bbdf6995ab530d6aca10c96`) after stacked PRs `#1786` (`#232`), `#1789` (`#159`), and `#1776` (`#130`) merged into the parent topic branch. Resolved rebase conflicts in `docs/reference/README.md`, `docs/reference/log.md`, `docs/reference/research/ux/wcag-conformance-baseline.md`, and `src/api/src/zava_forward/api/web/panels.js` so `#232`'s `residentPanel` `.table-scroll` (`"aria-label": "Resident decisions by measure"`), `<th scope="row">`, and textual `panelCue`/`panelReadiness` cues, `#130`'s `nominationPanel._routeForm` / `_explanationView` (`aria-invalid` site count remains `9`), `#159`'s conversational assistant Chromium CDP AXTree and polite live-region audit entries, and `#151`'s `technicalPanel` and `financeQueueView` `.table-scroll` + `<th scope="row">` wrappers, 8-dimension workbench audit, and 15-table inventory coexist cleanly. Updated `src/api/tests/test_housing_resident_wcag_232.py` (`test_static_shell_css_and_table_guards_hold`) from `self.assertEqual(tables, 14)` to `self.assertEqual(tables, 15)` to reflect `#151` adding `<caption class="sr-only">` to `sensorTable` in `ops.js`.
* Completion evidence: Clean rebase atop `f52679affff4b15b4bbdf6995ab530d6aca10c96` and zero failures across `src-ci.yml` parity checks and cross-PR `#151`/`#149`/`#232`/`#159`/`#130` suites.
* Validation: Passed (`ruff check .`, `ruff format --check .`, `mypy` across 298 source files, `55`-test combined parity suite, `74`-test `#130`/journey/content suite, `150`-test `*wcag*` suite, and `55`-test `epic149` suite).

## Implementation-Time Plan and Detail Updates

* none

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m ruff format --isolated --line-length 100 --check` | `test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`, `test_epic149_landmarks_skip_link_focus_order.py` | Passed | `3 files already formatted` (exit `0`) |
| `(cd src/api && python3 -m ruff check .)` | Full `src/api` `src-ci.yml` lint check | Passed | `All checks passed!` (exit `0`) |
| `(cd src/api && python3 -m ruff format --check .)` | Full `src/api` `src-ci.yml` format check (respecting `pyproject.toml` excludes without explicit excluded paths) | Passed | `214 files already formatted` (exit `0`) |
| `(cd src/api && python3 -m mypy)` | Full `src/api` `src-ci.yml` type check (`pyproject.toml` sets `mypy_path = ["src", "tests", "../core/src", "../core/tests"]`) | Passed | `Success: no issues found in 298 source files` (exit `0`; note: passing `MYPYPATH=../core/src:../agents/src` overrides installed untyped `zava-forward-agents` and flags `# type: ignore[import-untyped]` in `tests/test_ai_consumption_api.py:24-25` as `unused-ignore`) |
| `unittest` (`test_wcag_workbench_baseline_151.py`, `test_accessibility_baseline.py`, `test_epic149_landmarks_skip_link_focus_order.py`, `test_epic149_form_error_summary_associations.py`, `test_housing_resident_wcag_232.py`, `test_assistant_panel_a11y_159.py`) | Combined `#151`, `#149`, `#232`, and `#159` accessibility regression suites (including Chromium CDP AXTree) | Passed | `Ran 55 tests in 8.923s - OK` |
| `unittest` (`test_nomination_screen.py`, `test_nomination_api_routes.py`, `test_case_journey.py`, `test_content_standard.py`) | `#130` nomination dual-route/keyboard/Playwright, case journey, and plain-language guards | Passed | `Ran 74 tests in 13.943s - OK` |
| `unittest` (`test_*wcag*.py`) | All 19 role-screen and workbench WCAG suites in `src/api/tests` | Passed | `Ran 150 tests in 12.061s - OK` |
| `unittest` (`test_epic149_*.py`) | All Epic `#149` suites including `test_epic149_form_error_summary_associations.py` | Passed | `Ran 55 tests in 88.609s - OK` |

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
* Validation coverage: `ruff check .`, `ruff format --check .` (214 files), `mypy` (298 files), combined `#151`/`#149`/`#232`/`#159` WCAG suite (55), `#130`/journey/content suite (74), all 19 `*wcag*` suites (150), and all `epic149` suites (55) passed
* Blockers: none
* Current plan and detail updates: Checked `P01`, `P01-T01`, `P01-T02` and marked Phase Index `completed`
* Planning and critique state: ready (`Pass` critique with `0` findings)
* Follow-up items: standalone `/law.html` skip link, Web Interface Guidelines polish (`RV-001`), and human AT/zoom walkthroughs + CI live-browser probes (`#155`)
* Review readiness or no-handoff reason: ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
