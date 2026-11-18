<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #114 c1 CI Correction for Backend-Agnostic `SqlStoreTests` Pre-Reliance Proofs

## Metadata

* Task ID: issue-114-platform-sql-ledger-loadcheck-c1
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the `c1` CI correction for Issue `#114` (`PR #1814`) on branch `feat/platform-114-sql-ledger-loadcheck`, scoping edits strictly to `src/core/tests/test_sqlstore.py` plus dated `2026-11-15` `.copilot-tracking/` artifacts without pushing or opening a PR. Implement the 4-part fix: (1) add `SqlStoreTests._drop_audit_triggers(self, store)` branching on `isinstance(store, MssqlStore)`, (2) refactor `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` to use `self._drop_audit_triggers(s)`, `s.db.execute("UPDATE audit SET detail=? WHERE at=?", ...)`, and single-store reuse of `s` with 7-column `INSERT INTO audit` omitting `seq`, (3) refactor `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head` to use `self._drop_audit_triggers(s)` and `s.db.execute(...)` deletes, and (4) resolve `BaseSqlStore` inside `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` and add an offline unit check simulating `MssqlStoreTests` patching `test_sqlstore.SqlStore = lambda data, db, *a, **k: ...`.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-c1-research.md (`C1`-`C10`), .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md, .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md, src/core/tests/test_sqlstore.py, src/api/tests/test_mssqlstore.py, src/core/src/zava_forward/core/mssqlstore.py, and src/core/src/zava_forward/core/sqlstore.py.
* Decisions, dependencies, and acceptance criteria considered: Single-file implementation boundary (`src/core/tests/test_sqlstore.py`); preservation of module-level `SqlStore` symbol for `MssqlStoreTests.setUpClass` (`base.SqlStore = factory`); zero `mssql-python` runtime requirement in `src/core` unit tests; focused validation lock (`test_sqlstore.py`, `test_loadcheck.py`, `ruff check src/core/tests/test_sqlstore.py`, `(cd src/core && mypy)`); local commit only with no remote push or PR update.
* Assessment boundary: Evaluates plan and phase-detail accuracy, SQLite and T-SQL dialect parity, and offline `MssqlStoreTests` factory-hook mechanics strictly from the supplied artifacts and four code files. Live execution against the hosted SQL Server 2022 service container (`mssql` job in `Source projects CI`) is outside offline scope until the coordinator pushes the frozen commit.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Required Fix 1 (`_drop_audit_triggers` helper; `C2`, `C4`, `C6`) | Covered | `FR-1` and `P01-T01` match T-SQL `audit_append_only` (`src/core/src/zava_forward/core/mssqlstore.py:77`, `src/api/tests/test_mssqlstore.py:48`) and SQLite `audit_no_update` / `audit_no_delete` (`src/core/src/zava_forward/core/sqlstore.py:98-99`). |
| Required Fix 2 (multi-year tamper and dropped-2024 reuse of `s`; `C4`-`C9`) | Covered | `FR-1` and `P01-T01` replace `sqlite3.connect` with autocommitted `s.db.execute(...)`, reuse `s` to avoid SQL Server single-DB `s2` collision, omit `seq` on 7-column `INSERT INTO audit`, and retain all required assertions. |
| Required Fix 3 (`audit_head` mismatch and missing-head mutations; `C5`, `C6`, `C8`) | Covered | `FR-1` and `P01-T01` replace `sqlite3.connect` and `WHERE seq=6` with `self._drop_audit_triggers(s)`, `DELETE FROM audit WHERE at=?`, and `DELETE FROM audit_head WHERE id=1` via `s.db.execute(...)`. |
| Required Fix 4 (`BaseSqlStore` alias and `MssqlStoreTests` factory-hook check; `C2`, `C8`, `C10`) | Partial | `BaseSqlStore` resolution is sound, but `_SimulatedMssqlStore` and `_MssqlSqlGuard` in `P01-T02` have concrete initialization, SQL-guard, and per-method assertion gaps (`PC-001`, `PC-002`). |
| `P01` / `P01-T01` | Covered | Scoped cleanly to `src/core/tests/test_sqlstore.py` with verified autocommit and sequence-monotonicity semantics (`src/core/src/zava_forward/core/sqlstore.py:223,1525`, `src/core/src/zava_forward/core/mssqlstore.py:139`). |
| `P01-T02` and Test Ownership / Validation Lock | Partial | Validation commands match caller requirements, but `_SimulatedMssqlStore.__init__` / `_env` handling, post-init `_MssqlSqlGuard` wrapping, columnless `INSERT INTO audit VALUES` detection (`PC-001`), and replay assertions/cleanup/method coverage (`PC-002`) need direct planner refinement. |

## Verdict

* Verdict: Revise
* Rationale: Parts 1-3 (`P01-T01`) and `BaseSqlStore` resolution are well-grounded in `SqlStore` and `MssqlStore` code, but `P01-T02`'s `_SimulatedMssqlStore` and `_MssqlSqlGuard` specification contains concrete SQLite-vs-T-SQL initialization and assertion hazards (`PC-001`, `PC-002`) that would fail during implementation or miss columnless identity-insert regressions unless corrected in the plan and phase details. Both findings are direct planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `_SimulatedMssqlStore` and `_MssqlSqlGuard` in `P01-T02` leak `self._env` (`mssql=True`) into SQLite migrations and miss initialization and columnless-`INSERT` SQL-guard boundaries

* Related IDs: Required Fix 4, `FR-2`, `P01`, `P01-T02`, `C4`, `C5`, `C6`, `C8`, `C10`
* Evidence: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md (`P01-T02`), src/core/src/zava_forward/core/mssqlstore.py:217-219, src/core/src/zava_forward/core/sqlstore.py:98-99,196-207,273,285,293,328,591,647,1430, and src/core/tests/test_sqlstore.py:175
* Concern: Three implementation details in `P01-T02` conflict with `SqlStore` and `MssqlStore` internals:
  1. `P01-T02` item 2 lists `BaseSqlStore` hook delegations on `_SimulatedMssqlStore(MssqlStore)` without overriding `__init__` (or `assistant_connection`). Inheriting `MssqlStore.__init__` (`src/core/src/zava_forward/core/mssqlstore.py:218`) sets `self._env`, which causes `SqlStore._migrate()` (`src/core/src/zava_forward/core/sqlstore.py:328`), `continuity_suspension()` (`line 293`), and `_proc_write()` (`line 1430`) to evaluate `mssql=hasattr(self, "_env")` as `True` and issue T-SQL continuity statements against a `sqlite3.Connection`.
  2. During `BaseSqlStore._initialize` (`src/core/src/zava_forward/core/sqlstore.py:196-207`), `_create_schema()` and `_create_indexes()` call `self.db.executescript(...)` where `INDEXES` (`lines 98-99`) explicitly contains `CREATE TRIGGER IF NOT EXISTS audit_no_update` and `audit_no_delete`, `_seed()` and `_refresh_queue_membership()` call `self.db.executemany(...)` (`lines 591, 647`), and test cleanups call `s.db.close()`. Attaching `_MssqlSqlGuard` inside `_open` without permitting schema initialization or delegating `executemany`/`close` will break store setup or cleanup.
  3. `P01-T02` item 1 specifies rejecting explicit `seq` `INSERT INTO audit` statements, but the actual failing query in `src/core/tests/test_sqlstore.py:175` was columnless `INSERT INTO audit VALUES (?,?,?,?,?,?,?,?)`, which omits a column list and never mentions the token `seq` while still targeting `IDENTITY(1,1)` on SQL Server.
* Impact: Literal implementation of `_SimulatedMssqlStore` and `_MssqlSqlGuard` as written in `P01-T02` will either fail during `SqlStore._initialize` on SQLite (`continuity.sync_sql_gate(..., mssql=True)` / `executescript(INDEXES)` / `executemany`) or fail to catch columnless `INSERT INTO audit VALUES (...)` identity-insert regressions.
* Smallest useful change: Update `P01-T02` in `.copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md` so `_SimulatedMssqlStore(MssqlStore)` overrides `__init__` to call `BaseSqlStore.__init__(self, data_path, backing_db_path, digest_dir=os.path.join(os.path.dirname(db), "digests"))` without setting `self._env` (and delegates `assistant_connection = BaseSqlStore.assistant_connection`), wraps `self.db = _MssqlSqlGuard(self.db, ...)` after `BaseSqlStore.__init__` completes while forwarding non-guarded connection methods (`executemany`, `close`, etc.) via `__getattr__`, and rejects both columnless `INSERT INTO audit VALUES` and any `INSERT INTO audit (...)` column list containing `seq`.
* Action owner: planning_parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md` (`P01-T02`) explicitly specifies `BaseSqlStore.__init__` delegation without `self._env`, post-init `_MssqlSqlGuard` attachment with connection method delegation, and rejection of both columnless and explicit-`seq` `INSERT INTO audit` statements.
* Decision route: direct planner correction (planner can apply directly without a user decision)

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Factory-hook replay in `P01-T02` needs scoped trigger-drop assertions, `try/finally` resource cleanup, and alignment with `MssqlStoreTests`-inherited `SqlStoreTests` methods

* Related IDs: Required Fix 4, `FR-2`, Test Ownership and Validation Lock, `P01`, `P01-T02`, `C2`, `C8`
* Evidence: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md (`FR-2`, `Test Ownership and Validation Lock`), .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md (`P01` Completion Evidence, `P01-T02` item 3), src/core/tests/test_sqlstore.py:39-240, and src/api/tests/test_mssqlstore.py:596-620
* Concern: `P01-T02` item 3 states that the replay runs fresh `SqlStoreTests` instances (`setUp` -> method -> `tearDown` / `doCleanups`) for the three `test_pre_reliance_*` methods and asserts the T-SQL trigger drop path ran and `pw.sqlite` was never created:
  1. `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` calls `BaseSqlStore(self.data, mssql_db)` directly and never calls `SqlStore(...)` or `_drop_audit_triggers(...)`, so a per-method assertion that T-SQL trigger drop ran would fail on that third method unless scoped to the two trigger-dropping methods (`dropped_triggers == 1` on each of the first two `test_pre_reliance_*` methods, `0` on the third).
  2. Manual `setUp` -> method -> `tearDown` / `doCleanups` execution without `try ... finally` and without registering `case.addCleanup(store.db.close)` inside the simulated factory leaks open SQLite connections and temporary directories on assertion failure (and when replaying `SqlStoreTests` methods that do not manually register `s.db.close`).
  3. Caller Requirement 4 asks that "`SqlStoreTests` methods are verified under the `MssqlStoreTests` factory hook", and `MssqlStoreTests` (`src/api/tests/test_mssqlstore.py:596-620`) inherits 10 of `SqlStoreTests`'s 12 `test_*` methods (overriding only `test_ledger_is_append_only_and_detects_tampering` and disabling `test_list_filters_use_indexes = None`; note `SqlStoreTests` has 12 `test_*` methods, not 13 as written in `Test Ownership and Validation Lock` and `P01` Completion Evidence). Replaying all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods against a single per-test backing SQLite file (reset per `setUp`, matching `MssqlStoreTests.setUp` `wipe()`) takes negligible time on the 5-case fixture and guards every inherited `SqlStoreTests` method against `pw.sqlite` or `SqlStore` factory regressions.
* Impact: Unscoped per-method trigger-drop assertions will fail on the third `test_pre_reliance_*` method, missing `try/finally` + `store.db.close` cleanups risk leaked SQLite file handles/`ResourceWarning`, and replaying only 3 of the 10 inherited methods leaves the remaining 7 `MssqlStoreTests`-inherited `SqlStoreTests` methods unverified offline and misstates the `SqlStoreTests` method count (`13` vs `12`).
* Smallest useful change: Update `FR-2`, `Test Ownership and Validation Lock`, and `P01`/`P01-T02` in the plan and phase details to: (a) record the accurate `12` `SqlStoreTests` methods (`+ SqlImproveTests`), (b) replay all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods (all `test_*` on `SqlStoreTests` except `test_ledger_is_append_only_and_detects_tampering` and `test_list_filters_use_indexes`) with a single per-test backing SQLite path, `case.addCleanup(store.db.close)` in the simulated factory, and `try ... finally` calling `doCleanups()` and `tearDown()`, and (c) assert `not os.path.exists(case.db)` on every replayed method and T-SQL trigger-drop execution specifically on `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` and `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head`.
* Action owner: planning_parent
* Exact resolving evidence: `.copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md` (`FR-2`, `Test Ownership and Validation Lock`) and `.copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md` (`P01`, `P01-T02`) specify the 12 `SqlStoreTests` methods, replay of the 10 `MssqlStoreTests`-inherited methods with `try/finally` cleanup and per-test shared backing DB, `not os.path.exists(case.db)` across all replayed methods, and T-SQL trigger-drop assertions scoped to the two trigger-dropping methods.
* Decision route: direct planner correction (planner can apply directly without a user decision)

## Strengths and Residual Risk

* Single-store reuse (`s`) in `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` eliminates both `sqlite3.connect(db2)` and a real SQL Server shared-database collision because `MssqlStoreTests.setUp` runs `wipe()` only once per test method (`src/api/tests/test_mssqlstore.py:604`).
* Replacing `WHERE seq=...` and 8-column `INSERT INTO audit` with `WHERE at=?` and 7-column `INSERT INTO audit` omitting `seq` aligns cleanly with `MssqlStore`'s `BIGINT IDENTITY(1,1)` (`src/core/src/zava_forward/core/mssqlstore.py:50`) and `SqlStore._reliance_audit_snapshot`'s strictly monotonic `seq > prev_seq` contract (`src/core/src/zava_forward/core/sqlstore.py:1525`).
* Scoping the offline factory patch with `patch.dict(globals(), {"SqlStore": ...})` and a `_running_factory_hook` re-entrancy guard ensures `MssqlStoreTests`'s live SQL Server factory (`base.SqlStore = factory`) is preserved without recursion when `MssqlStoreTests` inherits and executes `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` in CI.
* Accepted residual risk: Local `src/core` validation does not spin up the `mcr.microsoft.com/mssql/server:2022-latest` container because `push` is explicitly excluded by the caller; hosted `mssql` job verification in `Source projects CI` remains an explicit coordinator follow-up once the frozen commit is pushed to `PR #1814`.

## Questions or Blocking Evidence Gaps

* None. All required evidence is present in the supplied research artifact and four code files, and no user decision is required.

## Limitations

* This critique did not execute code changes, run `unittest`, or run against a live SQL Server instance; assessment of T-SQL compatibility is grounded in static inspection of `MssqlStore`, `SqlStore`, `SqlStoreTests`, and `MssqlStoreTests`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md` and `.copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md` to apply `PC-001` and `PC-002`, record their `Critique Disposition`, mark the plan `Ready for Implementation`, and proceed to `rpi-implement` without a second critique pass.
* User response required: No
