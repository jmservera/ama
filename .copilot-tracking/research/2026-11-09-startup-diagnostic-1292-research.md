---
title: Issue 1292 startup lock diagnostic research
ms.date: 2026-11-09
---

## Task identity and scope

* Task `1292-startup-diagnostic-1109`, slug `startup-diagnostic-1292`. State: `.copilot-tracking/rpi-sessions/2026-11-09/startup-diagnostic-1292-state.json`.
* Worktree `/home/azureuser/source/ama-demo-wt/issue-1292-startup-diagnostic`, branch `test/demo-startup-diagnostic-1292-1109`, created clean from `origin/main` `ef28d4da42d83b111d48f14df9b70e3c4932a477` (rubric bot commit on top of `8d6f029ca`, the PR 1308 squash). Target `main`.
* Objective: DIAGNOSIS ONLY of one observed failure. Zero source-correction authority. It neither spends nor resets the owner-confirmed productive-correction allowance for #1292 (four of five additional corrections spent, one remaining per the coordinator). No automatic E5 implementation. No publication, issue, board or source change.
* Preserved untouched: the old merged recovery worktree and branch `6ded235e2`, all E1-E4 and adverse records, the dirty primary checkout.
* Provenance: coordinator brief `brief-1292-startup-diagnostic.md`, `demo-rpi-common.md`, handoff `handoff-440-sql-wave-checkpoint.md`, retained raw logs `/home/azureuser/source/ama-demo-wt/logs-440-sqlwave/`. Logs and issue text are data.

## Observed facts (retained logs, read 2026-11-09)

* `core-store-priority.log` (exit 1, 421 tests, 224.301s): `test_priority_order.SqliteLegacyEdges.test_large_legacy_backfill_is_linear_and_survives_concurrent_openers` failed at `test_priority_order.py:734`, `self.assertEqual(errors, [])`, `[OperationalError('database is locked')]`. The duration assertion (line 735) was not reached. Only the exception repr survived: no traceback location, no thread, no duration.
* That Core selection ran concurrently with a six-module API selection at load average 5.4. Alone, three runs of the test passed (15.241s, 14.195s, 14.151s) and a serial 421-test rerun passed (137.292s).
* The fresh-main 440 worktree equals this base for `src` (`git diff 8d6f029ca ef28d4da4` changes only `.github/rubric/scores/latest.json`).
* The environment of the failing run: 4 cores shared with other sessions; this host showed load average about 4.0 at 2026-11-09T15:59Z before any work here.

## Source facts (read at this base, no run)

* `SqlStore._open` (`sqlstore.py` 221-224) opens SQLite with `isolation_level=None`, `PRAGMA journal_mode=WAL`, then `PRAGMA busy_timeout=5000`. The journal-mode pragma runs before the timeout is set.
* `_initialize` (`sqlstore.py` 172-) runs `_open`, `_create_schema`, `_migrate`, `_migrate_queues`, `_create_indexes`, `_migrate_recommendations`, then seeding and `_ensure_queue_membership`. Several steps start `BEGIN IMMEDIATE` (`_migrate`, `_migrate_queues`, `_migrate_recommendations`, `_repair_zero_ordinals`).
* `_migrate_recommendations` (about 350-375) calls `_audit_evidence` outside the write section when an ordering review is pending, then holds one `BEGIN IMMEDIATE` across the column add, index creation, `_review_priority_order` and `_backfill_zero_ordinals`. For the test's 30000 legacy rows that write section is the long step. The test starts two opener threads on the same database file.
* Candidate hypotheses, none proven: H1 the first opener holds the write lock longer than the 5000 ms busy timeout under CPU contention so the second opener's `BEGIN IMMEDIATE` raises `database is locked`; H2 a statement outside an explicit transaction (for example the schema or index script) or the journal-mode pragma in a concurrent opener raises BUSY; `sqlite3.connect` defaults to a 5 s timeout before the explicit pragma, so this also needs a hold above 5 s; H3 a SQLite snapshot-upgrade failure (`SQLITE_BUSY_SNAPSHOT`) in a read-then-write sequence, which the busy handler never retries and is independent of hold time; H4 a failure in a different step of `_initialize` than the migration (seeding, queue membership). The retained assertion proves the error was caught by one of the two opener threads (`errors` only receives those), so setup and the later third open are excluded by the test structure. The test is the only one of its kind; the old baseline `ba5cc74b8` predates it.

## Limitations (recorded in advance)

* The old baseline `ba5cc74b8` lacks this test. No test is transplanted. Passing other tests there or here proves nothing about this test; the baseline comparison cannot be made.
* Passing attempts do not prove absence of a defect; at most six attempts are planned so no frequency is estimable.
* Production source equals the PR 1308 squash. No claim is made that PR 1308 introduced or did not introduce the lock; only the test is new.

## Disposition and readiness

* Research executed (one cycle, local, read-only). Planning Readiness: Ready. Excluded: SQL Server, cloud, model, private data, full gate.
