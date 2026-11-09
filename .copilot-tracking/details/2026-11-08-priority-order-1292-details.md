---
title: Issue 1292 priority recommendation creation order details
description: Phase details for the immutable creation ordinal, ordered reload, migration backfill and regression cases
ms.date: 2026-11-08
---

## Design contract

* Ordering key: `recommendations.created_ord BIGINT NOT NULL DEFAULT 0`. Assigned once at insert as `(SELECT COALESCE(MAX(created_ord),0)+1 FROM recommendations)` inside the already serialised write transaction. Never in an `UPDATE`. A row batch in one `save` is inserted in in-memory list order, so ordinals follow creation order even with one `seq` and one `created` second.
* Reload: `SELECT id, rowversion, body FROM recommendations WHERE seq > ? ORDER BY created_ord, id`. `id` is only a deterministic final tie-break; it can tie only for unmigrated `0` rows. Known rows are updated in place so an edit never moves a row. New rows append in ordinal order, matching `Store` append semantics.
* `Store.latest_priority` is unchanged: last eligible row for the user and not `ai_task`.

## Phase 3 details

### sqlstore.py

* The `recommendations` table is created inside the `INDEXES` script (not `SCHEMA`), so migration must run after `_create_indexes`. DDL gains `created_ord INTEGER NOT NULL DEFAULT 0`. The index `ix_recs_created_ord` is not added to `INDEXES` (the MSSQL `_indexes()` is derived from it and a legacy table has no column yet); `_migrate_recommendations` creates it through a dialect hook `_create_rec_order_index()` (SQLite `CREATE INDEX IF NOT EXISTS`; MSSQL `IF NOT EXISTS (sys.indexes ...)`).
* Cache reconciliation (critique C-1, C-3): `self._rec_ord` maps id to ordinal, filled by `_sync` (the load now selects `created_ord`) and by `save` after each insert (`SELECT created_ord ... WHERE id=?`). After any recommendation load, and after a save's post-commit `_sync`, `_order_recs()` stably sorts the whole cached `data["recommendations"]` by ordinal; unsaved pending rows (no ordinal) stay last. This corrects the local-insert-then-concurrent-older-commit interleaving and keeps `_discard` recovery order.
* Hook `_has_rec_order()`: SQLite `PRAGMA table_info(recommendations)`; MSSQL override `COL_LENGTH(N'recommendations', N'created_ord')`.
* `_migrate_recommendations()` called after `_migrate_queues()` and before `_create_indexes()`: `BEGIN IMMEDIATE`; if the column is missing, `_add_column_default("recommendations", "created_ord", "BIGINT", "0")`; read rows with `created_ord = 0` as `(id, seq, body)`, sort by `(body.created or "", seq, id)`, assign `start = MAX(created_ord)` + 1.. in order; when this is the first backfill (no row had an ordinal) store `meta rec_order_legacy` JSON `{"rows": n, "same_second_groups": g, "order": "created,seq,id"}` where `g` counts `created` values shared by more than one legacy row; `COMMIT`; rollback on any error. Bodies and `rowversion` are not modified; backfilled rows and `meta.seq` take one new `seq` value (critique C-3) so a running new-code reader reloads the persisted ordinals through the normal incremental sync. A reader that predates the fix is out of scope.
* `save`: the insert statement computes the ordinal in SQL.

### mssqlstore.py

* `TABLES["recommendations"]` gains `created_ord BIGINT NOT NULL DEFAULT 0` (fresh databases); `_create_rec_order_index` and `_has_rec_order` overrides as above.
* Ledger databases (critique C-4): the pre-existing deployment can have updatable ledger tables. `_add_column_default` already takes the ledger path (add nullable, backfill, CHECK, DEFAULT) and passes the `BIGINT` type unchanged. Not exercised by the local container unless it is ledger-enabled; recorded as unproven in the changes record.

### README

Section in `src/core/README.md` stating the ordering contract, why `seq` and `created` are not used, the legacy transition and `rec_order_legacy`, and the rolling-deployment limit.

## Regression cases (`test_priority_order.py`)

Fixture: synthetic staff from `dataset.DATA`; recommendations made by `ai_priority(mode="workflow-only")` with `uuid.uuid4` patched so ids sort opposite to creation (`zzz`, `mmm`, `aaa`), no model or cloud.

1. Batch: deep-copy a generated recommendation three times with new ids and one `created` string, one `save`; cold reload latest is the last appended on every engine (fails old SQL Server order by id).
2. Edit of oldest: `resolve_priority` on the first of three; cold and incremental (a second open store synchronised before the edit) reload still report the third (fails old SQLite).
3. Incremental: second store synchronised, first store adds a newer proposal and edits an older one; second store's latest is the new one.
4. Multiple users and `ai_task`: interleaved creation for two users plus a newest `ai_task`; each user's latest is its own newest non-`ai_task`.
5. Legacy transition (SQL only): read all rows, `DROP TABLE recommendations`, recreate it from the pre-fix DDL (the current DDL text with the `created_ord` clause removed; genuine pre-migration schema, no column or default constraint to drop, critique C-4), reinsert the rows, reopen; assert deterministic backfill order `(created, seq, id)`, the `rec_order_legacy` meta, bodies and `seq` unchanged, and a new proposal after migration is latest.
6. Interleaved writers (C-1): two stores on one database; store A appends a new proposal locally while store B commits an older-created proposal first; after A saves and syncs, A and a cold reload agree that A's proposal is latest. Plus a long-lived reader (C-3) that continues to report the right latest after a legacy backfill performed by another new-code process.
7. Fresh initialisation (C-2): a brand-new SQLite database initialises, has the column and index, and orders correctly.
8. Parity: the in-memory `Store` gives the same latest id for cases 1-4.

SQL Server variant: subclass using the existing opt-in `ZF_RESIDENT_MSSQL=1` and a per-test `zf_priority1292_<uuid>` database, dropped on cleanup; no skip when the opt-in is set.

## Validation commands (planned, from repository root unless stated)

* `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/core/tests ZF_DATA=/tmp/ama-1292-scratch/none.json HOME=/tmp/ama-1292-scratch python3 -m unittest test_priority_order -v` from `src/core/tests`-relative path as recorded in the changes record.
* Original selectors by dotted name (`test_resident_decisions.SqlResidentDecisions.<method>`, `...JsonResidentDecisions.<method>`); native `MssqlResidentControls.<method>` PENDING.
* `ruff check` and `mypy` on `tests/test_priority_order.py`; `ruff` on touched sources only where the existing config applies.
