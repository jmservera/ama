<!-- markdownlint-disable-file -->

# Task Research: issue-122-restart-gate-0228-c4

| Field              | Value                                                                          |
|--------------------|--------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                     |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                        |
| Status             | Complete                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c4-research.md |

## Research Brief

* What to research: Exact CI failure in `PR #1787` (`src-api` job `132800541482` on commit `573b86b41`) in `test_quality_sensors_c7.Upgrade.test_actual_c5_tables_are_upgraded_in_place_idempotently_and_keep_their_rows`, where `ALTER TABLE assistant_tasks DROP COLUMN dispatched` fails with `sqlite3.OperationalError: error in trigger assistant_tasks_gate_update after drop column: no such column: NEW.dispatched`.
* Why it matters: All 9 other CI jobs (`mssql`, `src-core`, `src-agents`, `src-importer`, `src-orchestrator`, `src-namespace`, `image-paths`, `src-changes`, `src-no-working-data`) and `3,772/3,773` `src-api` tests passed, leaving this single SQLite trigger column-reference incompatibility with C5 schema downgrade/upgrade simulation as the sole CI failure on `PR #1787`.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in automatic RPI Cycle 4 (`c4`), plus reviewers of `PR #1787`.
* Scope: `src/core/src/zava_forward/core/assistants.py`, `src/api/tests/test_quality_sensors_c7.py`, `src/api/tests/test_mssqlstore.py`, `src/core/tests/test_restart_gate_sql_fences.py`, and `src/api/tests/test_continuity_restart_gate.py`.
* Non-goals: Do not weaken any continuity SQL fence invariant on `assistant_tasks` or `assistant_attempts`; do not modify `test_quality_sensors_c7.Upgrade.downgrade()` to mask schema compatibility; do not push or open/modify PRs.
* Criteria: Every codebase finding uses stable `C#` IDs with workspace-relative `path:line`; verifies every `UPDATE assistant_tasks` statement in `src/` to confirm no continuity fence invariant depends on `dispatched` inside `assistant_tasks_gate_update` / `assistant_tasks_hold_update`, and checks whether any other dropped columns in `Upgrade.downgrade()` or other upgrade tests are referenced by triggers.
* Requested outputs: Convergence recommendation for `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` in `assistants.py` plus any coupled test assertions or regression tests.
* Output mode: convergence

## Research Parameters

| Field                             | Value                                                                                                                                      |
|-----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)              | Q1-Q4 covering `Upgrade.downgrade()` dropped columns vs. active triggers, every `UPDATE assistant_tasks` path vs. trigger invariants, T-SQL parity in `MSSQL_ATTEMPT_TRIGGERS`, and coupled test assertions |
| Codebase scope                    | `src/core/**`, `src/api/tests/**`, `.copilot-tracking/**/2026-11-15/issue-122-restart-gate-0228*`                                          |
| External scope                    | none (bounded internal repository and supplied CI failure trace)                                                                           |
| Initial internal candidate areas  | `src/core/src/zava_forward/core/assistants.py`, `src/api/tests/test_quality_sensors_c7.py`, `src/api/tests/test_mssqlstore.py`, `src/core/tests/test_restart_gate_sql_fences.py`, `src/api/tests/test_continuity_restart_gate.py` |
| Initial external candidate areas  | none                                                                                                                                       |
| Research posture                  | focused                                                                                                                                    |
| Posture provenance                | caller-supplied exact CI failure (`job 132800541482`, commit `573b86b41`) and bounded trigger targets                                      |
| Explicit limits / deadline        | Local worktree `/home/azureuser/source/ama-demo-wt/feat-122-restart-gate` (`feat/platform-122-restart-gate-0228`); no `git push`           |
| Posture-specific completion basis | All four questions answered with direct codebase evidence across all three waves (`Wider`, `Deeper`, `Contrarian`)                         |
| Edits allowed during research?    | no, research-only                                                                                                                          |
| Resolved evidence root            | `.copilot-tracking/`                                                                                                                       |
| Known constraints / excluded sources | Respect `[tool.ruff.format].exclude` in `src/core/pyproject.toml` and `src/api/pyproject.toml`                                           |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                          | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|-----------------------------------|-----------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` repository custom instruction | Focused validation tier, test commands, commit trailer, no unrequested push      | Selected: governs focused validation commands and local commit policy                     |
| Skill               | `rpi-research`                    | Active Phase 1 RPI skill                      | Read-only three-wave research artifact, `Planning Readiness`, and `disposition`  | Selected: active phase skill                                                              |
| Research specialist | `hve-core-all:rpi-researcher`     | Host subagent for independent lanes           | Subagent lane artifact under `.copilot-tracking/research/subagents/`             | Skipped (inline preferred): tightly coupled trigger definition and single upgrade harness |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                   | Answers / unanswered | Resulting decision or selected further research               |
|------------------|---------------------------------------------------------------------------------------------------------|----------------------|---------------------------------------------------------------|
| Intake           | Non-interactive session with exact CI stack trace, named trigger lines, and validation commands supplied | n/a (autonomous)     | Execute focused three-wave cycle in `convergence` mode.       |
| Direction change | Contrarian wave discovered `test_quality_sensors_e2.py:410` updates `dispatched` + `revision` on `'ready'` row | n/a (autonomous)     | Refined trigger fix to `BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision` (SQLite) and `UPDATE(...)` column guard (T-SQL) in addition to removing `dispatched`. |
| Convergence      | All questions Q1-Q4 answered with direct codebase evidence (`C1`-`C7`).                                  | n/a (autonomous)     | Selected column-scoped `UPDATE OF` / `UPDATE(...)` trigger guards removing all `dispatched` references (`Planning Readiness: Ready`). |

## Scope and Success Criteria

* Scope: Eliminating `dispatched` column references from `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` in `src/core/src/zava_forward/core/assistants.py` so `ALTER TABLE assistant_tasks DROP COLUMN dispatched` in `test_quality_sensors_c7.Upgrade.downgrade()` succeeds, while preserving non-review `dispatched`/`revision` updates (`test_quality_sensors_e2.py:410`, `test_permit_sql.py:269`) and every continuity SQL gate and open-hold fence invariant.
* Assumptions (verified):
  * Local branch `feat/platform-122-restart-gate-0228` is clean at commit `573b86b41`.
  * `assistant_tasks.dispatched` is the only column dropped on a trigger-bearing assistant/continuity table across the entire test suite (`C3`).

## Prior Knowledge and Decomposed Questions

* Prior artifacts `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md` and `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c3-changes.md` established `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` on `assistant_tasks` and skipped DML triggers on SQL Server `WITH LEDGER = ON` databases.
* Questions:
  * Q1: Why did `test_quality_sensors_c7.Upgrade.test_actual_c5_tables_are_upgraded_in_place_idempotently_and_keep_their_rows` fail in CI job `132800541482`, and are any other columns dropped on trigger-guarded tables across `src/`?
  * Q2: Would naively removing `AND NEW.dispatched = OLD.dispatched` (and `AND i.dispatched = d.dispatched`) break any existing `UPDATE assistant_tasks` path in `src/core` or `src/api/tests`?
  * Q3: How can SQLite and T-SQL `assistant_tasks` update triggers omit all references to `dispatched`, allow `dispatched`/`revision`-only updates, and still block every pre-gate or suspended `verify` (`ready -> ready` including `SET body = body, revision = revision + 1`), `accept`, and `edit-accept` mutation?
  * Q4: Which existing tests in `test_mssqlstore.py`, `test_continuity_restart_gate.py`, and `test_restart_gate_sql_fences.py` inspect trigger strings or counts, and what focused regression assertion should be added?

## Cycle 1 Execution

### Wave 1: Wider

* Inspected `src/core/src/zava_forward/core/assistants.py`, `src/api/tests/test_quality_sensors_c7.py`, `src/api/tests/test_quality_sensors_e2.py`, `src/api/tests/test_permit_sql.py`, `src/api/tests/test_mssqlstore.py`, `src/api/tests/test_continuity_restart_gate.py`, and `src/core/tests/test_restart_gate_sql_fences.py`, plus repository-wide searches for `dispatched`, `UPDATE assistant_tasks`, `ALTER TABLE`, and `DROP COLUMN`.

### Wave 2: Deeper

* **C1** (`src/core/src/zava_forward/core/assistants.py:1028-1039` and `1068-1077`): `SQLITE_ATTEMPT_TRIGGERS` (`assistant_tasks_gate_update`, `assistant_tasks_hold_update`) and `MSSQL_ATTEMPT_TRIGGERS` (`assistant_tasks_gate_update`) fire on unqualified `BEFORE UPDATE ON assistant_tasks` / `AFTER UPDATE` and check `OR (OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision AND NEW.dispatched = OLD.dispatched)` (and `i.dispatched = d.dispatched` in T-SQL).
* **C2** (`src/api/tests/test_quality_sensors_c7.py:267-269, 279`): `Upgrade.downgrade()` drops `ix_assistant_dispatched` and executes `ALTER TABLE assistant_tasks DROP COLUMN dispatched` to simulate an existing C5 database before `restarted.migrate()` re-adds and backfills `dispatched`. SQLite re-parses and validates every trigger on `assistant_tasks` during `ALTER TABLE ... DROP COLUMN` and raises `sqlite3.OperationalError: error in trigger assistant_tasks_gate_update after drop column: no such column: NEW.dispatched`.
* **C3** (Repository-wide `DROP COLUMN` audit across `src/**`): Across all `src/` packages and tests, `DROP COLUMN` appears only on `cases` (`test_sqlqueues.py`, `test_sqlreads.py`, `test_resident_decisions.py`), `chat_message` (`test_chatthreads.py`), and `assistant_tasks.dispatched` (`test_quality_sensors_c7.py:268`). No test drops `state`, `body`, `capability`, `review_gate_version`, or `reviewed_revision`.
* **C7** (`src/api/tests/test_mssqlstore.py:46-50`, `src/api/tests/test_continuity_restart_gate.py:1291-1300`, `src/core/tests/test_restart_gate_sql_fences.py:664-666`): Existing trigger shape assertions verify trigger names (`assistant_tasks_gate_update`), count (`len(MSSQL_ATTEMPT_TRIGGERS) == 6`), `"THROW 50004"`, and `"NOT EXISTS"` in `MSSQL_ATTEMPT_TRIGGERS[2:]`; none asserts the presence of `dispatched`.

### Wave 3: Contrarian

* **C4** (`src/api/tests/test_quality_sensors_e2.py:366-370, 409-413`): Contrarian audit of every `UPDATE assistant_tasks` in `src/` uncovered `Cursor.test_the_cap_is_unchanged_and_a_long_history_completes_over_scans_and_restarts`, which inserts `'oldzzz'` with `state='ready'`, `revision=1`, `dispatched=1.0`, and default `review_gate_version=''`, `reviewed_revision=0`, and then executes `UPDATE assistant_tasks SET dispatched=?,revision=revision+1 WHERE id='oldzzz'`. **Crucial finding**: naively deleting `AND NEW.dispatched = OLD.dispatched` without scoping the trigger's column list would cause `OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision` to match that `dispatched`-rewrite query and fail `test_quality_sensors_e2.py` in CI with `sqlite3.IntegrityError: continuity SQL gate mismatch`!
* **C5** (`src/core/src/zava_forward/core/assistants.py:3566-3576`, `src/api/tests/test_continuity_restart_gate.py:1213-1215`, `src/api/tests/test_permit_sql.py:269`):
  * Every real review update in `Assistants.review()` (both current and pre-gate images) includes `body` and `state` in `SET` (`UPDATE assistant_tasks SET body=?, state=?, ...`).
  * `test_continuity_restart_gate.py:1214` probes raw pre-gate verify with `UPDATE assistant_tasks SET body=body, revision=revision+1 WHERE id=?` (`NEW.body = OLD.body`, so `NEW.body <> OLD.body` alone would miss `SET body=body`, whereas `body` IS in the `SET` column list!).
  * `test_permit_sql.py:269` locks a task row with `UPDATE assistant_tasks SET revision=revision+1 WHERE id=?` (only `revision` in `SET`).
* **C6** (Column-scoped `UPDATE OF` / `UPDATE(...)` verification):
  * In SQLite, `BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks` (with `AND NEW.dispatched = OLD.dispatched` removed) contains zero references to `dispatched` (so `ALTER TABLE assistant_tasks DROP COLUMN dispatched` succeeds), does NOT fire when only `dispatched` and/or `revision` appear in `SET` (`test_quality_sensors_e2.py:410`, `test_permit_sql.py:269`), and DOES fire on every `UPDATE` whose `SET` list includes `state`, `body` (even `SET body = body`), `capability`, `review_gate_version`, or `reviewed_revision`.
  * In T-SQL (`MSSQL_ATTEMPT_TRIGGERS`), guarding `assistant_tasks_gate_update` with `IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision))` and removing `AND i.dispatched = d.dispatched` provides exact semantic parity on SQL Server (`UPDATE(col)` tests presence of `col` in the `UPDATE ... SET` clause).

## Parent Synthesis and Convergence

* **Accepted recommendation**:
  1. In `src/core/src/zava_forward/core/assistants.py`, change `assistant_tasks_gate_update` and `assistant_tasks_hold_update` in `SQLITE_ATTEMPT_TRIGGERS` to `BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks` and remove `AND NEW.dispatched = OLD.dispatched`.
  2. In `src/core/src/zava_forward/core/assistants.py`, guard `assistant_tasks_gate_update` in `MSSQL_ATTEMPT_TRIGGERS` with `IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision)) BEGIN ... END` and remove both `AND i.dispatched = d.dispatched` clauses.
  3. Add focused regression assertions in `src/core/tests/test_restart_gate_sql_fences.py` confirming that: (a) no trigger in `SQLITE_ATTEMPT_TRIGGERS` or `MSSQL_ATTEMPT_TRIGGERS` references `dispatched`, (b) `ALTER TABLE assistant_tasks DROP COLUMN dispatched` followed by `Assistants.migrate()` succeeds cleanly with active triggers, and (c) `UPDATE assistant_tasks SET dispatched=?, revision=revision+1` on a `'ready'` row is permitted while `SET body=body, revision=revision+1` and `SET state='accepted', revision=revision+1` still fail closed.
  4. Run all requested focused validation suites plus `test_quality_sensors_e2.py` to verify both `c7` schema downgrade/upgrade and `e2` `dispatched` retry updates pass!
* **Rejected alternatives**:
  * Removing `AND NEW.dispatched = OLD.dispatched` without `BEFORE UPDATE OF ...` / `IF (UPDATE(...))`: rejected because `test_quality_sensors_e2.py:410` executes `UPDATE assistant_tasks SET dispatched=?,revision=revision+1 WHERE id='oldzzz'` on a `'ready'` row and would fail in `src-api` CI (`C4`).
  * Replacing `AND NEW.dispatched = OLD.dispatched` with `AND NEW.body <> OLD.body`: rejected because `test_continuity_restart_gate.py:1214` probes pre-gate raw SQL verify using `UPDATE assistant_tasks SET body=body, revision=revision+1 WHERE id=?` where `NEW.body == OLD.body` (`C5`).
  * Dropping and recreating triggers inside `test_quality_sensors_c7.Upgrade.downgrade()`: rejected because schema column operations on non-gate columns (`dispatched`) should remain decoupled from continuity gate triggers in production SQLite migrations as well.
* **Risks and open items**: None within scope; all existing continuity SQL fence invariants and C5/E2 quality sensor upgrade/adoption paths are preserved.
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
