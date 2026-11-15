<!-- markdownlint-disable-file -->
# Review: Issue #122 Assistant Tasks Trigger Column Scope Fix (Cycle 4)

## Scope and Evidence

* Task ID: issue-122-restart-gate-0228-c4
* Parent Task ID: issue-122-restart-gate-0228-c3
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`)
* Assessed boundary: Cycle 4 remediation of the sole remaining `PR #1787` CI failure (`src-api` job `132800541482`, commit `573b86b41`) in `test_quality_sensors_c7.Upgrade.test_actual_c5_tables_are_upgraded_in_place_idempotently_and_keep_their_rows` (`sqlite3.OperationalError: error in trigger assistant_tasks_gate_update after drop column: no such column: NEW.dispatched`), covering column-scoped `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` in `src/core/src/zava_forward/core/assistants.py` and core regression assertions in `src/core/tests/test_restart_gate_sql_fences.py` (`FR-01` through `FR-03`, `NFR-01`, `NFR-02`, and `AC-01` through `AC-04`).
* Plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c4-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c4-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c4-research.md (`C1` through `C7`); working-tree diff across `src/core/src/zava_forward/core/assistants.py` and `src/core/tests/test_restart_gate_sql_fences.py`; local focused validation output across `test_quality_sensors_c7.py`, `test_quality_sensors_e2.py`, `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_mssqlstore.py`, `test_permit_sql.py`, `test_assistants.py`, `ruff`, `mypy`, and `tools/rename-zava-tests.py`.

## Opening Review State

* Interpreted review goal: Execute a single-pass, evidence-based, read-only post-implementation review of Cycle 4 (`issue-122-restart-gate-0228-c4`) across `P01` and `P02`, confirming complete removal of `dispatched` trigger coupling for C5 `DROP COLUMN dispatched` schema migration tests, preservation of `'ready'` `dispatched` retry rewrites (`test_quality_sensors_e2.py`) and row-lock `revision` updates (`test_permit_sql.py`), fail-closed continuity SQL gate and open-hold enforcement on every `verify`, `accept`, and `edit-accept` update path (including `SET body=body, revision=revision+1`), and clean routing of external follow-ups.
* Review scope: Full task (`P01`, `P02`)
* Evidence readiness: Ready; all `P01` and `P02` checklist markers (`P01-T01`, `P01-T02`, `P02-T01`), phase details, single-pass plan critique (`Pass`, `0` findings), changes record (`Completed`), and focused validation checks are complete and reconciled.
* Acceptance basis: `FR-01` through `FR-03`, `NFR-01`, `NFR-02`, and `AC-01` through `AC-04`.
* First comparison boundary: Compare `P01-T01` and `P01-T02` specifications against the working-tree diff in `src/core/src/zava_forward/core/assistants.py` and `src/core/tests/test_restart_gate_sql_fences.py`.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-c4-review.md` while the parent RPI Agent persists session state transitions and creates the requested local commit.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only post-implementation review on 2026-11-15 across `P01` (`P01-T01`, `P01-T02`) and `P02` (`P02-T01`), inspecting working-tree diffs in `src/core`, reconciled Cycle 4 RPI artifacts, independent trigger bypass analysis, and full local validation output.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Column-Scoped Assistant Tasks Continuity Triggers and Regression Lock | Reconciled | Scoped SQLite `assistant_tasks_gate_update` and `assistant_tasks_hold_update` to `BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks`, guarded T-SQL `assistant_tasks_gate_update` with `IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision)) BEGIN ... END`, removed `NEW.dispatched = OLD.dispatched` and `i.dispatched = d.dispatched`, and extended `RestartGateSqlFencesTest.test_sql_triggers_reject_old_image_and_suspended_scope_attempts` with trigger-text, `SET dispatched=99.0, revision=revision+1`, `SET body=body, revision=revision+1` (pre-suspend and suspended), and `DROP COLUMN dispatched` + `migrate()` assertions. |
| `P02` (`P02-T01`) | Focused Validation, Review, and Clean Local Commit | Reconciled | Passed `test_quality_sensors_c7.py` (`59` run, `9` skipped), `test_quality_sensors_e2.py` (`78` run, `39` skipped), `test_restart_gate_sql_fences.py` (`9/9`), `test_continuity_restart_gate.py` (`9/9`), `test_mssqlstore.py` (`244` run, `235` skipped), `test_assistants.py` (`139` run, `60` skipped), `ruff check`, `ruff format --check`, `mypy` (`src/core` and `src/api`), and `tools/rename-zava-tests.py` (`25/25`). |
| `Follow-Up Items` | Outer-workflow push + hosted `Source projects CI` observation and external `OD-35`/`OQ-017` + Azure ledger-head drills | Reconciled | Properly retained outside active `Pxx` scope under `Refs #122` and caller's no-push local commit instruction. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/core/src/zava_forward/core/assistants.py | Scoped SQLite `assistant_tasks_gate_update` and `assistant_tasks_hold_update` and T-SQL `assistant_tasks_gate_update` to `state, body, capability, review_gate_version, reviewed_revision` and removed all `dispatched` references. | Satisfies `FR-01`, `FR-02`, and `AC-01`. | Passed (`test_quality_sensors_c7.py`, `test_quality_sensors_e2.py`, `test_continuity_restart_gate.py`, `test_mssqlstore.py`, `test_assistants.py`) | Reconciled |
| `P01-T02` | src/core/tests/test_restart_gate_sql_fences.py | Added regression assertions inside `test_sql_triggers_reject_old_image_and_suspended_scope_attempts` covering zero `"dispatched"` references across all SQLite/T-SQL triggers, `SET dispatched=99.0, revision=revision+1` compatibility, fail-closed `SET body=body, revision=revision+1` rejection before and during suspension, and `ALTER TABLE assistant_tasks DROP COLUMN dispatched` + `self.service.migrate()` recovery. | Satisfies `FR-03` and `NFR-01` with `0` new test methods added. | Passed (`test_restart_gate_sql_fences.py` `9/9`, `ruff`, `mypy`) | Reconciled |
| `P02-T01` | .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan.md, .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c4-changes.md | Executed full focused validation suite plus contrarian `test_quality_sensors_e2.py` and `test_assistants.py` checks and reconciled plan/changes artifacts. | Satisfies `AC-02`, `AC-03`, and `NFR-02`. | Passed (`0` errors across all checks) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T02` (dual lifecycle `SET body=body, revision=revision+1` assertion) | Asserted `SET body=body, revision=revision+1` both before `self.store.suspend(...)` (`continuity SQL gate mismatch` from `assistant_tasks_gate_update`) and during suspension (`continuity scope is suspended` from `assistant_tasks_hold_update`, evaluated first by SQLite reverse trigger order). | SQLite `BEFORE UPDATE` trigger firing order on `assistant_tasks`. | Recorded in `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c4-changes.md`. | Not needed (strengthens `P01-T02` coverage across both update triggers without changing scope or test count). | Reconciled |
| `P02-T01` (`test_mssqlstore.py` root `PYTHONPATH`) | Ran `test_mssqlstore.py` both from `src/api` (per `.github/copilot-instructions.md`) and from repository root with `src/api` included in `PYTHONPATH` so `from tests.test_mvp import DATA` in `test_handoff_api.py` resolves cleanly. | Cross-test import layout under `src/api/tests`. | Recorded in `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c4-changes.md`. | Not needed (execution environment detail; zero code divergence). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Single-pass critique `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan-critique.md` returned `Verdict: Pass` with `0` findings across all severity levels and explicit acceptance of hosted CI live SQL Server 2022 coverage.
* Material revisions: None. Note that `assistant_tasks_gate_update` and `assistant_tasks_hold_update` were introduced in `PR #1787` and have never existed on `main` or `feat/demo-164-chat-grounding-provenance-0900`, so `CREATE TRIGGER IF NOT EXISTS` / `IF OBJECT_ID(..., N'TR') IS NULL` encounters no legacy trigger definition on any upstream database, and bare `revision`-only increments without touching `state`, `body`, `capability`, `review_gate_version`, or `reviewed_revision` cannot mutate any proposal output, review state, or case state.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Push `feat/platform-122-restart-gate-0228` and confirm all 10 hosted `Source projects CI` jobs pass on `PR #1787` | Caller explicitly instructed `Do NOT push or open a PR; return a clean frozen local commit`. | Owner / Outer Orchestrator: push frozen branch and read exact-head CI on `PR #1787`. | Open distinct follow-up; properly excluded from local freeze scope. |
| Owner-witnessed operational continuity/restart drill, `OD-35`/`OQ-017` human restart authority appointment, and immutable external Azure ledger-head drill | Non-code organizational and cloud-custody criteria of Issue `#122`. | Owner: Programme Sponsor / Building Safety / Platform. | Open distinct follow-up (`Refs #122`); properly excluded from active `Pxx` claims. |

## Findings

No material defects, decision gaps, or evidence gaps were found within the Cycle 4 task boundary (`0` Critical, `0` High, `0` Medium, `0` Low).

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None (active local scope) | none | Ready for local commit freeze on `feat/platform-122-restart-gate-0228` | All Cycle 4 requirements (`FR-01`–`FR-03`, `AC-01`–`AC-04`) are satisfied and verified |

## Residual Work

* Push `feat/platform-122-restart-gate-0228` via the outer orchestrator / owner workflow and verify all 10 hosted `Source projects CI` jobs (`src-api`, `mssql`, `src-core`, `src-agents`, `src-importer`, `src-orchestrator`, `src-namespace`, `image-paths`, `src-changes`, `src-no-working-data`) pass on `PR #1787`.
* Complete external non-code criteria of Issue `#122` (`OD-35`/`OQ-017` human restart authority appointment, witnessed drill, and external Azure ledger-head drill; `Refs #122`).

## Blockers and Remaining Work

* Blockers: none
* Remaining active task work: Persist `Follow-up` completion state in `.copilot-tracking/rpi-sessions/2026-11-15/issue-122-restart-gate-0228-c4-state.json` and commit all Cycle 4 changes cleanly on `feat/platform-122-restart-gate-0228` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.

## Outcome

* Execution status: Complete
* Outcome: Conformant
* Summary: Cycle 4 eliminates all `dispatched` column references from `assistant_tasks_gate_update` and `assistant_tasks_hold_update` in `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` using column-scoped `BEFORE UPDATE OF` / `IF (UPDATE(...))` guards, resolves the `test_quality_sensors_c7.Upgrade` `DROP COLUMN dispatched` CI failure while preserving `test_quality_sensors_e2.Cursor` `SET dispatched=?,revision=revision+1` compatibility and all continuity SQL gate/hold invariants, locks both behaviors in `src/core/tests/test_restart_gate_sql_fences.py`, and passes every focused unit, static typing, lint, formatting, and migration check.
