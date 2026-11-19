<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #122 SQL Server Ledger Trigger Guard and Base Merge (Cycle 3)

## Metadata

* Task ID: issue-122-restart-gate-0228-c3
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Remediate PR #1787 CI failure (job 132785382777) across `test_mssqlstore.MssqlLedgerMigration` (5 tests) and `test_assistants.MssqlLedgerTests` (2 tests) where SQL Server `WITH LEDGER = ON` databases forbid DML triggers on system-versioned `UPDATABLE_LEDGER_TABLE` tables; move `GATE_TRIGGERS` inside `else:` of `if ledger:` in `MssqlStore._create_schema_serialized`; initialize `ledger = False` and guard trigger execution with `if not (self.mssql and ledger):` in `Assistants.migrate` while running `continuity.sync_sql_gate` unconditionally; merge `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) cleanly without rewriting `d0d4135d3`, preserving `is_available_case_document` in `assistants.py:capture()`; add a `DialectTests` ledger unit test; run focused `unittest`, `mypy`, and `ruff check`; commit locally with `Refs #122` and Copilot trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c3-research.md, .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md, .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md, src/core/src/zava_forward/core/mssqlstore.py, src/core/src/zava_forward/core/assistants.py, src/core/src/zava_forward/core/continuity.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/chatthreads.py, src/api/tests/test_assistants.py, src/api/tests/test_mssqlstore.py, src/api/tests/test_continuity_restart_gate.py, src/core/README.md, and git object inspection of `HEAD` (`d0d4135d3`) vs `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`).
* Decisions, dependencies, and acceptance criteria considered: `FR-01` through `FR-04`, `NFR-01` through `NFR-02`, `AC-01` through `AC-04`, non-rewriting git merge contract, `[tool.ruff.format].exclude` preservation, and local freeze without `git push`.
* Assessment boundary: Evaluates correctness of the core SQL Server ledger trigger fix, merge compatibility with `origin/feat/demo-164-chat-grounding-provenance-0900`, and exact executability of the planned `DialectTests` unit test and validation commands against current source and test APIs. Does not execute live SQL Server 2022 container suites (`ZF_TEST_MSSQL=1` / `ZF_SQL_SERVER`), which run in hosted `Source projects CI`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-01 / AC-01 / P01-T01 / C8 | Covered | `git merge-tree --write-tree HEAD origin/feat/demo-164-chat-grounding-provenance-0900` succeeds cleanly (`2da3ef2acac94893dc32b4566409c2c0175852a4`) with zero conflicts, preserving `d0d4135d3` and `is_available_case_document(d)` in `src/core/src/zava_forward/core/assistants.py:capture()`. |
| FR-02 / AC-02 / P01-T02 / C1, C3, C4 | Covered | Moving `for trigger in GATE_TRIGGERS: self.db.execute(trigger)` inside `else:` of `if ledger:` in `src/core/src/zava_forward/core/mssqlstore.py:307-321` skips DML trigger creation on `WITH LEDGER = ON` databases while `SqlStore._migrate()` and `SqlStore._seed()` continue calling `continuity.sync_sql_gate`. |
| FR-03 / AC-02 / P01-T03 / C2, C4, C9 | Covered | Initializing `ledger = False` before `if self.mssql:` and wrapping trigger DDL in `if not (self.mssql and ledger):` in `src/core/src/zava_forward/core/assistants.py:1203-1244` keeps SQLite and non-ledger MSSQL triggers active, skips MSSQL ledger triggers, and runs `continuity.sync_sql_gate` unconditionally. |
| FR-04 (docs) / P01-T04 / C7 | Covered | Updating `src/core/README.md:4605-4613` accurately documents the SQL Server `WITH LEDGER = ON` trigger boundary alongside `sync_sql_gate` and Python fail-closed fences. |
| FR-04 (tests) / NFR-01 / AC-03 / P02-T01 / C5, C10 | Partial | `P02-T01` has two high-severity defects in `DialectConnection` branch ordering (`PC-001`) and `DialectTests` API/lifecycle assumptions (`PC-002`) that will fail or mask trigger checks at runtime. |
| NFR-01 / NFR-02 / AC-04 / P02-T02 / C6 | Partial | `NFR-01` and `P02-T02` invoke non-existent `src/api/tests/test_doc_controls.py` instead of `src/api/tests/test_document_controls.py` (`PC-003`). |

## Verdict

* Verdict: Revise
* Rationale: Phase P01 (`P01-T01` through `P01-T04`) is technically sound and verified against both `mssqlstore.py`/`assistants.py` and `git merge-tree` with `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`), but Phase P02 (`P02-T01`, `P02-T02`) and `NFR-01` contain concrete `DialectConnection` dispatch-order bugs, non-existent `test_assistants.py` / `SqlStore` / `MssqlStore` / `Assistants` symbols, connection-close/dialect hazards, and a wrong regression test filename that will cause immediate test failures unless revised by the planner before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: P02-T01 DialectConnection Branch Order Swallows ledger_type_desc Queries and Trigger Guards

* Related IDs: FR-04, AC-03, P02-T01, C5, C10
* Evidence: src/api/tests/test_assistants.py:1299-1314, src/core/src/zava_forward/core/mssqlstore.py:72-80,315, src/core/src/zava_forward/core/assistants.py:1039-1075,1224-1232, .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md
* Concern: In `DialectConnection.execute(self, sql, args=())` (`src/api/tests/test_assistants.py:1299-1308`), `if "FROM sys.tables" in sql:` currently rewrites any `sys.tables` query to `SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?` passing `args`, and `if "N'TR'" in sql or "sys.indexes" in sql or "COL_LENGTH" in sql:` returns `SELECT 1`. First, both `MssqlStore._create_schema_serialized` (`SELECT ledger_type_desc FROM sys.tables WHERE name = N'audit'`) and `Assistants.migrate` (`SELECT ledger_type_desc FROM sys.tables WHERE name=N'assistant_events'`) contain `"FROM sys.tables"` with `args=()` (literal table name, zero `?` placeholders), so evaluating `"SELECT ledger_type_desc" in sql` after `"FROM sys.tables" in sql` raises `sqlite3.ProgrammingError: Incorrect number of bindings supplied`. Second, every T-SQL trigger statement in `mssqlstore.py` (`APPEND_ONLY`, `GATE_TRIGGERS`) and `assistants.py` (`assistant_events_immutable`, `MSSQL_ATTEMPT_TRIGGERS`) uses `IF OBJECT_ID(N'...', N'TR') IS NULL EXEC(N'CREATE TRIGGER ...')` (none uses `CREATE OR ALTER TRIGGER`), so every T-SQL trigger contains `"N'TR'"`. Evaluating `if self.ledger and "CREATE TRIGGER" in sql:` after `if "N'TR'" in sql ...:` silently returns `SELECT 1` instead of raising `sqlite3.OperationalError("Cannot create a trigger on a system-versioned ledger table")`.
* Impact: Misordered `DialectConnection.execute` guards break `SELECT ledger_type_desc` execution with `ProgrammingError` and neutralize the negative-control `CREATE TRIGGER` failure simulation on ledger tables.
* Smallest useful change: Update `P02-T01` so `DialectConnection.execute` explicitly evaluates `if "SELECT ledger_type_desc" in sql:` before `if "FROM sys.tables" in sql:`, and evaluates `if self.ledger and "CREATE TRIGGER" in sql: raise sqlite3.OperationalError("Cannot create a trigger on a system-versioned ledger table")` before `if "N'TR'" in sql or "sys.indexes" in sql or "COL_LENGTH" in sql:`, removing the inapplicable `CREATE OR ALTER TRIGGER` normalization note.
* Action owner: planning_parent
* Exact resolving evidence: Revised `P02-T01` in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md specifying exact `DialectConnection.execute` branch ordering ahead of `"FROM sys.tables"` and `"N'TR'"`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: P02-T01 and NFR-01 Prescribe Non-Existent DialectTests Symbols, Store Hooks, and Connection Lifecycle

* Related IDs: FR-04, NFR-01, AC-03, P02-T01, C5, C10
* Evidence: src/api/tests/test_assistants.py:1-29,83-102,1325-1344, src/core/src/zava_forward/core/mssqlstore.py:307-308, src/core/src/zava_forward/core/sqlstore.py:194,258, src/core/src/zava_forward/core/assistants.py:1174,1333-1351,1423-1429, src/api/tests/test_continuity_restart_gate.py:42-59, .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md, .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md
* Concern: `NFR-01` and `P02-T01` reference multiple symbols and connection patterns that do not exist or fail in `src/api/tests/test_assistants.py`:
  1. Existing method name: `DialectTests` defines `test_mssql_sql_shapes_enqueue_claim_complete_review_scan` (`src/api/tests/test_assistants.py:1325`), not `test_mssql_dialect_translation_runs_in_transaction_and_claims`.
  2. Suspension helper and payload: `staff_member(...)` is not defined in `test_assistants.py`; `Base.setUp` provides `self.people["Quality Inspector"]`, and `self.store.suspend(user, body)` requires the structured continuity incident payload fields (`scope`, `reason`, `incident_owner`, `containment`, `comms_owner`, `comms_audience`, `evidence`, `resident_impact`, `remediation`, `restart_authority`, `synthetic`, `trigger`).
  3. Bare `MssqlStore` lock attribute: `ms = object.__new__(mssqlstore.MssqlStore)` omits `ms.dblock = threading.RLock()`, so `ms._create_schema_serialized()` (`with self.dblock:` at `mssqlstore.py:308`) raises `AttributeError`.
  4. `SqlStore` connection factory, path attribute, and `db.close()` lifecycle: `Base` defines `self.dbpath` (`test_assistants.py:83`), not `self.db`; `SqlStore` exposes `assistant_connection` (`sqlstore.py:258`, used at `test_assistants.py:1329`), not `connect`; and `Assistants.transaction()` closes the connection returned by `assistant_connection()` in its `finally:` block (`assistants.py:1351`), so returning a single shared `DialectConnection(raw, ...)` closes `raw` during `Assistants.__init__` before post-migration queries run. Wrapping `original = self.store.assistant_connection` with `lambda: DialectConnection(original(), assist_statements, ledger=True)` (matching line 1329) gives each transaction its own connection while keeping a separate SQLite connection open for inspection.
  5. `svc.sql` boolean and `svc.suspended` dialect mismatch: `svc.sql` is already a `bool` (`assistants.py:1174`), so `svc.sql.sql` raises `AttributeError`; and calling `svc.suspended(raw, "stock-prioritisation")` with a raw `sqlite3.Connection` while `svc.mssql` is `True` executes `SELECT name FROM sys.tables WHERE name = ?` directly on SQLite (`continuity.py:132`), raising `sqlite3.OperationalError: no such table: sys.tables`. Calling `svc.dispatch_hold("stock-prioritisation")` or `with svc.transaction() as db: svc.suspended(db, "stock-prioritisation")` routes through `DialectConnection`. `sqlite3` and `zava_forward.core.{continuity,mssqlstore}` also need explicit imports in `test_assistants.py`.
* Impact: Implementing `P02-T01` as specified causes immediate `NameError`, `AttributeError`, `ProgrammingError`, and `OperationalError` failures in `DialectTests`, blocking `AC-03` and `AC-04`.
* Smallest useful change: Revise `NFR-01` in the plan and `P02-T01` in phase details to name `test_mssql_sql_shapes_enqueue_claim_complete_review_scan`, use `self.people["Quality Inspector"]` with a complete `self.store.suspend(...)` incident dict, set `ms.dblock = threading.RLock()`, use `self.dbpath` for trigger/state setup and `self.store.assistant_connection = lambda: DialectConnection(original(), assist_statements, ledger=True)` per transaction, assert `svc.sql is True`, check suspension via `with svc.transaction() as db: self.assertIsNotNone(svc.suspended(db, "stock-prioritisation"))`, and list `sqlite3`, `continuity`, and `mssqlstore` imports.
* Action owner: planning_parent
* Exact resolving evidence: Updated `NFR-01` in .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md and `P02-T01` in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md matching verified `test_assistants.py`, `MssqlStore`, `SqlStore`, and `Assistants` interfaces.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: NFR-01 and P02-T02 Reference Non-Existent Test Module src/api/tests/test_doc_controls.py

* Related IDs: FR-01, NFR-01, AC-04, P02-T02
* Evidence: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md, .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md, src/api/tests/test_document_controls.py (on `origin/feat/demo-164-chat-grounding-provenance-0900` at `c7e5c8848`)
* Concern: `NFR-01` (plan) and step 2 of `P02-T02` (phase details) specify running `src/api/tests/test_doc_controls.py`, which does not exist in `HEAD` or `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`). The actual document-controls API test module updated by `#1781` (`#117`) is `src/api/tests/test_document_controls.py`.
* Impact: Executing the planned `P02-T02` `unittest` command verbatim fails immediately during module import/loading.
* Smallest useful change: Replace `src/api/tests/test_doc_controls.py` with `src/api/tests/test_document_controls.py` in `NFR-01` and `P02-T02`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `NFR-01` in .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md and `P02-T02` command in .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md referencing `src/api/tests/test_document_controls.py`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Core SQL Server ledger remediation in `P01-T02` (`mssqlstore.py:_create_schema_serialized`) and `P01-T03` (`assistants.py:migrate`) is minimal, exact, and aligned with existing `APPEND_ONLY` / `assistant_events_immutable` ledger branching while keeping SQLite and non-ledger SQL Server DML triggers intact and `continuity.sync_sql_gate` unconditional across all modes.
* Non-rewriting merge strategy (`P01-T01`) cleanly integrates `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) without rewriting published `PR #1787` commit `d0d4135d3`, verified conflict-free via `git merge-tree` with `is_available_case_document` retained in `assistants.py:capture()`.
* Residual risk (explicitly accepted in plan): Live SQL Server 2022 container suites (`MssqlLedgerMigration` and `MssqlLedgerTests`) skip locally when `ZF_TEST_MSSQL=1` / `ZF_SQL_SERVER` is absent and must be observed in hosted `Source projects CI` after the owner/orchestrator pushes the branch.

## Questions or Blocking Evidence Gaps

* None. All three findings are direct planner corrections fully resolved by existing repository and caller evidence.

## Limitations

* No live SQL Server 2022 instance was invoked during read-only plan critique; SQL Server 2022 `UPDATABLE_LEDGER_TABLE` behavior was assessed from the supplied CI failure contract (job `132785382777`) and existing ledger migration tests in `src/api/tests/test_mssqlstore.py` and `src/api/tests/test_assistants.py`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions to `NFR-01`, `P02-T01`, and `P02-T02` fixing `DialectConnection` guard ordering (`PC-001`), `DialectTests` symbol/connection/dialect usage (`PC-002`), and `src/api/tests/test_document_controls.py` path (`PC-003`), then finalize the plan for `rpi-implement` without another critique pass.
* User response required: no
