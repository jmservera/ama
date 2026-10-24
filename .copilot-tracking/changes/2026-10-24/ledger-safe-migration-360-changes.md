<!-- markdownlint-disable-file -->
# Ledger-Safe Migration Changes

Task ID: ledger-safe-migration-360
Date: 2026-10-24
Plan: .copilot-tracking/plans/2026-10-24/ledger-safe-migration-360-plan.md
Details: .copilot-tracking/details/2026-10-24/ledger-safe-migration-360-phase-details.md
Research: .copilot-tracking/research/2026-10-24/ledger-safe-migration-360-research.md
Order followed: research, plan and details, independent critique (REVISE, all four findings applied before code), implementation.

## Source
* src/core/src/zava_forward/core/sqlstore.py: new `_add_column_default` hook; `_migrate`, `_migrate_queues` and the SQLite chat_memory loop use it. SQLite statements are unchanged in effect. Removed the unused `_add_column` attribute.
* src/core/src/zava_forward/core/mssqlstore.py: `_is_ledger_table`, ledger-aware `_add_column_default` (nullable add, backfill, CHECK, DEFAULT), `LEDGER_TYPES` equal to the fresh-create DDL, `_migrate_chat_memory` now inside one transaction. Ordinary SQL Server statements are exactly the previous ones, including the named chat_memory default constraints.
* src/core/src/zava_forward/core/chatthreads.py: removed `MSSQL_MIGRATE` (replaced by the transactional method).
* src/core/README.md: ledger-database migration note.

## Tests
* src/core/tests/test_sqlqueues.py: the existing fake connection answers the new ledger probe (not ledger); assertions on the exact ALTER statements are unchanged.
* src/api/tests/test_mssqlstore.py: `LedgerAddColumnStatements` (always on) and `MssqlLedgerMigration` (opt-in, throwaway databases): previous schema migrates in a ledger database with data, derived values, column type/length/collation, CHECK, defaults, append-only audit and idempotency; rollback after a real backfill leaves no column, constraint or value and retry succeeds; ordinary database keeps NOT NULL; fresh ledger database initialises.

## Validation
* Reproduction: with the source change stashed, `test_previous_schema_migrates_in_a_ledger_database` fails with the live error "Only nullable columns without a default value WITH VALUES can be added to ledger tables".
* Local disposable SQL Server 2022 container ama-360-ledger-test-sql (not the owner's feedback container): gate SQL selectors plus the new tests: 253 run, OK, 1 skipped.
* ruff check, ruff format --check, mypy (ruff 0.17.1, mypy 2.4.0) pass for src/core and src/api. Core suite: 1243 run before the one fixed test update; focused core SQL tests 67 OK.

## Not Done and Not Proven
* No live schema change and no deployment. Azure SQL ledger behaviour is inferred from SQL Server 2022 (same engine feature and message); first proof is the fixed image starting against the live database through the approved route.
* The live `cases` column gap was not read; all columns are handled.
* Out of scope: sensor_consumer.py:351 `ALTER COLUMN`, kaniko Dockerfile variant, grant-application-admin.py `--apply` body_directory defect, legacy_roster_tenant.

## Correction cycle 1 (2026-10-24, PR 450, test-only)
Trigger: fresh external PR review (two findings: MssqlLedgerMigration fixture lacks the local-server guard; chat-memory rollback is untested with a populated row). Owner-approved first bounded correction; the original gate receipts above remain historical and no longer apply to the new head.
* src/api/tests/test_mssqlstore.py: `MssqlLedgerMigration.setUp` now refuses any `ZF_SQL_SERVER` other than localhost, 127.0.0.1 or sql before registering cleanup or connecting (same guard as test_assistants.py). New always-on `MssqlLedgerMigrationGuard` proves a remote host raises before any `_Conn` call or `drop_database`.
* New `test_populated_chat_memory_failure_rolls_back_and_retries`: legacy chat_memory row seeded; failure injected after the first real chat_memory backfill; asserts no added column, CHECK or default remains, then retry preserves the content, applies the three defaults and rejects explicit NULL.
* No source change; no coupled defect was exposed.
* Mutation check: with the BEGIN/COMMIT/ROLLBACK temporarily removed from `_migrate_chat_memory` the new test fails (item_class column left behind); the source was restored with git checkout.
* Local validation: ledger, guard and statement tests 11 OK on a disposable local SQL Server 2022 (own container, port 14361); remote host refused with no connection; gate-style ruff check, ruff format --check and mypy for src/api pass.
