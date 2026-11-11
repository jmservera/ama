---
title: Issue 1292 before-fix and closure-mapping research
ms.date: 2026-11-11
task_id: 1292-before-fix-closure-1111
---

## Scope and boundary

One evidence-only continuation of open #1292 on pinned `main` `cea1cee5b20f63d7bb134fb7cb87a1bbc7d8618f` (branch `test/demo-priority-before-fix-1292-1111`). Aim: (1) a literal map of the five acceptance criteria to surviving original evidence, kept separate from historical observations and fresh execution; (2) if compatible without changing maintained code, the missing half of AC3: the unchanged maintained regression failing against the original unordered source on an owned disposable SQL Server. Not Source E5, no source/test/fixture/config change, no startup-cause experiment (cause stays UNKNOWN), no push, PR, issue or board write. Research disposition: executed.

## Verified identities (Git, read-only)

* Old source commit `e2ecee2565e86889c6beb43cb32e7c5b54270e01` exists. Old blobs: `sqlstore.py` `d790455892b6965cc7506713f14b9315ea2dd641`, `store.py` `a99948569d64b3f0c2e0a34d409a5d810651dd06` (both match the issue), `mssqlstore.py` `842d790484eef7a129f9d04a514f71b4267016bf`.
* Current pinned base blobs: `sqlstore.py` `01a3a44c926981fbf02ba26e91fc23b9fc710225`, `store.py` `70d71de39a79670a75ee64ad18be3e5c472cd3da`, `mssqlstore.py` `c712ad4a8a15f794f3a555de48bead66bb86eb39` (equal to the stated value), `tests/test_priority_order.py` `c140d4a8249ba38042d86755a94445925ac5f7be`. sqlstore, store and the test file moved after `ba71894bb` (commits 8d6f029ca #1308 and later, last touch 01f461dd7 #1426); no whole-source identity is asserted.
* #1308 (merge `8d6f029cac004506953f36606862168bbe9d9412`) and #1326 (merge `2be660e9d290f95ff05fc5a56d6539768576732b`) are merged; 8d6f029ca is an ancestor of the base.
* `tests/dataset.py` is identical at the old commit and now. `tests/sqlguard.py` does not exist at the old commit (it is a test helper, not packaged code).

## Compatibility of the maintained regression with the original public API

The selected methods live on `JsonPriorityOrder` and are inherited by `SqlitePriorityOrder` and `MssqlPriorityOrder` (an `OwnedMssql` fixture). They use only `Store`, `SqlStore`, `MssqlStore(path, state_dir=...)`, `ai_priority(user, mode="workflow-only")`, `resolve_priority`, `latest_priority`, `data["recommendations"]` and `save`. At the old commit `MssqlStore.__init__(data_path, env=None, state_dir=None, **kw)`, `_Conn`, `connection_string` and those store methods all exist. The module-level imports (`continuity`, `ledger`, `SqlStore`, `Store`, `dataset`, `sqlguard`) resolve (the two test helpers from the current tests directory by the documented test-path convention: working directory `src/core/tests`). Methods that use `created_ord`, `TABLES["recommendations"]` DDL, ordinal metadata or legacy backfill are NOT selected because they test current-only behavior and would fail for missing columns, not for the ordering defect.

Selected SQL methods (5) on `MssqlPriorityOrder`: `test_batch_in_one_save_keeps_creation_order_despite_id_order`, `test_edit_of_older_proposal_does_not_make_it_newest`, `test_each_user_gets_own_newest_and_ai_task_is_excluded`, `test_decision_boundary_unchanged_by_ordering`, `test_edit_of_older_proposal_is_not_newest_after_incremental_reload`. Current-source parity: the same 5 on `SqlitePriorityOrder` and the first 4 on `JsonPriorityOrder` (the in-memory implementation). Current arm 14 tests (5 on SQL Server); old arm 5 tests, all on SQL Server.

Predictions, not criteria: on the old source the four reload-asserting methods should fail with the wrong (id-order, newest-by-id) recommendation and the decision-boundary method, which never reloads, may pass. Any other failure type (import, DDL, attribute, bootstrap timeout) is reported as that type, not as the ordering defect. A passing old arm is non-reproduction.

## Acceptance criteria and surviving evidence (preliminary; final matrix in the changes record)

* AC1 ordering across cold and incremental reloads, in-memory parity, requesting user and `ai_task` exclusion: original implementation commit `656bacb56` and merged #1308 source; reviewed by the original independent review (SQLite run, T-SQL read-only) and later real-SQL runs recorded in the pack (E2, current-main 148-test validation). Fresh execution here covers the selected methods only.
* AC2 same-timestamp/transaction batches, older-proposal edits, multiple users, truthful legacy transition: original tests and README/meta documentation; the legacy-row heuristic is documented as a heuristic needing a named data-owner decision. Not re-executed here beyond the batch, edit and multi-user methods.
* AC3 regression fails against old behavior, passes on actual SQL Server with zero skips, plus parity, with commands, counts and outcomes: the pass half has real-SQL evidence (E2, 2026-11-09 current-main validation: 148 tests, 67 SQL, 0 skips). The fails-half has only the original SQLite red on base source (`changes` line 26: 24 ran, 2 failures, 3 errors, 10 skipped, with schema-related errors, missing `created_ord`, mixed in; the native SQL log `changes/logs/1292-2026-11-08-sql/base-priority.stderr.txt` records ordering failures in all four selected reload tests and a decision-boundary pass, historical and from an earlier suite, not this fresh cleaner selection) and the issue's 13 SQL failures of two OTHER resident-control methods. A native SQL red of the focused regression is the missing item; this campaign attempts it.
* AC4 no decision automation, boundary preserved: `test_decision_boundary_unchanged_by_ordering`, original review (no change to review, approval, consent or ranking boundaries); no human, resident or live-Azure approval is inferred.
* AC5 research, plan, changes, review through the issue's own RPI branch and PR: records survive under `.copilot-tracking/` and PR 1308 merged; independent exact-head review outcomes are recorded there.

## Constraints that shape execution

Two venvs outside the repo built by pip from `git archive` snapshots (old commit `src/core`, and this head `src/core`), installed non-editable so installed files can be hashed against Git blobs and no `PYTHONPATH` substitutes source. One shared-heavy non-queued admission, one task-owned SQL Server container run from the locally present image id `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718` (to be re-verified), loopback only, existing `sqlguard` manifest. External session-only runner and verifier may be adapted from the earlier session files; this time the verifier also fails when cleanup, matching container ids or the leftover query status are missing (the earlier Q1 limitation).

## Planning Readiness

Ready.
