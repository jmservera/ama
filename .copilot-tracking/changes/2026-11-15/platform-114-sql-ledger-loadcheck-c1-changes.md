<!-- markdownlint-disable-file -->
# RPI Changes: Issue #114 c1 CI Correction for Backend-Agnostic `SqlStoreTests` Pre-Reliance Proofs

## Metadata

* Task ID: issue-114-platform-sql-ledger-loadcheck-c1
* Related plan: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`: `P01-T01`, `P01-T02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`
* All remaining active-plan markers: None
* Status basis: All planned changes in `src/core/tests/test_sqlstore.py` are complete and verified across `test_sqlstore.py`, `test_loadcheck.py`, `test_mssqlstore.py` offline checks, `ruff check`, and `mypy`.

## Execution Summary

Delivered the full `P01` correction in `src/core/tests/test_sqlstore.py` so all three `test_pre_reliance_*` methods on `SqlStoreTests` run portably across SQLite (`SqlStore`) and SQL Server (`MssqlStore`), and added an offline factory-hook verification (`_verify_mssqlstore_factory_hook`) replaying all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods under `test_sqlstore.SqlStore = factory`.

## Completed Work

### Backend-Agnostic Pre-Reliance Trigger Drop, Tamper, Dropped-Year, and `audit_head` Mutations

* Related phase or task: `P01-T01`
* Files: `src/core/tests/test_sqlstore.py`
* What changed and why: Added `SqlStoreTests._drop_audit_triggers(self, store)` (`IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only` when `isinstance(store, MssqlStore)`, else `DROP TRIGGER IF EXISTS audit_no_update` and `DROP TRIGGER IF EXISTS audit_no_delete`); replaced `sqlite3.connect(self.db)` and `WHERE seq=...` in `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` and `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head` with `s.db.execute(...)` (`WHERE at=?`); and reused `s` directly for the dropped-2024 check with 7-column `INSERT INTO audit (at, who, action, case_id, detail, prev, hash) VALUES (?,?,?,?,?,?,?)` omitting `seq` so both SQLite `AUTOINCREMENT` and SQL Server `BIGINT IDENTITY(1,1)` auto-number cleanly without shared-database collisions.
* Completion evidence: Zero `sqlite3.connect` calls remain in any `test_pre_reliance_*` method; both methods pass directly and under `_MssqlSqlGuard`.
* Validation: Passed (`test_sqlstore.py` 21/21 tests).

### `BaseSqlStore` Class Resolution and Offline `MssqlStoreTests` Factory-Hook Replay

* Related phase or task: `P01-T02`
* Files: `src/core/tests/test_sqlstore.py`
* What changed and why: Resolved `from zava_forward.core.sqlstore import SqlStore as BaseSqlStore` inside `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` for `issubclass(MssqlStore, BaseSqlStore)` and `BaseSqlStore(self.data, mssql_db)` while keeping module-global `SqlStore` patchable by `MssqlStoreTests.setUpClass`, and added `_verify_mssqlstore_factory_hook(self, base_sql_cls)` replaying all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods under `patch.dict(globals(), {"SqlStore": factory})` using `_SimulatedMssqlStore` + post-init `_MssqlSqlGuard` (`not os.path.exists(case.db)` on all 10 methods, `dropped_triggers == 1` on each of the two trigger-dropping methods, and rejection of SQLite trigger names, columnless `INSERT INTO audit VALUES`, and explicit-`seq` `INSERT INTO audit (...)`). Also sorted standard-library imports (`pathlib` before `unittest.mock`) for `ruff` `I` clean compliance.
* Completion evidence: All 10 inherited methods pass under the simulated `MssqlStoreTests` factory hook, `test_mssqlstore.py` offline discovery passes (`248` tests, `9` portable checks ok, `239` live-server tests skipped cleanly), and `ruff` + `mypy` exit `0`.
* Validation: Passed (`test_sqlstore.py`, `test_loadcheck.py`, `test_mssqlstore.py` offline, `ruff check`, `mypy`).

## Implementation-Time Plan and Detail Updates

None. Implementation matched the post-critique `Ready` plan without amendment or divergence.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_sqlstore.py' -v` | `src/core/tests/test_sqlstore.py` | Passed | `Ran 21 tests in 20.140s OK` (9 `SqlImproveTests` + 12 `SqlStoreTests`, including 10-method `MssqlStoreTests` factory-hook replay) |
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_loadcheck.py' -v` | `src/core/tests/test_loadcheck.py` | Passed | `Ran 20 tests in 0.174s OK` |
| `(cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p 'test_mssqlstore.py' -v)` | `src/api/tests/test_mssqlstore.py` | Passed | `Ran 248 tests in 0.629s OK (skipped=239)` confirming `MssqlStoreTests(base.SqlStoreTests)` class/method inheritance |
| `python3 -m ruff check src/core/tests/test_sqlstore.py` and `(cd src/core && python3 -m ruff check)` | `src/core` | Passed | `All checks passed!` |
| `(cd src/core && python3 -m mypy)` | `src/core` | Passed | `Success: no issues found in 373 source files` |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`, `P01-T01`, `P01-T02` checked `[x]`; `P01` marked `Complete` in phase details).
* Completed-work evidence and handoff prose: Current and synchronized across plan, details, and changes record.
* Validation, blockers, remaining work, and follow-up items: Current (`0` blockers, `0` remaining active-plan items, follow-up items synchronized).
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md, `## Follow-Up Items`
* Push the frozen commit to `PR #1814` and observe the hosted `mssql` job in `Source projects CI` (coordinator-owned).
* Carried-forward parent follow-ups: optional `RV-001`/`RV-002` offline hardening in `store.py`/`sqlstore.py`/`ledger.py`, live Azure SQL `GP_S_Gen5` metered `loadcheck` run (`Refs #114`), and witnessed `DH-005` Azure SQL point-in-time restore drill (`Refs #114`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`; completed `P01`, `P01-T01`, `P01-T02`; remaining: none)
* Validation coverage: `test_sqlstore.py` (21 passed), `test_loadcheck.py` (20 passed), `test_mssqlstore.py` offline checks (passed), `ruff check` (passed), `mypy` (passed)
* Blockers: None
* Current plan and detail updates: None
* Planning and critique state: Ready (`PC-001`, `PC-002` resolved directly)
* Follow-up items: Coordinator push + 3 carried-forward parent follow-ups
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
