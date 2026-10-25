<!-- markdownlint-disable-file -->
# Ledger-Safe Migration Research (issue 360 follow-up)

Task ID: ledger-safe-migration-360
Date: 2026-10-24
Parent task: entra-authoritative-access-360 (PR 449, merged as 7d4e89bb)
Research disposition: executed (code inspection plus reproduction on a disposable local SQL Server 2022 ledger database).
Planning Readiness: Ready.

## Trigger and Owner Direction
* Live revision ca-cutover-test-demo-api--0000003 (image 417a7100) crash-looped in open_store() -> MssqlStore -> SqlStore._migrate(). Rolled back to image 111b2622 (revision 0000004, Healthy). Old code is serving; Entra-authoritative login is not live.
* Owner approved a narrow ledger-safe migration source fix with the full RPI loop. No live schema workaround, no ledger recreation, no data discard, no ledger/security disablement, no silent fallback. The nullable add was a hypothesis, not a dictated solution.

## Evidence
* E1 (live error, from container logs, not reproduced against Azure SQL): `ALTER TABLE cases ADD <col> ... NOT NULL DEFAULT ...` failed with "Only nullable columns without a default value WITH VALUES can be added to ledger tables."
* E2 (source): sqlstore.py `_migrate` adds any CASE_COLS missing from `cases` with `NOT NULL DEFAULT`; `_migrate_queues` adds QUEUE_COLS with `INTEGER NOT NULL DEFAULT 0`. chatthreads.MSSQL_MIGRATE adds chat_memory columns with `NOT NULL CONSTRAINT .. DEFAULT`. All three are the same unsafe pattern on a ledger database. SQLite has no ledger; its path must not change.
* E3 (source): mssqlstore only makes `audit` APPEND_ONLY when `sys.databases.is_ledger_on` is true. In a ledger-enabled database every other table created by the store is an UPDATABLE ledger table, which is why `cases` rejected the ALTER.
* E4 (reproduction, disposable local container ama-360-ledger-test-sql, SQL Server 2022, `CREATE DATABASE .. WITH LEDGER = ON`): table type UPDATABLE_LEDGER_TABLE. The exact E1 message reproduces for `ADD b INT NOT NULL DEFAULT 0` and for `ADD .. NULL CONSTRAINT .. DEFAULT .. WITH VALUES`.
* E5 (reproduction): these succeed on a ledger table with existing rows: `ADD f INT NULL`; `UPDATE .. SET f=0 WHERE f IS NULL`; `ADD CONSTRAINT .. CHECK (f IS NOT NULL)` (validated against backfilled rows); `ADD CONSTRAINT .. DEFAULT 0 FOR f`. A later insert omitting f receives 0; an insert with explicit NULL is rejected by the CHECK.
* E6 (reproduction): `ALTER COLUMN f INT NOT NULL` fails on a ledger table because history rows hold NULL. So true NOT NULL cannot be reached by in-place migration.
* E7: the live Azure SQL ledger table behaviour is assumed to match local SQL Server 2022 for these statements (same engine feature, same message). This is not proven against Azure SQL; the live check happens only when the fixed image is deployed through the approved route.
* E8 (unmeasured): which columns the live `cases` table actually lacks. No live schema read was done; the fix must handle every column of CASE_COLS and QUEUE_COLS and the chat_memory additions.

## Options
* O1 Nullable add only, rely on application. Rejected: NULL could reach reads and loses the NOT NULL invariant silently.
* O2 Add nullable, backfill the declared default in the same transaction, then CHECK (col IS NOT NULL) and a DEFAULT constraint. Preserves default values, non-null invariant and fresh-insert behaviour; the ledger records the backfill UPDATE in the ledger history, which is the intended audit behaviour. Column remains nullable in metadata (E6).
* O3 Drop/recreate cases as a ledger table. Rejected: discards or rewrites ledger data; forbidden.
* O4 Disable ledger or swallow the error. Rejected: forbidden.

Selected: O2, applied only when the target table is a ledger table. Non-ledger SQL Server and SQLite keep the existing NOT NULL DEFAULT path unchanged.

## Risks and Tradeoffs
* Column is nullable in metadata on ledger databases; enforced by CHECK. Documented.
* The backfill UPDATE writes ledger history rows for every case. `_migrate` already rewrites derived columns on stale policy; accepted and tested.
* Types: legacy path adds TEXT on SQL Server. The ledger path uses the same widths as the fresh-create DDL for faithful columns; the existing non-ledger TEXT path is not changed (out of scope).
* Atomicity: `_migrate` runs inside BEGIN IMMEDIATE; DDL and backfill must roll back together on failure. Covered by a failure-injection test.
* Local SQL does not prove Azure SQL behaviour (E7); stated in review.

## Out of Scope
grant-application-admin.py body_directory defect, kaniko Dockerfile variant, legacy_roster_tenant initialisation, any live schema change, deployment.
