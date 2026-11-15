<!-- markdownlint-disable-file -->
# RPI Plan: Pass Node Test Payloads via Stdin and Trim Redundant Nomination Panel Formatting

## Task Metadata

* Task ID: nomination-api-routes-130-c3
* Task slug: nomination-api-routes-130-c3
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-c3-plan-critique.md

## Executive Summary

This Cycle 3 plan resolves the sole remaining CI failure on pull request `#1776` (`feat/ux-130-api-routes`, Issue `#130`), where `test_case_journey.CaseJourney.test_quality_errors_and_manual_action_pending_siblings` raised `OSError: [Errno 7] Argument list too long: 'node'` (`E2BIG`) when passing concatenated web bundles (`DOM + shipped_helpers() + ops.js + panels.js`) via `argv` (`["node", "-e", script]`). Passing JavaScript payloads over `stdin` (`["node", "-"]` and `["node", "--unhandled-rejections=strict", "-"]` with `input=...`) across all 22 `subprocess.run` Node invocations in `src/api/tests/test_case_journey.py` permanently removes Linux's `131,072`-byte per-argument `MAX_ARG_STRLEN` ceiling, while a surgical behavior-preserving formatting trim inside the `#130`-owned nomination section of `src/api/src/zava_forward/api/web/panels.js` keeps the module concise and conflict-free against stacked parent `PR #1639` (`origin/feat/demo-233-same-home-tensions-0825`).

### User Decisions and Requirements Highlights

* **Eliminate `MAX_ARG_STRLEN` (`E2BIG`) in `test_case_journey.py`**: Pass `script` via `stdin` (`["node", "-"]` with `input=script`) instead of `-e script` on `argv` in `test_quality_errors_and_manual_action_pending_siblings` and across the remaining concatenated-JS `subprocess.run` Node calls in `src/api/tests/test_case_journey.py` so `execve` never hits `131,072` bytes.
* **Keep `panels.js` concise without behavioral or merge regressions**: Trim redundant comments and verbose multiline object/option-array formatting strictly inside `#130`-owned nomination helpers in `src/api/src/zava_forward/api/web/panels.js` without changing runtime behavior, accessibility associations, content-standard copy, test slice anchors, or stacked-parent merge cleanliness.
* **Focused Tier verification and clean local commit**: Verify `test_case_journey.py`, `test_accessibility_baseline.py`, coupled nomination/Epic #149/content-standard suites, `ruff check .`, `ruff format --check .`, and `mypy` from `src/api`, preserve all Cycle 1 (`c1`) and Cycle 2 (`c2`) `.copilot-tracking/` artifacts unchanged, and commit cleanly on `feat/ux-130-api-routes` with `Refs #130` and the Copilot `Co-authored-by` trailer without pushing.

### What You May Not Know

* **Why CI hit `E2BIG` (`>131,072` bytes) while local `HEAD` (`f53340e8f`) passed at `129,031` bytes**: Linux enforces `MAX_ARG_STRLEN = PAGE_SIZE * 32 = 131,072` bytes on every single `argv` string passed to `execve`. On `f53340e8f`, `test_quality_errors_and_manual_action_pending_siblings` stood just `2,041` bytes below that limit; meanwhile, base branch `origin/feat/demo-233-same-home-tensions-0825` advanced by commit `50bd5acc0` (`#1786`), adding net growth in `actForm` and `residentPanel` inside `panels.js` that pushed GitHub Actions' `refs/pull/1776/merge` checkout past `131,072` bytes.
* **Merge-clean boundary in `panels.js`**: Commit `50bd5acc0` on `origin/feat/demo-233-same-home-tensions-0825` modifies only `actForm` and `residentPanel` near the top of `panels.js`, completely disjoint from `#130`'s `nominationPanel` and `nominationPanel._routeForm` section further down the file. Keeping conciseness trims strictly inside `nominationPanel` / `nominationPanel._explanationView` / `nominationPanel._routeForm` guarantees zero merge conflicts on `PR #1776`.
* **Shared-worktree `PYTHONPATH` safeguard**: In this shared host Python environment, an editable `.pth` entry points `zava_forward.api` at a removed sibling worktree, so running `unittest` from `src/api` requires `src` on `PYTHONPATH` (`PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests`) to test this worktree cleanly without mutating shared `pip` state for other sessions.

### Unresolved Decisions or Blockers

* No blockers exist for local Cycle 3 execution. Pushing `feat/ux-130-api-routes` to `origin` so hosted GitHub Actions confirms `10/10` green checks on `PR #1776`, running independent exact-head review, and completing external governance items (`OD-41`, `OD-42`) remain post-Review owner follow-ups.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan` with single-pass `rpi-plan-critique`, `implement`, `review`), writing Cycle 3 (`c3`) dated artifacts under `.copilot-tracking/` while preserving all `c1` and `c2` `.copilot-tracking/` artifacts unchanged (caller prompt).
* Update `src/api/tests/test_case_journey.py` so `test_quality_errors_and_manual_action_pending_siblings` and the other `subprocess.run(["node", ..., "-e", ...])` calls in `src/api/tests/test_case_journey.py` pass JavaScript source via `stdin` (`["node", "-"]` or `["node", "--unhandled-rejections=strict", "-"]` with `input=...`) rather than `-e script` on `argv`, eliminating Linux `MAX_ARG_STRLEN` (`131,072` bytes) `E2BIG` failures while preserving module-level `DOM`, `WEB`, and `shipped_helpers` imported by `test_safety_panel_ux.py` (caller prompt; research `C1`–`C5`).
* Keep `src/api/src/zava_forward/api/web/panels.js` concise by trimming redundant comments and verbose multiline object/option-array whitespace inside `#130`-owned `nominationPanel` / `nominationPanel._explanationView` / `nominationPanel._routeForm` without changing runtime behavior, test slice anchors, Epic #149 focus/describedby invariants, WCAG 2.2 / Web Interface Guidelines (`W1`) compliance, or merge disjointness with `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`) (caller prompt; research `C6`–`C8`, `W1`).
* Verify from `/home/azureuser/source/ama-demo-wt/feat-130-api-routes/src/api` that `tests/test_case_journey.py` and `tests/test_accessibility_baseline.py` (plus coupled nomination, Epic #149, content-standard, and safety-panel tests) pass under `unittest -v`, and that `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` exits `0` (caller prompt; research `C5`, `C7`, `C8`).
* Configure repository-local privacy-safe Git email via `gh api user` (`{id}+{login}@users.noreply.github.com`), commit cleanly on `feat/ux-130-api-routes` with `Refs #130` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push from inside the session (caller prompt; AMA Branch Workflow).

## Goals

* Eliminate `execve` `MAX_ARG_STRLEN` (`131,072`-byte) `OSError: [Errno 7] Argument list too long: 'node'` failures across all Node-evaluated tests in `src/api/tests/test_case_journey.py`, including payloads well above `131,072` UTF-8 bytes.
* Reduce redundant comment and formatting verbosity in `#130`'s `nominationPanel` section of `src/api/src/zava_forward/api/web/panels.js` with zero behavioral, accessibility, content-standard, slice-anchor, or stacked-branch merge impact.
* Verify unit, accessibility, lint, format, and static type checks cleanly from `src/api` and record a clean local Cycle 3 commit on `feat/ux-130-api-routes` without pushing.

## Scope and Non-Goals

### In Scope

* Converting all 22 `subprocess.run(["node", ..., "-e", ...])` invocations in `src/api/tests/test_case_journey.py` to pass JavaScript source via `stdin` (`"-"`, `input=...`), preserving existing `text=True`, `capture_output=True`, `timeout=...`, `check=...`, and `--unhandled-rejections=strict` options.
* Adding `1` focused regression test in `src/api/tests/test_case_journey.py` verifying that executing `DOM + shipped_helpers() + ops.js + panels.js` padded well beyond Linux's `131,072`-byte `MAX_ARG_STRLEN` limit succeeds via `stdin`.
* Trimming redundant comments and verbose multiline descriptor formatting strictly within `#130`-owned `nominationPanel`, `nominationPanel._explanationView`, and `nominationPanel._routeForm` in `src/api/src/zava_forward/api/web/panels.js`.
* Running Focused Tier unit, WCAG baseline, coupled nomination/content/Epic #149, Ruff, and Mypy checks from `src/api`, recording Cycle 3 `.copilot-tracking/` artifacts, and committing locally on `feat/ux-130-api-routes`.

### Non-Goals

* Pushing any commit or branch to `origin` or rebasing/rewriting existing branch commits.
* Modifying, renaming, or deleting any Cycle 1 (`c1`) or Cycle 2 (`c2`) `.copilot-tracking/` artifacts.
* Editing `actForm` or `residentPanel` in `src/api/src/zava_forward/api/web/panels.js` (touched by `50bd5acc0` on `origin/feat/demo-233-same-home-tensions-0825`) or altering any runtime UI/API behavior.
* Modifying out-of-scope test files in `src/api/tests/` that already read JS from disk via `fs.readFileSync` or evaluate `<3 KB` slices.

## Functional Requirements

* Every `subprocess.run` Node invocation in `src/api/tests/test_case_journey.py` (including `evaluate()`, standard `["node", "-"]` harnesses, and the `--unhandled-rejections=strict` harness) must supply JavaScript source through `input=...` on `stdin` with `"-"` rather than `-e <script>` in `argv`.
  * Observable acceptance criteria: `0` occurrences of `"-e"` remain in `src/api/tests/test_case_journey.py`, module-level `DOM`, `WEB`, and `shipped_helpers` remain intact for `test_safety_panel_ux.py`, and all existing plus `>131,072`-byte padded Node executions in `test_case_journey.py` exit `0`.
* Conciseness edits in `src/api/src/zava_forward/api/web/panels.js` must preserve identical DOM construction, event listeners (`isSelect`-guarded `"change"` and universal `"input"`), refusal/error handling, copy literals, and slice markers (`const panelOwned = `, `\nconst PANEL_SUPPORT`, `function bindCaseMutationForm`, `function actForm`, `function captureChallengeDrafts`, `function nominationPanel`, `\nfunction affectedChallengePanel`, `  const residentForm = `, `  const serviceForm`, `  const formFor = `, `  const staff`).
  * Observable acceptance criteria: `panels.js` byte size decreases while `test_case_journey.py`, `test_nomination_screen.py`, `test_nomination_api_routes.py`, `test_epic149_form_error_summary_associations.py`, `test_accessibility_baseline.py`, and `test_content_standard.py` all exit `0`.

## Non-Functional Requirements

* Static accessibility, Epic #149 error-focus association, plain-language content, and Web Interface Guidelines (`W1`) preservation in `src/api/src/zava_forward/api/web/panels.js`.
  * Objective threshold or evaluation condition: `setAttribute("aria-invalid", "true")` count across `web/*.js` remains `9`, `input.focus()` remains within `±4` lines of `input.setAttribute("aria-invalid", "true")` in `panels.js`, `"aria-describedby": status.id` and `tabindex: -1` remain intact, `0` banned content-standard words appear, and fresh `web-design-guidelines` review reports `0` violations on changed web lines.
  * Operating condition or verification approach, if needed: Run `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_content_standard.py`, and fresh `web-design-guidelines` check during `rpi-review`.
  * Observable acceptance criteria: All static accessibility/content suites pass (`0` failures) and `rpi-review` records `0` `W1` regressions.
* Lint, formatting, and static type-check cleanliness in `src/api`.
  * Objective threshold or evaluation condition: `0` `ruff check .` diagnostics, `0` `ruff format --check .` diffs, and `0` `mypy` errors when run from `src/api`.
  * Operating condition or verification approach, if needed: Execute `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` from `/home/azureuser/source/ama-demo-wt/feat-130-api-routes/src/api`.
  * Observable acceptance criteria: Command exits `0`.
* Locked test ownership and conflict-free diff bounds.
  * Objective threshold or evaluation condition: Exact test removals: `none`. Maximum new test additions: `1` unit test method (`test_node_stdin_handles_scripts_above_linux_max_arg_strlen`) in `src/api/tests/test_case_journey.py` providing both regression proof (`len(script.encode("utf-8")) > 131_072` reproducing and defeating the CI merge-commit `E2BIG` boundary) and semantic proof (executing `DOM + shipped_helpers() + ops.js + panels.js` assertions via `["node", "-"]` stdin). Canonical targets: `src/api/tests/test_case_journey.py` and `#130`-owned nomination helpers in `src/api/src/zava_forward/api/web/panels.js`. Generated targets: `none`.
  * Observable acceptance criteria: `git diff HEAD -- src/api/src/zava_forward/api/web/panels.js` touches only lines inside `nominationPanel` / `_explanationView` / `_routeForm` (disjoint from `50bd5acc0`), and only those two repository source/test files plus new `-c3-` `.copilot-tracking/` files are added or modified.

## Acceptance Criteria

* All 22 `subprocess.run` Node invocations in `src/api/tests/test_case_journey.py` pass JavaScript source via `stdin` (`"-"`, `input=...`), with `0` `"-e"` invocations remaining and `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` proving clean execution above `131,072` UTF-8 bytes.
* `src/api/src/zava_forward/api/web/panels.js` trims redundant comment/multiline whitespace strictly within `#130`'s `nominationPanel` helpers without changing runtime behavior or overlapping `origin/feat/demo-233-same-home-tensions-0825` (`50bd5acc0`).
* From `/home/azureuser/source/ama-demo-wt/feat-130-api-routes/src/api`, `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_case_journey.py tests/test_accessibility_baseline.py -v` passes (`OK`), and coupled `tests/test_nomination_screen.py`, `tests/test_nomination_api_routes.py`, `tests/test_epic149_form_error_summary_associations.py`, `tests/test_content_standard.py`, and `tests/test_safety_panel_ux.py` also pass (`OK`).
* From `/home/azureuser/source/ama-demo-wt/feat-130-api-routes/src/api`, `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` passes (`exit 0`).
* All Cycle 1 (`c1`) and Cycle 2 (`c2`) `.copilot-tracking/` artifacts remain unmodified (`git status --short` shows zero edits to `-c2-`, `-ci-fix-`, or initial `-130-` files); no `.copilot-tracking/` references appear in code, tests, or commit message; local commit on `feat/ux-130-api-routes` uses `{id}+{login}@users.noreply.github.com` from `gh api user`, `Refs #130`, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; `git status --short` ends empty; no remote push is performed.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/nomination-api-routes-130-c3-plan.md                                                            |
| Phase details                    | .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md                                                 |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/nomination-api-routes-130-c3-plan-critique.md with Pass disposition (0 PC findings)    |
| Relevant research                | .copilot-tracking/research/2026-11-15/nomination-api-routes-130-c3-research.md                                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md (Complete across P01, P02, P03)                       |
| Planning execution and readiness | Complete and ready for implementation                                                                                              |
| Continuation context             | Confirmed automatic RPI Agent session; parent advances automatically to rpi-implement                                              |

## Sources

* `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-c3-research.md`: Primary Cycle 3 evidence (`C1`–`C8`, `W1`) covering CI run `43707070068` (`E2BIG`), `MAX_ARG_STRLEN` (`131,072` B), all 22 `node` calls in `test_case_journey.py`, cross-test imports, `50bd5acc0` diff boundaries, and Epic #149 / slice invariants.
* `src/api/tests/test_case_journey.py`: Shipped-JavaScript case-journey test suite containing `evaluate()` and 21 inline `subprocess.run` Node harnesses.
* `src/api/src/zava_forward/api/web/panels.js`: Workbench panels script containing `nominationPanel`, `nominationPanel._explanationView`, and `nominationPanel._routeForm`.
* `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_epic149_form_error_summary_associations.py`: Static WCAG 2.2 and form-error association checks over `web/*.js`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Pass JavaScript payloads via `stdin` across `src/api/tests/test_case_journey.py` and add `MAX_ARG_STRLEN` regression test

* Intent: Eliminate `execve` `MAX_ARG_STRLEN` (`131,072`-byte) `E2BIG` failures in `test_quality_errors_and_manual_action_pending_siblings` and every other Node subprocess in `test_case_journey.py`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Convert all 22 `subprocess.run` Node invocations in `src/api/tests/test_case_journey.py` from `-e <script>` on `argv` to `"-"` with `input=<script>`

* Requirement and evidence: Caller Requirement 1 and research `C1`–`C5`.
* Expected result: `evaluate()`, all 20 standard `["node", "-e", script]` harnesses (including `test_quality_errors_and_manual_action_pending_siblings`), and the `["node", "--unhandled-rejections=strict", "-e", script]` harness pass scripts via `input=...` to `["node", "-"]` or `["node", "--unhandled-rejections=strict", "-"]`, preserving `text=True`, `capture_output=True`, `timeout=...`, `check=...`, and exported `DOM`, `WEB`, and `shipped_helpers`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add `>131,072`-byte `MAX_ARG_STRLEN` stdin regression test in `src/api/tests/test_case_journey.py`

* Requirement and evidence: Caller Requirement 1 (`execve` never hits `MAX_ARG_STRLEN` = `131,072` bytes) and research `C1`–`C3`, `C6`.
* Expected result: `test_node_stdin_handles_scripts_above_linux_max_arg_strlen` pads `DOM + shipped_helpers() + ops.js + panels.js` above `140,000` UTF-8 bytes (`> 131,072`) and verifies `["node", "-"]` with `input=script` executes shipped-JS assertions cleanly with exit code `0`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Trim redundant comments and formatting verbosity in `#130` nomination helpers inside `panels.js`

* Intent: Keep `src/api/src/zava_forward/api/web/panels.js` concise without changing runtime behavior, accessibility invariants, slice boundaries, or merge cleanliness with `origin/feat/demo-233-same-home-tensions-0825`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Compact redundant comment and multiline descriptor formatting inside `nominationPanel` and `nominationPanel._routeForm`

* Requirement and evidence: Caller Requirement 1 (concise `panels.js`) and research `C6`–`C8`, `W1`.
* Expected result: Redundant explanatory comments and expanded single-key-per-line field/option arrays inside `nominationPanel`, `nominationPanel._explanationView`, and `nominationPanel._routeForm` are compacted cleanly while keeping all runtime logic, copy strings, Epic #149 `±4`-line focus window, `9` `aria-invalid` sites, slice boundary anchors, and `actForm`/`residentPanel` regions untouched.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Run Focused Tier validation from `src/api` across unit, WCAG baseline, lint, format, and type checks

* Intent: Prove complete test, accessibility, Ruff, and Mypy cleanliness from `/home/azureuser/source/ama-demo-wt/feat-130-api-routes/src/api` before creating the clean local Cycle 3 commit.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute targeted `unittest`, `ruff check`, `ruff format --check`, and `mypy` suites from `src/api`

* Requirement and evidence: Caller Requirement 2 and research `C5`, `C7`, `C8`.
* Expected result: `tests/test_case_journey.py` and `tests/test_accessibility_baseline.py` (`-v`), coupled `test_nomination_screen.py` / `test_nomination_api_routes.py` / `test_epic149_form_error_summary_associations.py` / `test_content_standard.py` / `test_safety_panel_ux.py`, and `python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` all exit `0`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/nomination-api-routes-130-c3-phase-details.md

## Dependencies

* Local Python 3.12, Node.js, `ruff`, and `mypy`: Required for `P01`–`P03` implementation and verification from `src/api`.
* `.copilot-tracking/research/2026-11-15/nomination-api-routes-130-c3-research.md`: Supplies verified root-cause, cross-test import, static-anchor, and stacked-branch merge evidence (`C1`–`C8`, `W1`).

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`Pass`, 0 `PC-xxx` findings) | resolved | Candidate verified ready across all 22 `subprocess.run` Node sites, `>131,072`-byte regression test bounds, `50bd5acc0` merge disjointness, Epic #149/WCAG/slice invariants, and Focused Tier validation; preserve `evaluate(expression: str)` 1-arg signature with `check=True` in `P01-T01` and single-line `panelOwned(` calls in `P02-T01`. |

## Follow-Up Items

* Push `feat/ux-130-api-routes` to `origin`, confirm `10/10` green hosted GitHub Actions checks on `PR #1776` (including `src-api` on `refs/pull/1776/merge` with `50bd5acc0`), and run independent exact-head review (`Refs #130`): Excluded from session by explicit caller no-push boundary; owned by repository owner.
* Extend `src/api/checks/nomination_browser_check.py` to run axe-core 4.10.3 over expanded dual-route nomination acknowledgement and correction `<details>` disclosures: Deferred post-CI enhancement from earlier cycles.
* Resolve external governance open decisions `OD-41` and `OD-42` and record human representative comprehension sign-off before Issue `#130` closure: External human governance dependency (`Refs #130`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/nomination-api-routes-130-c3-changes.md
* Ready phase or task: `P01` (`P01-T01`, `P01-T02`), followed by `P02` (`P02-T01`) and `P03` (`P03-T01`)
* Remaining provisional question or blocker: None
