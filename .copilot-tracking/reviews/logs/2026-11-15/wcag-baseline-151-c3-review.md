<!-- markdownlint-disable-file -->
# Review: Focused Cycle 3 Safety-Screen Table Header Remediation for PR #1802 (#151)

## Scope and Evidence

* Task ID: 2026-11-15-wcag-baseline-151-c3
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`)
* Assessed boundary: Option 2 remediation of `SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned` in `src/api/tests/test_safety_screens.py` for `<th scope="col">` and `<th scope="row">` table semantics, Locked Test Ownership and Bounds, Focused-tier `unittest` / `ruff` / `mypy` validation without `tools/rpi-checks.py`, Cycle 1 and Cycle 2 `.copilot-tracking/` preservation, and local commit readiness on `feat/ux-151-wcag-baseline` without pushing.
* Plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-c3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-c3-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/wcag-baseline-151-c3-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/wcag-baseline-151-c3-research.md (`C1`-`C10`, `W1`), git diff of `src/api/tests/test_safety_screens.py`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_wcag_workbench_baseline_151.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `git status --short`, and Vercel Web Interface Guidelines check (`0` web asset files modified in `c3`).

## Opening Review State

* Interpreted review goal: Verify that Cycle 3 (`c3`) resolves the sole `PR #1802` `src-api` CI failure (`SafetyScreens.test_rendered_tables_are_labelled_focusable_and_aligned`) in full alignment with WCAG 2.2 SC 1.3.1, peer workbench test suites, Focused validation gates, and tracking-retention constraints.
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`)
* Evidence readiness: Complete and reconciled across research, finalized plan, phase details, single-pass critique (`Pass`), changes record (`Complete`), and direct `git diff` / `git status` inspection.
* Acceptance basis: User Decisions and Requirements, Functional and Non-Functional Requirements, Acceptance Criteria, Locked Test Ownership and Bounds, and Critique Disposition in `.copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md`.
* First comparison boundary: Plan-to-change reconciliation across `P01`, `P01-T01`, `P01-T02`, and `## Follow-Up Items`, excluding hosted CI re-execution and human assistive-technology walkthroughs (`Not run` locally).
* Active read-only boundaries: Write authority limited strictly to `.copilot-tracking/reviews/logs/2026-11-15/wcag-baseline-151-c3-review.md`.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass comparison on `2026-11-15` across all Cycle 3 RPI artifacts, `src/api/tests/test_safety_screens.py` diff, Focused validation outputs, and `git status --short` verification that Cycle 1 and Cycle 2 tracking files are untouched.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`[x]`) | Full phase completed across `P01-T01` and `P01-T02` | Reconciled | Checked `[x]` in `wcag-baseline-151-c3-plan.md` and marked `completed` in `wcag-baseline-151-c3-phase-details.md`. |
| `P01-T01` (`[x]`) | `Update SafetyScreens Table Header and Column Alignment Assertions` | Reconciled | `src/api/tests/test_safety_screens.py` updated within locked bounds (`0` test removals, `0` new test methods/files, `0` `.copilot-tracking/` references in code). |
| `P01-T02` (`[x]`) | `Execute Focused Unittest, Ruff, and Mypy Validation` | Reconciled | `65` tests across `6` modules, `ruff check .`, `ruff format --check .`, and strict `mypy` all exited `0`; `tools/rpi-checks.py` skipped as required. |
| `## Follow-Up Items` | Three canonical follow-up items mirrored in `wcag-baseline-151-c3-changes.md` | Reconciled | Kept outside active `P01` completion and acceptance claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/tests/test_safety_screens.py` | Separated `(thead,) = find_all(table, "thead")` (`heads = find_all(thead, "th")` with `scope == "col"`) from `(tbody,) = find_all(table, "tbody")` rows, asserting each `<tr>` starts with `<th scope="row">` containing non-empty stripped `string_leaves` text followed by `<td>` cells (`row["kids"][1:] == tds`) where `1 + len(tds) == len(heads)`. Preserves `role-screens.js` default `rowHeader = true`, `test_wcag_workbench_baseline_151.py`, and `wcag-conformance-baseline.md`. | `git diff src/api/tests/test_safety_screens.py` | Passed (`14` tests in `test_safety_screens.py` `OK`; `1 file already formatted`) | Reconciled |
| `P01-T02` (`P01`) | `src/api/tests/test_safety_screens.py` (verified with `src/api`) | Executed the caller-mandated Focused validation suite (`6` `unittest` modules, `ruff check .`, `ruff format --check .`, `mypy`) without invoking `tools/rpi-checks.py`, and confirmed zero edits to Cycle 1 or Cycle 2 `.copilot-tracking/` artifacts or web assets. | Validation Record in `wcag-baseline-151-c3-changes.md` and `git status --short` | Passed (`65` tests `OK`; `ruff check .` `All checks passed!`; `ruff format --check .` `214 files already formatted`; `mypy` `Success: no issues found in 298 source files`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` in `.copilot-tracking/details/2026-11-15/wcag-baseline-151-c3-phase-details.md` | Clarified `test_safety_screens.py` standalone test count from `12` to `14` (`65` six-suite total unchanged). | `Ran 14 tests in 0.983s — OK`; user decision: `none` (factual target clarification). | Updated `P01-T01` validation expectation and `P01` status in `wcag-baseline-151-c3-phase-details.md`. | Not needed (preserves approved intent and locked test bounds). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Single-pass critique in `.copilot-tracking/reviews/plans/2026-11-15/wcag-baseline-151-c3-plan-critique.md` completed with verdict `Pass` and `0` `PC-xxx` findings, recorded in `.copilot-tracking/plans/2026-11-15/wcag-baseline-151-c3-plan.md` (`## Critique Disposition`).
* Material revisions: None. No material discovery or scope/architecture change occurred during implementation.
* Dependent-work pause assessment: `P01-T02` ran only after `P01-T01` passed its targeted test and formatting check and was marked `[x]`.
* Justification assessment: Supported by repository evidence (`C1`-`C10`, `W1`).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Add `.skip-link` bypass anchor and polite status region to standalone `/law.html` if brought into workbench conformance scope | `/law.html` is outside the Cycle 3 `PR #1802` `test_safety_screens.py` CI remediation | Follow-up UX cycle | Open; routed as distinct follow-up |
| Apply optional Web Interface Guidelines typography and locale polish (`RV-001` from Cycle 1: `tabular-nums`, `Intl.NumberFormat` in `bars()`, `<meta name="theme-color">`) | Non-WCAG polish outside single-test `c3` remediation | Follow-up UX polish task | Open; routed as distinct follow-up |
| Execute human assistive-technology and browser zoom walkthroughs (`NVDA`, `VoiceOver`, `200%` text resize, `400%` reflow), record `O-1`, and integrate rendered Playwright / axe-core CI probes (`#155`, `#619`) | Requires human screen-reader/zoom verification and CI browser-probe workflow work | Human reviewer / `#155` CI task | Open; routed as distinct follow-up |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `P01` or `P01-T01`/`P01-T02` implementation, completion, or acceptance scope.

## Findings

* None (`Critical: 0`, `High: 0`, `Medium: 0`, `Low: 0`). No defects, decision gaps, or evidence gaps were found within the assessed Cycle 3 boundary. Note: Zero web files (`*.html`, `*.css`, `*.js`) changed in Cycle 3, so no new Web Interface Guidelines `file:line` findings were introduced.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| none | none | none | Conformant implementation within assessed `c3` boundary |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Standalone `/law.html` skip-link/status-region alignment (if brought into workbench scope), Cycle 1 `RV-001` Web Interface Guidelines typography/locale polish, and human AT/zoom walkthroughs plus rendered Playwright/axe-core CI probes (`#155`, `#619`) remain distinct follow-up items outside Cycle 3.
* Local Git commit on `feat/ux-151-wcag-baseline` (without pushing) is executed by the parent workflow at closeout per caller handoff instructions, followed by coordinator push, hosted `PR #1802` CI verification, and independent exact-head review.

## Blockers and Remaining Work

* Blockers: none for Cycle 3 implementation and review (`PR #1802` publication/merge still requires hosted CI and independent human review outside this local non-push run).
* Remaining active work: none (`P01`, `P01-T01`, and `P01-T02` are complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `(cd src/api && PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest tests/test_safety_screens.py -q)` | `src/api/tests/test_safety_screens.py` | Passed | `Ran 14 tests in 0.983s — OK` |
| `(cd src/api && PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest tests/test_safety_screens.py tests/test_wcag_workbench_baseline_151.py tests/test_accessibility_baseline.py tests/test_epic149_landmarks_skip_link_focus_order.py tests/test_housing_resident_wcag_232.py tests/test_role_screens.py -q)` | `src/api/tests/` (`6` modules) | Passed | `Ran 65 tests in 3.746s — OK` |
| `(cd src/api && python3 -m ruff check .)` | `src/api` | Passed | `All checks passed!` |
| `(cd src/api && python3 -m ruff format --check .)` | `src/api` | Passed | `214 files already formatted` |
| `(cd src/api && python3 -m mypy)` | `src/api` (`src`, `tests`, `checks`) | Passed | `Success: no issues found in 298 source files` |
| `python3 tools/rpi-checks.py` | Repository gate | Skipped | Explicitly prohibited by caller instructions (`Focused` validation tier) |
| Hosted `PR #1802` `src-api` CI & human AT walkthroughs | Remote PR / assistive technology | Unavailable | Local non-push handoff requested (`Do NOT push`); human AT checks remain `Not run` (`Refs #151, #119`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: All Cycle 3 requirements, acceptance criteria, and locked test bounds are satisfied with verified test (`65` tests `OK`), lint (`ruff check .`), formatting (`ruff format --check .`), and strict type-check (`mypy`) evidence, zero regressions to `test_wcag_workbench_baseline_151.py` or `wcag-conformance-baseline.md`, and untouched Cycle 1 / Cycle 2 tracking records.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Retain ranked follow-ups in RPI session state and complete caller-requested local commit handoff without pushing |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused `unittest` (`65` tests `OK`), `ruff check .` (`Passed`), `ruff format --check .` (`214` files `Passed`), `mypy` (`298` files `Passed`); `tools/rpi-checks.py` skipped per caller instruction; hosted CI and human AT checks pending post-handoff
* Blockers: none
