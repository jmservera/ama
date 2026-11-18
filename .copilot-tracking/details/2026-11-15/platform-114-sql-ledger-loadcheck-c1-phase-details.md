<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #114 c1 CI Correction for Backend-Agnostic `SqlStoreTests` Pre-Reliance Proofs

## Metadata

* Task ID: issue-114-platform-sql-ledger-loadcheck-c1
* Task slug: platform-114-sql-ledger-loadcheck-c1
* Related plan: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-c1-research.md, src/core/tests/test_sqlstore.py, src/api/tests/test_mssqlstore.py, src/core/src/zava_forward/core/mssqlstore.py, src/core/src/zava_forward/core/sqlstore.py

## Phase Index

| Phase ID | Name                                                                               | Status  | Detail sections       |
|----------|------------------------------------------------------------------------------------|---------|-----------------------|
| P01      | Backend-Agnostic `SqlStoreTests` Pre-Reliance Proofs and Factory-Hook Guard        | Complete | P01, P01-T01, P01-T02 |

<!-- rpi:phase id=P01 -->
## P01: Backend-Agnostic `SqlStoreTests` Pre-Reliance Proofs and Factory-Hook Regression Guard

### Context

`MssqlStoreTests` (`src/api/tests/test_mssqlstore.py:596`) subclasses `SqlStoreTests` (`src/core/tests/test_sqlstore.py:30`) and sets `base.SqlStore = factory` in `setUpClass`, where `factory(data, db, *a, **k)` returns `MssqlStore(data, state_dir=os.path.dirname(db))` (`C2`). In `PR #1814`, the three `test_pre_reliance_*` methods on `SqlStoreTests` failed in the `mssql` CI job (`C3`, `C8`) because they opened `sqlite3.connect(self.db)` (an uninitialized SQLite file when `SqlStore` is `factory`), issued SQLite-only `DROP TRIGGER` statements and 8-column `INSERT INTO audit` statements including `IDENTITY(1,1)` `seq`, and passed the patched function `SqlStore` to `issubclass(MssqlStore, SqlStore)`.

### Intent

Update `src/core/tests/test_sqlstore.py` so all three `test_pre_reliance_*` methods run cleanly on both SQLite (`SqlStore`) and SQL Server (`MssqlStore`), and verify that contract offline by simulating `MssqlStoreTests`'s `SqlStore = lambda data, db, *a, **k: ...` factory hook.

### Boundaries

* Included: `src/core/tests/test_sqlstore.py`.
* Excluded: `src/api/tests/test_mssqlstore.py`, production `src/core/src/` modules, and unrelated test files.

### Likely Targets

* `src/core/tests/test_sqlstore.py`: Add `_drop_audit_triggers`, refactor `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` and `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head`, and update `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` with `BaseSqlStore` and the simulated `MssqlStoreTests` factory hook.

### Dependencies

* None.

### Validation Expectations

* Run `test_sqlstore.py`, `test_loadcheck.py`, `ruff check src/core/tests/test_sqlstore.py`, and `(cd src/core && mypy)`.

### Completion Evidence

* All 12 `SqlStoreTests` methods + 1 `SqlImproveTests` method pass directly, and all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods pass under the simulated `MssqlStoreTests` factory hook, with zero lint or type errors.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Refactor `SqlStoreTests` pre-reliance tamper, dropped-year, and `audit_head` tests to use `_drop_audit_triggers` and `s.db.execute`

#### Context

Both `SqlStore.db` (`isolation_level=None`, `C6`) and `MssqlStore.db` (`autocommit=True`, `C5`) autocommit single statements via `s.db.execute(sql, args)`. On SQL Server `master`, `MssqlStore` protects `audit` with `audit_append_only` (`C4`) and numbers `audit.seq` via `BIGINT IDENTITY(1,1)` (`C4`), while `SqlStore._reliance_audit_snapshot` accepts any strictly increasing positive integer `seq` sequence (`C7`).

#### Intent

Eliminate direct `sqlite3.connect(self.db)` calls, SQLite-only trigger names, secondary store creation (`s2`), and explicit `seq` inserts from `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` and `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head`.

#### Boundaries

* Included:
  * Define `_drop_audit_triggers(self, store)` on `SqlStoreTests`:
    * If `isinstance(store, MssqlStore)`: `store.db.execute("IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only")`.
    * Else: `store.db.execute("DROP TRIGGER IF EXISTS audit_no_update")` and `store.db.execute("DROP TRIGGER IF EXISTS audit_no_delete")`.
  * In `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years`:
    * Drop triggers via `self._drop_audit_triggers(s)` and tamper the 2025 row via `s.db.execute("UPDATE audit SET detail=? WHERE at=?", ("tampered-2025", "2025-02-15T11:00:00"))`.
    * Reuse `s` directly (since `year-2024.json` and `year-2025.json` are already sealed in `s.digest_dir` and triggers are already dropped on `s.db`): run `s.db.execute("DELETE FROM audit")`, rebuild the kept `2025` + `2026` chain from `prev = ledger.GENESIS`, insert each row via `s.db.execute("INSERT INTO audit (at, who, action, case_id, detail, prev, hash) VALUES (?,?,?,?,?,?,?)", (at, who, action, cid, detail, prev, entry["hash"]))`, update `audit_head` via `s.db.execute("UPDATE audit_head SET count=?, hash=? WHERE id=1", (len(kept), prev))`, and assert `s.verify_audit() is True`, `dropped["reliance_allowed"] is False`, `dropped["missing_years"] == ["2024"]`, and `"missing_audit_year"` in `{p["code"] for p in dropped["problems"]}`.
  * In `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head`:
    * Drop triggers via `self._drop_audit_triggers(s)`, delete the tail 2026 row via `s.db.execute("DELETE FROM audit WHERE at=?", ("2026-06-01T10:00:00",))`, verify `audit_head_mismatch`, then run `s.db.execute("DELETE FROM audit_head WHERE id=1")` and verify `audit_head_missing`.
* Excluded: Modifying `test_ledger_is_append_only_and_detects_tampering` (already overridden directly on `MssqlStoreTests` in `src/api/tests/test_mssqlstore.py:608`).

#### Likely Targets

* `src/core/tests/test_sqlstore.py`

#### Dependencies

* None.

#### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_sqlstore.py' -v`

#### Completion Evidence

* Both methods pass without opening `sqlite3.connect` and under `_MssqlSqlGuard` in `P01-T02`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Resolve `BaseSqlStore`, add offline `MssqlStoreTests` factory-hook simulation, and run focused `src/core` validation

#### Context

When `MssqlStoreTests.setUpClass` sets `base.SqlStore = factory`, module-global `SqlStore` inside `test_sqlstore.py` becomes a function rather than a class (`C2`), causing `issubclass(MssqlStore, SqlStore)` to raise `TypeError` (`C8`). In addition, `src/core` CI runs without `mssql-python` (`C10`), so without an offline factory-hook test in `test_sqlstore.py`, future SQLite-only edits to `SqlStoreTests` would only surface later in the SQL Server container job.

#### Intent

Resolve `BaseSqlStore` directly from `zava_forward.core.sqlstore` inside `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` and add a self-contained unit check that patches `test_sqlstore.SqlStore = lambda data, db, *a, **k: ...` to a SQLite-backed `MssqlStore` double with strict T-SQL/identity assertions and runs all three `test_pre_reliance_*` methods under that hook.

#### Boundaries

* Included:
  * Import `from zava_forward.core.sqlstore import SqlStore as BaseSqlStore` inside `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` (preserving module-level `from zava_forward.core.sqlstore import LedgerRelianceError, SqlStore` so `MssqlStoreTests.setUpClass` continues patching `base.SqlStore` seamlessly) and use `BaseSqlStore` in `self.assertTrue(issubclass(MssqlStore, BaseSqlStore))` and `base = BaseSqlStore(self.data, mssql_db)`.
  * Add a helper / unit check invoked from `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` (guarded by `if not getattr(self, "_running_factory_hook", False):`) that:
    1. Defines a lightweight `_MssqlSqlGuard` connection wrapper attached to `store.db` *after* `BaseSqlStore.__init__` finishes (so `executescript(INDEXES)` creates SQLite triggers cleanly during schema init), forwarding non-guarded methods (`executemany`, `close`, etc.) via `__getattr__`, intercepting `"IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only"` (incrementing `dropped_triggers` and dropping SQLite's `audit_no_update` / `audit_no_delete` triggers), and raising `AssertionError` if SQLite trigger names (`audit_no_update` / `audit_no_delete`), columnless `INSERT INTO audit VALUES (...)`, or explicit-`seq` `INSERT INTO audit (...)` statements are sent.
    2. Defines a SQLite-backed `_SimulatedMssqlStore(MssqlStore)` subclass overriding `__init__` to call `BaseSqlStore.__init__(self, data_path, backing_db_path, digest_dir=os.path.join(os.path.dirname(db), "digests"))` without setting `self._env` (keeping `hasattr(self, "_env")` `False` so SQLite continuity queries remain SQLite-compatible), delegating `assistant_connection = BaseSqlStore.assistant_connection` plus `BaseSqlStore` storage hooks (`_open`, `_create_schema`, `_create_indexes`, `_columns`, `_has_rec_order`, `_create_rec_order_index`, `_meta_set`, `_insert_ignore`, `_priority_correction_rows`, `_epoch_sql`, `_add_column_default`, `_contains`, `_limit`, `dberror = sqlite3.Error`), wrapping `self.db = _MssqlSqlGuard(self.db)` post-init, and storing its SQLite file at a per-replayed-method backing path separate from `db` (`pw.sqlite` remains non-existent on disk, matching real `MssqlStoreTests.setUp` `wipe()`).
    3. Patches module-global `SqlStore` via `patch.dict(globals(), {"SqlStore": lambda data, db, *a, **k: ...})` (registering `case.addCleanup(store.db.close)` inside the simulated factory) and replays fresh `SqlStoreTests` instances (`_running_factory_hook = True`, `setUp` -> method -> `try/finally` `doCleanups()` + `tearDown()`) for all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods (all `test_*` on `SqlStoreTests` except `test_ledger_is_append_only_and_detects_tampering` and `test_list_filters_use_indexes`), asserting `not os.path.exists(case.db)` on every method and `dropped_triggers == 1` specifically on `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` and `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head` (`0` on the remaining 8).
  * Run all four required validation commands (`test_sqlstore.py`, `test_loadcheck.py`, `ruff check src/core/tests/test_sqlstore.py`, `(cd src/core && mypy)`).
* Excluded: Requiring `mssql-python` or external network/container dependencies.

#### Likely Targets

* `src/core/tests/test_sqlstore.py`

#### Dependencies

* `P01-T01`

#### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_sqlstore.py' -v`
* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_loadcheck.py' -v`
* `python3 -m ruff check src/core/tests/test_sqlstore.py`
* `(cd src/core && mypy)`

#### Completion Evidence

* All validation commands exit `0` and `_MssqlSqlGuard` confirms T-SQL trigger-drop dispatch and non-creation of `pw.sqlite`.

#### Unresolved Items

* None.
