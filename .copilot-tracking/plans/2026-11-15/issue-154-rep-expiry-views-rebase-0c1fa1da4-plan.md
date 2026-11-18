<!-- markdownlint-disable-file -->
# RPI Plan: Issue #154 Rebase Continuation onto 0c1fa1da4

## Task Metadata

* Task ID: issue-154-rep-expiry-views-rebase-0c1fa1da4
* Task slug: issue-154-rep-expiry-views-rebase-0c1fa1da4
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-plan-critique.md

## Executive Summary

This plan executes the **rebase-continuation RPI loop** for `feat/ux-154-rep-expiry-views` (currently at `99a596629`, anchored on `02ab20cac`) onto the newly merged parent tip `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, after PR #1761 `7f83f4749` and PR #1769 `0c1fa1da4` merged), spending zero correction cycles.

Read-only `git merge-tree` verification confirmed that `src/api/src/zava_forward/api/server.py` auto-merges cleanly and `src/api/tests/test_role_endpoint_inventory.py` is the sole merge conflict. During implementation, `git rebase` replays `99a596629` onto `0c1fa1da4`, resolves `src/api/tests/test_role_endpoint_inventory.py` by preserving **both** `0c1fa1da4`'s overdue/unowned/escalated handoff route inventory entries and `99a596629`'s representative task-limited view and session-expiry entries, runs the focused unit test, lint, format, strict `mypy`, and `rename-zava-tests.py` validations, updates the `#154` `.copilot-tracking/` changes, review, and state records with the rebased base (`0c1fa1da4`) and validation evidence, and commits all tracking artifacts locally after post-implementation review without pushing so `git status --short` is empty.

### User Decisions and Requirements Highlights

* Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` and rebase `feat/ux-154-rep-expiry-views` (`99a596629`) onto `0c1fa1da4`.
* Preserve both `0c1fa1da4`'s handoff overdue/escalation endpoint inventory entries and `99a596629`'s representative view/session-expiry endpoint inventory entries in `src/api/tests/test_role_endpoint_inventory.py`.
* Update `.copilot-tracking/` changes and review artifacts for `#154` to record the rebased base (`0c1fa1da4`) and focused validation results, run the specified `unittest`, `ruff`, `mypy`, and `rename-zava-tests.py` gates, and commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.

### What You May Not Know

* Modifying tracked `#154` artifacts prior to running `git rebase` would block `git rebase` with an unstaged-changes error; keeping tracked files unmodified until `git rebase --continue` succeeds ensures a clean single-conflict replay.
* Existing `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json` contains a missing comma between `confirmed_decisions` entries 3 and 4; updating `#154` tracking artifacts post-rebase repairs valid JSON syntax alongside recording the `0c1fa1da4` lineage.

### Unresolved Decisions or Blockers

* None. All merge hunks, route invariants, and validation gates are verified from workspace evidence (`C1`–`C7`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI rebase-continuation loop (`rpi-research`, `rpi-plan`, `rpi-implement`, `rpi-review`) in `/home/azureuser/source/ama-demo-wt/feat-154-rep-expiry-views` on branch `feat/ux-154-rep-expiry-views` (`99a596629`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) (caller prompt).
* Run `git fetch origin feat/demo-164-chat-grounding-provenance-0900` and rebase `feat/ux-154-rep-expiry-views` (`99a596629`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) (caller Scope #1).
* Resolve the single merge conflict in `src/api/tests/test_role_endpoint_inventory.py` by preserving BOTH `0c1fa1da4`'s handoff overdue/escalation endpoint inventory entries (`/api/handoffs/unowned`, `/api/handoffs/escalated`, `/api/handoffs/escalate-overdue`) AND `99a596629`'s representative task-limited view / session-expiry endpoint inventory entries (`/api/cases/ZF-1/representative-view?representative_ref=SYN-REP`, `/api/cases/ZF-1/representative-view`, `"representative-view"`) (caller Scope #2; research `C3`, `C4`).
* Update the `.copilot-tracking/` changes and review artifacts for `#154` to record the rebased base (`0c1fa1da4`) and validation results (caller Scope #3).
* Run focused validation (`test_role_endpoint_inventory.py` plus `#154` representative view/expiry unit test modules `test_representative_expiry_api.py` and `test_resident_journey_design.py`, `src/core` `ruff check`/`ruff format --check`/`mypy`, `src/api` `ruff check`/`ruff format --check`, and `python3 tools/rename-zava-tests.py`) (caller Scope #4).
* Commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, do NOT push, leave a clean frozen working tree (`git status --short` empty), and exit immediately without interactive prompts (caller Scope #5).

## Goals

* Replay `99a596629` cleanly onto `0c1fa1da4` (`origin/feat/demo-164-chat-grounding-provenance-0900`) while preserving 100% of PR #1761, PR #1769, and `#154` C3 endpoint inventory and runtime behavior.
* Prove post-rebase conformance across the focused unit test, role-inventory, linter, formatter, type-checker, and migration-regression suites.
* Leave durable, reconciled `#154` and rebase-continuation `.copilot-tracking/` records committed cleanly with an empty `git status --short` and zero remote writes.

## Scope and Non-Goals

### In Scope

* Rebasing `feat/ux-154-rep-expiry-views` (`99a596629`) onto `0c1fa1da4` and resolving `src/api/tests/test_role_endpoint_inventory.py`.
* Focused validation across `src/api/tests/test_role_endpoint_inventory.py`, `src/api/tests/test_representative_expiry_api.py`, `src/core/tests/test_resident_journey_design.py`, `src/core` (`ruff`, `mypy`), `src/api` (`ruff`, `mypy`), and `tools/rename-zava-tests.py`.
* Updating `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md`, and `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json`, plus committing the rebase-continuation `.copilot-tracking/` artifacts locally.

### Non-Goals

* Modifying `src/api/src/zava_forward/api/web/role-screens.js` or any non-conflicting production Python files beyond git rebase's clean auto-merge of `server.py`.
* Pushing commits to `origin`, creating/updating GitHub PRs, or running full external gate (`tools/rpi-checks.py --all`).

## Functional Requirements

* **FR-REB-01 (Clean Rebase onto `0c1fa1da4` & Union Conflict Resolution)**: `feat/ux-154-rep-expiry-views` contains `0c1fa1da4` in its immediate ancestry (`git merge-base --is-ancestor 0c1fa1da4 HEAD`), `server.py` retains both PR #1761/#1769 routes and `#154` `/api/cases/<id>/representative-view` routes, and `src/api/tests/test_role_endpoint_inventory.py` retains:
  * `GET_ENDPOINTS`: `"/api/handoffs/unowned"`, `"/api/handoffs/escalated"`, and `"/api/cases/ZF-1/representative-view?representative_ref=SYN-REP"`.
  * `POST_ENDPOINTS`: `("/api/handoffs/escalate-overdue", {})` and `("/api/cases/ZF-1/representative-view", {"representative_ref": "SYN-REP", "action": "view_task_briefing"})`.
  * `test_inventory_covers_dynamic_case_actions_added_by_integration`: `"representative-view"` in dynamic case actions tuple.
  * Observable acceptance criteria: `git log` shows rebased feature commit directly atop `0c1fa1da4`, zero conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) remain, and `test_role_endpoint_inventory.py` passes all 24 tests.
* **FR-REB-02 (`#154` Tracking Artifact Lineage & Validation Update)**: `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md`, and `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json` record the rebased parent commit `0c1fa1da4` (`origin/feat/demo-164-chat-grounding-provenance-0900`), the rebased feature commit SHA, and the post-rebase validation results, with valid JSON in both state files.
  * Observable acceptance criteria: `python3 -m json.tool` succeeds on both state JSON files and `#154` changes/review Markdown artifacts explicitly cite `0c1fa1da4` and the post-rebase validation pass.

## Non-Functional Requirements

* **NFR-REB-01 (Focused Validation & Static Hygiene)**: Rebased `src/core`, `src/api`, and repository migration guards pass cleanly.
  * Objective threshold or evaluation condition: Exit code `0` across all caller-specified `unittest`, `ruff check`, `ruff format --check`, `mypy`, and `tools/rename-zava-tests.py` commands, plus `git diff --check`.
  * Operating condition or verification approach: Direct CLI runs in the worktree after `git rebase --continue`.
  * Observable acceptance criteria: Zero test, lint, format, type-check, whitespace, or rename-guard errors.
* **NFR-REB-02 (Clean Local Git Hygiene & Privacy-Safe Author Identity)**: Commits use the repository-local privacy-safe `{id}+{login}@users.noreply.github.com` email resolved from `gh api user` and include `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, with zero unpushed remote side effects and an empty working tree on exit.
  * Objective threshold or evaluation condition: `git status --short` outputs empty string; `git log -1` shows expected `Author` noreply email and `Co-authored-by` trailer; remote branch ref is untouched.
  * Operating condition or verification approach: Verified via `git status --short` and `git --no-pager log -n 3` prior to final response.
  * Observable acceptance criteria: Clean frozen working tree at completion.

## Acceptance Criteria

* AC1: `feat/ux-154-rep-expiry-views` is rebased onto `0c1fa1da4` (`origin/feat/demo-164-chat-grounding-provenance-0900`) with `src/api/tests/test_role_endpoint_inventory.py` preserving both `0c1fa1da4`'s handoff inventory entries and `99a596629`'s `representative-view` entries.
* AC2: Focused unit tests (`test_role_endpoint_inventory.py`, `test_representative_expiry_api.py`, `test_resident_journey_design.py`, `test_resident_decisions.py`, `test_resident_showcase.py`, `test_handoff_escalation_api_83.py`), `src/core` (`ruff check`, `ruff format --check`, `mypy`), `src/api` (`ruff check`, `ruff format --check`, plus targeted `#154` `mypy` on `resident_demo/app.py` and `test_representative_expiry_api.py`), and `python3 tools/rename-zava-tests.py` all pass (exit `0`).
* AC3: `#154` `.copilot-tracking/` changes, review, and state artifacts plus child `issue-154-rep-expiry-views-rebase-0c1fa1da4` RPI artifacts accurately record the `0c1fa1da4` base, rebased feature SHA, validation results, and single-pass `rpi-review` outcome.
* AC4: All changes are committed locally with privacy-safe noreply email and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, nothing is pushed, and `git status --short` is empty.

## Test Ownership and Change Budget Lock

* Canonical production targets:
  * `src/api/src/zava_forward/api/server.py` (clean git 3-way auto-merge during rebase only; zero manual code changes)
* Canonical test targets:
  * `src/api/tests/test_role_endpoint_inventory.py` (single rebase conflict resolution combining `0c1fa1da4` and `99a596629` entries)
* Generated targets: `none`
* Exact test removals: `none`
* Maximum test files touched/added: `1` (`src/api/tests/test_role_endpoint_inventory.py` during rebase conflict resolution)
* Semantic vs regression coverage:
  * Semantic coverage: `RoleEndpointInventory` route-completeness check (`test_inventory_covers_every_route_in_the_server`), dynamic case action check (`test_inventory_covers_dynamic_case_actions_added_by_integration`), all-role matrix (`test_every_role_against_every_endpoint`), and `#154` representative view/expiry suites (`test_representative_expiry_api.py`, `test_resident_journey_design.py`).
  * Regression coverage: `ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, plus `tools/rename-zava-tests.py`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-plan.md                                             |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-phase-details.md                                  |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-plan-critique.md with Pass disposition (0 findings) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-research.md                                      |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-changes.md is created by implementation           |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                 |
| Continuation context             | Parent return to confirmed automatic `RPI Agent`                                                                                   |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-research.md`: Verifies `02ab20cac..0c1fa1da4` commits, `git merge-tree` single-file conflict in `test_role_endpoint_inventory.py`, clean `server.py` auto-merge, and `#154` state JSON comma fix (`C1`–`C7`).
* `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md` & `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md`: Parent `#154` tracking artifacts to update with rebased base `0c1fa1da4` and post-rebase validation results.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase Branch onto 0c1fa1da4 and Resolve Role Endpoint Inventory Conflict

* Intent: Replay `99a596629` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) with privacy-safe git identity configured and resolve the single conflict in `src/api/tests/test_role_endpoint_inventory.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Configure local privacy-safe git email, run git rebase onto 0c1fa1da4, and resolve test_role_endpoint_inventory.py

* Requirement and evidence: `FR-REB-01`, `NFR-REB-02`; research `C1`–`C5`
* Expected result: `feat/ux-154-rep-expiry-views` sits cleanly atop `0c1fa1da4` with both handoff and `representative-view` entries in `src/api/tests/test_role_endpoint_inventory.py` and zero conflict markers.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Execute Focused Rebase Validation Gates

* Intent: Verify endpoint inventory, representative task-limited view/expiry behavior, static linting/formatting/typing, and Zava rename regression checks on the rebased tree.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run unittest, ruff, mypy, and rename-zava-tests.py across rebased tree

* Requirement and evidence: `FR-REB-01`, `NFR-REB-01`; research `C3`–`C6`
* Expected result: `test_role_endpoint_inventory.py`, `test_representative_expiry_api.py`, `test_resident_journey_design.py`, `src/core` (`ruff check`, `ruff format --check`, `mypy`), `src/api` (`ruff check`, `ruff format --check`, plus targeted `#154` `mypy`), and `tools/rename-zava-tests.py` all exit `0`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Update #154 Tracking Artifacts and Prepare Post-Review Clean Local Commit

* Intent: Record the rebased base (`0c1fa1da4`), rebased feature SHA, and focused validation results across `#154` and child rebase-continuation `.copilot-tracking/` artifacts, then commit cleanly after single-pass `rpi-review` state finalization without pushing.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Update #154 changes, review, and state records and record child implementation changes

* Requirement and evidence: `FR-REB-02`, `NFR-REB-02`; research `C7`
* Expected result: `#154` changes, review, and state artifacts plus `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-changes.md` record `0c1fa1da4`, the rebased feature SHA, and validation results cleanly, ready for `rpi-review` and final clean tracking commit leaving `git status --short` empty.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-phase-details.md

## Dependencies

* Remote branch `origin/feat/demo-164-chat-grounding-provenance-0900` fetched at `0c1fa1da4`: Verified in research (`C1`).
* Tracked working tree clean before `git rebase`: Verified (`git status --short` has no modified tracked files; child `.copilot-tracking/` artifacts use distinct untracked filenames).

## Critique Disposition

Single-pass `rpi-plan-critique` completed on 2026-11-15 with verdict **Pass** (`0` `PC-xxx` findings).

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 (`Pass`, `none`)   | resolved    | Zero blocking or non-blocking findings; rebase explicitly targets `0c1fa1da4` (`origin/feat/demo-164-chat-grounding-provenance-0900`). |

## Follow-Up Items

* Render task-limited representative view and expired/held renewal cards in `ResidentDemo` UI (`src/api/src/zava_forward/api/resident_demo/web/`) — separate frontend slice outside backend rebase scope.
* Complete remaining parent Issue #154 sibling criteria (`C2` resident portal journey screens `J1`–`J6` and `C5` empirical resident/representative usability validation under Issue #155).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-changes.md
* Ready phase or task: Complete (`P01`–`P03` completed; ready for `rpi-review`)
* Remaining provisional question or blocker: none
