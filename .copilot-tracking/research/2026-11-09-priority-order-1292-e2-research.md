<!-- markdownlint-disable-file -->
# Research: issue 1292 extension E2, SQL bootstrap index race (2026-11-09)

Task `1292-e2-1109`, parent `1292-e1-1109`. Extension cycle E2 is the second of five owner-approved new cycles E1-E5 (after spent C5); three remain after this. Authorization: conditional, only if the actual SQL reproduction confirmed a directly coupled bootstrap or order defect. No reset, no extra grant. Research disposition: `executed`.

## E1 validation outcome (actual SQL, nonqueued admission)

Admission: pre-admission proof showed no `flock` holder on `/tmp/ama-rpi-heavy.lock` (the 1288 E3 holder had finished and removed its database), then one `flock -n` succeeded (rc 0). Evidence directory (coordinator files): `e1-sql-admission2-132322-2818937`. Source identity: the five changed source files match the sha256 record of the earlier admission attempt (`e1-sql-admission-130658-2807205/source-sha256.txt`). Fresh container `ama1292-vc-sql-2818957-6311`, image `mcr.microsoft.com/mssql/server:2022-latest` `sha256:cf8f0ab2ebe6...`, SQL Server 2022 RTM-CU27-GDR 16.0.4305.5, removed at exit, no leftover databases.

| Phase | Selector | Exit | Result |
| --- | --- | --- | --- |
| priority | `test_priority_order` (all SQLite plus owned SQL Server classes, `MssqlBeginRecovery`, `MssqlLockTimeoutBegin`) | 0 | 142 tests OK, skipped=1 (R2 skip only) |
| resident | `test_resident_decisions.MssqlResidentControls` | 0 | 91 tests OK, skipped=1 (pre-existing) |
| r2repro | out-of-tree subclass running the unskipped R2 test on owned SQL Server | 1 | 1 test FAILED |

R2 reproduction (smallest actual SQL case: two concurrent first opens of a database whose `recommendations` table lacks `ix_recs_seq`): the second opener fails with `The operation failed because an index or statistics with name 'ix_recs_seq' already exists on table 'recommendations'`.

## Root cause

`MssqlStore._create_indexes` runs each `IF NOT EXISTS (SELECT 1 FROM sys.indexes ...) CREATE INDEX ...` check-then-create statement in autocommit, under only the per-process `dblock`. Two store instances (two processes, replicas or threads with their own store) both pass the existence check and the loser raises. `_create_schema` and `_migrate_chat_memory` already serialize through `BEGIN IMMEDIATE` (`sp_getapplock` `zavaforward_write`); the index step does not. The defect is in schema bootstrap code unchanged by this issue, and is exposed by the concurrent-open guarantee that this issue's ordinal backfill (`created_ord`, `ix_recs_created_ord`) relies on, so it is directly coupled to the claim tested.

## Planning readiness

Ready. Fix: run the index statements inside the existing serialized write transaction (`BEGIN IMMEDIATE` ... `COMMIT`, rollback on error), the pattern `_create_schema` uses. `_create_indexes` is called from `SqlStore._initialize` with no open transaction. SQLite is unaffected (its `CREATE INDEX IF NOT EXISTS` is atomic). Regression: remove the skip from `MssqlLegacyEdges` (the SQL test then runs as designed) and keep the test unchanged.
