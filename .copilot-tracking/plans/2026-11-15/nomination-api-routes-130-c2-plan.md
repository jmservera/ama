<!-- markdownlint-disable-file -->
# RPI Plan: Rebase Issue 130 Branch and Fix Refusal Feedback Focus-Blur Clearing

## Task Metadata

* Task ID: nomination-api-routes-130-c2
* Task slug: nomination-api-routes-130-c2
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-c2-plan-critique.md

## Executive Summary

This Cycle 2 plan rebases pull request `#1776` (`feat/ux-130-api-routes`, Issue `#130`) onto the updated parent branch `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, pull request `#1639`) and resolves the hosted `src-api` browser-check failure in `src/api/checks/case_journey_browser_check.py` (`mutation_reconstruction`, `family == "challenge"`, `outcome == "refusal"`). Scoping `"change"` event clearing in `nominationPanel._routeForm` strictly to `<select>` controls prevents programmatic focus transfer (`status.focus()`) from wiping newly recorded refusal messages when a focused text control blurs.

### User Decisions and Requirements Highlights

* **Rebase onto updated stacked parent**: Fetch `origin/feat/demo-233-same-home-tensions-0825` and rebase `PR #1776`'s active head branch `feat/ux-130-api-routes` cleanly onto `6510b6fbc`, preserving all `#130` and parent `#1639` changes without pushing.
* **Fix blur-triggered refusal message wipe in `panels.js`**: Inside `nominationPanel._routeForm` in `src/api/src/zava_forward/api/web/panels.js`, attach `"change"` -> `clearInvalid` only on `<select>` elements (`Boolean(options)`), keeping `"input"` -> `clearInvalid` on `<input>` and `<textarea>` elements so blurring a focused text input during `status.focus()` never clears `mutation.message`.
* **Focused Tier validation and local commit**: Run the requested targeted `src/core` and `src/api` unit suites, end-to-end `src/api/checks/case_journey_browser_check.py`, `ruff`, and `mypy` without invoking `tools/rpi-checks.py`, then commit all code and Cycle 2 `.copilot-tracking/` artifacts locally using privacy-safe Git author/committer config (`8036360+jmservera@users.noreply.github.com`), `Refs #130`, and the Copilot `Co-authored-by` trailer without pushing.

### What You May Not Know

* **Why Node unit tests passed in Cycle 1 while Chromium failed**: `test_case_journey.py` mocks `focus()` as a no-op in Node, whereas real Chromium blurs `#challenge-open-request` synchronously when `bindCaseMutationForm` calls `status.focus()`, dispatching a native DOM `"change"` event on `#challenge-open-request` after `mutation.pending` has already flipped to `false`.
* **Manual blur safety benefit**: Scoping `"change"` to `<select>` controls (`isSelect: Boolean(options)`) not only prevents `status.focus()` from wiping refusal feedback, it also prevents a keyboard user pressing `Tab` out of an edited text field after an error from accidentally clearing the refusal message before typing a fix.
* **Branch identity and conflict-free rebase**: Live inspection via `gh pr view 1776` confirmed the active open PR branch in `/home/azureuser/source/ama-demo-wt/feat-130-api-routes` is `feat/ux-130-api-routes` (reconciling the prompt's `feat/ux-130-nomination-api-routes` shorthand per AMA branch-reuse rules). Between merge-base `a1d0be5f6` and `6510b6fbc`, only `src/api/src/zava_forward/api/web/app.js` overlaps with `#130`, in completely disjoint sections, and untracked Cycle 2 `-c2-` tracking files do not collide with any tracked path on either side of the rebase.

### Unresolved Decisions or Blockers

* No blockers exist for local Cycle 2 execution. Remote `--force-with-lease` push of the rebased branch to `PR #1776`, hosted GitHub Actions confirmation, and external governance items (`OD-41`, `OD-42`) remain post-Review owner follow-ups.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan` with single-pass `rpi-plan-critique`, `implement`, `review`), writing new Cycle 2 (`-c2`) dated artifacts under `.copilot-tracking/` without deleting or overwriting existing `.copilot-tracking/` artifacts (caller prompt).
* Fetch `origin/feat/demo-233-same-home-tensions-0825` and rebase the active `PR #1776` branch (`feat/ux-130-api-routes`, reconciled from prompt shorthand via `gh pr view 1776` in research `C6`) onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), preserving all `#130` and parent `#1639` changes cleanly (caller prompt; research `C6`).
* Update `nominationPanel._routeForm` in `src/api/src/zava_forward/api/web/panels.js` so `addEventListener("change", clearInvalid)` is attached only on `<select>` elements (`options` truthy), keeping `addEventListener("input", clearInvalid)` for `<input>` and `<textarea>` controls so `status.focus()` blurring a text control never wipes `mutation.message` (caller prompt; research `C1`–`C5`, `W1`).
* Verify `<select>` vs `<input>`/`<textarea>` event behavior in `src/api/tests/test_nomination_screen.py` and run Focused Tier validation (`src/core` nomination unit discovery, `src/api` nomination unit discovery, `test_resident_api.py`, `test_accessibility_baseline.py`, `case_journey_browser_check.py`, `ruff check`, `ruff format --check`, and `mypy` on `src/core` and `src/api`) without running `tools/rpi-checks.py` (caller prompt; research `C5`, `C7`).
* Configure repository-local Git user email `8036360+jmservera@users.noreply.github.com` (verified with `gh api user`), commit all code and `.copilot-tracking/` Cycle 2 artifacts with `Refs #130` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave `git status --short` empty, and do not push (caller prompt; AMA Branch Workflow).

## Goals

* Rebase `feat/ux-130-api-routes` cleanly onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) with zero lost changes from `#130` or `#1639`/`#1784`.
* Preserve polite live refusal feedback (`mutation.message` and `#...-feedback` text) in `nominationPanel._routeForm` when `status.focus()` blurs a focused `<input>` or `<textarea>` control after a refused mutation, while retaining `"input"` clearing on text/date controls and `"change"` clearing plus conditional visibility updates on `<select>` controls.
* Prove end-to-end and unit regression safety under Focused Tier validation, including full headless-Chromium execution of `src/api/checks/case_journey_browser_check.py`.

## Scope and Non-Goals

### In Scope

* Fetching `origin/feat/demo-233-same-home-tensions-0825` and rebasing `feat/ux-130-api-routes` onto `6510b6fbc`.
* Updating `nominationPanel._routeForm` in `src/api/src/zava_forward/api/web/panels.js` to record `isSelect: Boolean(options)` per field and attach `"change"` -> `clearInvalid` only when `isSelect` is true.
* Adding `1` focused unit regression test in `src/api/tests/test_nomination_screen.py` covering focus-transfer blur `"change"` on `<input>`/`<textarea>` after a 409 refusal versus subsequent `"input"` and `<select>` `"change"` events.
* Running Focused Tier unit, browser-check, lint, format, and type-check suites and creating a clean local commit with Cycle 2 `.copilot-tracking/` artifacts.

### Non-Goals

* Pushing any branch or commit to `origin` or altering remote pull request state.
* Running `tools/rpi-checks.py`.
* Deleting, amending, or overwriting existing `.copilot-tracking/` Cycle 1 or parent artifacts.
* Modifying `bindCaseMutationForm`, `src/api/checks/case_journey_browser_check.py`, or unrelated workbench modules.

## Functional Requirements

* `feat/ux-130-api-routes` must contain `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) as a direct ancestor with all prior `#130` commits cleanly replayed on top.
  * Observable acceptance criteria: `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD` exits `0` and `git rev-parse origin/feat/demo-233-same-home-tensions-0825` equals `6510b6fbc38533a16b9492cacd3ab7e7331c1610` (or the latest fetched tip if updated).
* `nominationPanel._routeForm` in `src/api/src/zava_forward/api/web/panels.js` must attach `clearInvalid` to `"input"` for all controls and attach `clearInvalid` to `"change"` only when `options` is truthy (`<select>` controls).
  * Observable acceptance criteria: When a focused `<input>` or `<textarea>` edited during a pending mutation is blurred by `status.focus()` upon a `409` refusal, `#...-feedback` retains the `panelOwned` refusal message; subsequent `"input"` events on `<input>`/`<textarea>` and `"change"` events on `<select>` clear `aria-invalid`, update conditional field visibility (`syncVisibility`), and clear stale `mutation.message` when `!mutation.pending && !session?.historyBarrier`.
* End-to-end `mutation_reconstruction` in `src/api/checks/case_journey_browser_check.py` must pass across all families (`advance`, `resident`, `challenge`, `challenge-rebuilt`) and outcomes (`refusal`, `reload-failure`, `committed`, `uncertain`, `malformed-*`).
  * Observable acceptance criteria: `PYTHONPATH=src/core/src:src/agents/src:src/api/src python3 src/api/checks/case_journey_browser_check.py` exits `0`.

## Non-Functional Requirements

* Static accessibility, plain-language content, and form-error association baseline preservation in `src/api/src/zava_forward/api/web/panels.js`.
  * Objective threshold or evaluation condition: `setAttribute("aria-invalid", "true")` count remains `9`, `h("table", {}, ...)` count remains `14`, Epic #149 focus/describedby associations remain intact, `0` banned copy words appear in `web/*.js`, and Vercel Web Interface Guidelines (`W1`) pass with `0` violations on changed lines.
  * Operating condition or verification approach, if needed: Run `test_accessibility_baseline.py`, `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`, and fresh `web-design-guidelines` inspection in `rpi-review`.
  * Observable acceptance criteria: All static accessibility/content tests exit `0` and `rpi-review` records `0` `W1` regressions.
* Lint, formatting, and static type-check cleanliness across `src/core` and `src/api`.
  * Objective threshold or evaluation condition: `0` diagnostics from `ruff check src/core src/api`, `0` formatting diffs from `ruff format --check src/core src/api`, and `0` `mypy` errors in both `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Execute the exact `ruff` and `mypy` commands from the repository root.
  * Observable acceptance criteria: All lint, format, and type-check commands exit `0`.
* Locked test ownership and surgical diff bounds.
  * Objective threshold or evaluation condition: Exact test removals: `none`. Maximum new test additions: `1` unit test method (`test_route_form_blur_change_preserves_refusal_message_while_input_and_select_clear`) in `src/api/tests/test_nomination_screen.py` providing deterministic Node semantic-and-regression proof alongside the existing end-to-end Playwright browser check (`src/api/checks/case_journey_browser_check.py`). Canonical production target: `src/api/src/zava_forward/api/web/panels.js`. Generated targets: `none`.
  * Observable acceptance criteria: In the new Cycle 2 commit on top of the rebased `#130` commits, only `src/api/src/zava_forward/api/web/panels.js`, `src/api/tests/test_nomination_screen.py`, and new `-c2-` `.copilot-tracking/` artifacts are added or modified.

## Acceptance Criteria

* `feat/ux-130-api-routes` is cleanly rebased onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) with both prior `#130` commits preserved.
* `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s src/core/tests -p "test_*nomination*.py" -q` passes (`OK`).
* `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest discover -s src/api/tests -p "test_*nomination*.py" -q` passes (`OK`), including the new focus-blur regression test in `test_nomination_screen.py`.
* `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_resident_api.py src/api/tests/test_accessibility_baseline.py -q` and coupled `test_case_journey.py`, `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`, and `test_programme_coordinator_wcag_230.py` pass (`OK`).
* `PYTHONPATH=src/core/src:src/agents/src:src/api/src python3 src/api/checks/case_journey_browser_check.py` completes end-to-end and exits `0`.
* `python3 -m ruff check src/core src/api && python3 -m ruff format --check src/core src/api` and `(cd src/core && python3 -m mypy) && (cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` exit `0`.
* No `.copilot-tracking/` references appear in production code, test files, or commit messages; all existing `.copilot-tracking/` artifacts remain untouched; local commit uses `8036360+jmservera@users.noreply.github.com`, `Refs #130`, and the Copilot `Co-authored-by` trailer; `git status --short` is empty; no remote push is performed.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c2-plan.md                                                            |
| Phase details                    | .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md                                                 |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-c2-plan-critique.md with Pass disposition (0 PC findings)        |
| Relevant research                | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c2-research.md                                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md (Complete across P01, P02, P03)                       |
| Planning execution and readiness | Complete and ready for implementation                                                                                              |
| Continuation context             | Confirmed automatic RPI Agent session; parent advances automatically to rpi-implement                                               |

## Sources

* `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-c2-research.md`: Primary Cycle 2 evidence (`C1`–`C7`, `W1`) covering `bindCaseMutationForm` focus-blur ordering, original `formFor` parity, `<select>` event contracts, and rebase hunk disjointness.
* `src/api/src/zava_forward/api/web/panels.js`: Workbench panel script defining `bindCaseMutationForm`, `nominationPanel._routeForm`, and `affectedChallengePanel`.
* `src/api/checks/case_journey_browser_check.py`: End-to-end Playwright + axe-core browser check containing `mutation_reconstruction`.
* `src/api/tests/test_nomination_screen.py`: Node-evaluated unit test suite for `nominationPanel` and `nominationPanel._routeForm`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Fetch and rebase `feat/ux-130-api-routes` onto `origin/feat/demo-233-same-home-tensions-0825`

* Intent: Incorporate parent branch commit `6510b6fbc` (`#1784` on `PR #1639`) cleanly beneath the existing `#130` commits without conflict or loss of tracking artifacts.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fetch target parent branch and rebase `feat/ux-130-api-routes` onto `6510b6fbc`

* Requirement and evidence: Caller Step 1 and research `C6`.
* Expected result: `git fetch origin feat/demo-233-same-home-tensions-0825` and `git rebase origin/feat/demo-233-same-home-tensions-0825` replay both prior `#130` commits cleanly on top of `6510b6fbc` while preserving untracked Cycle 2 `-c2-` tracking files.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Restrict `_routeForm` `"change"` clearing to `<select>` controls and add unit regression test

* Intent: Prevent `status.focus()` blur events on `<input>` and `<textarea>` controls from clearing newly recorded refusal messages while preserving `<select>` change handling and `"input"` clearing.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Scope `addEventListener("change", clearInvalid)` to `<select>` elements in `nominationPanel._routeForm`

* Requirement and evidence: Caller Step 2 and research `C1`–`C5`, `C7`, `W1`.
* Expected result: `nominationPanel._routeForm` in `src/api/src/zava_forward/api/web/panels.js` attaches `"change"` -> `clearInvalid` only when `isSelect` (`Boolean(options)`) is true, leaving `"input"` -> `clearInvalid` on all controls.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Add Node unit regression test in `src/api/tests/test_nomination_screen.py`

* Requirement and evidence: Caller Step 2 (`test_nomination_screen.py` verification) and research `C2`, `C3`, `C5`.
* Expected result: `test_route_form_blur_change_preserves_refusal_message_while_input_and_select_clear` verifies that a blur-triggered `"change"` on an edited `<input>` during `status.focus()` after a `409` refusal leaves `mutation.message` and `#...-feedback` intact, while `"input"` on `<input>` and `"change"` on `<select>` clear `aria-invalid` and stale feedback and sync conditional visibility.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Run Focused Tier validation across unit tests, `case_journey_browser_check.py`, `ruff`, and `mypy`

* Intent: Confirm end-to-end browser-check resolution and zero regressions across `src/core` and `src/api` under Focused Tier rules before local commit.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute targeted unit suites, `case_journey_browser_check.py`, `ruff`, and `mypy`

* Requirement and evidence: Caller Step 3 and research `C1`, `C5`–`C7`.
* Expected result: All caller-specified unit tests, coupled `test_case_journey.py` / `test_content_standard.py` / `test_epic149_form_error_summary_associations.py` / `test_programme_coordinator_wcag_230.py` suites, `case_journey_browser_check.py`, `ruff check`, `ruff format --check`, and `mypy` exit `0`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c2-phase-details.md

## Dependencies

* `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`): Target parent branch tip for `PR #1776` rebase in `P01`.
* Local Python 3.12, Node.js, Playwright + headless Chromium, `ruff`, and `mypy`: Required for `P02` unit testing and `P03` end-to-end `case_journey_browser_check.py` + static validation.
* `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-c2-research.md`: Supplies verified root-cause evidence (`C1`–`C7`, `W1`).

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`Pass`, 0 `PC-xxx` findings) | resolved | Candidate verified ready across rebase disjointness, `isSelect`-scoped `"change"` listener semantics, locked test bounds, and Focused Tier validation; include `const PANEL_SUPPORT` alongside `panelOwned` and `bindCaseMutationForm` when slicing `panels.js` in `P02-T02`. |

## Follow-Up Items

* Push rebased `feat/ux-130-api-routes` (`--force-with-lease`) to `PR #1776`, confirm green hosted GitHub Actions `src-api` and browser checks, and run independent exact-head review (`Refs #130`): Excluded from local no-push boundary; owned by repository owner after Review.
* Extend `src/api/checks/nomination_browser_check.py` to scan interactive dual-route nomination acknowledgement and correction disclosures with axe-core 4.10.3: Deferred enhancement outside Cycle 2 bugfix scope.
* Resolve governance open decisions `OD-41` and `OD-42` and obtain human representative comprehension sign-off before Issue `#130` closure: External human governance dependency (`Refs #130`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c2-changes.md
* Ready phase or task: `P01` (`P01-T01`), followed by `P02` (`P02-T01`, `P02-T02`) and `P03` (`P03-T01`)
* Remaining provisional question or blocker: None
