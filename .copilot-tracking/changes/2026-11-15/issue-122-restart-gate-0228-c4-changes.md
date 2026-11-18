---
title: "Implementation Changes - Issue #122 Assistant Tasks Trigger Column Scope Fix (Cycle 4)"
description: "Implementation and validation evidence for decoupling assistant_tasks continuity update triggers from dispatched"
author: "Copilot"
ms.date: "2026-11-15"
---

## Metadata

* Task ID: `issue-122-restart-gate-0228-c4`
* Parent Task ID: `issue-122-restart-gate-0228-c3`
* Plan Path: `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c4-phase-details.md`
* Critique Path: `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan-critique.md` (`Pass`)
* Declared Scope: Full plan (`P01-T01`, `P01-T02`, `P02-T01`)
* Execution Status: `Completed`

## Opening Implementation State

* Active checklist markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`) — all completed (`[x]`).
* First dependency-ready task: `P01-T01`.
* Blockers: `none`.

## Completed Phase and Task Evidence

| Marker | Files Changed | Summary of Changes | Validation |
| --- | --- | --- | --- |
| `P01-T01` | `src/core/src/zava_forward/core/assistants.py` | Scoped SQLite `assistant_tasks_gate_update` and `assistant_tasks_hold_update` in `SQLITE_ATTEMPT_TRIGGERS` to `BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks` and removed `AND NEW.dispatched = OLD.dispatched`; guarded T-SQL `assistant_tasks_gate_update` in `MSSQL_ATTEMPT_TRIGGERS` with `IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision)) BEGIN ... END` and removed `AND i.dispatched = d.dispatched` (`FR-01`, `FR-02`). | `test_quality_sensors_c7.py` (`59` run, `9` skipped, `OK`), `test_quality_sensors_e2.py` (`78` run, `39` skipped, `OK`), `test_continuity_restart_gate.py` (`9/9` `OK`), `test_mssqlstore.py` (`244` run, `235` skipped, `OK`) |
| `P01-T02` | `src/core/tests/test_restart_gate_sql_fences.py` | Extended `RestartGateSqlFencesTest.test_sql_triggers_reject_old_image_and_suspended_scope_attempts` to assert zero `"dispatched"` references across `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS`, fail-closed `SET body=body, revision=revision+1` blocking both before suspension (`continuity SQL gate mismatch`) and during suspension (`continuity scope is suspended`), compatibility of `SET dispatched=99.0, revision=revision+1` on `'T-READY-1'`, and clean `DROP INDEX IF EXISTS ix_assistant_dispatched` + `ALTER TABLE assistant_tasks DROP COLUMN dispatched` + `self.service.migrate()` recovery with active triggers (`FR-03`, `NFR-01`). | `test_restart_gate_sql_fences.py` (`9/9` `OK` in `5.524s`) |
| `P02-T01` | `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan.md`, `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c4-changes.md` | Ran all focused unit, lint, formatting, strict `mypy`, and migration regression validations across `src/core` and `src/api` and reconciled all `P01` and `P02` checklist markers (`AC-02`, `AC-03`, `NFR-02`). | All checks passed (`0` failures) |

## Implementation-Time Plan and Detail Updates

* Local judgment (`P01-T02`): Verified `UPDATE assistant_tasks SET body=body, revision=revision+1 WHERE id='T-READY-1'` at two lifecycle points inside `test_sql_triggers_reject_old_image_and_suspended_scope_attempts` — before suspension (asserting `continuity SQL gate mismatch` from `assistant_tasks_gate_update`) and during suspension (asserting `continuity scope is suspended` from `assistant_tasks_hold_update`, which SQLite evaluates first in reverse trigger creation order) — proving both update triggers enforce column-list firing on `body=body`.
* Local judgment (`P02-T01`): Included `src/api` on `PYTHONPATH` when running `test_mssqlstore.py` from the repository root (`PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/api:src/core/tests:src/agents/tests`, as well as from `src/api` per repository instructions) so `from tests.test_mvp import DATA` in `test_handoff_api.py` resolves cleanly.

## Validation Results

| Check | Command | Result |
| --- | --- | --- |
| `test_quality_sensors_c7.py` (exact CI failure module) | `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_quality_sensors_c7.py" -v` | Passed (`59` tests run, `9` skipped, `0` failures) |
| `test_quality_sensors_e2.py` (contrarian `'ready'` `dispatched` update guard) | `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_quality_sensors_e2.py" -v` | Passed (`78` tests run, `39` skipped, `0` failures) |
| `test_restart_gate_sql_fences.py` | `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/core/tests -p "test_restart_gate_sql_fences.py" -v` | Passed (`9` tests in `5.524s`, `0` failures) |
| `test_continuity_restart_gate.py` | `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_continuity_restart_gate.py" -v` | Passed (`9` tests in `15.013s`, `0` failures) |
| `test_mssqlstore.py` & `test_permit_sql.py` | `(cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_mssqlstore.py" -v)` + `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/api:src/core/tests:src/agents/tests python3 -m unittest discover -s src/api/tests -p "test_mssqlstore.py" -q` | Passed (`244` tests run, `235` skipped; `test_permit_sql.py` `7` skipped) |
| Ruff lint & format check | `python3 -m ruff check src/core src/api && python3 -m ruff format --check src/core src/api` | Passed (`All checks passed!`; `515 files already formatted`) |
| Mypy (`src/core` and `src/api`) | `(cd src/core && PYTHONPATH=src python3 -m mypy) && (cd src/api && PYTHONPATH=../core/src:../agents/src:src python3 -m mypy)` | Passed (`0` issues in `354` `src/core` files + `298` `src/api` files) |
| Migration regression check | `python3 tools/rename-zava-tests.py` | Passed (`25` tests in `0.830s`) |

## Blockers, Remaining Work, and Follow-Ups

* Blockers: `none`
* Remaining active implementation work: `none` (`P01` and `P02` implementation and validation complete; proceeding to single-pass `rpi-review` and local commit)
* Follow-up items outside local scope (`Refs #122`):
  * Push `feat/platform-122-restart-gate-0228` via the outer orchestrator / owner workflow and verify all 10 hosted `Source projects CI` jobs pass on `PR #1787`.
  * Execute owner-witnessed operational continuity/restart drill and record appointed OD-35 / OQ-017 restart authority delegation once governance sign-off exists.
  * Provision immutable external Azure ledger-head container and run owned Azure SQL continuity/restart drill.
