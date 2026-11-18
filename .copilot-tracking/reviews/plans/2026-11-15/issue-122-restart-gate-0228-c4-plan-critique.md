<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #122 Assistant Tasks Trigger Column Scope Fix (Cycle 4)

## Metadata

* Task ID: issue-122-restart-gate-0228-c4
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c4-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Remediate the single remaining CI failure on PR #1787 (`src-api` job `132800541482`, commit `573b86b41`) in `test_quality_sensors_c7.Upgrade.test_actual_c5_tables_are_upgraded_in_place_idempotently_and_keep_their_rows` (`sqlite3.OperationalError: error in trigger assistant_tasks_gate_update after drop column: no such column: NEW.dispatched`); remove all `dispatched` references from `assistant_tasks_gate_update` and `assistant_tasks_hold_update` across `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` in `src/core/src/zava_forward/core/assistants.py` while preserving every continuity SQL fence invariant and compatibility with `test_quality_sensors_e2.py` (`SET dispatched=?,revision=revision+1` on a `'ready'` row), `test_permit_sql.py` (`SET revision=revision+1`), and `test_continuity_restart_gate.py` (`SET body=body, revision=revision+1`); add focused core regression assertions in `src/core/tests/test_restart_gate_sql_fences.py`; run focused validation (`test_quality_sensors_c7.py`, `test_quality_sensors_e2.py`, `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_mssqlstore.py`, `ruff check`, `ruff format --check`, `mypy` in `src/core` and `src/api`, `tools/rename-zava-tests.py`); and commit cleanly locally on `feat/platform-122-restart-gate-0228` without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c4-research.md, .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c4-plan.md, .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c4-phase-details.md, src/core/src/zava_forward/core/assistants.py, src/core/src/zava_forward/core/continuity.py, src/core/tests/test_restart_gate_sql_fences.py, src/api/tests/test_quality_sensors_c7.py, src/api/tests/test_quality_sensors_e2.py, src/api/tests/test_continuity_restart_gate.py, src/api/tests/test_mssqlstore.py, src/api/tests/test_assistants.py, src/core/pyproject.toml, src/api/pyproject.toml, and .github/workflows/src-ci.yml.
* Decisions, dependencies, and acceptance criteria considered: `FR-01` through `FR-03`, `NFR-01` through `NFR-02`, `AC-01` through `AC-04`, parent task `issue-122-restart-gate-0228-c3` SQL Server ledger guard preservation, `[tool.ruff.format].exclude` preservation on `assistants.py`, strict `mypy` compliance on `test_restart_gate_sql_fences.py`, zero new test methods (`9 + 9 = 18` `#122` test method ceiling), and local commit hygiene without `git push`.
* Assessment boundary: Evaluates SQLite `BEFORE UPDATE OF ...` and T-SQL `IF (UPDATE(...) OR ...) BEGIN ... END` syntax, compile-time column-list firing semantics, bypass resistance across all 39 `UPDATE assistant_tasks` call sites in `src/`, `ALTER TABLE assistant_tasks DROP COLUMN dispatched` schema re-validation, `Assistants.migrate()` signature/transaction/lock behavior in `test_restart_gate_sql_fences.py`, and exact validation commands. Does not execute live SQL Server 2022 container tests (`ZF_TEST_MSSQL=1`), which execute in hosted `Source projects CI`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-01 / AC-01 / P01-T01 / C1, C2, C3, C4, C5, C6 | Covered | `BEFORE UPDATE OF state, body, capability, review_gate_version, reviewed_revision ON assistant_tasks` in `SQLITE_ATTEMPT_TRIGGERS` (`src/core/src/zava_forward/core/assistants.py:1028-1037`) eliminates all SQLite trigger references to `dispatched` so `ALTER TABLE assistant_tasks DROP COLUMN dispatched` in `src/api/tests/test_quality_sensors_c7.py:268` succeeds, skips firing on `SET dispatched=?,revision=revision+1` (`src/api/tests/test_quality_sensors_e2.py:410`) and `SET revision=revision+1` (`src/core/src/zava_forward/core/assistants.py:3040`, `src/api/tests/test_permit_sql.py:269`), and fires on every review transition and pre-gate raw SQL probe including `SET body=body, revision=revision+1` (`src/api/tests/test_continuity_restart_gate.py:1212`). |
| FR-02 / AC-01 / P01-T01 / C1, C6, C7 | Covered | Wrapping the two `IF EXISTS (...) THROW 50004` statements in `assistant_tasks_gate_update` (`src/core/src/zava_forward/core/assistants.py:1068-1076`) inside `IF (UPDATE(state) OR UPDATE(body) OR UPDATE(capability) OR UPDATE(review_gate_version) OR UPDATE(reviewed_revision)) BEGIN ... END` and removing `AND i.dispatched = d.dispatched` preserves valid T-SQL escaping inside `EXEC(N'...')`, works on `NVARCHAR(MAX)` (`body`), preserves `len(MSSQL_ATTEMPT_TRIGGERS) == 6`, `"NOT EXISTS"`, and `"THROW 50004"` assertions (`src/api/tests/test_continuity_restart_gate.py:1294-1297`, `src/core/tests/test_restart_gate_sql_fences.py:664-666`), and stays compatible with `DialectConnection` (`src/api/tests/test_assistants.py:1310`). |
| FR-03 / NFR-01 / AC-03 / P01-T02 / C2, C4, C5, C6, C7 | Covered | Extending `RestartGateSqlFencesTest.test_sql_triggers_reject_old_image_and_suspended_scope_attempts` (`src/core/tests/test_restart_gate_sql_fences.py:486-611`) keeps new test method count at `0`, operates safely on autocommit `conn = sqlite3.connect(self.db_path, isolation_level=None)` without holding write locks across `self.service.migrate()` (zero-arg `Assistants.migrate(self)` at `src/core/src/zava_forward/core/assistants.py:1203`), and confirms `_upgrade(db)` re-adds and backfills `dispatched` (`UPDATE assistant_tasks SET dispatched=COALESCE(...) WHERE attempts>0` at line 1322) even while `CAPABILITY` is suspended. |
| NFR-02 / AC-02 / AC-03 / AC-04 / P02-T01 | Covered | All 10 planned validation commands in `P02-T01` resolve valid module paths, `pyproject.toml` lint/format exclusions (`assistants.py` excluded from `ruff format`, `test_restart_gate_sql_fences.py` formatted and strictly checked by `mypy`), `tools/rename-zava-tests.py`, and privacy-safe local commit creation without `git push`. |

## Verdict

* Verdict: Pass
* Rationale: The plan and phase details accurately diagnose both the `c7` SQLite `DROP COLUMN dispatched` trigger re-validation failure (`C1`, `C2`) and the contrarian `e2` `SET dispatched=?,revision=revision+1` regression trap (`C4`), and resolve both cleanly using compile-time column-scoped trigger guards in SQLite (`BEFORE UPDATE OF ...`) and T-SQL (`IF (UPDATE(...) OR ...) BEGIN ... END`). Every SQL construct, `Assistants.migrate()` API call, SQLite autocommit lock boundary, strict `mypy` constraint, and validation command in `P01-T01`, `P01-T02`, and `P02-T01` is verified directly against the repository codebase with zero actionable defects.

## Findings

* None. All requirements (`FR-01` through `FR-03`, `NFR-01` through `NFR-02`), acceptance criteria (`AC-01` through `AC-04`), and phase tasks (`P01-T01`, `P01-T02`, `P02-T01`) are complete, internally consistent, and executable without revision.

## Strengths and Residual Risk

* Contrarian verification (`C4`, `C5`) prevented a secondary CI failure in `src/api/tests/test_quality_sensors_e2.py:410` (`UPDATE assistant_tasks SET dispatched=?,revision=revision+1 WHERE id='oldzzz'`) while preserving fail-closed rejection on no-op-value column writes (`UPDATE assistant_tasks SET body=body, revision=revision+1` in `src/api/tests/test_continuity_restart_gate.py:1212`), because both SQLite `BEFORE UPDATE OF` and T-SQL `UPDATE(col)` inspect the `SET` column list rather than post-update value inequality.
* All 39 `UPDATE assistant_tasks` statements across `src/` were checked against the narrowed column scope: non-review row-lock and dispatch/backfill updates (`SET revision=revision+1`, `SET dispatched=..., revision=revision+1`, `SET dispatched=COALESCE(...)`, `SET lease_until=?`, `SET fence=fence+1`, `SET attempts=?`) do not fire the review gate/hold triggers, setup-only `SET body=?` mutations with unchanged `revision` on non-`accepted` rows remain permitted as in Cycle 3, and every `verify`, `accept`, and `edit-accept` update path (`SET body=?, state=?, ..., revision=revision+1`) remains fail-closed under gate mismatch or active hold.
* Calling `self.service.migrate()` after `ALTER TABLE assistant_tasks DROP COLUMN dispatched` in `P01-T02` while `CAPABILITY` is suspended simultaneously exercises `_upgrade(db)`'s `UPDATE assistant_tasks SET dispatched=COALESCE(...) WHERE attempts>0` backfill on `'T-READY-1'` (`attempts=1`) under an active continuity hold, proving migration recovery cannot be blocked by open holds.
* Residual risk (explicitly accepted in plan): Live SQL Server 2022 trigger execution (`test_mssqlstore.py` with `ZF_TEST_MSSQL=1`) skips locally without a running SQL Server container and remains verified by the hosted `mssql` job in `Source projects CI` once the outer workflow pushes `feat/platform-122-restart-gate-0228`. Optional execution of `src/api/tests/test_permit_sql.py` alongside `P02-T01` is safe if desired, though `Assistants.permit` row-lock updates are already exercised by `test_quality_sensors_c7.py`, `test_continuity_restart_gate.py`, and `P01-T02`.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Read-only critique did not mutate source files or invoke a live SQL Server 2022 engine; T-SQL `IF (UPDATE(...) OR ...) BEGIN ... END` syntax, quote escaping inside `EXEC(N'...')`, and `DialectConnection` compatibility were verified statically against `src/core/src/zava_forward/core/assistants.py` and `src/api/tests/test_assistants.py`.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning_parent
* Smallest next action: Finalize plan status for `issue-122-restart-gate-0228-c4` and proceed directly to `rpi-implement`.
* User response required: no
