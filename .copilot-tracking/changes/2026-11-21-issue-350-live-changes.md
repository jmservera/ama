# Changes 2026-11-21: issue 350 legacy-body repair

Started after cherry-pick of 4a282143e. Source edits (reverted once and re-applied after this record, to keep the witness order): `src/core/src/zava_forward/core/sqlstore.py` repair skips bodies `_row` cannot build; test `test_repair_skips_legacy_bodies_that_lack_row_fields` in `src/core/tests/test_sqlreads.py`.

Tier FULL (src change); no rpi-checks --all run by the worker.

## Validation

* `test_sqlreads` + `test_sqlstore`: 38 tests OK, including the new legacy-body test.
* Full `src/core` discover run: summary line not captured in the output tail; treat as not separately confirmed. Targeted tests above are the recorded evidence.
* `mypy` in src/core: 23 errors in 4 files, identical before and after the change (none in sqlstore.py). `ruff check` passed.
* MSSQL selector (`test_mssqlstore.MssqlLedgerMigration`): not run; no ZF_TEST_MSSQL/ZF_SQL_* configuration and no SQL Server in this worktree. The failing path (`KeyError: 'appointments'` in `_row`) is covered by the SQLite unit test.

## Per-criterion status (issue #350)

| Criterion | Status | Reason |
| --- | --- | --- |
| Anonymous API 401 in browser mode | Unproven this run | No live probe run; see 2026-11-20 live r4 note |
| Tenant/staff prerequisite and parity rows | Unproven | Needs live multi-role execution; out of scope for this fix |
| Continuing synthetic baseline | Unproven | No data restore performed |
| Model deployment and assistants | Unproven | No Azure change in goal |
| Map provider | Unproven | Not configured or tested |
| Delegated photo token | Unproven | Not tested |
| Law store seed | Unproven | Not tested |
| Ledger/document/digest durability | Unproven | MSSQL selector not run; code fix only |
| Time capture gating | Unproven | Not tested |
| Per-role results record | Unproven | Not tested |
