<!-- markdownlint-disable-file -->
# Ledger-Safe Migration Plan

## Task Metadata
Task ID: ledger-safe-migration-360
Date: 2026-10-24
Branch: fix/ledger-safe-migration-360 from origin/main df3e9643 (separate worktree issue360-ledger-fix)
Status: Implemented and independently reviewed (PASS, three test-quality findings applied); exact-head gate pending.

## Executive Summary
Make every store column-adding migration safe on an Azure SQL ledger database without altering behaviour on SQLite or non-ledger SQL Server, so the Entra-authoritative image can start against the live database.

## Sources
.copilot-tracking/research/2026-10-24/ledger-safe-migration-360-research.md
src/core/src/zava_forward/core/sqlstore.py (_migrate, _migrate_queues), mssqlstore.py, chatthreads.py (MSSQL_MIGRATE).

## User Decisions and Requirements
* Narrow source fix, full RPI, no live schema workaround, no ledger recreation/disablement/data discard/silent fallback.
* Preserve intended defaults and invariants and ledger audit behaviour. Synthetic ledger fixture on local SQL; state the Azure SQL gap.
* Related to #360, no closing keyword. Gate, independent review and coordinator release before publication.

## Phases
* P01 Shared add-column hook: SqlStore._add_column_default(table, col, sqltype, default) keeps the SQLite statement byte-identical; replace the two call sites and drop the unused `_add_column` attribute.
* P02 MssqlStore override: detect ledger table via sys.tables.ledger_type; ledger path = ADD NULL, backfill, CHECK, DEFAULT in the caller's transaction; non-ledger path = current statement. Route chat_memory additions through the same hook.
* P03 Tests: unit tests with a recording connection (statement order, non-ledger unchanged, SQLite unchanged); opt-in live ledger tests in src/api/tests/test_mssqlstore.py using a throwaway ledger database (old-schema fixture with rows, migrate, defaults/backfill/CHECK/audit intact, idempotent rerun, rollback on failure, fresh ledger DB initialises).
* P04 Docs: core README migration note and the change record; no unrelated edits.
* P05 Validation: focused tests, ruff, mypy on the touched package, local SQL ledger run, then independent review, then exact-head full gate.

## Success Criteria
* Old-schema cases table in a ledger database migrates with data and ledger history intact; defaults equal the fresh-create defaults; explicit NULL insert rejected.
* No behaviour change for SQLite and non-ledger SQL Server.
* Failure inside the migration leaves schema and meta unchanged.

## Critique
Executed once, 2026-10-24, by an independent rubber-duck agent before implementation. Verdict REVISE, one blocking and three non-blocking findings. All applied directly; none conflicts with an owner decision.
* C1 Blocking, applied: chat_memory additions run after `_migrate` commits, outside any transaction, so an interrupted ledger sequence could leave a partial column and collide on retry. P02 now runs them in one BEGIN IMMEDIATE transaction with rollback, and adds a real mid-sequence failure/retry test.
* C2 Non-blocking, recorded out of scope: sensor_consumer.py:351 `ALTER COLUMN .. NOT NULL` is the consumer's own table in the sensor consumer path, not store startup and not the failing path. It is not changed; listed as a possible follow-up if that table is ever placed in a ledger database.
* C3 Non-blocking, applied: one canonical per-column type map equal to `TABLES["cases"]`; the live test compares type, max length, nullability and collation of migrated columns against a freshly created table.
* C4 Non-blocking, applied: the rollback test injects the failure after the real backfill UPDATE on the disposable ledger database and asserts no column, CHECK, DEFAULT or backfilled values remain, then reruns successfully.
