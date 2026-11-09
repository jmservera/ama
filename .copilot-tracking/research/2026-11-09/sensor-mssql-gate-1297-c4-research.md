<!-- markdownlint-disable-file -->
# Research: #1297 correction C4 (indoor_projection.py exercised sensor fixture dependency)

* Task ID: issue-1297-c4; slug sensor-mssql-gate-1297-c4
* Date: 2026-11-09
* Start state verified: HEAD 08e13f6e6bafe74a22a65f47151d5c762d6638ef, tree d733df6418bf421d234562bc6ac76accae7e0940, base fa7ae0c9770e890f82482456bfcb8e97f1e05429; `git status --short --ignored` shows only the retained ignored tools/__pycache__/.
* Output mode: convergence. Posture: focused (named defect, named files, supplied failure evidence). Research disposition: executed (inline waves; no subagent needed).
* Extensions: repository instructions (branch, commit, evidence) apply; no domain skill or specialist needed.

## Brief

The coordinator's pre-gate assessment of C3: `changed_groups` omits `mssql` for src/core/src/zava_forward/core/synthetic/indoor_projection.py, so a focused run that changes it can accept the eight sensor MSSQL discovery skips without running the SQL suite. Address this with the smallest fail-closed change and a regression, investigate other actually-exercised first-party dependencies, make no exhaustive-closure claim, and do not require SQL for all core changes.

## Wider wave

* C1: sensor_consumer_fixture.observations() calls sensor_backfill.sensor_for and sensor_backfill.readings, then sensor_faults (src/core/tests/sensor_consumer_fixture.py:38-47).
* C2: sensor_backfill.readings with composed=False calls `_indoor`, which calls indoor_projection.project (src/core/src/zava_forward/core/synthetic/sensor_backfill.py:99-100, 103-122); sensor_for uses DWELLINGS and AGE_BANDS from indoor_projection (same file, lines 46-47, 69-73).
* C3: both suite callers use `observations()` with no fault and no composed flag (test_sensor_analysis_*.py, the only call sites found).
* C4: indoor_projection.py has no keyword (store, schema, sql, assistants, sensor) in its path and is not in SENSOR_MSSQL_DIRECT_DEPENDENCIES, so it selects project-core only.

## Deeper wave: executed-function evidence

Method: a throwaway script in /tmp (/tmp/trace1297.py and /tmp/trace1297b.py, PYTHONDONTWRITEBYTECODE=1, worktree src paths first on sys.path, no SQL) used sys.setprofile to record first-party functions called during `sensor_consumer_fixture.observations()` after import.

* Functions called during observations(): indoor_projection (`_bounded_noise`, `_number`, `_project`, `project`, `saturation_pressure`), sensor_backfill (`_indoor`, `readings`, `sensor_for`, `sensor_id`), sensor_faults (`choose`, `configure`, `observation`, `packets`), and the fixture itself.
* Of these, only indoor_projection.py lacks a selecting keyword. sensor_backfill.py and sensor_faults.py contain "sensor" and already select mssql.
* household_conditions, retrofit_effects, sensor_stock, stock_fabric, scale_fixture, provenance and sensor_identity are imported by sensor_backfill but not called during observations() (composed=False); at import time only module and class bodies run. They are not exercised by this path and are not added.
* Import-time (not call-time) loading also pulls dataset.py, store.py, sqlstore.py, workflows.py and mixins through `import dataset`; C3 covers dataset.py and the exact dependency set only. Evidence boundary: the trace covers observations() with no fault, no composed flag; store_at/SqlStore/MssqlStore and the test bodies were not traced because they need SQL or the suite harness. No exhaustive claim is made.

## Contrarian wave

* Adding indoor_projection.py only: minimal, exercised, no cost to unrelated core changes. Counter-risk: other test-body code paths (for example sensor_analysis.py, selected by keyword) are already covered; non-keyword modules reached only from SQL-gated test bodies were not traced and remain a residual.
* Selecting by sensor_backfill's import list (adds household_conditions, retrofit_effects, scale_fixture and more) is import-based, not execution-based; rejected as over-broad without exercised evidence.
* Selecting mssql for all project-core changes is a cost/coverage policy decision and is not made here.
* Making this derived by a runtime trace in the gate was rejected: heavy, brittle and out of scope.

## Parent synthesis

* Decision: add src/core/src/zava_forward/core/synthetic/indoor_projection.py to SENSOR_MSSQL_DIRECT_DEPENDENCIES and extend the C3 regression with an exercised-dependency assertion (a static check that sensor_backfill calls indoor_projection and that the path selects mssql), plus an unrelated-path negative (household_conditions.py is imported but not exercised, so it stays unselected; recorded as an explicit boundary, not a claim of safety).
* The existing C3 AST test requires the keyword-missed set of resolved direct imports to equal the constant; the constant now also holds a non-direct (exercised) path, so that equality must become "direct keyword-missed set is a subset of the constant, and the remaining entries are the documented exercised dependency".
* Planning Readiness: Ready. No owner decision needed. Residual for owner: broader cost/coverage policy (closure-wide or project-core-wide mssql) remains open.
