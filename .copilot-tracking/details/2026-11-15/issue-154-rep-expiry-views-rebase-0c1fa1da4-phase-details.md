<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #154 Rebase Continuation onto 0c1fa1da4

## Metadata

* Task ID: issue-154-rep-expiry-views-rebase-0c1fa1da4
* Task slug: issue-154-rep-expiry-views-rebase-0c1fa1da4
* Related plan: .copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-research.md (`C1`–`C7`), `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md`

## Phase Index

| Phase ID | Name                                                                          | Status | Detail sections |
|----------|-------------------------------------------------------------------------------|--------|-----------------|
| P01      | Rebase Branch onto 0c1fa1da4 and Resolve Role Endpoint Inventory Conflict     | Ready  | P01, P01-T01    |
| P02      | Execute Focused Rebase Validation Gates                                       | Ready  | P02, P02-T01    |
| P03      | Update #154 Tracking Artifacts and Prepare Post-Review Clean Local Commit     | Ready  | P03, P03-T01    |

<!-- rpi:phase id=P01 -->
## P01: Rebase Branch onto 0c1fa1da4 and Resolve Role Endpoint Inventory Conflict

### Context

Branch `feat/ux-154-rep-expiry-views` currently has single feature commit `99a596629` atop `02ab20cac`. Parent branch `origin/feat/demo-164-chat-grounding-provenance-0900` advanced by two commits (`7f83f4749` PR #1761 and `0c1fa1da4` PR #1769). Read-only `git merge-tree --write-tree --messages 0c1fa1da4 99a596629` (`C2`) confirmed `src/api/src/zava_forward/api/server.py` auto-merges cleanly and `src/api/tests/test_role_endpoint_inventory.py` is the only conflict.

### Intent

Replay `99a596629` onto `0c1fa1da4` cleanly, resolving `src/api/tests/test_role_endpoint_inventory.py` with the union of both sides' endpoint inventory entries while preserving privacy-safe noreply git author/committer configuration.

### Boundaries

* Included: `gh api user` local git email verification/configuration, `git fetch origin feat/demo-164-chat-grounding-provenance-0900`, `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, conflict resolution in `src/api/tests/test_role_endpoint_inventory.py`, and `GIT_EDITOR=true git rebase --continue`.
* Excluded: Manual edits to `server.py`, `role-screens.js`, or any tracked `.copilot-tracking/` file prior to `git rebase --continue`.

### Likely Targets

* `src/api/tests/test_role_endpoint_inventory.py`: Resolve the single rebase merge conflict across `GET_ENDPOINTS` and `POST_ENDPOINTS` while keeping `"representative-view"` in `test_inventory_covers_dynamic_case_actions_added_by_integration`.

### Dependencies

* Clean tracked working tree (`git diff --quiet` and `git diff --cached --quiet`).

### Validation Expectations

* `git merge-base --is-ancestor 0c1fa1da4 HEAD` exits `0`.
* Zero conflict markers in `src/api/tests/test_role_endpoint_inventory.py` or `src/api/src/zava_forward/api/server.py` (`git diff --check` clean).

### Completion Evidence

* Rebased feature commit SHA recorded atop `0c1fa1da4`.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure local privacy-safe git email, run git rebase onto 0c1fa1da4, and resolve test_role_endpoint_inventory.py

#### Context

`0c1fa1da4` added `"/api/handoffs/unowned"` and `"/api/handoffs/escalated"` to `GET_ENDPOINTS` and `("/api/handoffs/escalate-overdue", {})` to `POST_ENDPOINTS` (`C3`). `99a596629` added `"/api/cases/ZF-1/representative-view?representative_ref=SYN-REP"` to `GET_ENDPOINTS`, `("/api/cases/ZF-1/representative-view", {"representative_ref": "SYN-REP", "action": "view_task_briefing"})` to `POST_ENDPOINTS`, and `"representative-view"` to `test_inventory_covers_dynamic_case_actions_added_by_integration` (`C4`).

#### Intent

Complete the git rebase onto `0c1fa1da4` with both endpoint sets intact in `src/api/tests/test_role_endpoint_inventory.py`.

#### Boundaries

* Included: Local `git config --local user.email` verification via `gh api user`, `git rebase`, `edit` of `src/api/tests/test_role_endpoint_inventory.py`, `git add src/api/tests/test_role_endpoint_inventory.py`, and `GIT_EDITOR=true git rebase --continue`.
* Excluded: `git push` or any remote mutation.

#### Likely Targets

* `src/api/tests/test_role_endpoint_inventory.py`: Keep `"/api/handoffs/unowned", "/api/handoffs/escalated"` on line 22, `"/api/cases/ZF-1/representative-view?representative_ref=SYN-REP"` at the end of `GET_ENDPOINTS` before `"/api/nothing"`, `("/api/handoffs/escalate-overdue", {})` on the first line of `POST_ENDPOINTS`, `("/api/cases/ZF-1/representative-view", {"representative_ref": "SYN-REP", "action": "view_task_briefing"})` in `POST_ENDPOINTS`, and `"representative-view"` in `test_inventory_covers_dynamic_case_actions_added_by_integration`.

#### Dependencies

* none

#### Validation Expectations

* `git --no-pager log -n 2 --oneline` shows the rebased feature commit directly atop `0c1fa1da4`.

#### Completion Evidence

* Clean rebase completion and `git diff --check` exit `0`.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Execute Focused Rebase Validation Gates

### Context

Caller Scope #4 specifies exact focused validation checks covering the merged endpoint inventory, `#154` representative view and session-expiry unit/HTTP tests, `src/core` and `src/api` linting/formatting/type-checking, and the Zava migration regression script.

### Intent

Confirm zero semantic, typing, lint, formatting, or naming regressions after rebasing onto `0c1fa1da4`.

### Boundaries

* Included: Running `unittest` (`test_role_endpoint_inventory.py`, `test_representative_expiry_api.py`, `test_resident_journey_design.py`), `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/api`, and `python3 tools/rename-zava-tests.py`.
* Excluded: Modifying unrelated test modules or invoking cloud/SQL external gates.

### Likely Targets

* Read-only validation execution across `src/core`, `src/api`, and `tools/rename-zava-tests.py`.

### Dependencies

* P01

### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/api/tests/test_role_endpoint_inventory.py src/api/tests/test_representative_expiry_api.py src/core/tests/test_resident_journey_design.py -q` exits `0`.
* `cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy` exits `0`.
* `cd src/api && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy src/zava_forward/api/resident_demo/app.py tests/test_representative_expiry_api.py` exits `0` (following caller Scope #4 for `src/api` ruff checks plus targeted `#154` strict typing).
* `python3 tools/rename-zava-tests.py` exits `0`.

### Completion Evidence

* Exact test counts and exit `0` outputs recorded in `.copilot-tracking/` changes artifacts.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run unittest, ruff, mypy, and rename-zava-tests.py across rebased tree

#### Context

Merged `server.py` now includes PR #1761 (`chat_eval`), PR #1769 (`/api/handoffs/unowned`, `/api/handoffs/escalated`, `/api/handoffs/escalate-overdue`), and `#154` (`/api/cases/<id>/representative-view`). Running `RoleEndpointInventory` exercises every staff/contractor/mystery role against the combined route table.

#### Intent

Prove all combined routes, `#154` representative expiry/view tests, static checks, and rename regression tests pass on the rebased tree.

#### Boundaries

* Included: CLI execution of all four validation command groups.
* Excluded: Unrelated test edits.

#### Likely Targets

* `src/api/tests/test_role_endpoint_inventory.py`
* `src/api/tests/test_representative_expiry_api.py`
* `src/core/tests/test_resident_journey_design.py`
* `tools/rename-zava-tests.py`

#### Dependencies

* P01-T01

#### Validation Expectations

* All validation commands return exit code `0`.

#### Completion Evidence

* Captured CLI test counts and zero-error `ruff`/`mypy`/`rename-zava-tests.py` outputs.

#### Unresolved Items

* none

<!-- rpi:phase id=P03 -->
## P03: Update #154 Tracking Artifacts and Prepare Post-Review Clean Local Commit

### Context

Caller Scope #3 and #5 require updating `#154`'s `.copilot-tracking/` changes and review artifacts to record the rebased base (`0c1fa1da4`) and validation results, then committing cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing and leaving `git status --short` empty. Because automatic `RPI Agent` runs single-pass `rpi-review` and transitions the state JSON to `Follow-up` after `rpi-implement`, executing the final tracking commit immediately after the post-Review state write ensures every `.copilot-tracking/` artifact (including the final review log and state JSON) is committed and `git status --short` is empty at exit.

### Intent

Update `#154` tracking records (`.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md`, and `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json`), record `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-changes.md`, reconcile plan/detail markers before `rpi-review`, and commit the finalized tracking tree cleanly after `rpi-review` completes.

### Boundaries

* Included: `.copilot-tracking/` `#154` changes/review/state updates (including JSON comma fix at line 35 of `issue-154-rep-expiry-views-state.json`), child rebase-continuation changes/plan/state reconciliation, JSON syntax verification, and clean local `git commit` with `Co-authored-by` trailer after `rpi-review` records its outcome.
* Excluded: `git push`, `git commit --amend` on already-committed history without need, or touching production files in `P03`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`: Add Rebase Continuation (`0c1fa1da4`) section and validation record.
* `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md`: Record rebased base `0c1fa1da4`, rebased feature commit SHA, and post-rebase validation summary per caller Scope #3.
* `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json`: Repair missing comma and record rebased base `0c1fa1da4` provenance.
* `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-changes.md`: Record full `P01`–`P03` rebase-continuation execution evidence.

### Dependencies

* P02

### Validation Expectations

* `python3 -m json.tool .copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json >/dev/null` and `python3 -m json.tool .copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-state.json >/dev/null` exit `0`.
* After post-Review state finalization and tracking commit, `git status --short` is empty and `git log -1` carries `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.

### Completion Evidence

* Updated `#154` and child `.copilot-tracking/` artifacts validated and committed cleanly on `feat/ux-154-rep-expiry-views`.

### Unresolved Items

* none

<!-- rpi:task id=P03-T01 -->
### P03-T01: Update #154 changes, review, and state records and record child implementation changes

#### Context

Parent `#154` artifacts currently describe the pre-rebase commit on `02ab20cac`, and `issue-154-rep-expiry-views-state.json` lacks a comma after `confirmed_decisions[2]`.

#### Intent

Synchronize `#154` tracking artifacts with the `0c1fa1da4` rebase and focused validation results, repair the JSON syntax in `issue-154-rep-expiry-views-state.json`, and complete child changes/plan reconciliation for `rpi-review` and final local commit.

#### Boundaries

* Included: `.copilot-tracking/` files listed in `P03` Likely Targets.
* Excluded: Production code and remote git state.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-changes.md`
* `.copilot-tracking/reviews/logs/2026-11-15/issue-154-rep-expiry-views-review.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/issue-154-rep-expiry-views-state.json`
* `.copilot-tracking/changes/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-changes.md`
* `.copilot-tracking/plans/2026-11-15/issue-154-rep-expiry-views-rebase-0c1fa1da4-plan.md`

#### Dependencies

* P02-T01

#### Validation Expectations

* `python3 -m json.tool` passes on both `.copilot-tracking/rpi-sessions/2026-11-15/*154*.json` files; `git diff --check` exits `0`.

#### Completion Evidence

* Reconciled `#154` and child tracking files verified prior to `rpi-review` and committed cleanly immediately after final post-Review state persistence.

#### Unresolved Items

* none
