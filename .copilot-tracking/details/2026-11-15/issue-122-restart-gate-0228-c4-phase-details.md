---
title: "Phase Details - Issue #122 Assistant Tasks Trigger Column Scope Fix (Cycle 4)"
description: "Evidence-based task specifications for decoupling assistant_tasks continuity triggers from dispatched while preserving all continuity SQL fence invariants"
author: "Copilot"
ms.date: "2026-11-15"
---

## Task Context

* Task ID: `issue-122-restart-gate-0228-c4`
* Parent Task ID: `issue-122-restart-gate-0228-c3`
* Plan Path: `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan.md`
* Research Path: `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c4-research.md`

<!-- P01 -->
## Phase P01: Column-Scoped Assistant Tasks Continuity Triggers and Regression Lock

### Phase Direction

Replace `NEW.dispatched = OLD.dispatched` (SQLite) and `i.dispatched = d.dispatched` (T-SQL) in the `assistant_tasks` continuity update triggers with explicit column-scoped trigger firing (`BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision` on SQLite and `IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision))` on T-SQL), then lock both the `ALTER TABLE assistant_tasks DROP COLUMN dispatched` upgrade simulation and `dispatched`-rewrite compatibility in `test_restart_gate_sql_fences.py`.

<!-- P01-T01 -->
### Task P01-T01: Update `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` in `assistants.py`

* Target file: `src/core/src/zava_forward/core/assistants.py` (listed in `[tool.ruff.format].exclude` in `src/core/pyproject.toml`; preserve surrounding formatting).
* Evidence: `C1`, `C2`, `C4`, `C5`, `C6`, `C7` in `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c4-research.md`.
* In `SQLITE_ATTEMPT_TRIGGERS`:
  * Update `assistant_tasks_gate_update` to:
    ```python
    "CREATE TRIGGER IF NOT EXISTS assistant_tasks_gate_update "
    "BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks "
    "WHEN ((NEW.state = 'accepted' AND (OLD.state <> 'accepted' OR NEW.revision <> OLD.revision OR NEW.body <> OLD.body)) "
    "OR (OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision)) "
    "AND (NEW.reviewed_revision <> NEW.revision OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = NEW.review_gate_version)) "
    "BEGIN SELECT RAISE(ABORT, 'continuity SQL gate mismatch'); END",
    ```
  * Update `assistant_tasks_hold_update` to:
    ```python
    "CREATE TRIGGER IF NOT EXISTS assistant_tasks_hold_update "
    "BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks "
    "WHEN ((NEW.state = 'accepted' AND (OLD.state <> 'accepted' OR NEW.revision <> OLD.revision OR NEW.body <> OLD.body)) "
    "OR (OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision)) "
    "AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = 'all' OR h.scope = NEW.capability) "
    "BEGIN SELECT RAISE(ABORT, 'continuity scope is suspended'); END",
    ```
* In `MSSQL_ATTEMPT_TRIGGERS`:
  * Update `assistant_tasks_gate_update` to:
    ```python
    "IF OBJECT_ID(N'assistant_tasks_gate_update', N'TR') IS NULL EXEC(N'CREATE TRIGGER assistant_tasks_gate_update ON assistant_tasks "
    "AFTER UPDATE AS "
    "IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision)) "
    "BEGIN "
    "IF EXISTS (SELECT 1 FROM inserted i JOIN deleted d ON d.id = i.id WHERE ((i.state = ''accepted'' AND (d.state <> ''accepted'' OR i.revision <> d.revision OR i.body <> d.body)) "
    "OR (d.state = ''ready'' AND i.state = ''ready'' AND i.revision <> d.revision)) "
    "AND (i.reviewed_revision <> i.revision OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = i.review_gate_version))) "
    "THROW 50004, ''continuity SQL gate mismatch'', 1; "
    "IF EXISTS (SELECT 1 FROM inserted i JOIN deleted d ON d.id = i.id WHERE ((i.state = ''accepted'' AND (d.state <> ''accepted'' OR i.revision <> d.revision OR i.body <> d.body)) "
    "OR (d.state = ''ready'' AND i.state = ''ready'' AND i.revision <> d.revision)) "
    "AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = ''all'' OR h.scope = i.capability COLLATE Latin1_General_100_BIN2)) "
    "THROW 50004, ''continuity scope is suspended'', 1; "
    "END')",
    ```
* Completion expectation: Neither `SQLITE_ATTEMPT_TRIGGERS` nor `MSSQL_ATTEMPT_TRIGGERS` contains `"dispatched"`; `MSSQL_ATTEMPT_TRIGGERS` still has length `6` and retains `"NOT EXISTS"` and `"THROW 50004"` in `assistant_tasks_gate_update`.

<!-- P01-T02 -->
### Task P01-T02: Add `DROP COLUMN dispatched` and `dispatched`-Update Assertions in `test_restart_gate_sql_fences.py`

* Target file: `src/core/tests/test_restart_gate_sql_fences.py` (formatted by `ruff format`).
* Evidence: `C2`, `C4`, `C5`, `C6`, `C7`.
* Inside `RestartGateSqlFencesTest.test_sql_triggers_reject_old_image_and_suspended_scope_attempts`:
  1. Assert that `"dispatched"` does not appear in any statement of `ASSISTANTS_MOD.SQLITE_ATTEMPT_TRIGGERS` or `ASSISTANTS_MOD.MSSQL_ATTEMPT_TRIGGERS`.
  2. Verify that while `CAPABILITY` is suspended (and `'T-READY-1'` has `review_gate_version = ''`, `reviewed_revision = 0`), a non-review `dispatched` + `revision` update (`conn.execute("UPDATE assistant_tasks SET dispatched=99.0, revision=revision+1 WHERE id='T-READY-1'")`) succeeds without firing `assistant_tasks_gate_update` or `assistant_tasks_hold_update`, whereas `conn.execute("UPDATE assistant_tasks SET body=body, revision=revision+1 WHERE id='T-READY-1'")` raises `sqlite3.IntegrityError`.
  3. Verify that dropping `ix_assistant_dispatched` and `ALTER TABLE assistant_tasks DROP COLUMN dispatched` on `conn` succeeds with all `SQLITE_ATTEMPT_TRIGGERS` installed, and calling `self.service.migrate()` idempotently restores the `dispatched` column on `assistant_tasks`.
* Completion expectation: `test_restart_gate_sql_fences.py` directly fails if `dispatched` is ever re-referenced in a trigger, if `SET dispatched=?, revision=revision+1` is inadvertently blocked, or if `SET body=body, revision=revision+1` stops failing closed.

<!-- P02 -->
## Phase P02: Focused Validation, Review, and Clean Local Commit

### Phase Direction

Run all requested focused unit tests (plus `test_quality_sensors_e2.py`), lint/format checks, strict `mypy` across `src/core` and `src/api`, and migration checks, reconcile tracking artifacts, complete `rpi-review`, and freeze a clean local commit on `feat/platform-122-restart-gate-0228`.

<!-- P02-T01 -->
### Task P02-T01: Execute Focused Validation Commands, Reconcile Evidence, and Commit Locally

* Execute from repository root `/home/azureuser/source/ama-demo-wt/feat-122-restart-gate`:
  1. `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_quality_sensors_c7.py" -v`
  2. `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_quality_sensors_e2.py" -v`
  3. `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/core/tests -p "test_restart_gate_sql_fences.py" -v`
  4. `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_continuity_restart_gate.py" -v`
  5. `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_mssqlstore.py" -v`
  6. `python3 -m ruff check src/core src/api`
  7. `python3 -m ruff format --check src/core src/api`
  8. `(cd src/core && PYTHONPATH=src python3 -m mypy)`
  9. `(cd src/api && PYTHONPATH=../core/src:../agents/src:src python3 -m mypy)`
  10. `python3 tools/rename-zava-tests.py`
* Persist implementation evidence in `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c4-changes.md`, complete single-pass `rpi-review` into `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-c4-review.md` (and update `.copilot-tracking/reviews/2026-11-15/122-restart-gate-review.md`), persist `Follow-up` completion state in `.copilot-tracking/rpi-sessions/2026-11-15/issue-122-restart-gate-0228-c4-state.json`, configure privacy-safe `git config --local user.email`, and create a single clean local commit with `Refs #122` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.
* Completion expectation: All 10 validation commands exit `0` and `git status --short` is empty.
