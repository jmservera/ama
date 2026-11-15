<!-- markdownlint-disable-file -->
# RPI Plan: Issue 231 Cycle 1 Rebase CSS Focus Rule Recovery (PR 1767)

## Task Metadata

* Task ID: 2026-11-15-retrofit-technical-quality-wcag-231-c1
* Task slug: retrofit-technical-quality-wcag-231-c1
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan-critique.md

## Executive Summary

When PR #1767 (Issue #231 retrofit technical and quality screens WCAG 2.2 conformance) was rebased onto parent commit fe6398197, 9 of 10 hosted CI jobs and 3,569 of 3,570 src-api unit tests passed, leaving one failure in sibling Issue #229's test_workspace_jump_nav_and_click_activation_focus_target_headings in src/api/tests/test_housing_resident_screen_wcag.py. During rebase conflict resolution in src/api/src/zava_forward/api/web/style.css, parent commit fe6398197's standalone `[tabindex="-1"]:focus` rule was combined into a comma-separated selector list (`[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible { ... }`), preventing `[tabindex="-1"]:focus\s*\{\s*outline:` from matching.

This plan splits that combined rule in src/api/src/zava_forward/api/web/style.css into two consecutive standalone Fluent 2 dual-ring focus rules (`[tabindex="-1"]:focus { ... }` followed by `.screen-record h2[tabindex="-1"]:focus-visible { ... }`), adds one focused regression assertion in src/api/tests/test_technical_quality_screens_wcag.py so Issue #231's own test suite guards the standalone `[tabindex="-1"]:focus` rule on future rebases, runs focused validation across all Issue #231, sibling #229/#230/finance, WCAG baseline, content-standard, design-system, ruff, mypy, and test-rename suites, and records a clean local commit referencing Issue #231 without pushing.

### User Decisions and Requirements Highlights

* Restore and preserve the standalone `[tabindex="-1"]:focus` outline rule in the workbench stylesheet so both sibling housing/resident WCAG tests and Issue #231 WCAG tests pass with zero regressions.
* Record full Cycle 1 dated RPI tracking artifacts under .copilot-tracking/ across research, plans, details, changes, and reviews.
* Execute focused unittest, ruff check, ruff format check, mypy, and tools/rename-zava-tests.py validation, then create a clean frozen local commit with `Refs #231` and the Copilot `Co-authored-by` trailer without pushing to remote.

### What You May Not Know

* Simply reversing the two selectors inside one comma-separated CSS rule would fix test_housing_resident_screen_wcag.py while immediately breaking test_focus_ring_and_screen_css_invariants in src/api/tests/test_technical_quality_screens_wcag.py, because both regex contracts anchor `\s*\{` immediately after their own selector; only two standalone CSS rules satisfy every test contract simultaneously while keeping identical browser cascade behavior.
* The caller prompt uses shorthand alias names (`feat-231-quality-finance-wcag`, `styles.css`, and `test_quality_finance_screen_wcag.py`) for PR #1767's verified worktree /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag on branch feat/ux-231-retrofit-wcag (HEAD db52dfff4 targeting feat/demo-233-same-home-tensions-0825 at fe6398197), stylesheet src/api/src/zava_forward/api/web/style.css, and Issue #231 test module src/api/tests/test_technical_quality_screens_wcag.py alongside existing finance and data-steward WCAG test modules (`test_finance_screen_wcag.py`, `test_finance_grants_screen_wcag.py`, `test_finance_screens_wcag_225.py`, and `test_data_steward_screen_wcag.py`); focused validation executes all of them.

### Unresolved Decisions or Blockers

* None for Cycle 1 implementation; external human assistive-technology and role-representative sign-off under #151 and #155 remains tracked as a post-review follow-up (`Refs #231` is used rather than a closing keyword).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full Cycle 1 (`c1`) RPI loop in order (research, plan, implement, review) with dated tracking artifacts under .copilot-tracking/ (`research/`, `plans/`, `details/`, `changes/`, `reviews/`) for Issue #231 (`PR #1767`) at HEAD db52dfff4 rebased onto fe6398197 (source: caller prompt).
* Inspect parent commit fe6398197's workbench stylesheet against current HEAD around `[tabindex="-1"]:focus` and Issue #231 screen styles, and restore/preserve the `[tabindex="-1"]:focus` outline rule so both src/api/tests/test_housing_resident_screen_wcag.py and Issue #231's WCAG test suite pass without regressions (source: caller prompt; research C1, C3, C4, C5, C6).
* Run focused validation covering Issue #231 and sibling WCAG unit tests (including housing/resident, programme, finance, data-steward, accessibility baseline, content standard, and design system suites), ruff lint and format checks, mypy type-checking in src/api, and python3 tools/rename-zava-tests.py (source: caller prompt; research C8).
* Create a local git commit referencing `Refs #231` with trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, configure repository-local noreply git user email via GitHub CLI, do not push to remote, and leave `git status --short` empty (source: caller prompt and .github/copilot-instructions.md).

## Goals

* Restore standalone `[tabindex="-1"]:focus` Fluent 2 dual-ring focus styling in src/api/src/zava_forward/api/web/style.css while preserving `.screen-record h2[tabindex="-1"]:focus-visible` and all rebase changes from db52dfff4.
* Guard the standalone `[tabindex="-1"]:focus` CSS contract directly inside Issue #231's WCAG test suite so future rebases cannot silently merge or drop the rule.
* Prove zero regressions across WCAG, Fluent 2 design-system, plain-language content-standard, lint, type-check, and test-naming gates, then freeze a clean local commit on branch feat/ux-231-retrofit-wcag.

## Scope and Non-Goals

### In Scope

* Splitting the combined `[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible` rule in src/api/src/zava_forward/api/web/style.css into two consecutive standalone rules with identical Fluent 2 focus-token declarations.
* Adding one focused regex assertion in test_focus_ring_and_screen_css_invariants within src/api/tests/test_technical_quality_screens_wcag.py (`none` test removals; maximum `1` assertion addition; `none` generated file targets).
* Authoring Cycle 1 RPI artifacts under .copilot-tracking/ and committing all Cycle 1 changes locally with `Refs #231` and the required Copilot trailer after focused validation passes.

### Non-Goals

* Modifying sibling test suites (`src/api/tests/test_housing_resident_screen_wcag.py`, `src/api/tests/test_data_steward_screen_wcag.py`, `src/api/tests/test_programme_screen_wcag.py`, or finance WCAG tests).
* Bundling unrelated Cycle 0 follow-up items (`RV-001` JSON `ensure_ascii=False`, `RV-002` `defect.fixed_by` independence check, or `RV-003` Cycle 0 prose cleanup) into this surgical CI recovery commit.
* Pushing commits to `origin` or mutating remote PR #1767 state.

## Functional Requirements

* Standalone programmatic focus rule in src/api/src/zava_forward/api/web/style.css restores exact parent fe6398197 syntax `[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` immediately followed by `.screen-record h2[tabindex="-1"]:focus-visible { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }`.
  * Observable acceptance criteria: `test_workspace_jump_nav_and_click_activation_focus_target_headings` in src/api/tests/test_housing_resident_screen_wcag.py, `test_focus_ring_and_screen_css_invariants` in src/api/tests/test_technical_quality_screens_wcag.py, and `test_rebase_preserves_housing_resident_helpers_alongside_steward_screen` in src/api/tests/test_data_steward_screen_wcag.py all pass.
* Issue #231 WCAG test suite owns regression coverage for standalone `[tabindex="-1"]:focus` alongside `.screen-record h2[tabindex="-1"]:focus-visible` in `TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants` within src/api/tests/test_technical_quality_screens_wcag.py, with `none` test removals and `1` assertion addition.
  * Observable acceptance criteria: `test_focus_ring_and_screen_css_invariants` fails if `[tabindex="-1"]:focus` is combined before `{` and passes when both standalone rules exist.
* Implementation configures repository-local GitHub noreply `user.email` via `gh api user` and verifies worktree hygiene across source, test, and tracking files (including parent state .copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json), and the active RPI parent records one atomic local commit on feat/ux-231-retrofit-wcag immediately after single-pass `rpi-review` persists its review log and final state transitions, using `Refs #231` and the Copilot trailer with zero `.copilot-tracking/` citations in commit message or code and no remote push.
  * Observable acceptance criteria: `git status --short` outputs nothing after RPI parent closeout, `git log -1` shows `Refs #231` and the Copilot `Co-authored-by` trailer, and `git status -sb` shows local branch ahead of remote by 1 unpushed commit.

## Non-Functional Requirements

* WCAG 2.2 AA and Fluent 2 focus-token conformance
  * Objective threshold or evaluation condition: Focus rules use exclusively `--focus-w`, `--focus-ink`, `--focus-off`, and `--focus` tokens, add zero `outline: none` or `outline: 0` declarations, add zero `animation` or `transition` declarations on `.screen-*` blocks, and keep total `position:fixed` rules in src/api/src/zava_forward/api/web/style.css at `2`.
  * Operating condition or verification approach, if needed: Verified via src/api/tests/test_accessibility_baseline.py, src/api/tests/test_design_system.py, src/api/tests/test_content_standard.py, and Vercel Web Interface Guidelines check.
  * Observable acceptance criteria: All baseline accessibility, design-system, and content-standard unit suites exit `0`.
* Static analysis, formatting, type safety, and test naming discipline
  * Objective threshold or evaluation condition: Zero ruff lint errors, zero ruff formatting diffs, zero mypy errors on `src` and target WCAG test files, and zero missing `zava` prefixes reported by tools/rename-zava-tests.py.
  * Operating condition or verification approach, if needed: Executed from src/api and worktree root with Python 3 toolchain.
  * Observable acceptance criteria: `ruff check .`, `ruff format --check .`, `mypy`, and `python3 tools/rename-zava-tests.py` all exit `0`.

## Acceptance Criteria

* Standalone `[tabindex="-1"]:focus` and `.screen-record h2[tabindex="-1"]:focus-visible` rules coexist on consecutive lines in src/api/src/zava_forward/api/web/style.css using Fluent 2 focus tokens.
* `test_focus_ring_and_screen_css_invariants` in src/api/tests/test_technical_quality_screens_wcag.py asserts both standalone focus rules (`0` removals, `1` assertion addition).
* Focused unittest command passes across src/api/tests/test_technical_quality_screens_wcag.py, src/api/tests/test_housing_resident_screen_wcag.py, src/api/tests/test_data_steward_screen_wcag.py, src/api/tests/test_programme_screen_wcag.py, src/api/tests/test_finance_screen_wcag.py, src/api/tests/test_finance_grants_screen_wcag.py, src/api/tests/test_finance_screens_wcag_225.py, src/api/tests/test_accessibility_baseline.py, src/api/tests/test_content_standard.py, and src/api/tests/test_design_system.py.
* `ruff check .`, `ruff format --check .`, `mypy` (`src`, `tests/test_technical_quality_screens_wcag.py`, `tests/test_housing_resident_screen_wcag.py`), and `python3 tools/rename-zava-tests.py` exit `0`.
* Dated Cycle 1 RPI artifacts (`research`, `plan`, `phase-details`, `plan-critique`, `changes`, `review`, and `state.json`) are complete and reconciled under .copilot-tracking/.
* Local commit on feat/ux-231-retrofit-wcag includes `Refs #231` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, omits `.copilot-tracking/` citations in commit text, is not pushed, and leaves `git status --short` empty.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan.md                                                        |
| Phase details                    | .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md                                             |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan-critique.md with Revise verdict; PC-001 through PC-003 resolved directly |
| Relevant research                | .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-c1-research.md                                                 |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Planning complete; Ready for implementation                                                                                              |
| Continuation context             | Confirmed automatic RPI Agent mode returns to parent to continue automatically to Implement                                              |

## Sources

* .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-c1-research.md: Verified git diff between fe6398197 and db52dfff4 (`C3`, `C4`), reproduced hosted CI failure (`C5`), verified all CSS regex contracts (`C6`, `C7`, `C8`), and confirmed Web Interface Guidelines alignment (`W1`).
* src/api/src/zava_forward/api/web/style.css: Workbench stylesheet containing the merged `[tabindex="-1"]:focus, .screen-record h2[tabindex="-1"]:focus-visible` selector rule.
* src/api/tests/test_housing_resident_screen_wcag.py: Sibling Issue #229 WCAG test module asserting `r'\[tabindex="-1"\]:focus\s*\{\s*outline:'`.
* src/api/tests/test_technical_quality_screens_wcag.py: Issue #231 WCAG test module asserting `.screen-record h2[tabindex="-1"]:focus-visible\s*\{` and `.screen-*` motion/focus invariants.
* docs/reference/research/ux/wcag-conformance-baseline.md: Authoritative WCAG 2.2 AA focus-appearance (`--focus`, `--focus-ink`, `--focus-w`, `--focus-off`) and validation contract.
* .github/copilot-instructions.md and copilot-tracking.instructions.md: Repository engineering, focused-tier validation, git commit identity/trailer, and tracking artifact rules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Restore standalone programmatic focus CSS rule and guard regression

* Intent: Split the rebase-merged focus selector in src/api/src/zava_forward/api/web/style.css into two standalone rules and add a direct regression assertion in src/api/tests/test_technical_quality_screens_wcag.py.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Split merged programmatic focus rule in workbench stylesheet

* Requirement and evidence: Caller Required Fix items 1-2; research C3, C4, C5, C6, C7, W1.
* Expected result: src/api/src/zava_forward/api/web/style.css defines standalone `[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }` immediately followed by standalone `.screen-record h2[tabindex="-1"]:focus-visible { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add standalone programmatic focus regex guard in Issue 231 WCAG tests

* Requirement and evidence: Caller Required Fix item 2 and code-change test discipline; research C5, C6.
* Expected result: `test_focus_ring_and_screen_css_invariants` in src/api/tests/test_technical_quality_screens_wcag.py asserts `r'\[tabindex="-1"\]:focus\s*\{\s*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)'` alongside the existing `.screen-record h2[tabindex="-1"]:focus-visible` assertion (`0` removals, `1` addition).
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Validate focused WCAG, static-analysis, and repository gates and prepare commit hygiene

* Intent: Prove all Issue #231, sibling WCAG, accessibility baseline, design-system, content-standard, Web Interface Guidelines, ruff, mypy, and test-rename checks pass, configure repository-local git noreply author identity, and verify pre-review worktree hygiene so the RPI parent can record one atomic local commit immediately after single-pass review.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused WCAG unit tests, ruff, mypy, test-rename, and Web Interface Guidelines validation

* Requirement and evidence: Caller Required Fix item 4 and .github/copilot-instructions.md focused validation tier and Web Development Guidance; research C1, C8, W1.
* Expected result: Unittest across all 10 target WCAG/baseline modules, `ruff check .`, `ruff format --check .`, `mypy`, `python3 tools/rename-zava-tests.py`, and refreshed `web-design-guidelines` `file:line` review of src/api/src/zava_forward/api/web/style.css all pass with zero issues, recorded in .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Configure repository-local git noreply identity and verify pre-review worktree hygiene

* Requirement and evidence: Caller Required Fix item 5 and .github/copilot-instructions.md git identity/commit rules; critique PC-001.
* Expected result: Repository-local git `user.email` is configured to `{id}+{login}@users.noreply.github.com` from `gh api user`, source/test diffs contain zero `.copilot-tracking/` substrings, and `git status --short` accounts for every expected Cycle 1 file (including modified parent state .copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json) ready for the RPI parent's post-review atomic local commit.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-c1-phase-details.md

## Dependencies

* Worktree /home/azureuser/source/ama-demo-wt/feat-231-retrofit-wcag at HEAD db52dfff4 (rebased onto fe6398197): Provides the exact PR #1767 source state where hosted CI job 132700405590 failed.
* Python 3 environment with `unittest`, `ruff`, `mypy`, and `node` (used by Node-backed DOM evaluation tests in `src/api/tests/test_technical_quality_screens_wcag.py` and sibling suites): Required to run all focused validation checks locally.
* Authenticated `gh` CLI session: Required by .github/copilot-instructions.md to configure repository-local `{id}+{login}@users.noreply.github.com` before committing.

## Critique Disposition

Single-pass `rpi-plan-critique` completed in .copilot-tracking/reviews/plans/2026-11-15/retrofit-technical-quality-wcag-231-c1-plan-critique.md (`Revise` verdict with `0` Critical, `0` High, `1` Medium, `2` Low findings). All three planner-owned findings were applied directly without requiring user decisions:

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 (Medium: P02-T02 circular dependency on rpi-review and omitted parent state JSON) | resolved | Scoped P02-T02 to pre-review git author configuration and worktree hygiene including .copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json, and assigned the final atomic `git add` / `git commit` (`Refs #231` plus Copilot trailer, no push, `git status --short` empty) to the active RPI parent immediately after single-pass `rpi-review` persists its review log and `Follow-up` state. |
| PC-002 (Low: non-existent test method in test_data_steward_screen_wcag.py and mismatched TestCase class name in test_technical_quality_screens_wcag.py) | resolved | Updated Functional Requirement 1 to `test_rebase_preserves_housing_resident_helpers_alongside_steward_screen` and updated P01-T02 to `TechnicalAndQualityWcagTests.test_focus_ring_and_screen_css_invariants`. |
| PC-003 (Low: P02-T01 omitted web-design-guidelines refresh and file:line audit step) | resolved | Added explicit `web-design-guidelines` refresh and `file:line` review of src/api/src/zava_forward/api/web/style.css to P02 and P02-T01 validation expectations and changes-record completion evidence. |
| Residual risk (external manual assistive-technology and zoom acceptance under #151 and #155) | accepted with risk | Automated unit and static suites verify engineering invariants; commit uses `Refs #231` rather than a closing keyword while human AT sign-off remains tracked as a follow-up. |

## Follow-Up Items

* Cycle 0 RV-001 and RV-003 (`ensure_ascii=False` in `json.dumps(tree)` inside `src/api/tests/test_technical_quality_screens_wcag.py` and historical Cycle 0 prose cleanup): Outside immediate surgical CI rebase fix scope; retained for user selection at post-Review checkpoint.
* Cycle 0 RV-002 (extend `qualityAcceptanceGap(r)` in `src/api/src/zava_forward/api/web/app.js` to check `defect.fixed_by` alongside `submitted_by`): Outside immediate CSS rebase regression scope; retained for user selection at post-Review checkpoint.
* External human assistive-technology and role-representative validation (`#151`, `#155`): Requires human NVDA/VoiceOver and zoom walkthrough before Issue #231 closes (`Refs #231` preserved).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-c1-changes.md
* Ready phase or task: All active plan phases complete (P01, P01-T01, P01-T02, P02, P02-T01, P02-T02); ready for single-pass `rpi-review`, followed immediately by the RPI parent's post-review atomic local commit (`Refs #231` + Copilot trailer, no push).
* Remaining provisional question or blocker: None
