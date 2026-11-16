# Research: issue 1297 rpi-checks skip allowlist and env wiring

Date: 2026-11-16. Base: origin/main 5e0c7f74432ffce73cfeaa672e4e40a605ca6274. Research disposition: executed.

## Findings (evidence: direct test runs and tools/rpi-checks.py reading)

* `check_skips()` allows only reasons in `EXPECTED_SKIP_REASONS`; the sensor MSSQL discovery skip is the only per-test allowance (`SENSOR_MSSQL_DISCOVERY_SKIPS`, project-core).
* `opt-in local Chromium` is further restricted to the single chat-panel test (#1273), so 5 later browser classes (21 tests) skip-fail project-api although the browser group never runs them.
* project-core: `MssqlDraftCases` (22, `ZF_SENSOR_DRAFT_MSSQL=1`) is wired nowhere; `JsonResidentDecisions.test_supersede_binding_changed_during_sql_replay_is_refused` skips "SQL replay only" on the non-SQL variant.
* project-api (68 skips, verified by a run of the 8 modules): MssqlStaffIntakeApi 39 (`ZF_STAFF_INTAKE_MSSQL=1` + `ZF_SQL_SERVER=127.0.0.1`), ReceiverMinimumGrantTests 2 (`ZF_SENSOR_MSSQL=1`), JsonStaffIntakeApi 4 (SQL-store-only contract, not applicable), StaffIntakeBrowser 2 (`ZF_STAFF_INTAKE_BROWSER=1` + `ZF_AXE_PATH`), 5 Chromium classes 21 (`ZF_BROWSER_TESTS=1`).
* infra: `infra` group runs `discover -s infra/tests` with `integration=True` (every skip rejected); `PublicSimulationStartupTests` (4) needs `ZF_API_IMAGE`, which only the image-api group produces.
* Receipt verification (`verify_commands`/`required_checks`) mirrors the Runner command list; both must change together.
* Out of scope gap: `ZF_RESIDENT_MSSQL` classes are tolerated by a global reason and run nowhere (follow-up).

## Approach selected

Bind each discovery skip to an exact (module.Class, reason) pair per group and add required zero-skip executions: SQL group step (staff intake, receiver, draft classes), browser group steps (Chromium classes; staff-intake axe class after the pinned axe download), image-api step (public simulation tests with `ZF_API_IMAGE`). Class-level evidence: each pinned class must have at least one executed ok test. Selection couples the test modules to mssql/browser/image-api.

Planning Readiness: Ready
