<!-- markdownlint-disable-file -->
# Review: Issue #114 c1 CI Correction for Backend-Agnostic `SqlStoreTests` Pre-Reliance Proofs

## Scope and Evidence

* Task ID: issue-114-platform-sql-ledger-loadcheck-c1
* Review date: 2026-11-15
* Review scope: Full task (`P01`: `P01-T01`, `P01-T02`)
* Assessed boundary: Backend-agnostic refactoring of `SqlStoreTests` `test_pre_reliance_*` methods (`_drop_audit_triggers`, `s.db.execute`, single-store reuse omitting `seq`, `BaseSqlStore` resolution, and offline `MssqlStoreTests` factory-hook replay) in `src/core/tests/test_sqlstore.py`, focused `src/core` validation, and reconciliation of dated `2026-11-15` RPI artifacts.
* Plan: .copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/platform-114-sql-ledger-loadcheck-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/platform-114-sql-ledger-loadcheck-c1-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/platform-114-sql-ledger-loadcheck-c1-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-c1-research.md (`C1`–`C10`), `src/core/tests/test_sqlstore.py`, `src/api/tests/test_mssqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/sqlstore.py`, focused validation test/lint/type outputs, and independent read-only `rubber-duck` review lens.

## Opening Review State

* Interpreted review goal: Verify that the `c1` implementation satisfies all four caller requirements (`FR-1`, `FR-2`), resolves plan critique findings `PC-001` and `PC-002`, passes all locked validation checks, and preserves full compatibility with `MssqlStoreTests(base.SqlStoreTests)` on SQL Server 2022 (`master`).
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`)
* Evidence readiness: Ready (all research, plan, details, critique, changes, diff, and validation artifacts present and reconciled)
* Acceptance basis: Caller 4-part specification, `FR-1`, `FR-2`, NFR portability/lint/typing, `PC-001` and `PC-002` critique dispositions, and locked validation commands
* First comparison boundary: `src/core/tests/test_sqlstore.py` diff versus `MssqlStoreTests` (`src/api/tests/test_mssqlstore.py`) and `MssqlStore` (`src/core/src/zava_forward/core/mssqlstore.py`)
* Active read-only boundaries: Write access limited strictly to `.copilot-tracking/reviews/logs/2026-11-15/platform-114-sql-ledger-loadcheck-c1-review.md`
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass assessment on 2026-11-15 comparing the full `c1` artifact set, `git diff src/core/tests/test_sqlstore.py`, focused validation runs (`test_sqlstore.py`, `test_loadcheck.py`, `test_mssqlstore.py` offline discovery, `ruff check`, `mypy`), and an independent read-only review lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | Backend-Agnostic Pre-Reliance Trigger Drop, Tamper, Dropped-Year, and `audit_head` Mutations | Reconciled | Checked `[x]` in plan, marked `Complete` in phase details, and evidenced in `src/core/tests/test_sqlstore.py`. |
| `P01` / `P01-T02` | `BaseSqlStore` Class Resolution and Offline `MssqlStoreTests` Factory-Hook Replay | Reconciled | Checked `[x]` in plan, marked `Complete` in phase details, and evidenced by 21/21 passing `test_sqlstore.py` tests (including 10-method factory-hook replay). |
| `## Follow-Up Items` | Coordinator push to `PR #1814` for hosted `mssql` CI + 3 carried-forward parent follow-ups | Reconciled | Preserved identically across plan, changes record, and session state outside active `P01` scope. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/tests/test_sqlstore.py` | Added `_drop_audit_triggers(self, store)`, replaced `sqlite3.connect(self.db)` and `WHERE seq=...` with `s.db.execute(...)` (`WHERE at=?`), and reused `s` directly for the dropped-2024 check with 7-column `INSERT INTO audit` omitting `seq`. | Zero `sqlite3.connect` calls remain in `test_pre_reliance_*`; SQL statements are valid on both SQLite and SQL Server (`autocommit=True`, `IDENTITY(1,1)`). | Passed (`test_sqlstore.py` 21/21) | Reconciled |
| `P01-T02` | `src/core/tests/test_sqlstore.py` | Resolved `BaseSqlStore` directly from `zava_forward.core.sqlstore` inside `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` and added `_verify_mssqlstore_factory_hook` replaying all 10 `MssqlStoreTests`-inherited `SqlStoreTests` methods under `_SimulatedMssqlStore` + `_MssqlSqlGuard`. | `patch.dict(globals(), {"SqlStore": factory})` cleanly restores any outer `MssqlStoreTests` factory, avoids recursion via `_running_factory_hook`, verifies `not os.path.exists(case.db)` on all 10 methods, and verifies `dropped_triggers == 1` on both trigger-dropping methods. | Passed (`test_sqlstore.py`, `test_loadcheck.py`, `test_mssqlstore.py` offline, `ruff`, `mypy`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None | No implementation-time plan or detail amendments were needed after `PC-001` and `PC-002` were applied prior to `Implement`. | None | All markers, status fields, and handoff prose synchronized. | Ready (`PC-001` and `PC-002` resolved directly) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Both `PC-001` (`_SimulatedMssqlStore` `BaseSqlStore.__init__` delegation without `self._env`, post-init `_MssqlSqlGuard` attachment with `__getattr__`, and rejection of both columnless and explicit-`seq` `INSERT INTO audit`) and `PC-002` (exact 12 `SqlStoreTests` method count, 10-method `MssqlStoreTests` replay, `try/finally` cleanup, and scoped `dropped_triggers` assertions) were completely implemented as specified.
* Material revisions: None during implementation.
* Dependent-work pause assessment: No pause required; single-phase plan executed cleanly in order.
* Justification assessment: Fully supported by codebase evidence (`C1`–`C10`) and passing validation.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Push frozen commit on `feat/platform-114-sql-ledger-loadcheck` to `PR #1814` and observe hosted `mssql` job in `Source projects CI` | Caller explicitly forbade pushing or opening/updating a PR in this worktree run | Coordinator / owner push | Distinct follow-up route |
| Optional parent `RV-001`/`RV-002` offline defense-in-depth hardening in `store.py`, `sqlstore.py`, and `ledger.py` | Outside `c1` test-portability boundary (`src/core/tests/test_sqlstore.py` only) | Future `src/core` hardening slice | Distinct follow-up route |
| Live Azure SQL serverless (`GP_S_Gen5`) metered `loadcheck` run (`Refs #114`) | Requires human-approved live Azure SQL provisioning | Cloud validation slice (`Refs #114`) | Distinct follow-up route |
| Witnessed Azure SQL point-in-time restore drill (`DH-005`, `Refs #114`) | Requires live Azure SQL + immutable WORM Blob storage | Operational recovery drill (`Refs #114`) | Distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: `_MssqlSqlGuard` inspects `execute` statements only and delegates `executemany` directly

* Related scope: `P01-T02`
* Evidence: `src/core/tests/test_sqlstore.py` (`SqlStoreTests._verify_mssqlstore_factory_hook`, `_MssqlSqlGuard`)
* Impact: Current `SqlStoreTests` and `SqlStore._append_audit` (`INSERT INTO audit (at, who, action, case_id, detail, prev, hash)`) omit `seq`, and all test tamper/rebuild mutations call `s.db.execute(...)`. However, if a future test called `s.db.executemany(...)` with an explicit-`seq` or columnless `INSERT INTO audit`, `__getattr__` delegation to `self._raw.executemany` would bypass `_MssqlSqlGuard`'s SQL check offline.
* Destination: follow-up
* Smallest useful next action: Optionally add `executemany(self, sql, seq_of_params)` on `_MssqlSqlGuard` sharing the SQL check helper if `SqlStoreTests` is touched again.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: `_verify_mssqlstore_factory_hook` ignores the boolean return value of `case.doCleanups()`

* Related scope: `P01-T02`
* Evidence: `src/core/tests/test_sqlstore.py` (`SqlStoreTests._verify_mssqlstore_factory_hook` `finally` block)
* Impact: `unittest.TestCase.doCleanups()` catches exceptions inside cleanup callbacks and returns `False` rather than raising when no `Outcome` is active. `sqlite3.Connection.close()` is idempotent in Python `sqlite3`, so current cleanups succeed reliably, but asserting `self.assertTrue(case.doCleanups(), method_name)` when no primary test exception is in flight would surface any future failing cleanup callback explicitly.
* Destination: follow-up
* Smallest useful next action: Optionally assert `case.doCleanups()` truthiness when no exception is active if `_verify_mssqlstore_factory_hook` is touched again.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` [Low] | `follow-up` | Optional future test-guard polish in `src/core/tests/test_sqlstore.py` | Non-blocking defense-in-depth enhancement on test double (`executemany` parity) |
| `RV-002` [Low] | `follow-up` | Optional future test-guard polish in `src/core/tests/test_sqlstore.py` | Non-blocking defense-in-depth assertion on `case.doCleanups()` return value |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Coordinator push of the frozen commit on `feat/platform-114-sql-ledger-loadcheck` to `PR #1814` to observe the live SQL Server 2022 `mssql` job in `Source projects CI`.
* Optional Low test-guard polish (`RV-001`, `RV-002`) and carried-forward parent `Issue #114` follow-ups (`store.py`/`sqlstore.py`/`ledger.py` hardening, live Azure SQL `loadcheck` metering, witnessed `DH-005` restore drill).

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01`, `P01-T01`, and `P01-T02` are complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_sqlstore.py' -v` | `src/core/tests/test_sqlstore.py` | Passed | `Ran 21 tests in 20.140s OK` |
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_loadcheck.py' -v` | `src/core/tests/test_loadcheck.py` | Passed | `Ran 20 tests in 0.174s OK` |
| `(cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p 'test_mssqlstore.py' -v)` | `src/api/tests/test_mssqlstore.py` | Passed | `Ran 248 tests in 0.629s OK (skipped=239)` |
| `python3 -m ruff check src/core/tests/test_sqlstore.py` and `(cd src/core && python3 -m ruff check)` | `src/core` | Passed | `All checks passed!` |
| `(cd src/core && python3 -m mypy)` | `src/core` | Passed | `Success: no issues found in 373 source files` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every caller requirement (`FR-1`, `FR-2`), acceptance criterion, and critique disposition (`PC-001`, `PC-002`) is satisfied with clean, verified `src/core` test, lint, and type-check evidence; zero defects or decision gaps remain (`RV-001` and `RV-002` are Low non-blocking test-double enhancements routed to `follow-up`).

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up | Coordinator push to `PR #1814` for hosted `mssql` CI; optional `RV-001`/`RV-002` test-guard polish and carried-forward Issue `#114` live Azure SQL follow-ups |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `test_sqlstore.py` (21 passed), `test_loadcheck.py` (20 passed), `test_mssqlstore.py` offline discovery (passed), `ruff check` (passed), `mypy` (passed)
* Blockers: None
