---
title: Issue 82 combined 1490 candidate prospective amendment (rebase plus RV01 consolidation)
ms.date: 2026-11-12
task_id: combined-1490-funding-2310
---

## Objective

Produce one coherent same-issue PR 1490 candidate, so the coordinator publishes once. It combines three things for #82 only:

* The original 1490 commit (`dc9fb68e0`, store.py funding denial) rebased onto the UX parent `feat/demo-ux-integration-1112` at `8f8be74e14c5fe1b6911a9493cd74d0750151085`, which now contains PR 1487 (stale-stage refusal). The rebase was needed because `git merge-tree` confirmed a textual conflict in `src/api/tests/test_mvp.py`.
* The already-authored, frozen RV01 funding-reader commits `c4fe717ef` (prospective research, plan, critique) and `4ce5bae61` (three readers, `MEMBERSHIP_REVISION` 3, tests, changes, review) from `research/demo-82-followup-2250`, cherry-picked in original order with their original gates, reader scope and evidence.
* This dated amendment, its one independent critique and one final independent Review of the combined candidate.

Parent task `server-gate-readiness-82-1112`; RV01 task `funding-readers-82-2250`. Refs #82 only; whole #82 stays open.

## Rebase resolution (already applied, recorded here as the prospective rule)

* Original 1490 backup ref: `backup/pre-combined-1490-dc9fb68e0` (local only; the PR head `dc9fb68e0` is untouched on the remote).
* `src/api/tests/test_mvp.py`: keep both complete, independent methods, `test_stale_advance_refusal_names_case_owner_and_next_action` (153, 400, no `reasons`, owner and next action) and `test_advance_with_missing_funding_is_a_funding_conflict_not_a_missing_case` (82, 409, funding reason). Each builds its own fixture state and HTTP server; no shared mutable state.
* `src/core/src/zava_forward/core/store.py` auto-merged; `advance` keeps the stage check before `gate_reasons`, so a wrong-stage case gets the 153 refusal and a ready-stage case with missing or non-boolean funding gets the 82 409 reasons. The two paths are not merged.
* The source `PYTHONPATH` shortcut from the preflight is rejected: validation uses pip installs of `src/core`, `src/agents` and `src/api` into a temporary virtual environment outside the repository, plus only the test-helper path the component guide documents (`PYTHONPATH=../core/tests:../agents/tests`).

## Phases

* [x] Phase 0: parent fetched (`8f8be74e1`), conflict confirmed, rebase and test_mvp resolution applied.
* [x] Phase 1: one independent critique of this combined candidate plan in [critique](combined-1490-funding-2310-critique.md); compatible findings PC-01 to PC-03 applied below.
* [ ] Phase 2: cherry-pick `c4fe717ef` then `4ce5bae61` with the repository-local privacy-safe identity and `Co-authored-by` trailer preserved; resolve any conflict without altering reader scope or evidence.
* [ ] Phase 3: validation of the combined modified and impacted core and API tests with pip-installed packages in a temporary virtual environment outside the repository, pinned Ruff 0.17.1 and mypy 2.4.0. Verify imports resolve to the candidate worktree, enumerate the focused modules, record exit codes and skips, and stop on any unexpected failure. Failing-first: in an isolated temporary worktree at the combined head, restore only the three reader sources and `taskqueues.py` revision to their pre-RV01 content, run the new tests, record the expected failures, then run the fixed candidate. Run the `MEMBERSHIP_REVISION` negative control separately and verify restoration.
* [ ] Phase 4: combined changes record, one genuine independent final Review, local frozen exact head.

## Boundaries and stop rules

* Carry original RPI evidence and order, original gates and reader scope (`chat_case_answers.py`, `taskqueues.py`, `home_case.py`) and `MEMBERSHIP_REVISION` 3. No new grants, readers, helpers, policy, role, consent or gate changes. No unrelated readers (`export_fields.py`, `resident_preview_fixture.py`, `ai_eval.py` stay unchanged).
* The frozen RV01 reviewer worktree `issue-82-funding-readers-2250` and branch `research/demo-82-followup-2250` are read from and never altered.
* No default complete gate; the focused tier applies with its basis recorded in the changes record. Opt-in SQL Server tests are classified as skipped by the harness, not claimed as real SQL acceptance.
* No push, force-push, PR, merge, issue edit, tick, human approval, cleanup, cloud, model or spend call, and no private data. The coordinator assesses and publishes once.
* One critique and one Review for this task. Stop on any material Review finding (gate weakening, regression, lost evidence) rather than deferring it; only explicitly non-blocking findings become later work.
