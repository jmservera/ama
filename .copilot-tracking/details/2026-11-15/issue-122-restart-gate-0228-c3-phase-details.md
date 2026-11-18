---
title: "Phase Details - Issue #122 SQL Server Ledger Trigger Guard and Base Merge (Cycle 3)"
description: "Evidence-based task specifications for Cycle 3 SQL Server WITH LEDGER = ON trigger guards, base merge, and DialectTests verification"
author: "Copilot"
ms.date: "2026-11-15"
---

## Task Context

* Task ID: `issue-122-restart-gate-0228-c3`
* Parent Task ID: `issue-122-restart-gate-0228-c2`
* Plan Path: `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md`
* Research Path: `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c3-research.md`

<!-- P01 -->
## Phase P01: Base-Branch Synchronization and SQL Server Ledger Trigger Guards

### Phase Direction

Bring `feat/platform-122-restart-gate-0228` up to date with `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) via a clean, non-rewriting merge that preserves `PR #1781`'s `is_available_case_document` filter in `assistants.py:capture()`, then guard DML trigger DDL in `MssqlStore._create_schema_serialized` and `Assistants.migrate` so SQL Server `WITH LEDGER = ON` databases never execute `CREATE OR ALTER TRIGGER` on system-versioned updatable ledger tables.

<!-- P01-T01 -->
### Task P01-T01: Configure Privacy-Safe Git Identity and Merge `origin/feat/demo-164-chat-grounding-provenance-0900`

* Evidence: `C8` in `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c3-research.md`.
* Resolve privacy-safe GitHub noreply email (`gh api user` -> `{id}+{login}@users.noreply.github.com`, falling back to existing repo noreply author only if `gh api` is blocked by host policy) and set `git config --local user.email`.
* Merge `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) into `feat/platform-122-restart-gate-0228` without `--rebase` (`git merge --no-ff` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer) so `d0d4135d3` remains an intact ancestor of `HEAD`.
* Verify `src/core/src/zava_forward/core/assistants.py` contains `from .doc_controls import is_available_case_document` and `if d.get("kind") in kinds and is_available_case_document(d)` in `capture()`.
* Completion expectation: Clean merge commit with zero conflicts and `is_available_case_document` preserved alongside `#122` changes.

<!-- P01-T02 -->
### Task P01-T02: Guard `GATE_TRIGGERS` in `MssqlStore._create_schema_serialized`

* Target file: `src/core/src/zava_forward/core/mssqlstore.py` (`[tool.ruff.format].exclude` in `src/core/pyproject.toml`).
* Evidence: `C1`, `C3`, `C4`, `C6`.
* In `_create_schema_serialized(self)`:
  * Keep `if ledger:` verifying `LEDGER_APPEND_ONLY_TABLES` against `APPEND_ONLY_LEDGER_TABLE`.
  * Move `for trigger in GATE_TRIGGERS: self.db.execute(trigger)` inside the `else:` branch right after `self.db.execute(APPEND_ONLY)`.
* Completion expectation: `MssqlStore._create_schema_serialized` executes zero `CREATE OR ALTER TRIGGER` statements when `ledger` is `True` and executes `APPEND_ONLY` plus both `GATE_TRIGGERS` when `ledger` is `False`; `SqlStore._migrate()` still calls `continuity.sync_sql_gate(self.db, read_meta=True, mssql=hasattr(self, "_env"))`.

<!-- P01-T03 -->
### Task P01-T03: Guard `MSSQL_ATTEMPT_TRIGGERS` in `Assistants.migrate`

* Target file: `src/core/src/zava_forward/core/assistants.py` (`[tool.ruff.format].exclude` in `src/core/pyproject.toml`).
* Evidence: `C2`, `C3`, `C4`, `C6`, `C9`.
* In `Assistants.migrate(self, db)`:
  * Initialize `ledger = False` before `if self.mssql:` so `ledger` is statically bound on both SQLite and MSSQL code paths.
  * After `self._upgrade(db)`, wrap the trigger loop in `if not (self.mssql and ledger):`:
    ```python
    if not (self.mssql and ledger):
        for trigger in (MSSQL_ATTEMPT_TRIGGERS if self.mssql else SQLITE_ATTEMPT_TRIGGERS):
            db.execute(trigger)
    continuity.sync_sql_gate(db, read_meta=True, mssql=self.mssql)
    ```
* Completion expectation: SQLite always installs `SQLITE_ATTEMPT_TRIGGERS`, non-ledger SQL Server installs `assistant_events_immutable` + `MSSQL_ATTEMPT_TRIGGERS`, ledger SQL Server (`self.mssql and ledger`) installs zero DML triggers, and all three modes run `continuity.sync_sql_gate(db, read_meta=True, mssql=self.mssql)`.

<!-- P01-T04 -->
### Task P01-T04: Update `src/core/README.md` Trigger Boundary Documentation

* Target file: `src/core/README.md`.
* Evidence: `C7`.
* Update the continuity SQL gate bullet to clarify that SQLite and non-ledger SQL Server databases enforce monotonic `continuity_gate_state` and `assistant_attempts` / `assistant_tasks` gate triggers in SQL, while SQL Server `WITH LEDGER = ON` databases omit DML triggers (which SQL Server forbids on system-versioned updatable ledger tables) and rely on `continuity_gate_state` `CHECK` constraints, `sync_sql_gate` synchronization of `continuity_gate_state` and `continuity_open_holds`, and Python fail-closed fences.
* Completion expectation: Documentation matches runtime behavior with no `.copilot-tracking/` references.

<!-- P02 -->
## Phase P02: Ledger Dialect Unit Test, Validation, and Local Commit Freeze

### Phase Direction

Prove locally via `DialectTests` in `src/api/tests/test_assistants.py` that `SELECT is_ledger_on -> 1` skips every `CREATE TRIGGER` statement in both `MssqlStore._create_schema_serialized` and `Assistants.migrate` while still synchronizing `continuity_gate_state` and `continuity_open_holds`, then run the full focused validation suite.

<!-- P02-T01 -->
### Task P02-T01: Extend `DialectConnection` and Add Ledger Mode Test in `DialectTests`

* Target file: `src/api/tests/test_assistants.py` (`[tool.ruff.format].exclude` in `src/api/pyproject.toml`).
* Evidence: `C5`, `C6`, `C10`, `PC-001`, `PC-002`.
* Imports: add `sqlite3` and `from zava_forward.core import continuity, mssqlstore` (preserving existing import style in `test_assistants.py`).
* Update `DialectConnection`:
  * Accept `ledger=False` in `__init__(self, raw, statements, ledger=False)` and store `self.ledger = ledger`.
  * Exact guard ordering in `execute(self, sql, args=())` (`PC-001`):
    1. `if "SELECT is_ledger_on" in sql: return self.raw.execute(f"SELECT {1 if self.ledger else 0}")`
    2. `if "SELECT ledger_type_desc" in sql: return self.raw.execute("SELECT 'APPEND_ONLY_LEDGER_TABLE'")` (must run BEFORE `if "FROM sys.tables" in sql:`, because `LEDGER_TYPE` and `Assistants.migrate` query `FROM sys.tables` with literal table names and zero `?` bindings).
    3. `if "FROM sys.tables" in sql:` (existing SQLite `sqlite_master` check).
    4. `if "SELECT name FROM sys.columns" in sql:` (existing `PRAGMA table_info` check).
    5. `if self.ledger and "CREATE TRIGGER" in sql: raise sqlite3.OperationalError("Cannot create a trigger on a system-versioned ledger table")` (must run BEFORE `if "N'TR'" in sql or "sys.indexes" in sql or "COL_LENGTH" in sql:`, because every T-SQL trigger uses `IF OBJECT_ID(..., N'TR') IS NULL EXEC(N'CREATE TRIGGER ...')`).
    6. `if "N'TR'" in sql or "sys.indexes" in sql or "COL_LENGTH" in sql:` (existing `SELECT 1` fallback for non-ledger trigger DDL, index DDL, and `COL_LENGTH`).
    7. In `if sql.startswith("IF OBJECT_ID"):` also strip `" WITH (LEDGER = ON (APPEND_ONLY = ON))"`, `" IDENTITY(1,1)"`, and Unicode string prefix `N'` (`re.sub(r"\bN'", "'", sql)`) so `MssqlStore.TABLES` DDL executes cleanly against SQLite.
* Update `DialectTests` (`PC-002`):
  * In `test_mssql_sql_shapes_enqueue_claim_complete_review_scan`: assert `any("CREATE TRIGGER" in s for s in statements)` so non-ledger mode (`is_ledger_on = 0`) explicitly verifies trigger installation.
  * Add `test_mssql_ledger_mode_skips_triggers_and_syncs_continuity_gate`:
    1. Suspend `"stock-prioritisation"` on `self.store` using `self.people["Quality Inspector"]` and complete continuity incident fields (`scope="stock-prioritisation"`, `reason`, `incident_owner`, `containment`, `comms_owner`, `comms_audience`, `trigger="guardrail breach"`, `evidence`, `resident_impact`, `remediation`, `restart_authority`, `synthetic=True`) to obtain an active suspension (epoch `1`).
    2. Create an in-memory SQLite connection `raw_ms = sqlite3.connect(":memory:", isolation_level=None)` (`self.addCleanup(raw_ms.close)`), wrap in `ms_conn = DialectConnection(raw_ms, ms_statements, ledger=True)`, instantiate `ms = object.__new__(mssqlstore.MssqlStore)` with `ms.db = ms_conn`, `ms.dblock = threading.RLock()`, and `ms._env = {}`, call `ms._create_schema_serialized()`, insert the wrapped continuity document (`continuity.dump_sql(self.store.data["continuity"])`) into `meta('continuity')`, and call `continuity.sync_sql_gate(ms_conn, read_meta=True, mssql=True)`. Assert `not any("CREATE TRIGGER" in s for s in ms_statements)`, `any("SELECT ledger_type_desc" in s for s in ms_statements)`, `raw_ms.execute("SELECT id, gate_version, epoch FROM continuity_gate_state").fetchone() == (1, continuity.GATE_VERSION, 1)`, and `raw_ms.execute("SELECT scope, incident_id, epoch FROM continuity_open_holds").fetchall() == [("stock-prioritisation", suspension["id"], 1)]`.
    3. On `inspect_conn = sqlite3.connect(self.dbpath, isolation_level=None)` (`self.addCleanup(inspect_conn.close)`), drop existing SQLite triggers (`SELECT name FROM sqlite_master WHERE type='trigger'`) so `self.dbpath` mirrors a trigger-free ledger database, reset `continuity_gate_state` (`epoch = 0`) and clear `continuity_open_holds` (`DELETE FROM continuity_open_holds`) while `meta('continuity')` holds the active suspension, set `self.store._env = {}`, wrap `original = self.store.assistant_connection` via `self.store.assistant_connection = lambda: DialectConnection(original(), assist_statements, ledger=True)` (cleaning up both `assistant_connection` and `_env`), and construct `svc = Assistants(self.store, config())`. Assert `svc.sql is True`, `not any("CREATE TRIGGER" in s for s in assist_statements)`, `any("SELECT ledger_type_desc" in s for s in assist_statements)`, `inspect_conn.execute("SELECT id, gate_version, epoch FROM continuity_gate_state").fetchone() == (1, continuity.GATE_VERSION, 1)`, `inspect_conn.execute("SELECT scope, incident_id, epoch FROM continuity_open_holds").fetchall() == [("stock-prioritisation", suspension["id"], 1)]`, and `with svc.transaction() as db: self.assertIsNotNone(svc.suspended(db, "stock-prioritisation"))`.
* Completion expectation: `DialectTests` deterministically verifies both `MssqlStore._create_schema_serialized` and `Assistants.migrate` under `is_ledger_on = 1` and `is_ledger_on = 0`.

<!-- P02-T02 -->
### Task P02-T02: Execute Focused Validation Suite and Prepare Review Evidence

* Run:
  1. `python3 -m unittest discover -s src/core/tests -p "test_restart_gate_sql_fences.py" -v`
  2. `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_continuity_restart_gate.py src/api/tests/test_assistants.py src/api/tests/test_document_controls.py -v`
  3. `(cd src/core && python3 -m mypy)` and `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` (plus bare `(cd src/core && mypy)` and `(cd src/api && mypy)` check matching caller syntax)
  4. `python3 -m ruff check src/core src/api`
* Record implementation evidence in `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c3-changes.md`, reconcile plan checkboxes, complete single-pass `rpi-review`, and commit all tracked changes cleanly with `Refs #122` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.
* Completion expectation: Zero test, type, or lint failures; clean frozen worktree (`git status --short` empty).
