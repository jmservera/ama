---
title: Issue 1292 current-main priority SQL regression validation research
ms.date: 2026-11-09
task_id: 1292-current-main-sql-1109
---

## Disposition and readiness

* Research executed (read-only: issue, merged PR, source, tests, prior evidence). Planning Readiness: Ready.
* Trigger: the earlier lifecycle/priority current-source SQL checkpoint remains due. The controls and photo documents (#1322) explicitly do not satisfy it.
* Scope: ONE finite, bounded validation of current `main` source on a task-owned disposable SQL Server. This is VALIDATION ONLY. It is not Source E5 authorization, not a third historical-load equivalence experiment, not a new correction grant. No source, test, fixture or harness edit, no observer experiment, no load simulation, no private data, no cloud.

## Inputs and identities

* Pinned merged main and candidate base: `ba71894bb1a94d6a24aabf9828312668f88f3ff5` (tree `83ab51163dd0d24f6a48ea1a329b1693881e8f38`), equal to freshly fetched `origin/main` on 2026-11-09. Worktree `issue-1292-current-main-sql`, branch `test/demo-priority-sql-main-1292-1109`, eventual target `main`.
* Original fix and SQL index bootstrap are already merged: PR #1308 squash `8d6f029cac004506953f36606862168bbe9d9412` (merged 2026-11-09T15:30:40Z) is an ancestor of this base (`git merge-base --is-ancestor` true).
* Source blobs at the base: `sqlstore.py` `89f409ee000b6ce97c25d0efb1d60732551da410`, `mssqlstore.py` `c712ad4a8a15f794f3a555de48bead66bb86eb39`, `store.py` `a941ad9f3868ab2f774d057cff56747a8487de9d`, `test_priority_order.py` `c098970d1c4c6321228ed75f2a2ac46ba52fa8fd`, `test_resident_decisions.py` `8529a652a758204ab56c6e9e2816e9a1c07b5a05`, `sqlguard.py` `e78506358ee8628ee8500ee8668e87971c75d66d`, `dataset.py` `46f0241d842c22680fdf56e843d81f9cb63dc952`.
* Current main reload uses `created_ord` (`sqlstore.py` lines 79, 343-359, 1004: `ORDER BY created_ord, id`), not an unordered query.

## Issue acceptance criteria (literal, abridged) and what this lane can and cannot add

* AC1 deterministic newest-created order across cold and incremental reloads, in-memory parity, requesting user and `ai_task` exclusion.
* AC2 same-interval creations, edits of older proposals, multiple users, truthful legacy transition.
* AC3 focused regression failing against old behavior and passing on a task-owned actual SQL Server with zero skips, plus SQLite/in-memory parity; record commands, counts, outcomes.
* AC4 review/approval boundary and ranking policy preserved.
* AC5 research, plan, changes and review through the issue's own RPI branch and PR.
* This lane produces fresh current-main SQL evidence relevant to AC1 to AC3 only as a source-qualified observation. It does not prove the fails-against-old-behavior half of AC3 (a test of the pre-fix source is out of scope), AC4 human boundaries, AC5 publication, any live or Azure criterion, or whole-issue closure. The coordinator maps each literal criterion; this lane ticks and closes nothing (#1292, #81, #440 stay as they are).

## Prior evidence reviewed (preserved, not re-derived)

* Original proof (issue text): on 2026-11-08 two unchanged `MssqlResidentControls` methods failed 6/10 and 7/10 on a task-owned SQL Server 2022; all 13 failures followed random ID order. A timed-out earlier run is explicitly not attributed to this defect.
* E1 (interrupted/busy receipts), E2 (index race reproduced, fixed under the write lock; priority 142 passed with zero skips at `a2047273`, 536.7 s and 558.0 s in two earlier runs; resident 91 passed), E3 (hosted mypy), E4 (typed fake-driver fixture only; no production SQL change) are preserved unchanged. E4 real-SQL evidence was not rerun for the fixture-only change.
* The unknown historical startup failure is a different observation from the proven unordered-priority defect. Original-load diagnostics ended 0 of 2 pairs with cause UNKNOWN; one failure in five total executions followed by four passes. One Source E5 remains, neither granted nor spent here.

## Selection analysis (smallest reliable current-source SQL regression)

* `test_priority_order.py` holds 142 tests (counted by loading, not running): JsonPriorityOrder 4, LegacyMetadata 3, LoopbackGuard 7, MssqlBeginRecovery 2, SqlitePriorityOrder 19, SqliteLegacyEdges 8, SqliteC3 15, SqliteC4 19, MssqlPriorityOrder 19, MssqlLegacyMetadata 3, MssqlLegacyEdges 8, MssqlC3 15, MssqlC4 19, MssqlLockTimeoutBegin 1. The 65 `Mssql*` tests (excluding the two fake-driver recovery tests and the guard tests) are skipped unless `ZF_RESIDENT_MSSQL=1`.
* The Mssql classes inherit their tests from the SQLite classes through a shared fixture, so the SQLite and in-memory parity cases cannot be separated from the SQL classes without losing the parity relationship. Selecting a handful of methods would also drop the same-interval, edit, legacy backfill and creation-boundary cases that AC2 names. The whole module is therefore the smallest reliable focused selector.
* Prior full-module runs took 536.7 s and 558.0 s, about 90 to 93 percent of the 600 s per-process bound. To keep a timeout from being the likely outcome, the same 142 tests are split once by class across two processes (no test is run twice): process A 108 tests (31 SQL) and process B 34 tests (`MssqlC3Corrections`, `MssqlC4Corrections`). This is a scheduling split, not a reduced selection.
* Resident controls: the two original methods `test_resident_decisions.MssqlResidentControls.test_challenge_source_exact_dependency_manifest_and_original_reviews` and `test_failed_priority_accept_edit_remove_disposition_and_audit` are inherited from `JsonResidentDecisions` through `SqlResidentDecisions`. The same two method names on `JsonResidentDecisions` (in-memory) and `SqlResidentDecisions` (SQLite) supply parity: six tests in one process, two of them on SQL Server.
* Expected totals: three test processes, 142 + 6 = 148 tests, zero skips (any skip, including any SQL skip, is a failed expectation to report, not to waive).

## Prerequisites (read-only, rechecked before admission)

* Image `mcr.microsoft.com/mssql/server:2022-latest`, id `cf8f0ab2ebe6`, digest `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`, present locally. `docker ps -a` empty; no holder of `/tmp/ama-rpi-heavy.lock` by `fuser`; 15983 MB memory with about 10 GB available, 134 GB free disk.
* Driver: the SQL store imports `mssql_python` (declared `sql` extra `mssql-python==1.15.0`). The own environment `.venv` in this worktree (git-ignored, own env only) installs `-e src/core[sql] -e src/agents` per repository policy; no global install, no `PYTHONPATH=mvp`. Imports come from this worktree's `src` (verified before running).
* Existing task-owned fixture contract: `sqlguard.py` requires a `ZF_SQL_TASK_MANIFEST` for a labelled loopback container with a password digest only. Existing session runner `sql-1292-vc.sh` implements EULA, label `zf.task=1292-sql-disposable`, `127.0.0.1` publishing, `flock -n /tmp/ama-rpi-heavy.lock`. The planned runner is a parameterized copy of it (session files only, not repository content) with per-process `timeout`, import-path and version records, and output redaction.

## Limits

* One current PASS does not mark the unknown startup cause fixed, does not prove whole-SQL acceptance, a full gate, scale or lock-duration behavior, Azure or live behavior, resident or professional approval, or independent review. A failure would be reported with its smallest precise reproduction and existing owners deduplicated; no automatic Source E5, retry or correction.
* Source fulfillment, current observed behavior and root cause are kept as separate statements in every later record.
