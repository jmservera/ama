<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #76 C2 Rebase Continuation onto `#1641` (`36aeddae3`)

## Metadata

* Task ID: issue-76-c2-rebase
* Task slug: ux-76-hazard-clock-owner-c2-rebase
* Related plan: .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-research.md, .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan-critique.md, .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan.md

## Phase Index

| Phase ID | Name                                                                                          | Status   | Detail sections       |
|----------|-----------------------------------------------------------------------------------------------|----------|-----------------------|
| P01      | Rebase onto `#1641` (`36aeddae3`) and Unify `#116` + `#215` + `#76` Projection/Store Behavior | Complete | P01, P01-T01, P01-T02 |
| P02      | Focused Validation and Local `Refs #76` Commit Closeout                                       | Complete | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Rebase onto `#1641` (`36aeddae3`) and Unify `#116` + `#215` + `#76` Projection/Store Behavior

### Context

Research `C1`–`C6` and critique `PC-001` established that `origin/feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) advanced from `08c36e4dc` to `36aeddae345426fdf8ee53565fef1540979de967` via `71f5c9f9b` (`PR #1772`, Issue `#154`), `243764945` (`PR #1766`, Issue `#116`), and `36aeddae3` (`PR #1773`, Issue `#215`). Replaying `feat/ux-76-hazard-clock-owner` (`6e9eb39de`, `8f8d85342`, `941806d9d`) onto `36aeddae3` conflicts only during Commit 1 (`6e9eb39de`) in `src/core/src/zava_forward/core/projection.py` (1 hunk in `hold_notes`) and `src/core/src/zava_forward/core/store.py` (6 formatting-colliding hunks), while Commit 2 (`8f8d85342` SQL Server row-order invariant fix) and Commit 3 (`941806d9d`) replay conflict-free and `#215` (`chat_case_answers.py` + 13 API test suites) auto-merges cleanly. In addition, `#116`'s `project_case_visibility` and `withheld_scope_values` inspect raw `store.cases` dicts via `redact_staff_detail` -> `hold_notes` without calling `Store.detail()` / `safeguarding_view()`, requiring raw standalone safeguarding container support in `projection.py`.

### Intent

Stash and restore the untracked `2026-11-15` `c2-rebase` tracking files across the rebase, rebase all three `#76` commits cleanly onto `36aeddae345426fdf8ee53565fef1540979de967`, preserve `#116`, `#215`, and `#76`, and ensure `#116`'s Entra/role field-level visibility recheck covers `#76`'s raw standalone safeguarding items alongside projected hazard/safeguarding views.

### Boundaries

* Included: `git fetch origin feat/demo-164-chat-grounding-provenance-0900`; `git stash push -u` before rebase and `git stash pop` after rebase for untracked `2026-11-15` `c2-rebase` tracking artifacts; `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`; conflict resolution in `projection.py` and `store.py`; raw safeguarding visibility hardening in `projection.py` and 1 regression test in `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`.
* Excluded: Modifying unrelated `#154` / `#215` / `#83` modules, running `tools/rpi-checks.py`, or pushing to `origin`.

### Likely Targets

* `src/core/src/zava_forward/core/projection.py`
* `src/core/src/zava_forward/core/store.py`
* `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`

### Dependencies

* Clean tracked working tree with untracked `ux-76-hazard-clock-owner-c2-rebase-*` `.copilot-tracking/` files stashed prior to `git rebase` and restored immediately after.

### Validation Expectations

* `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exits `0`; zero conflict markers remain; `ruff`, `mypy`, and `#76` + `#116` + `#215` unit tests pass.

### Completion Evidence

* Clean rebased history atop `36aeddae3`, restored `c2-rebase` tracking files, unified `projection.py` and `store.py`, and passing cross-feature regression test in `test_hazard_safeguarding_clock_owner_76.py`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae3`), stash/restore untracked `c2-rebase` files, rebase `feat/ux-76-hazard-clock-owner`, and resolve `projection.py` and `store.py`

#### Context

During `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, Commit 1 (`6e9eb39de`) stops on:
1. `src/core/src/zava_forward/core/projection.py` around `hold_notes`: `#116` ran `ruff format` on `private_hazard` while `#76` introduced `is_safety_dict = ("category" in c and "released" in c) or c.get("item_kind") in ("hazard", "safeguarding")` and widened `private_hazard` keys to `("source", "job", "summary", "reason")`.
2. `src/core/src/zava_forward/core/store.py` across 6 hunks (`gate_reasons`, `summary`, `_work_context`, `focus`, `counts`, `require_safety_clear`): `#116` applied multi-line `ruff format` wrapping to the original `#76` base lines while `#76` wired `Store._open_safety_items`, `insights.has_hazard(c)`, `taskqueues.has_open_safeguarding(c)`, `staff=staff_list`, `(cat, own)` tuple unpacking in `Building Safety Liaison` focus, `taskqueues.has_open_safety(c)` in `counts`, and `active[0][1]` in `require_safety_clear`.

#### Intent

Replay `6e9eb39de`, `8f8d85342`, and `941806d9d` cleanly onto `36aeddae345426fdf8ee53565fef1540979de967` while stashing and restoring untracked `2026-11-15` `c2-rebase` tracking files and preserving every `#116`, `#215`, and `#76` change in `ruff format` style.

#### Boundaries

* Included:
  * Run `git fetch origin feat/demo-164-chat-grounding-provenance-0900` and confirm `git rev-parse origin/feat/demo-164-chat-grounding-provenance-0900` equals `36aeddae345426fdf8ee53565fef1540979de967`.
  * Stash untracked `2026-11-15` `c2-rebase` tracking files with `git stash push -u -m "c2-rebase-tracking"`.
  * Run `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`.
  * Resolve `src/core/src/zava_forward/core/projection.py` preserving `#76`'s `is_safety_dict` + `("source", "job", "summary", "reason")` logic inside `hold_notes` alongside all `#116` visibility helpers and `redact_staff_detail` AI output rechecks.
  * Resolve all 6 hunks in `src/core/src/zava_forward/core/store.py` preserving `#76`'s `_open_safety_items`, `gate_reasons`, `summary` (`hazard=insights.has_hazard(c)`, `safeguarding=taskqueues.has_open_safeguarding(c)`), `_work_context` (`staff=staff_list`), `focus` (`for cat, own in open_h`), `counts` (`taskqueues.has_open_safety(c)`), `detail` (`safeguarding_items` + `hazards`), and `require_safety_clear` (`active[0][1]`) formatted with `ruff format`, while keeping all `#116` AI/document store methods intact.
  * Stage both files and finish with `GIT_EDITOR=true git rebase --continue`, confirming Commits 2 (`8f8d85342`) and 3 (`941806d9d`) replay cleanly, then restore the untracked `2026-11-15` `c2-rebase` tracking files with `git stash pop`.
* Excluded: Squashing prior history or pushing.

#### Likely Targets

* `src/core/src/zava_forward/core/projection.py`
* `src/core/src/zava_forward/core/store.py`

#### Dependencies

* Clean tracked working tree.

#### Validation Expectations

* `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exits `0`; conflict-marker grep across `src/` returns zero matches.

#### Completion Evidence

* Rebased 3-commit stack above `36aeddae345426fdf8ee53565fef1540979de967` with restored `c2-rebase` tracking files and `ruff format --check` clean on `projection.py` and `store.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Harden raw standalone safeguarding visibility in `projection.py` and add `#116` + `#76` regression test

#### Context

Research `C6` identified that `#116`'s `projection.project_case_visibility(user, raw_case)` and `projection.withheld_scope_values(store, user, case_ids)` run `redact_staff_detail` -> `hold_notes` directly on raw case dicts in `store.cases` without running `Store.detail()` / `workflows.safeguarding_view()`. Because raw standalone safeguarding items in `raw_case["safeguarding_items"]` or `raw_case["safeguarding"]` need not carry `"item_kind"` or `"released"`, `hold_notes` must hold `("source", "job", "summary", "reason")` on raw safeguarding item dicts inside those containers (matching `taskqueues.SAFEGUARDING_ITEM_KEYS`, while leaving passive note-only `{"note": "..."}` canaries and `documents[*]["summary"]` untouched), and `_is_high_sensitivity_path` must treat `summary` under `("hazards", "safeguarding_items", "safeguarding")` as high-sensitivity.

#### Intent

Ensure `#116`'s Entra/role field-level visibility and AI output recheck treat `#76` raw standalone safeguarding private fields identically to projected `Store.detail()` views.

#### Boundaries

* Included:
  * Import `SAFEGUARDING_ITEM_KEYS` from `.taskqueues` in `src/core/src/zava_forward/core/projection.py` (`taskqueues.py` imports stdlib only, introducing zero import cycles and obeying `test_dependency_rule.py`).
  * In `projection.hold_notes(c)`, hold truthy `("source", "job", "summary", "reason")` keys on dict entries inside `c["safeguarding_items"]` (list) and `c["safeguarding"]` (list, or dict intersecting `SAFEGUARDING_ITEM_KEYS`) before recursing into child values.
  * In `projection._is_high_sensitivity_path(path)`, return `True` when `path[-1] == "summary"` and any segment is in `("hazards", "safeguarding_items", "safeguarding")`.
  * Add 1 focused test method in `src/core/tests/test_hazard_safeguarding_clock_owner_76.py` verifying that for a raw case with standalone `safeguarding_items` (`summary`, `source`, `reason`, `job`, `note`), `projection.project_case_visibility` holds all five fields for `Retrofit Coordinator` (`not can_see_reason`), `projection.withheld_scope_values` includes them, `projection.redact_staff_detail` replaces AI `documents[*]["summary"]` and `funding["draft"]` containing any of those withheld safeguarding strings with `NOTE_HELD` while keeping clean summaries for authorized roles, and passive note-only `{"note": "..."}` canaries remain passive.
* Excluded: Creating new test files (`0` new test files, `0` test removals, `1` added test method in canonical `test_hazard_safeguarding_clock_owner_76.py`).

#### Likely Targets

* `src/core/src/zava_forward/core/projection.py`
* `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`

#### Dependencies

* P01-T01 completed.

#### Validation Expectations

* New and existing tests in `test_hazard_safeguarding_clock_owner_76.py` and `test_data_protection.py` pass; `ruff` and strict `mypy` pass.

#### Completion Evidence

* Updated `projection.py` and passing cross-feature regression test in `test_hazard_safeguarding_clock_owner_76.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Focused Validation and Local `Refs #76` Commit Closeout

### Context

Caller Step 4 requires focused validation in `src/core` and `src/api` (`unittest discover -s tests -p "test_*case_workbench*.py" -q && ruff check . && ruff format --check . && mypy`) without running `tools/rpi-checks.py`. Because `-p "test_*case_workbench*.py"` matches `0` files (`C8`), `P02-T01` executes both the exact caller commands AND the real `#76`, `#116`, and `#215` `unittest` modules. Step 5 requires committing locally with `Refs #76` and the Copilot trailer with `git status --short` clean and no `git push`.

### Intent

Verify full focused-tier unit, lint, format, and static type coverage across `src/core` and `src/api`, complete `rpi-review`, and leave a clean local `c2-rebase` commit without pushing.

### Boundaries

* Included: Exact caller step-4 commands; targeted `#76`, `#116`, and `#215` `unittest` runs; diff-boundary and privacy-safe `user.email` checks; `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-changes.md`; `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`; post-`rpi-review` local commit with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
* Excluded: `tools/rpi-checks.py` and `git push`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan.md`
* `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md`
* `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`

### Dependencies

* P01 completed.

### Validation Expectations

* All step-4 and targeted `#76`, `#116`, and `#215` validation commands exit `0`; post-Review commit leaves `git status --short` empty.

### Completion Evidence

* Recorded validation evidence in `changes.md`, completed `review.md` + `state.json`, and clean `git status --short`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused validation (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`) and targeted `#76`, `#116`, and `#215` suites in `src/core` and `src/api`

#### Context

Running both the literal caller step-4 commands and the targeted `#76`, `#116`, and `#215` test modules verifies lint, formatting, and `mypy` across the full `src/core` and `src/api` packages AND exercises every rebased and hardened code path in `projection.py`, `store.py`, `sqlstore.py`, `taskqueues.py`, `workflows.py`, `chat_case_answers.py`, and `server.py`.

#### Intent

Confirm zero regressions across `src/core` and `src/api`.

#### Boundaries

* Included:
  * `(cd src/core && PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*case_workbench*.py" -q && ruff check . && ruff format --check . && mypy)`
  * `(cd src/api && PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_*case_workbench*.py" -q && ruff check . && ruff format --check . && mypy)`
  * `(cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_hazard_safeguarding_clock_owner.py tests/test_hazard_safeguarding_clock_owner_76.py tests/test_data_protection.py tests/test_taskqueues.py tests/test_sqlqueues.py tests/test_dependency_rule.py -q)`
  * `(cd src/api && PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests:tests python3 -m unittest tests/test_hazard_safeguarding_clock_owner_api_76.py tests/test_ai_tasks.py tests/test_task_queue_api.py tests/test_alert_chat_owner_clock_safe_action_215.py tests/test_alert_chat_visit_consent_boundary_215.py -q)`
* Excluded: Running `tools/rpi-checks.py` or adding lint/type suppressions.

#### Likely Targets

* Read-only validation across `src/core` and `src/api`.

#### Dependencies

* P01-T02 completed.

#### Validation Expectations

* `-p "test_*case_workbench*.py"` discovery confirms `0` matching files (Python 3.12 exit code `5` `NO TESTS RAN`), while `ruff check . && ruff format --check . && mypy` and all targeted `#76`, `#116`, and `#215` `unittest` runs exit `0`.

#### Completion Evidence

* Pass counts and command outputs recorded in `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile RPI artifacts, complete `rpi-review`, and commit locally with `Refs #76` and Copilot trailer leaving `git status --short` clean

#### Context

Repository commit conventions require `{id}+{login}@users.noreply.github.com` in repository-local `user.email`, `Refs #76`, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, with `git status --short` completely clean, no `.copilot-tracking/` strings in the commit message, and no `git push`.

#### Intent

Reconcile `Implement` artifacts cleanly ahead of `rpi-review`, then commit the post-rebase hardening and complete `ux-76-hazard-clock-owner-c2-rebase-*` tracking set locally immediately after `rpi-review` writes `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md` and `state.json`.

#### Boundaries

* Included:
  * Verify `git config --local user.email` matches `{id}+{login}@users.noreply.github.com` from `gh api user` (configuring locally if needed).
  * Verify `git diff origin/feat/demo-164-chat-grounding-provenance-0900 --name-status` contains only `#76` code/doc/test paths plus `.copilot-tracking/` artifacts.
  * Persist `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-changes.md` and mark `[x]` / `Complete` across `P01` and `P02` in `plan.md` and `phase-details.md` prior to `rpi-review`.
  * After `rpi-review` persists `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md` and updates `.copilot-tracking/rpi-sessions/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-state.json` to `active_phase: "Follow-up"`, `status: "completed"`, stage `projection.py`, `test_hazard_safeguarding_clock_owner_76.py`, and all `ux-76-hazard-clock-owner-c2-rebase-*` tracking artifacts and commit locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` (keeping `.copilot-tracking/` paths out of the commit message), then verify `git status --short` is empty.
* Excluded: Pushing to `origin`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-changes.md`
* `.copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-plan.md`
* `.copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-phase-details.md`
* `.copilot-tracking/reviews/2026-11-15/ux-76-hazard-clock-owner-c2-rebase-review.md`

#### Dependencies

* P02-T01 completed.

#### Validation Expectations

* Local commit succeeds; `git status --short` outputs empty; `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exits `0`.

#### Completion Evidence

* Clean `git status --short` and verified local commit metadata.

#### Unresolved Items

* None.
