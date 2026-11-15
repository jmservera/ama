---
title: "Implementation Plan - Issue #122 Assistant Tasks Trigger Column Scope Fix (Cycle 4)"
description: "Surgical CI remediation removing dispatched column coupling from assistant_tasks continuity triggers while preserving dispatched-only retry updates and all SQL gate/hold invariants"
author: "Copilot"
ms.date: "2026-11-15"
---

## Metadata

* Task ID: `issue-122-restart-gate-0228-c4`
* Task Slug: `issue-122-restart-gate-0228-c4`
* Parent Task: `issue-122-restart-gate-0228-c3`
* Branch: `feat/platform-122-restart-gate-0228` (targeting `feat/demo-164-chat-grounding-provenance-0900`, `PR #1787` -> `PR #1641`)
* Date: `2026-11-15`
* Planning Status: `Ready after Critique`
* Validation Tier: `Focused` (targeted SQL trigger column-scope bug fix in `src/core/src/zava_forward/core/assistants.py` with focused unit suites `test_quality_sensors_c7.py`, `test_quality_sensors_e2.py`, `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_mssqlstore.py`, `ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, and `tools/rename-zava-tests.py`)
* Research Artifact: `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c4-research.md` (`executed`)
* Phase Details Artifact: `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c4-phase-details.md`
* Critique Artifact: `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan-critique.md`
* Downstream Changes Artifact: `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c4-changes.md`

## Executive Summary

Cycle 4 (`issue-122-restart-gate-0228-c4`) resolves the sole remaining CI failure on `PR #1787` (`src-api` job `132800541482` on commit `573b86b41`, where all 9 other CI jobs and `3,772/3,773` `src-api` tests passed):

1. **Decouple `assistant_tasks` Continuity Triggers from `dispatched` (`src/core/src/zava_forward/core/assistants.py`)**: `test_quality_sensors_c7.Upgrade.downgrade()` simulates a C5 schema by executing `ALTER TABLE assistant_tasks DROP COLUMN dispatched`, causing SQLite trigger schema re-validation to fail with `no such column: NEW.dispatched` on `assistant_tasks_gate_update` and `assistant_tasks_hold_update`. Furthermore, contrarian research (`C4`) found that `test_quality_sensors_e2.Cursor` executes `UPDATE assistant_tasks SET dispatched=?,revision=revision+1 WHERE id='oldzzz'` on a `'ready'` row, which would fail if `AND NEW.dispatched = OLD.dispatched` were deleted without scoping the trigger column list. Scoping SQLite `assistant_tasks_gate_update` and `assistant_tasks_hold_update` to `BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks` (and T-SQL `assistant_tasks_gate_update` to `IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision))`) while removing `NEW.dispatched = OLD.dispatched` and `i.dispatched = d.dispatched` eliminates every reference to `dispatched`, keeps `dispatched`/`revision`-only updates working, and preserves every continuity SQL gate and open-hold fence invariant (including `SET body=body, revision=revision+1` pre-gate verify probes).
2. **Focused Regression Assertions (`src/core/tests/test_restart_gate_sql_fences.py`)**: Extend `RestartGateSqlFencesTest.test_sql_triggers_reject_old_image_and_suspended_scope_attempts` to verify zero `dispatched` references in `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS`, non-review `SET dispatched=?, revision=revision+1` compatibility on a `'ready'` row, fail-closed `SET body=body, revision=revision+1` rejection, and `ALTER TABLE assistant_tasks DROP COLUMN dispatched` + idempotent `Assistants.migrate()` recovery with active SQLite triggers.

## Sources and Evidence

* `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c4-research.md` (`C1`–`C7`)
* `src/core/src/zava_forward/core/assistants.py` (`SQLITE_ATTEMPT_TRIGGERS`, `MSSQL_ATTEMPT_TRIGGERS`, `Assistants._upgrade`, `Assistants.review`)
* `src/api/tests/test_quality_sensors_c7.py` (`Upgrade.downgrade`, `test_actual_c5_tables_are_upgraded_in_place_idempotently_and_keep_their_rows`)
* `src/api/tests/test_quality_sensors_e2.py` (`Cursor.test_the_cap_is_unchanged_and_a_long_history_completes_over_scans_and_restarts`)
* `src/api/tests/test_continuity_restart_gate.py` (`test_old_image_worker_and_upgraded_ddl_fail_closed_across_queued_leased_and_ready`, `test_mssql_ddl_and_trigger_shapes_include_continuity_gate_fences`)
* `src/api/tests/test_mssqlstore.py` (`wipe`)
* `src/core/tests/test_restart_gate_sql_fences.py` (`RestartGateSqlFencesTest`)

## User Decisions and Requirements

* Run the full RPI loop (`research`, `plan`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` for Issue `#122` (`PR #1787` correction cycle `c4`) on `feat/platform-122-restart-gate-0228`.
* Fix the `src-api` CI failure in `test_quality_sensors_c7.Upgrade.test_actual_c5_tables_are_upgraded_in_place_idempotently_and_keep_their_rows` (`sqlite3.OperationalError: error in trigger assistant_tasks_gate_update after drop column: no such column: NEW.dispatched`).
* Remove `dispatched` references (`NEW.dispatched = OLD.dispatched` in `SQLITE_ATTEMPT_TRIGGERS` and `i.dispatched = d.dispatched` in `MSSQL_ATTEMPT_TRIGGERS`) from `assistant_tasks_gate_update` and `assistant_tasks_hold_update` in `src/core/src/zava_forward/core/assistants.py` while preserving every continuity SQL fence invariant and existing `src-api` suite compatibility.
* Run the focused validation commands (`test_quality_sensors_c7.py`, `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_mssqlstore.py`, `ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, and `tools/rename-zava-tests.py`, plus `test_quality_sensors_e2.py` uncovered in contrarian research).
* Commit all changes cleanly on `feat/platform-122-restart-gate-0228` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing or opening/modifying a PR.

## Goals

* Eliminate all `dispatched` column references from `assistant_tasks` SQLite and T-SQL triggers so `ALTER TABLE assistant_tasks DROP COLUMN dispatched` succeeds cleanly during C5 schema downgrade/upgrade verification.
* Preserve non-review `dispatched` and `revision` updates on `'ready'` rows (`test_quality_sensors_e2.py`) and row-lock `revision` updates (`test_permit_sql.py`) without weakening any continuity SQL gate or open-hold fence on `verify`, `accept`, or `edit-accept` transitions.
* Lock the `DROP COLUMN dispatched` and `dispatched`-update trigger invariants directly in `src/core/tests/test_restart_gate_sql_fences.py`.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/assistants.py` (`SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS`)
* `src/core/tests/test_restart_gate_sql_fences.py` (focused regression assertions in existing trigger test method)
* `.copilot-tracking/` Cycle 4 RPI artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`)

### Non-Goals

* Modifying `src/api/tests/test_quality_sensors_c7.py` or `src/api/tests/test_quality_sensors_e2.py`.
* Changing `assistant_attempts` triggers, `continuity_gate_state` triggers, or `WITH LEDGER = ON` SQL Server guards from Cycle 3.
* Pushing commits or modifying remote pull requests.

## Functional Requirements

* `FR-01` (SQLite `assistant_tasks` Update Trigger Column Scope): `assistant_tasks_gate_update` and `assistant_tasks_hold_update` in `SQLITE_ATTEMPT_TRIGGERS` (`src/core/src/zava_forward/core/assistants.py`) must use `BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks` and omit `AND NEW.dispatched = OLD.dispatched`, so neither trigger references `dispatched`, `ALTER TABLE assistant_tasks DROP COLUMN dispatched` succeeds, `UPDATE assistant_tasks SET dispatched=?, revision=revision+1` on a `'ready'` row does not fire the trigger, and any `UPDATE` touching `state`, `body` (including `SET body=body, revision=revision+1`), `capability`, `review_gate_version`, or `reviewed_revision` remains fail-closed under gate mismatch or active hold.
* `FR-02` (T-SQL `assistant_tasks_gate_update` Column Scope Parity): `assistant_tasks_gate_update` in `MSSQL_ATTEMPT_TRIGGERS` (`src/core/src/zava_forward/core/assistants.py`) must wrap its two `IF EXISTS (...) THROW 50004` checks inside `IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision)) BEGIN ... END` and omit `AND i.dispatched = d.dispatched`, maintaining exact semantic parity with SQLite while retaining `NOT EXISTS` and `THROW 50004`.
* `FR-03` (Core SQL Fence Regression Assertions): `RestartGateSqlFencesTest.test_sql_triggers_reject_old_image_and_suspended_scope_attempts` in `src/core/tests/test_restart_gate_sql_fences.py` must verify that: (a) no trigger in `SQLITE_ATTEMPT_TRIGGERS` or `MSSQL_ATTEMPT_TRIGGERS` contains `"dispatched"`, (b) `UPDATE assistant_tasks SET dispatched = 99.0, revision = revision + 1` on `'T-READY-1'` succeeds while `UPDATE assistant_tasks SET body = body, revision = revision + 1` fails closed, and (c) `DROP INDEX IF EXISTS ix_assistant_dispatched` + `ALTER TABLE assistant_tasks DROP COLUMN dispatched` succeeds with active triggers and `self.service.migrate()` idempotently restores `dispatched`.

## Non-Functional Requirements

* `NFR-01` (Test Ownership and Bounds):
  * Canonical test target: `src/core/tests/test_restart_gate_sql_fences.py` (`RestartGateSqlFencesTest.test_sql_triggers_reject_old_image_and_suspended_scope_attempts`).
  * Regression validation targets (read-only execution): `src/api/tests/test_quality_sensors_c7.py`, `src/api/tests/test_quality_sensors_e2.py`, `src/api/tests/test_continuity_restart_gate.py`, `src/api/tests/test_mssqlstore.py`, and `tools/rename-zava-tests.py`.
  * Generated targets: `none`.
  * Exact test removals: `none`.
  * Maximum new test methods: `0` new test methods (focused assertions added inside existing `test_sql_triggers_reject_old_image_and_suspended_scope_attempts`, keeping the `9 + 9 = 18` combined core+api `#122` test method count unchanged).
* `NFR-02` (Static Analysis, Formatting, and Commit Hygiene):
  * Zero errors in `python3 -m ruff check src/core src/api`, `python3 -m ruff format --check src/core src/api`, `(cd src/core && PYTHONPATH=src python3 -m mypy)`, and `(cd src/api && PYTHONPATH=../core/src:../agents/src:src python3 -m mypy)`.
  * Preserve formatting style of `[tool.ruff.format].exclude` file `src/core/src/zava_forward/core/assistants.py`, while formatting `src/core/tests/test_restart_gate_sql_fences.py` cleanly under `ruff format --check`.
  * Configure privacy-safe repository-local `git config --local user.email` (`{id}+{login}@users.noreply.github.com`), include `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and `Refs #122`, exclude `.copilot-tracking/` paths from production code and commit messages, and leave `git status --short` empty without pushing.

## Acceptance Criteria

* `AC-01`: `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` in `src/core/src/zava_forward/core/assistants.py` contain zero references to `dispatched` and scope `assistant_tasks` update enforcement to `state`, `body`, `capability`, `review_gate_version`, and `reviewed_revision`.
* `AC-02`: `test_quality_sensors_c7.py` (`Upgrade.test_actual_c5_tables_are_upgraded_in_place_idempotently_and_keep_their_rows`) and `test_quality_sensors_e2.py` (`Cursor.test_the_cap_is_unchanged_and_a_long_history_completes_over_scans_and_restarts`) both pass in full.
* `AC-03`: `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_mssqlstore.py`, `ruff check src/core src/api`, `ruff format --check src/core src/api`, `mypy` (`src/core` and `src/api`), and `tools/rename-zava-tests.py` all pass with zero errors.
* `AC-04`: All source, test, and Cycle 4 `.copilot-tracking/` changes are committed cleanly on `feat/platform-122-restart-gate-0228` with the required Copilot co-author trailer and `git status --short` empty (no `git push`).

## Phase Checklist

<!-- P01 -->
### Phase P01: Column-Scoped Assistant Tasks Continuity Triggers and Regression Lock

* [x] `P01-T01`: Scope `assistant_tasks_gate_update` and `assistant_tasks_hold_update` in `SQLITE_ATTEMPT_TRIGGERS` and `assistant_tasks_gate_update` in `MSSQL_ATTEMPT_TRIGGERS` to `state, body, capability, review_gate_version, reviewed_revision` and remove `dispatched` references in `src/core/src/zava_forward/core/assistants.py` (`FR-01`, `FR-02`).
* [x] `P01-T02`: Extend `test_sql_triggers_reject_old_image_and_suspended_scope_attempts` in `src/core/tests/test_restart_gate_sql_fences.py` to assert zero `dispatched` trigger references, `SET dispatched=?, revision=revision+1` compatibility, fail-closed `SET body=body, revision=revision+1` blocking, and `ALTER TABLE assistant_tasks DROP COLUMN dispatched` + `Assistants.migrate()` recovery (`FR-03`, `NFR-01`).

<!-- P02 -->
### Phase P02: Focused Validation, Review, and Clean Local Commit

* [x] `P02-T01`: Run all focused unit suites (`test_quality_sensors_c7.py`, `test_quality_sensors_e2.py`, `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_mssqlstore.py`), `ruff check`, `ruff format --check`, `mypy` (`src/core`, `src/api`), and `tools/rename-zava-tests.py`, record changes evidence, execute single-pass `rpi-review`, and create a clean local commit on `feat/platform-122-restart-gate-0228` (`AC-02`, `AC-03`, `AC-04`, `NFR-02`).

## Critique Disposition

* Critique artifact: `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan-critique.md` (`Complete`, single-pass verdict: `Pass`; `0` Critical, `0` High, `0` Medium, `0` Low findings; zero user decisions required).
* Residual risk disposition: Live SQL Server 2022 T-SQL execution of `IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision))` runs in hosted `Source projects CI` (`mssql` job) once pushed; local `DialectTests`, `test_continuity_restart_gate.py`, `test_mssqlstore.py`, and `test_restart_gate_sql_fences.py` verify trigger shape, absence of `dispatched`, and SQLite trigger enforcement.

## Follow-Up Items

* Push `feat/platform-122-restart-gate-0228` via the outer orchestrator / owner workflow and verify all 10 hosted `Source projects CI` jobs pass on `PR #1787`.
* Execute owner-witnessed operational continuity/restart drill and record appointed OD-35 / OQ-017 restart authority delegation once governance sign-off exists (`Refs #122`).
* Provision immutable external Azure ledger-head container and run owned Azure SQL continuity/restart drill (`Refs #122`).

## Handoff

* Downstream implementation changes path: `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c4-changes.md`.
* Downstream review path: `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-c4-review.md`.
