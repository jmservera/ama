---
title: Issue 1292 C1 correction details
description: Phase details for the fence, audit-recovered backfill, batch records, linear migration and loopback test guard
ms.date: 2026-11-08
---

## sqlstore.py

* `_backfill_zero_ordinals(seq)`: no transaction of its own; the caller holds the write section. Reads rows with `created_ord = 0` (`id, seq, body`). Reads `audit` ordered by `seq` and verifies it with `ledger.verify_entries` against `audit_head`; when intact, builds `{record id: audit seq}` from `ai_run_end` details starting `priority_recommendation <id> `. Sort key `(created, 0 if audited else 1, audit seq or seq, id)`. Ordinals start after `MAX(created_ord)`. Updates through one `executemany` stamping the supplied `seq`. Counts timestamp groups with `Counter`. A same-second group is `recovered` only when all members are audited and `ambiguous` otherwise. Appends one entry to meta `rec_order_backfills` (`at`, `rows`, `first_ord`, `last_ord`, `audited`, `heuristic`, `same_second_groups`, `ambiguous_groups`, `ambiguous_total`, bounded `ambiguous_ids`, `audit_chain`, `order`) and, only when `rec_order_legacy` does not exist, writes it as before. Returns the row count.
* `_migrate_recommendations` keeps column and index creation, then calls the helper in its own `BEGIN IMMEDIATE` and bumps `meta.seq` when rows were repaired.
* `_sync`: after the early-return check and before loading recommendations, probe `SELECT 1 FROM recommendations WHERE created_ord = 0` (one row). When found, repair: inside an existing write transaction (thread-local `writing`, set by `_queue_candidates`) call the helper directly, otherwise open `BEGIN IMMEDIATE`, call it, bump `meta.seq`, commit, rollback on error. The reader then recomputes `seq` and loads normally. Any failure propagates, so a zero ordinal is never served.
* `save`: before allocating the first new ordinal in the transaction, call the helper with the transaction's `new` seq so an old-writer zero row committed earlier receives its ordinal before the new row does.

## mssqlstore.py

No change expected: the helper uses `executemany` (present on the connection adapter), `ORDER BY seq` on audit (already used by `merge_seed`), and standard SQL. Unproven on SQL Server until a separately admitted run.

## Tests

* Shared helper `tests/sqlguard.py`: `require_task_owned_loopback(env)` raises `RuntimeError` unless `ZF_SQL_SERVER` is `localhost` or a loopback IP literal and `ZF_SQL_AUTH` is `password`; no DNS lookup, no connection. Called first in `MssqlPriorityOrder.setUp` and `MssqlResidentControls.setUp`, before the `mssqlstore` import and any DDL.
* New tests in `tests/test_priority_order.py` as listed in the plan. Tests that rewrite a table to the legacy schema use the existing `make_legacy` hook, so the SQL Server subclass inherits them; SQLite-only cases (audit trigger tamper, 20,000-row scale) sit in a class the SQL Server subclass does not inherit, which is declared as pending for SQL Server.
* Red run: unchanged source against the new tests. Green run: corrected source. Retained under a new `changes/logs/1292-2026-11-08-c1/`.

## Boundaries preserved

No change to `store.latest_priority`, `user` and `ai_task` filtering, human review or approval, resident consent, ranking policy or audit contents. Bodies are never rewritten. No private data, cloud or model.
