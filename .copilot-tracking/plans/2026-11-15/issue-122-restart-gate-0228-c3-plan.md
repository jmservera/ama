---
title: "Implementation Plan - Issue #122 SQL Server Ledger Trigger Guard and Base Merge (Cycle 3)"
description: "Surgical CI remediation for SQL Server WITH LEDGER = ON trigger prohibition in mssqlstore.py and assistants.py plus base-branch merge preserving PR #1781 is_available_case_document"
author: "Copilot"
ms.date: "2026-11-15"
---

## Metadata

* Task ID: `issue-122-restart-gate-0228-c3`
* Task Slug: `issue-122-restart-gate-0228-c3`
* Parent Task: `issue-122-restart-gate-0228-c2`
* Branch: `feat/platform-122-restart-gate-0228` (targeting `feat/demo-164-chat-grounding-provenance-0900`, `PR #1787` -> `PR #1641`)
* Date: `2026-11-15`
* Planning Status: `Ready after Critique`
* Validation Tier: `Focused` (targeted bug fix in `mssqlstore.py` and `assistants.py` ledger DDL guard with local `DialectTests` verification, `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_assistants.py`, `test_document_controls.py`, `mypy`, and `ruff check`; hosted `Source projects CI` runs live SQL Server 2022 `MssqlLedgerMigration` and `MssqlLedgerTests` after owner/orchestrator push)
* Research Artifact: `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c3-research.md` (`executed`)
* Phase Details Artifact: `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md`
* Critique Artifact: `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan-critique.md`
* Downstream Changes Artifact: `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c3-changes.md`

## Executive Summary

Cycle 3 (`issue-122-restart-gate-0228-c3`) remediates the `PR #1787` CI failure in job `132785382777` (`test_mssqlstore.MssqlLedgerMigration` `5` tests and `test_assistants.MssqlLedgerTests` `2` tests) and synchronizes `feat/platform-122-restart-gate-0228` with its updated target branch `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`):

1. **Base-Branch Merge Preserving `PR #1781` (`#117`) `is_available_case_document`**: Merge `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) cleanly without rewriting published `PR #1787` commit history (`d0d4135d3`), preserving `from .doc_controls import is_available_case_document` and `if d.get("kind") in kinds and is_available_case_document(d)` in `src/core/src/zava_forward/core/assistants.py:capture()` alongside `#122`'s restart-gate changes.
2. **SQL Server `WITH LEDGER = ON` Trigger Guard (`mssqlstore.py` and `assistants.py`)**: Move `for trigger in GATE_TRIGGERS: self.db.execute(trigger)` inside the `else:` branch of `if ledger:` in `MssqlStore._create_schema_serialized`, and initialize `ledger = False` plus guard trigger installation with `if not (self.mssql and ledger):` in `Assistants.migrate`, so DML triggers are never created on system-versioned `UPDATABLE_LEDGER_TABLE` tables in SQL Server `WITH LEDGER = ON` databases while `continuity.sync_sql_gate` and all Python fail-closed fences remain active everywhere (and SQLite plus non-ledger SQL Server retain full DML trigger enforcement).
3. **Deterministic Ledger Dialect Unit Test (`src/api/tests/test_assistants.py`) and Documentation Sync (`src/core/README.md`)**: Extend `DialectConnection` (`ledger=False`) to simulate `SELECT is_ledger_on -> 1`, `SELECT ledger_type_desc -> 'APPEND_ONLY_LEDGER_TABLE'`, and SQL Server's `CREATE TRIGGER` error on ledger tables, and add `DialectTests.test_mssql_ledger_mode_skips_triggers_and_syncs_continuity_gate` proving neither `MssqlStore._create_schema_serialized` nor `Assistants.migrate` executes `CREATE TRIGGER` under `is_ledger_on = 1` while both synchronize `continuity_gate_state` and `continuity_open_holds`.

## Sources and Evidence

* `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c3-research.md` (`C1`–`C10`)
* `src/core/src/zava_forward/core/mssqlstore.py` (`GATE_TRIGGERS`, `_create_schema_serialized`)
* `src/core/src/zava_forward/core/assistants.py` (`capture`, `migrate`, `MSSQL_ATTEMPT_TRIGGERS`, `SQLITE_ATTEMPT_TRIGGERS`)
* `src/core/src/zava_forward/core/continuity.py` (`sync_sql_gate`)
* `src/core/src/zava_forward/core/doc_controls.py` (`is_available_case_document` via `origin/feat/demo-164-chat-grounding-provenance-0900` at `c7e5c8848`)
* `src/api/tests/test_assistants.py` (`DialectConnection`, `DialectTests`, `MssqlLedgerTests`)
* `src/api/tests/test_mssqlstore.py` (`MssqlLedgerMigration`)
* `src/core/README.md` (restart-gate SQL trigger documentation)
* `src/core/pyproject.toml` and `src/api/pyproject.toml` (`[tool.ruff.format].exclude`)

## User Decisions and Requirements

* Fix the `PR #1787` CI failure (job `132785382777`) on `test_mssqlstore.MssqlLedgerMigration` (`5` tests) and `test_assistants.MssqlLedgerTests` (`2` tests) caused by `Cannot create a trigger on a system-versioned ledger table` in SQL Server `WITH LEDGER = ON` databases.
* Move `for trigger in GATE_TRIGGERS: self.db.execute(trigger)` inside the `else:` branch of `if ledger:` in `src/core/src/zava_forward/core/mssqlstore.py:_create_schema_serialized`.
* Guard trigger installation in `src/core/src/zava_forward/core/assistants.py:migrate` with `if not (self.mssql and ledger):` (with `ledger` safely initialized before `if self.mssql:`) so `MSSQL_ATTEMPT_TRIGGERS` runs only when `ledger` is `False` on SQL Server and `SQLITE_ATTEMPT_TRIGGERS` always runs on SQLite.
* Fetch `origin` and merge/synchronize cleanly with `origin/feat/demo-164-chat-grounding-provenance-0900`, preserving `from .doc_controls import is_available_case_document` and `if d.get("kind") in kinds and is_available_case_document(d)` in `capture()` (`src/core/src/zava_forward/core/assistants.py`).
* Add a unit test in `src/api/tests/test_assistants.py` (`DialectTests`) verifying that when `SELECT is_ledger_on` returns `1`, neither `MssqlStore._create_schema_serialized` nor `Assistants.migrate` executes `CREATE TRIGGER` statements while still synchronizing `continuity_gate_state` and `continuity_open_holds`.
* Update `.copilot-tracking/` artifacts for `#122` (`c3`), run all requested unit/type/lint validations, commit locally with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and `Refs #122`, leave `git status --short` empty, and do NOT push directly.

## Goals

* Restore green schema creation and migration on SQL Server `WITH LEDGER = ON` databases across `MssqlStore` and `Assistants` without weakening SQLite or non-ledger SQL Server DML trigger fences or Python continuity gating.
* Synchronize `feat/platform-122-restart-gate-0228` cleanly with `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) without rewriting published commit `d0d4135d3`, preserving `PR #1781` (`#117`) document-scan availability checks in `assistants.py:capture()`.
* Prevent regression locally via deterministic SQLite `DialectTests` ledger simulation even when no SQL Server container is running.

## Scope and Non-Goals

### In Scope

* Git merge of `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) into `feat/platform-122-restart-gate-0228`
* `src/core/src/zava_forward/core/mssqlstore.py`
* `src/core/src/zava_forward/core/assistants.py`
* `src/core/README.md`
* `src/api/tests/test_assistants.py`
* `.copilot-tracking/` Cycle 3 RPI artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`)

### Non-Goals

* Pushing commits to `origin` (`git push` explicitly excluded by caller).
* Altering SQLite triggers (`SQLITE_ATTEMPT_TRIGGERS`, `SqlStore._create_schema`) or non-ledger SQL Server triggers (`GATE_TRIGGERS`, `MSSQL_ATTEMPT_TRIGGERS`, `APPEND_ONLY`, `assistant_events_immutable`).
* Modifying `[tool.ruff.format].exclude` lists or reformatting excluded legacy files.

## Functional Requirements

* `FR-01` (Base-Branch Merge & `#1781` Preservation): Merging `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) into `feat/platform-122-restart-gate-0228` must preserve published commit `d0d4135d3` in ancestry and retain `from .doc_controls import is_available_case_document` plus `if d.get("kind") in kinds and is_available_case_document(d)` in `src/core/src/zava_forward/core/assistants.py:capture()`.
* `FR-02` (`MssqlStore._create_schema_serialized` Ledger Guard): When `SELECT is_ledger_on FROM sys.databases WHERE name = DB_NAME()` returns truthy (`ledger is True`), `MssqlStore._create_schema_serialized` must verify `LEDGER_APPEND_ONLY_TABLES` and skip both `APPEND_ONLY` and `GATE_TRIGGERS`; when `ledger is False`, it must execute both `APPEND_ONLY` and `GATE_TRIGGERS`. `SqlStore._migrate()` and `SqlStore._seed()` continue calling `continuity.sync_sql_gate(self.db, read_meta=True, mssql=hasattr(self, "_env"))` in both modes.
* `FR-03` (`Assistants.migrate` Ledger Guard): `Assistants.migrate` must initialize `ledger = False` before `if self.mssql:`, compute `ledger = bool(row and row[0])` when `self.mssql` is `True`, execute `MSSQL_ATTEMPT_TRIGGERS` when `self.mssql and not ledger`, execute `SQLITE_ATTEMPT_TRIGGERS` when `not self.mssql`, skip trigger execution when `self.mssql and ledger`, and unconditionally execute `continuity.sync_sql_gate(db, read_meta=True, mssql=self.mssql)`.
* `FR-04` (`DialectTests` Ledger Simulation & `src/core/README.md` Sync): `DialectConnection` in `src/api/tests/test_assistants.py` must support `ledger: bool = False` (returning `1` for `SELECT is_ledger_on`, `'APPEND_ONLY_LEDGER_TABLE'` for `SELECT ledger_type_desc`, normalizing `WITH (LEDGER = ON (APPEND_ONLY = ON))`, `IDENTITY(1,1)`, and `N'...'` literals in `IF OBJECT_ID` table DDL, and raising `sqlite3.OperationalError` if `CREATE TRIGGER` is executed while `ledger=True`), and `DialectTests` must verify that under `is_ledger_on = 1` neither `MssqlStore._create_schema_serialized` nor `Assistants.migrate` executes `CREATE TRIGGER` while both synchronize `continuity_gate_state` and `continuity_open_holds` (and non-ledger `is_ledger_on = 0` still executes `CREATE TRIGGER`). `src/core/README.md` must accurately state the ledger-database trigger boundary.

## Non-Functional Requirements

* `NFR-01` (Test Ownership and Bounds):
  * Canonical test target: `src/api/tests/test_assistants.py` (`DialectConnection` and `DialectTests`).
  * Regression validation targets (read-only execution): `src/core/tests/test_restart_gate_sql_fences.py`, `src/api/tests/test_continuity_restart_gate.py`, and `src/api/tests/test_document_controls.py` (brought in by merging `#1781`).
  * Generated targets: `none`.
  * Exact test removals: `none`.
  * Maximum new test methods: `1` new method on `DialectTests` (`test_mssql_ledger_mode_skips_triggers_and_syncs_continuity_gate`) plus `1` assertion in existing `test_mssql_sql_shapes_enqueue_claim_complete_review_scan` confirming non-ledger mode emits `CREATE TRIGGER`.
* `NFR-02` (Static Analysis, Formatting, and Commit Hygiene):
  * Zero errors in `(cd src/core && python3 -m mypy)`, `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)`, and `python3 -m ruff check src/core src/api`.
  * Preserve formatting style of `[tool.ruff.format].exclude` files (`mssqlstore.py`, `assistants.py`, `test_assistants.py`).
  * Configure privacy-safe repository-local `git config --local user.email` (`{id}+{login}@users.noreply.github.com`) before creating merge/fix commits, include `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` on every created commit, reference `Refs #122`, keep `.copilot-tracking/` paths out of production files and commit messages, and leave `git status --short` empty without pushing.

## Acceptance Criteria

* `AC-01`: `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) is merged cleanly into `feat/platform-122-restart-gate-0228` without rewriting `d0d4135d3`, and `src/core/src/zava_forward/core/assistants.py` retains `from .doc_controls import is_available_case_document` and `if d.get("kind") in kinds and is_available_case_document(d)` in `capture()`.
* `AC-02`: `MssqlStore._create_schema_serialized` executes `GATE_TRIGGERS` only inside `else:` (`not ledger`), and `Assistants.migrate` executes `MSSQL_ATTEMPT_TRIGGERS` / `SQLITE_ATTEMPT_TRIGGERS` only under `if not (self.mssql and ledger):` while running `continuity.sync_sql_gate` unconditionally.
* `AC-03`: `DialectTests` in `src/api/tests/test_assistants.py` passes both non-ledger (`is_ledger_on = 0`, `CREATE TRIGGER` emitted) and ledger (`is_ledger_on = 1`, zero `CREATE TRIGGER` statements across `MssqlStore._create_schema_serialized` and `Assistants.migrate`, with `continuity_gate_state` and `continuity_open_holds` synchronized).
* `AC-04`: `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_assistants.py`, `mypy` (`src/core` and `src/api`), and `ruff check src/core src/api` all pass cleanly, and all changes plus Cycle 3 `.copilot-tracking/` artifacts are committed locally on a clean worktree (`git status --short` empty) without pushing.

## Phase Checklist

<!-- P01 -->
### Phase P01: Base-Branch Synchronization and SQL Server Ledger Trigger Guards

* [x] `P01-T01`: Configure privacy-safe local git author email and merge `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) cleanly, verifying `is_available_case_document` in `assistants.py:capture()` (`FR-01`, `NFR-02`).
* [x] `P01-T02`: Move `for trigger in GATE_TRIGGERS: self.db.execute(trigger)` inside the `else:` branch of `if ledger:` in `src/core/src/zava_forward/core/mssqlstore.py:_create_schema_serialized` (`FR-02`).
* [x] `P01-T03`: Initialize `ledger = False` and guard trigger execution with `if not (self.mssql and ledger):` in `src/core/src/zava_forward/core/assistants.py:migrate` (`FR-03`).
* [x] `P01-T04`: Update SQL trigger documentation in `src/core/README.md` to state the `WITH LEDGER = ON` trigger boundary (`FR-04`).

<!-- P02 -->
### Phase P02: Ledger Dialect Unit Test, Validation, and Local Commit Freeze

* [x] `P02-T01`: Extend `DialectConnection` (`ledger=False`) and add `test_mssql_ledger_mode_skips_triggers_and_syncs_continuity_gate` in `src/api/tests/test_assistants.py` (`FR-04`, `NFR-01`).
* [x] `P02-T02`: Run focused `unittest`, `mypy`, and `ruff check` validations across `src/core` and `src/api`, reconcile `.copilot-tracking/` Cycle 3 artifacts, and commit locally after post-implementation Review (`AC-03`, `AC-04`, `NFR-02`).

## Critique Disposition

* Critique artifact: `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan-critique.md` (`Complete`, single-pass verdict: `Revise`; all 3 findings `direct_planner_correction`, zero user decisions required).
* `PC-001` (`High`, accepted and applied directly): Updated `P02-T01` in phase details so `DialectConnection.execute` evaluates `if "SELECT ledger_type_desc" in sql:` ahead of `if "FROM sys.tables" in sql:` and evaluates `if self.ledger and "CREATE TRIGGER" in sql: raise sqlite3.OperationalError(...)` ahead of `if "N'TR'" in sql or "sys.indexes" in sql or "COL_LENGTH" in sql:`.
* `PC-002` (`High`, accepted and applied directly): Updated `NFR-01` and `P02-T01` to reference `test_mssql_sql_shapes_enqueue_claim_complete_review_scan`, `self.people["Quality Inspector"]`, structured `self.store.suspend(...)` incident fields, `ms.dblock = threading.RLock()`, `self.dbpath`, `self.store.assistant_connection = lambda: DialectConnection(original(), assist_statements, ledger=True)`, `svc.sql is True`, `with svc.transaction() as db: self.assertIsNotNone(svc.suspended(db, "stock-prioritisation"))`, and explicit `sqlite3`, `continuity`, and `mssqlstore` imports.
* `PC-003` (`Medium`, accepted and applied directly): Corrected regression test path from `src/api/tests/test_doc_controls.py` to `src/api/tests/test_document_controls.py` in `NFR-01` and `P02-T02`.

## Follow-Up Items

* Execute owner-witnessed operational continuity/restart drill and record appointed OD-35 / OQ-017 restart authority delegation once governance sign-off exists (non-code organizational criterion of Issue `#122`).
* Provision immutable external Azure ledger-head container and run owned Azure SQL continuity/restart drill, plus observe hosted `Source projects CI` (`MssqlLedgerMigration` and `MssqlLedgerTests`) after the branch is pushed by the owner/orchestrator.

## Handoff

* Downstream implementation changes path: `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c3-changes.md`.
* Downstream review path: `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-c3-review.md`.
