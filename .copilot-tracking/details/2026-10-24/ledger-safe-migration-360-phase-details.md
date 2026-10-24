<!-- markdownlint-disable-file -->
# Ledger-Safe Migration Phase Details

Task ID: ledger-safe-migration-360
Plan: .copilot-tracking/plans/2026-10-24/ledger-safe-migration-360-plan.md
Research: .copilot-tracking/research/2026-10-24/ledger-safe-migration-360-research.md

## P01 Shared hook
In sqlstore.py add `_add_column_default(self, table, col, sqltype, default)` executing `ALTER TABLE {table} ADD COLUMN {col} {sqltype} NOT NULL DEFAULT {default}` (identical SQL to today). `_migrate` and `_migrate_queues` call it. Remove `_add_column` class attributes in both stores. The chat_memory SQLite loop keeps its existing statement via the hook.

## P02 MssqlStore
Override the hook. Ledger test: `SELECT ledger_type FROM sys.tables WHERE object_id = OBJECT_ID(N'<table>')` non-zero. Ledger path statements, in order, using the caller's open transaction: `ALTER TABLE t ADD col <type> NULL`; `UPDATE t SET col = <default> WHERE col IS NULL`; `ALTER TABLE t ADD CONSTRAINT ck_<t>_<col>_nn CHECK (col IS NOT NULL)`; `ALTER TABLE t ADD CONSTRAINT df_<t>_<col> DEFAULT <default> FOR col`. Type for text columns comes from a small width map equal to the fresh-create DDL (default NVARCHAR(200) COLLATE Latin1_General_100_BIN2); INT stays INT. Non-ledger path: the current NOT NULL DEFAULT statement. Chat memory additions: make MSSQL_MIGRATE data (column, width, default) and drive it through the hook inside `IF COL_LENGTH IS NULL`, preserving constraint names on the non-ledger path.
Identifiers come only from module constants, never input.
Critique amendment (C1, C3): the chat_memory additions run inside one `BEGIN IMMEDIATE` .. `COMMIT` with rollback on any error, before the index statements; the type map is one module constant equal to TABLES["cases"] and verified against a fresh create. C4: rollback test uses a failure injected after the backfill UPDATE.

## P03 Tests
Always-on: recording-connection tests for statement order and the non-ledger/SQLite parity. Opt-in (ZF_TEST_MSSQL=1): create a throwaway database WITH LEDGER = ON on the harness server, build the previous-schema `cases` (drop priority_correction, queue_* and a TEXT column via a handcrafted old table), insert synthetic rows, open MssqlStore, assert columns/defaults/backfill/CHECK/ledger history rows/audit append-only/idempotent rerun, and inject a failure to prove rollback. Skipped live tests are not evidence; run them on the disposable container and record that.

## P04 Docs
One paragraph in src/core/README.md on ledger-database migrations and the nullable-in-metadata tradeoff.

## P05 Validation
Run ruff and mypy as the gate defines for src/core and src/api, unittest for the touched suites, then the gate itself per the outer handoff.
