<!-- markdownlint-disable-file -->
# RPI Plan: Focused Cycle 3 Safety-Screen Table Header Remediation for PR #1802 (#151)

## Task Metadata

* Task ID: 2026-11-15-wcag-baseline-151-c3
* Task slug: wcag-baseline-151-c3
* Parent task: 2026-11-15-wcag-baseline-151-c2 (`wcag-baseline-151-c2`)
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-c3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-c3-plan-critique.md

## Executive Summary

This focused Cycle 3 (`c3`) plan resolves the single `src-api` CI failure (`1` of `3,612` tests) on `PR #1802` (`feat/ux-151-wcag-baseline`) for GitHub issue `#151`: `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py`. Cycle 1 changed `screenTable(..., rowHeader = true)` in `src/api/src/zava_forward/api/web/role-screens.js` so every specialist data table emits `<th scope="row">` for its row-identifying first cell in `<tbody>` alongside `<th scope="col">` column headers in `<thead>`. Because `test_safety_screens.py` queried `find_all(table, "th")` across both `<thead>` and `<tbody>` and expected every `<th>` to carry `scope="col"` and every `<tbody>` cell to be a `<td>`, that assertion failed. Based on completed `c3` research, Option 2 is selected: update `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` to verify `<thead>` `<th scope="col">` headers and `<tbody>` leading `<th scope="row">` plus `<td>` alignment matching `len(heads)`, preserving WCAG 2.2 SC 1.3.1 row headers on the 10-, 6-, and 13-column safety tables as well as `test_wcag_workbench_baseline_151.py` and `docs/reference/research/ux/wcag-conformance-baseline.md`.

### User Decisions and Requirements Highlights

* Remediate `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` using Option 2 (`thead` `th[scope="col"]` and `tbody` `<th scope="row">` + `<td>` cells matching `len(heads)`).
* Validate under the Focused tier without running `tools/rpi-checks.py`: execute `test_safety_screens.py`, `test_wcag_workbench_baseline_151.py`, `test_accessibility_baseline.py`, `test_epic149_landmarks_skip_link_focus_order.py`, `test_housing_resident_wcag_232.py`, and `test_role_screens.py`, followed by `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)`.
* Persist full dated `c3` `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `changes`, `reviews/plans`, `reviews/logs`) while leaving Cycle 1 and Cycle 2 artifacts intact, and commit locally on `feat/ux-151-wcag-baseline` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.

### What You May Not Know

* Candidate Option 1 (reverting `rowHeader = false` in `src/api/src/zava_forward/api/web/role-screens.js`) would crash the Node-VM runtime assertion in `src/api/tests/test_wcag_workbench_baseline_151.py`, which invokes `screenTable("Ready homes", ["Home", "Stage"], [["ZF-1", "Design"]])` with default arguments and reads `specialist.querySelector("tbody").querySelector("th").getAttribute("scope")`, and would contradict `docs/reference/research/ux/wcag-conformance-baseline.md` where all 15 table builders are documented as emitting `<th scope="row">`.
* All three safety-screen tables (`Hazard referrals for this home`, `Scoped pause and release evidence`, and `Hazard referrals by home`) place a unique item or home-and-item identifier (`H-1`, `C-1 H-1`, `C-9`, `C-3`, `C-4`) in column `0`, so asserting `<th scope="row">` in `test_safety_screens.py` aligns it with the ten peer specialist WCAG suites and `src/api/checks/role_screens_browser_check.py`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Work in `/home/azureuser/source/ama-demo-wt/feat-151-wcag-baseline` on branch `feat/ux-151-wcag-baseline` (`PR #1802`, based on `origin/feat/demo-233-same-home-tensions-0825`) for Issue `#151` (`c3` remediation) (user prompt).
* Resolve the `src-api` CI failure in `src/api/tests/test_safety_screens.py` (`SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned`) by selecting Option 2: inspect `thead` `th` (`scope="col"`) and `tbody` `<th scope="row">` + `<td>` cells matching `len(heads)` (user prompt; `.copilot-tracking/research/2026-11-15/wcag-baseline-151-c3-research.md`).
* Run the Focused validation tier only (`test_safety_screens.py`, `test_wcag_workbench_baseline_151.py`, `test_accessibility_baseline.py`, `test_epic149_landmarks_skip_link_focus_order.py`, `test_housing_resident_wcag_232.py`, and `test_role_screens.py`, plus `ruff check .`, `ruff format --check .`, and `mypy` in `src/api`); do NOT run `tools/rpi-checks.py` (user prompt).
* Write dated `c3` RPI artifacts under `.copilot-tracking/` (`research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `changes/2026-11-15/`, `reviews/logs/2026-11-15/`, and `reviews/plans/2026-11-15/`) preserving historical Cycle 1 and Cycle 2 artifacts (user prompt; `.github/copilot-instructions.md`).
* Commit all changes and `.copilot-tracking/` `c3` artifacts locally on `feat/ux-151-wcag-baseline` with trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and do NOT push (user prompt).

## Goals

* Update `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` to assert `<thead>` `<th scope="col">` headers and `<tbody>` leading `<th scope="row">` plus `<td>` cell alignment across both rendered home and cross-home summary views.
* Confirm green execution across all six target `unittest` suites plus full `ruff check .`, `ruff format --check .`, and `mypy` in `src/api`.
* Record complete `c3` RPI artifacts and create a clean local commit on `feat/ux-151-wcag-baseline` without pushing.

## Scope and Non-Goals

### In Scope

* Updating `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py`.
* Running the six required `src/api/tests/` modules and `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)`.
* Authoring `c3` `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, and `rpi-sessions`) and committing locally with privacy-safe repository-local Git identity and the Copilot trailer.

### Non-Goals

* Modifying `src/api/src/zava_forward/api/web/role-screens.js` or any other web asset or knowledge-base document.
* Running `tools/rpi-checks.py` or browser harness scripts.
* Modifying historical Cycle 1 or Cycle 2 `.copilot-tracking/` artifacts, or pushing commits to a remote.

## Functional Requirements

* `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` must inspect `<thead>` `<th>` cells (`scope="col"`) separately from `<tbody>` rows, verifying that each `<tbody>` `<tr>` starts with `<th scope="row">` (containing non-empty text) followed by `<td>` cells such that `1 + len(tds) == len(heads)`.
  * Observable acceptance criteria: `(cd src/api && PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest tests/test_safety_screens.py tests/test_wcag_workbench_baseline_151.py tests/test_accessibility_baseline.py tests/test_epic149_landmarks_skip_link_focus_order.py tests/test_housing_resident_wcag_232.py tests/test_role_screens.py -q)` passes all 65 tests with `0` failures.

## Non-Functional Requirements

* Static lint, formatting, type safety, and historical evidence integrity
  * Objective threshold or evaluation condition: `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` exits `0`, and `git status --short` shows zero modifications to Cycle 1 or Cycle 2 `.copilot-tracking/` files.
  * Observable acceptance criteria: Zero Ruff lint/format diagnostics, zero Mypy errors across `src/api`, and untouched Cycle 1 / Cycle 2 tracking files.

## Acceptance Criteria

* `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` asserts `<thead>` `<th scope="col">` headers and `<tbody>` leading `<th scope="row">` (non-empty text) + `<td>` cells matching `len(heads)`.
* The six-module `unittest` suite (`test_safety_screens.py`, `test_wcag_workbench_baseline_151.py`, `test_accessibility_baseline.py`, `test_epic149_landmarks_skip_link_focus_order.py`, `test_housing_resident_wcag_232.py`, `test_role_screens.py`) passes completely.
* `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` passes with exit code `0`.
* Dated `c3` `.copilot-tracking/` artifacts exist under `research/2026-11-15/`, `plans/2026-11-15/`, `details/2026-11-15/`, `changes/2026-11-15/`, `reviews/plans/2026-11-15/`, and `reviews/logs/2026-11-15/`, and all changes are committed locally on `feat/ux-151-wcag-baseline` with `Refs #151, #119` and the Copilot trailer without pushing.

## Locked Test Ownership and Bounds

* Canonical test targets:
  * `src/api/tests/test_safety_screens.py` (update `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned`; `0` test removals, `0` new test methods, `0` new test files)
* Exact test removals: `none`
* Maximum test additions: `0` new test files, `0` new test methods
* Generated targets: `none`
* Semantic-versus-regression coverage: Semantic verification of WCAG 2.2 SC 1.3.1 `<thead>` `<th scope="col">` and `<tbody>` leading `<th scope="row">` + `<td>` column-count alignment across `safety-lead` and `hazard-triage` home and summary views, paired with regression execution of `test_wcag_workbench_baseline_151.py`, `test_accessibility_baseline.py`, `test_epic149_landmarks_skip_link_focus_order.py`, `test_housing_resident_wcag_232.py`, and `test_role_screens.py`.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/wcag-baseline-151-c3-phase-details.md |
| Latest critique | `Pass` (`0` findings) in .copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-c3-plan-critique.md |
| Relevant research | .copilot-tracking/research/2026-11-15/wcag-baseline-151-c3-research.md (`C1`-`C10`, `W1`) |
| Changes-record role | .copilot-tracking/changes/2026-11-15/wcag-baseline-151-c3-changes.md (`Complete` across `P01`, `P01-T01`, `P01-T02`) |
| Planning execution and readiness | Complete and implementation-ready (`Pass`) |
| Continuation context | Confirmed automatic RPI Agent child loop (`c3`) |

## Sources

* .copilot-tracking/research/2026-11-15/wcag-baseline-151-c3-research.md: Cycle 3 research synthesis comparing Option 1 and Option 2 (`C1`-`C10`, `W1`).
* src/api/tests/test_safety_screens.py: Safety and hazard triage specialist screen unit tests.
* src/api/src/zava_forward/api/web/role-screens.js: Shared `screenTable` helper (`rowHeader = true`) and `safety-lead` / `hazard-triage` screen definitions.
* src/api/tests/test_wcag_workbench_baseline_151.py: Cycle 1 deterministic Node-VM and static verification suite asserting `screenTable` default `scope="row"`.
* docs/reference/research/ux/wcag-conformance-baseline.md: Workbench WCAG 2.2 baseline record documenting `<th scope="col">` and `<th scope="row">` across all 15 table builders.
* src/api/pyproject.toml: Ruff (`line-length = 100`) and strict Mypy configuration covering `tests/test_safety_screens.py`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Align Safety-Screen Table Header Test Assertions and Run Focused Validation

* Intent: Update `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` for `<th scope="col">` + `<th scope="row">` table semantics and run the full Focused validation suite (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`).
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update SafetyScreens table header and column alignment assertions

* Intent: Inspect `<thead>` `<th scope="col">` headers and `<tbody>` leading `<th scope="row">` (with non-empty text) plus `<td>` cells matching `len(heads)` in `src/api/tests/test_safety_screens.py`.
* Dependencies: None

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Execute Focused unittest, Ruff, and Mypy validation

* Intent: Verify the six required `unittest` modules plus `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` pass with zero errors.
* Dependencies: P01-T01

## Critique Disposition

* Critique artifact: .copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-c3-plan-critique.md
* Critique execution status: `Complete` (single-pass gate satisfied)
* Verdict: `Pass` (`Critical: 0`, `High: 0`, `Medium: 0`, `Low: 0`)
* Finding dispositions: `none` (`0` `PC-xxx` findings raised; Option 2, locked test bounds, Ruff/Mypy strictness, and retention/commit boundaries verified).

## Follow-Up Items

* Add a `.skip-link` bypass anchor and polite status region to standalone `/law.html` (and shrink `NO_SKIP_LINK` to `set()`) if `/law.html` enters workbench conformance scope.
* Apply optional Web Interface Guidelines typography and locale polish (`RV-001` from Cycle 1: `tabular-nums`, `Intl.NumberFormat` in `bars()`, `<meta name="theme-color">`).
* Execute human assistive-technology and browser zoom walkthroughs (`NVDA`, `VoiceOver`, `200%` text resize, `400%` reflow), record owner confirmation `O-1`, and integrate rendered Playwright / axe-core CI probes (`#155`, `#619`).
