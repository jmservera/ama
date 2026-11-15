<!-- markdownlint-disable-file -->
# RPI Plan: Focused Cycle 2 Correction for Workbench WCAG 2.2 Baseline (#151)

## Task Metadata

* Task ID: 2026-11-15-wcag-baseline-151-c2
* Task slug: wcag-baseline-151-c2
* Parent task: 2026-11-15-wcag-baseline-151 (`wcag-baseline-151`)
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-c2-plan-critique.md

## Executive Summary

This focused Cycle 2 (`c2`) plan resolves the blocking test regression identified by independent functional review (`rev-151-wcag`) on branch `feat/ux-151-wcag-baseline` for GitHub issue `#151` and aligns test formatting with `--isolated --line-length 100`. Adding `.skip-link` to `src/api/src/zava_forward/api/web/welcome.html` closed the `/` route skip-link gap, so the shrink-only `NO_SKIP_LINK` set in `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` must shrink from `{"/", "/law.html"}` to `{"/law.html"}`. In addition, `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py` must be formatted with `python3 -m ruff format --isolated --line-length 100` while keeping `"self.assertEqual(sites, 9,"` on one line in `test_accessibility_baseline.py` so `src/api/tests/test_epic149_form_error_summary_associations.py` continues to pass.

### User Decisions and Requirements Highlights

* Update `NO_SKIP_LINK` in `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` to `{"/law.html"}` so `SkipLink.test_skip_link_gaps_are_recorded_and_shrink_only` enforces the `/` welcome skip link.
* Format `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py` with `python3 -m ruff format --isolated --line-length 100`.
* Run the targeted `unittest` suites and `ruff check src tests`, record the Cycle 2 `.copilot-tracking/` `changes` and `reviews` artifacts without overwriting historical Cycle 1 artifacts, and commit on `feat/ux-151-wcag-baseline` with the Copilot trailer without pushing.

### What You May Not Know

* `src/api/pyproject.toml` excludes `tests/test_accessibility_baseline.py` from default `ruff format`, so an `--isolated --line-length 100` formatting pass wraps the 106-character `self.assertEqual(sites, 9, "new aria-invalid site: ...")` call across three lines unless the message string is bound to a local variable first; wrapping that call breaks `FormErrorAssociations.test_counted_baseline_is_unchanged_and_fully_mapped` in `src/api/tests/test_epic149_form_error_summary_associations.py`, which asserts `"self.assertEqual(sites, 9," in BASELINE_TEST.read_text()`.
* Preserving original Cycle 1 critique and review artifacts (`wcag-baseline-151-plan-critique.md`, `wcag-baseline-151-changes.md`, `wcag-baseline-151-review.md`) is mandatory under repository governance; Cycle 2 records separate `wcag-baseline-151-c2-*` artifacts linked via `parent_task`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Work in `/home/azureuser/source/ama-demo-wt/feat-151-wcag-baseline` on branch `feat/ux-151-wcag-baseline` for issue `#151` under the Focused validation tier (user prompt).
* Update `NO_SKIP_LINK` in `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` from `{"/", "/law.html"}` to `{"/law.html"}` to resolve the `rev-151-wcag` blocking regression after `welcome.html` gained `.skip-link` (user prompt).
* Format `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py` with `python3 -m ruff format --isolated --line-length 100` (user prompt).
* Run `test_epic149_landmarks_skip_link_focus_order.py`, `test_wcag_workbench_baseline_151.py`, `test_accessibility_baseline.py`, and `(cd src/api && python3 -m ruff check src tests)`, plus verify tightly coupled `test_epic149_form_error_summary_associations.py` and `mypy` (user prompt; repository rules).
* Update `.copilot-tracking/` `changes` and `reviews` artifacts for `#151` while preserving original Cycle 1 critique/Review records, and commit locally on `feat/ux-151-wcag-baseline` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (user prompt; `.github/copilot-instructions.md`).

## Goals

* Shrink `NO_SKIP_LINK` to `{"/law.html"}` so `test_epic149_landmarks_skip_link_focus_order.py` passes and enforces the `/` skip link alongside `/app`.
* Format `test_accessibility_baseline.py` and `test_wcag_workbench_baseline_151.py` cleanly under `ruff format --isolated --line-length 100` without breaking `test_epic149_form_error_summary_associations.py` or `ruff check` / `mypy`.
* Persist complete Cycle 2 RPI tracking evidence and create one clean local commit on `feat/ux-151-wcag-baseline`.

## Scope and Non-Goals

### In Scope

* Updating `NO_SKIP_LINK` in `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py`.
* Keeping `"self.assertEqual(sites, 9,"` single-line-safe in `src/api/tests/test_accessibility_baseline.py` and formatting `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py` with `python3 -m ruff format --isolated --line-length 100`.
* Focused validation across the requested test modules, coupled `test_epic149_*` checks, `ruff check`, `ruff format --isolated --line-length 100 --check`, and `mypy`.
* Recording Cycle 2 `.copilot-tracking/` artifacts and committing locally on `feat/ux-151-wcag-baseline`.

### Non-Goals

* Modifying any web assets (`*.html`, `*.css`, `*.js`), application runtime code, or `pyproject.toml` lint/format configuration.
* Overwriting or deleting historical Cycle 1 `.copilot-tracking/` artifacts.
* Pushing commits to any remote.

## Functional Requirements

* `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` must declare `NO_SKIP_LINK = {"/law.html"}` so `/` and `/app` are enforced as having `.skip-link` while standalone `/law.html` remains the sole recorded skip-link gap.
  * Observable acceptance criteria: `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/api/src python3 -m unittest discover -s src/api/tests -p 'test_epic149_landmarks_skip_link_focus_order.py' -q` passes all 14 tests with `0` failures.
* `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py` must conform to `python3 -m ruff format --isolated --line-length 100` while preserving `"self.assertEqual(sites, 9,"` in `test_accessibility_baseline.py`.
  * Observable acceptance criteria: `python3 -m ruff format --isolated --line-length 100 --check` exits `0` on all three touched test files, and `test_accessibility_baseline.py`, `test_wcag_workbench_baseline_151.py`, and `test_epic149_form_error_summary_associations.py` all pass.

## Non-Functional Requirements

* Lint, static typing, and historical artifact preservation
  * Objective threshold or evaluation condition: `(cd src/api && python3 -m ruff check src tests)` and `mypy` on touched test modules exit `0`, and `git diff HEAD` modifies zero historical Cycle 1 `.copilot-tracking/` files (except if parent follow-up pointer is intentionally untouched).
  * Observable acceptance criteria: Zero lint/type errors and zero mutations to Cycle 1 `wcag-baseline-151-*` tracking files.

## Acceptance Criteria

* `NO_SKIP_LINK = {"/law.html"}` is set in `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` and all 14 tests in that module pass.
* `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_wcag_workbench_baseline_151.py` pass `python3 -m ruff format --isolated --line-length 100 --check`, `unittest` discovery, `test_epic149_form_error_summary_associations.py`, `(cd src/api && python3 -m ruff check src tests)`, and `mypy`.
* Cycle 2 `.copilot-tracking/` artifacts (`changes` and `reviews` plus plan/details/critique/state) are persisted cleanly alongside unchanged Cycle 1 artifacts, and committed locally on `feat/ux-151-wcag-baseline` with `Refs #151, #119` and the Copilot trailer without pushing.

## Locked Test Ownership and Bounds

* Canonical test targets:
  * `src/api/tests/test_epic149_landmarks_skip_link_focus_order.py` (update `NO_SKIP_LINK` shrink-only set; `0` test removals, `0` new test methods)
  * `src/api/tests/test_accessibility_baseline.py` (extract message string variable to preserve `"self.assertEqual(sites, 9,"` under 100-column formatting and apply `ruff format --isolated --line-length 100`; `0` test removals, `0` new test methods)
  * `src/api/tests/test_wcag_workbench_baseline_151.py` (apply `ruff format --isolated --line-length 100`; `0` test removals, `0` new test methods)
* Exact test removals: `none`
* Maximum test additions: `0` new test files, `0` new test methods
* Generated targets: `none`
* Semantic-versus-regression coverage: Regression enforcement of `/` skip-link presence via shrink-only `NO_SKIP_LINK` and preservation of `test_epic149_form_error_summary_associations.py`'s verbatim `self.assertEqual(sites, 9,` check.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c2-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/wcag-baseline-151-c2-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-c2-plan-critique.md with `Pass` verdict (`0` findings) |
| Relevant research | Satisfied-and-skipped from caller-supplied `rev-151-wcag` evidence and direct reproduction (`test_epic149_landmarks_skip_link_focus_order.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`) |
| Changes-record role | .copilot-tracking/changes/2026-11-15/wcag-baseline-151-c2-changes.md is created by `rpi-implement` |
| Planning execution and readiness | Complete and `Ready` for `rpi-implement` |
| Continuation context | Confirmed automatic RPI Agent child loop (`c2`) |

## Sources

* src/api/tests/test_epic149_landmarks_skip_link_focus_order.py: Shrink-only `NO_SKIP_LINK` set and `SkipLink.test_skip_link_gaps_are_recorded_and_shrink_only`.
* src/api/src/zava_forward/api/web/welcome.html: Cycle 1 `welcome.html` `.skip-link` addition targeting `#welcome-main`.
* src/api/tests/test_accessibility_baseline.py: WCAG 2.2 static baseline checks (`sites == 9` assertion).
* src/api/tests/test_epic149_form_error_summary_associations.py: Cross-file guard checking `"self.assertEqual(sites, 9,"` in `test_accessibility_baseline.py`.
* src/api/tests/test_wcag_workbench_baseline_151.py: Cycle 1 deterministic Node-VM and static verification suite.
* .copilot-tracking/changes/2026-11-15/wcag-baseline-151-changes.md: Cycle 1 implementation evidence record.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Shrink-Only Skip-Link Baseline Fix, Isolated Formatting, and Focused Validation

* Intent: Update `NO_SKIP_LINK` in `test_epic149_landmarks_skip_link_focus_order.py`, format `test_accessibility_baseline.py` and `test_wcag_workbench_baseline_151.py` cleanly at line length 100 without breaking cross-test invariants, and run focused validation.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update NO_SKIP_LINK and format #151 baseline test modules

* Intent: Remove `"/"` from `NO_SKIP_LINK` in `test_epic149_landmarks_skip_link_focus_order.py`, preserve single-line `"self.assertEqual(sites, 9,"` in `test_accessibility_baseline.py`, and run `python3 -m ruff format --isolated --line-length 100` on `test_accessibility_baseline.py` and `test_wcag_workbench_baseline_151.py`.
* Dependencies: None

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Execute focused unittest, ruff, and mypy validation

* Intent: Verify all four caller-requested commands plus coupled `test_epic149_form_error_summary_associations.py`, `ruff format --isolated --line-length 100 --check`, and `mypy` pass cleanly.
* Dependencies: P01-T01

## Critique Disposition

Single-pass plan critique executed at `.copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-c2-plan-critique.md` (`Execution status: Complete`, `Verdict: Pass`, `0` Critical, `0` High, `0` Medium, `0` Low findings). No revisions or user decisions were required.

## Follow-Up Items

* Add a `.skip-link` bypass anchor and polite status region to standalone `/law.html` (and shrink `NO_SKIP_LINK` to `set()`) if `/law.html` enters workbench conformance scope.
* Apply optional Web Interface Guidelines typography and locale polish (`RV-001` from Cycle 1: `tabular-nums`, `Intl.NumberFormat` in `bars()`, `<meta name="theme-color">`).
* Execute human assistive-technology and browser zoom walkthroughs (`NVDA`, `VoiceOver`, `200%` text resize, `400%` reflow), record owner confirmation `O-1`, and integrate rendered Playwright / axe-core CI probes (`#155`, `#619`).
