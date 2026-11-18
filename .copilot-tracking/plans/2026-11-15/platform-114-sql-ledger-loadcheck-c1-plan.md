<!-- markdownlint-disable-file -->
# RPI Plan: Issue #114 c1 CI Correction for Backend-Agnostic `SqlStoreTests` Pre-Reliance Proofs

## Task Metadata

* Task ID: issue-114-platform-sql-ledger-loadcheck-c1
* Task slug: platform-114-sql-ledger-loadcheck-c1
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan-critique.md

## Executive Summary

This plan delivers the `c1` CI correction for `PR #1814` (Issue `#114`: Move cases, recommendations and the audit ledger to Azure SQL) inside `src/core/tests/test_sqlstore.py`. In `Source projects CI`, the `mssql` job runs `MssqlStoreTests(base.SqlStoreTests)` (`src/api/tests/test_mssqlstore.py`), which patches `test_sqlstore.SqlStore = factory` so every `SqlStoreTests` method runs against SQL Server (`MssqlStore`). The three new `test_pre_reliance_*` methods added in `PR #1814` failed under `MssqlStoreTests` because (1) two methods bypassed `s.db` via `sqlite3.connect(self.db)` and issued SQLite-only `DROP TRIGGER audit_no_update` / `DROP TRIGGER audit_no_delete` plus explicit `seq` inserts into an `IDENTITY(1,1)` table, and (2) the third method called `issubclass(MssqlStore, SqlStore)` after `SqlStore` had been patched to a factory function.

The plan updates `src/core/tests/test_sqlstore.py` in one bounded phase (`P01`) so all three `test_pre_reliance_*` methods use backend-agnostic `s.db.execute(...)` mutations, `_drop_audit_triggers(self, store)`, single-store reuse with 7-column `INSERT INTO audit` (omitting `seq`), and `BaseSqlStore` class resolution, plus an offline unit check simulating `MssqlStoreTests` patching `test_sqlstore.SqlStore = lambda data, db, *a, **k: ...` with a strict SQL-guard `MssqlStore` double so regressions are caught in `src/core` unit tests without needing a live SQL Server container.

### User Decisions and Requirements Highlights

* **Backend-agnostic `SqlStoreTests` pre-reliance proofs (`P01-T01`)**: Add `_drop_audit_triggers(self, store)` on `SqlStoreTests` (`IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only` when `isinstance(store, MssqlStore)`, else `DROP TRIGGER IF EXISTS audit_no_update` and `audit_no_delete`), replace `sqlite3.connect(self.db)` with `s.db.execute(...)` (`WHERE at=?`), reuse `s` directly for the dropped-2024 check with 7-column `INSERT INTO audit (at, who, action, case_id, detail, prev, hash) VALUES (?,?,?,?,?,?,?)` omitting `seq`, and resolve `from zava_forward.core.sqlstore import SqlStore as BaseSqlStore` while keeping `SqlStore = BaseSqlStore` patchable at module scope.
* **Offline `MssqlStoreTests` factory-hook regression check (`P01-T02`)**: Extend `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` with a unit check that patches `test_sqlstore.SqlStore = lambda data, db, *a, **k: ...` and replays all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods against a SQLite-backed `MssqlStore` test double enforcing post-init T-SQL trigger DDL, non-existent `pw.sqlite`, and auto-generated `seq` inserts (rejecting both columnless `INSERT INTO audit VALUES` and explicit `seq` column lists), then run focused `src/core` validation (`test_sqlstore.py`, `test_loadcheck.py`, `ruff check`, `mypy`) and leave a clean frozen local commit without pushing or opening a PR.

### What You May Not Know

* **Reusing `s` for the dropped-2024 check prevents a shared SQL Server database collision**: `MssqlStoreTests.setUp` runs `wipe()` once per test method (`src/api/tests/test_mssqlstore.py:604`), so opening a second `s2 = SqlStore(self.data, db2)` inside the same test method on SQL Server would attach to the already-populated `master` database and shared `digests` directory. Reusing `s` after `s.db.execute("DELETE FROM audit")` works identically on SQLite and SQL Server.
* **Offline factory-hook replay must restore `globals()["SqlStore"]` and guard against self-recursion**: Because `MssqlStoreTests` inherits `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` and runs it in CI with `globals()["SqlStore"]` already set to `test_mssqlstore.factory`, scoping the offline simulation with `patch.dict(globals(), {"SqlStore": ...})` and a `_running_factory_hook` flag ensures `MssqlStoreTests`'s real SQL Server factory is preserved and never recurses infinitely.

### Unresolved Decisions or Blockers

* None. Hosted `mssql` CI execution on `PR #1814` will run once the coordinator pushes the frozen commit.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop (`rpi-research`, `rpi-plan`, `rpi-implement`, `rpi-review`) in order, writing dated `2026-11-15` artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) for Issue `#114` (`c1` CI correction on `PR #1814`) on branch `feat/platform-114-sql-ledger-loadcheck` without pushing or opening a PR (caller prompt).
* Add `_drop_audit_triggers(self, store)` on `SqlStoreTests` in `src/core/tests/test_sqlstore.py`, dispatching `IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only` when `isinstance(store, MssqlStore)` and `DROP TRIGGER IF EXISTS audit_no_update` / `DROP TRIGGER IF EXISTS audit_no_delete` otherwise (caller Required Fix 1).
* Update `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` to use `self._drop_audit_triggers(s)` and `s.db.execute("UPDATE audit SET detail=? WHERE at=?", ("tampered-2025", "2025-02-15T11:00:00"))`, and reuse `s` directly for the dropped-2024 check (`DELETE FROM audit`, 7-column `INSERT INTO audit (at, who, action, case_id, detail, prev, hash) VALUES (?,?,?,?,?,?,?)` omitting `seq`, `UPDATE audit_head SET count=?, hash=? WHERE id=1`, and existing assertions on `verify_audit()`, `reliance_allowed`, `missing_years == ["2024"]`, and `"missing_audit_year"`) (caller Required Fix 2).
* Update `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head` to use `self._drop_audit_triggers(s)`, `s.db.execute("DELETE FROM audit WHERE at=?", ("2026-06-01T10:00:00",))`, and `s.db.execute("DELETE FROM audit_head WHERE id=1")` instead of `sqlite3.connect(self.db)` (caller Required Fix 3).
* Update `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` to resolve `from zava_forward.core.sqlstore import SqlStore as BaseSqlStore` for `issubclass(MssqlStore, BaseSqlStore)` and `BaseSqlStore(self.data, mssql_db)`, and add a unit check simulating `MssqlStoreTests` patching `test_sqlstore.SqlStore = lambda data, db, *a, **k: ...` so `SqlStoreTests` methods are verified under the `MssqlStoreTests` factory hook (caller Required Fix 4).
* Run focused validation (`test_sqlstore.py`, `test_loadcheck.py`, `ruff check src/core/tests/test_sqlstore.py`, and `(cd src/core && mypy)`) and commit code plus `.copilot-tracking/` artifacts locally with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` (caller Validation Commands).

## Goals

* Make all three `test_pre_reliance_*` methods on `SqlStoreTests` completely portable between SQLite (`SqlStore`) and SQL Server (`MssqlStore` via `MssqlStoreTests`).
* Catch any `MssqlStoreTests` factory-patching, trigger-DDL, `pw.sqlite` path, or identity-column regression offline inside `src/core/tests/test_sqlstore.py` without requiring `mssql-python` or a live SQL Server container.

## Scope and Non-Goals

### In Scope

* `src/core/tests/test_sqlstore.py`.
* Dated `2026-11-15` RPI tracking artifacts for `platform-114-sql-ledger-loadcheck-c1`.

### Non-Goals

* Editing `src/api/tests/test_mssqlstore.py` or any module under `src/core/src/`.
* Running `python3 tools/rpi-checks.py --all`, pushing to `origin`, or opening/updating a pull request.

## Functional Requirements

* **FR-1 (Backend-agnostic audit trigger drop and tamper/dropped-year/head mutations in `SqlStoreTests`)**:
  * `SqlStoreTests._drop_audit_triggers(self, store)` executes `IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only` when `isinstance(store, MssqlStore)` and `DROP TRIGGER IF EXISTS audit_no_update` + `DROP TRIGGER IF EXISTS audit_no_delete` otherwise.
  * `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` drops triggers via `self._drop_audit_triggers(s)`, tampers via `s.db.execute("UPDATE audit SET detail=? WHERE at=?", ("tampered-2025", "2025-02-15T11:00:00"))`, and reuses `s` directly (`DELETE FROM audit`, 7-column `INSERT INTO audit (at, who, action, case_id, detail, prev, hash) VALUES (?,?,?,?,?,?,?)` omitting `seq`, `UPDATE audit_head SET count=?, hash=? WHERE id=1`) to verify `s.verify_audit() is True`, `dropped["reliance_allowed"] is False`, `dropped["missing_years"] == ["2024"]`, and `"missing_audit_year"` in `{p["code"] for p in dropped["problems"]}`.
  * `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head` drops triggers via `self._drop_audit_triggers(s)`, deletes the unsealed tail row via `s.db.execute("DELETE FROM audit WHERE at=?", ("2026-06-01T10:00:00",))`, verifies `audit_head_mismatch`, deletes `audit_head` via `s.db.execute("DELETE FROM audit_head WHERE id=1")`, and verifies `audit_head_missing`.
  * Observable acceptance criteria: Neither `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` nor `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head` calls `sqlite3.connect(...)`, references SQLite trigger names directly, opens a secondary store, or inserts explicit `seq` values into `audit`.
* **FR-2 (`BaseSqlStore` class resolution and offline `MssqlStoreTests` factory-hook verification)**:
  * `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` resolves `from zava_forward.core.sqlstore import SqlStore as BaseSqlStore` so `issubclass(MssqlStore, BaseSqlStore)` and `BaseSqlStore(self.data, mssql_db)` succeed even when module-global `test_sqlstore.SqlStore` is patched to a function.
  * When not already inside a simulated hook (`not getattr(self, "_running_factory_hook", False)`), `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` patches module-global `SqlStore = lambda data, db, *a, **k: ...` via `patch.dict(globals(), ...)` to return a SQLite-backed `MssqlStore` test double (calling `BaseSqlStore.__init__` without setting `self._env`, storing its DB outside `db` so `pw.sqlite` never exists, attaching `_MssqlSqlGuard` post-init with `__getattr__` delegation, enforcing T-SQL `audit_append_only` drop syntax, and rejecting SQLite trigger names, columnless `INSERT INTO audit VALUES`, and explicit-`seq` `INSERT INTO audit (...)` statements) and replays all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods with `try/finally` resource cleanup.
  * Observable acceptance criteria: All 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods pass under the simulated `SqlStore = lambda data, db, *a, **k: ...` `MssqlStore` factory hook with `not os.path.exists(case.db)` on every method, T-SQL trigger-drop count `1` on each of the two trigger-dropping pre-reliance methods (`0` on the remaining 8), and `globals()["SqlStore"]` restored afterward.

## Non-Functional Requirements

* **SQLite and T-SQL dialect portability without `mssql-python` offline dependency**
  * Objective threshold or evaluation condition: Zero `mssql_python` imports required during `src/core` unit tests, zero `sqlite3.connect(self.db)` calls inside `test_pre_reliance_*`, and 100% compatibility with `MssqlStore._Conn.execute` (`autocommit=True`, `?` placeholders, `[key]`/`[user]` rewrites).
  * Operating condition or verification approach: Offline `unittest` run of `test_sqlstore.py` (including `_MssqlSqlGuard` assertions) plus `ruff check` and `mypy`.
  * Observable acceptance criteria: `test_sqlstore.py`, `test_loadcheck.py`, `ruff check`, and `mypy` all exit `0`.

## Acceptance Criteria

* `_drop_audit_triggers(self, store)` exists on `SqlStoreTests` and dispatches T-SQL `audit_append_only` for `MssqlStore` instances and SQLite `audit_no_update`/`audit_no_delete` otherwise.
* `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` and `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head` perform all tamper/delete/insert operations via `s.db.execute(...)`, reuse `s` directly for the dropped-2024 check, and omit `seq` on `INSERT INTO audit`.
* `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` uses `BaseSqlStore` for `issubclass` and `BaseSqlStore(...)` instantiation and verifies all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods under `test_sqlstore.SqlStore = lambda data, db, *a, **k: ...`.
* All validation commands (`test_sqlstore.py`, `test_loadcheck.py`, `ruff check src/core/tests/test_sqlstore.py`, `(cd src/core && mypy)`) exit `0`, and changes + `.copilot-tracking/` artifacts are committed locally on `feat/platform-114-sql-ledger-loadcheck` with the Copilot trailer and no push/PR.

## Test Ownership and Validation Lock

* Canonical test target: `src/core/tests/test_sqlstore.py` (`SqlStoreTests`).
* Generated targets: None.
* Exact test removals: `none` (all 12 existing `SqlStoreTests` methods + 1 `SqlImproveTests` method = 13 total methods in `src/core/tests/test_sqlstore.py` are preserved).
* Maximum new `test_*` method additions: `0` to `1` (all required checks update the 3 existing `test_pre_reliance_*` methods in place and add helper methods `_drop_audit_triggers` / factory-hook verification inside `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore`, so `MssqlStoreTests` inherits the exact intended suite without redundant duplicate methods).
* Semantic vs regression coverage: Semantic coverage proves multi-year (`2024`, `2025`, `2026`) pre-reliance tamper, dropped-year, `audit_head`, and secret-scrubbing contracts on both SQLite and `MssqlStore`; regression coverage replays all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods under the `MssqlStoreTests` `SqlStore = lambda ...` factory hook offline so `sqlite3.connect(self.db)`, SQLite trigger names, columnless or explicit-`seq` identity inserts, and `issubclass(..., SqlStore)` regressions fail immediately.
* Locked validation commands:
  * `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_sqlstore.py' -v`
  * `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_loadcheck.py' -v`
  * `python3 -m ruff check src/core/tests/test_sqlstore.py`
  * `(cd src/core && mypy)`

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md                                           |
| Phase details                    | .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md                                |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan-critique.md with Revise (PC-001, PC-002 resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-c1-research.md                                    |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/platform-114-sql-ledger-loadcheck-c1-changes.md is created by implementation         |
| Planning execution and readiness | Complete; Ready for Implementation                                                                                        |
| Continuation context             | Confirmed automatic RPI Agent parent advances directly to `rpi-implement`                                                 |

## Sources

* `.copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-c1-research.md`: Primary `c1` research findings (`C1`–`C10`) and T-SQL/SQLite portability verification.
* `src/core/tests/test_sqlstore.py`: Target test suite containing `SqlStoreTests` and the three `test_pre_reliance_*` methods.
* `src/api/tests/test_mssqlstore.py`: `MssqlStoreTests(base.SqlStoreTests)` factory-patching harness (`base.SqlStore = factory`, `wipe()`).
* `src/core/src/zava_forward/core/mssqlstore.py` and `src/core/src/zava_forward/core/sqlstore.py`: `MssqlStore` and `SqlStore` connection, trigger, `IDENTITY(1,1)`, and `_reliance_audit_snapshot` implementations.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Backend-Agnostic `SqlStoreTests` Pre-Reliance Proofs and Factory-Hook Regression Guard

* Intent: Refactor the three `test_pre_reliance_*` methods in `src/core/tests/test_sqlstore.py` to be backend-agnostic across `SqlStore` and `MssqlStore`, add the offline `MssqlStoreTests` factory-hook check, and verify all focused `src/core` checks pass.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Refactor `SqlStoreTests` pre-reliance tamper, dropped-year, and `audit_head` tests to use `_drop_audit_triggers` and `s.db.execute`

* Requirement and evidence: FR-1 (`C2`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`)
* Expected result: `SqlStoreTests` defines `_drop_audit_triggers(self, store)` and updates `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` and `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head` to mutate via `s.db.execute(...)`, reuse `s` directly for the dropped-2024 check, and insert 7 columns into `audit` without `seq`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Resolve `BaseSqlStore`, add offline `MssqlStoreTests` factory-hook simulation, and run focused `src/core` validation

* Requirement and evidence: FR-2, NFR portability & lint/typing (`C2`, `C4`, `C5`, `C8`, `C10`)
* Expected result: `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` uses `BaseSqlStore` and replays all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods under a guarded `SqlStore = lambda data, db, *a, **k: ...` `MssqlStore` factory double; `test_sqlstore.py`, `test_loadcheck.py`, `ruff check`, and `mypy` all pass cleanly.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md

## Dependencies

* Python 3.12 environment with `zava_forward.core`, `ruff`, and `mypy` installed (verified in workspace).

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High]: `_SimulatedMssqlStore` `self._env` leak, post-init `_MssqlSqlGuard` attachment, and columnless `INSERT INTO audit VALUES` rejection | Resolved | Updated `FR-2` and `P01-T02` so `_SimulatedMssqlStore.__init__` delegates to `BaseSqlStore.__init__` without setting `self._env` (and sets `assistant_connection = BaseSqlStore.assistant_connection`), wraps `self.db` in `_MssqlSqlGuard` after `BaseSqlStore.__init__` completes with `__getattr__` forwarding (`executemany`, `close`, etc.), and rejects both columnless `INSERT INTO audit VALUES` and explicit-`seq` `INSERT INTO audit (...)` statements. |
| `PC-002` [Medium]: Scoped trigger-drop assertions, `try/finally` cleanup, and full 10-method `MssqlStoreTests`-inherited replay | Resolved | Updated `FR-2`, `Test Ownership and Validation Lock`, and `P01`/`P01-T02` to record the exact method counts (`12` `SqlStoreTests` + `1` `SqlImproveTests`), replay all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods with `case.addCleanup(store.db.close)` and `try/finally` `doCleanups()`/`tearDown()`, assert `not os.path.exists(case.db)` on all 10 methods, and assert T-SQL trigger-drop count `1` on each of the two trigger-dropping pre-reliance methods (`0` on the other 8). |
| Residual risk: Live SQL Server container execution deferred to hosted CI | Accepted with risk | Caller explicitly forbids remote push/PR updates in this run; hosted `mssql` job verification in `Source projects CI` remains tracked in `## Follow-Up Items` for coordinator push. |

## Follow-Up Items

* Push the frozen commit to `PR #1814` and observe the hosted `mssql` job in `Source projects CI` (owned by coordinator/owner; push excluded in this run).
* Carried-forward parent follow-ups: optional `RV-001`/`RV-002` offline hardening in `store.py`/`sqlstore.py`/`ledger.py`, live Azure SQL `GP_S_Gen5` metered `loadcheck` run (`Refs #114`), and witnessed `DH-005` Azure SQL point-in-time restore drill (`Refs #114`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/platform-114-sql-ledger-loadcheck-c1-changes.md
* Ready phase or task: Complete (ready for `rpi-review`)
* Remaining provisional question or blocker: None
