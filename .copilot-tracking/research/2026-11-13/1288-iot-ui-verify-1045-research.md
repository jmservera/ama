# Research: #1288 IoT to Quality UI connected local verification (1288-iot-ui-verify-1045)

* Base: 3b05143179f83235c5b4e80e70aad99bdc44d83f (stacked on docs/demo-wave-integration-parent-1045). Research disposition: executed (bounded). Planning Readiness: Ready.
* Refs #1288, #109, #110, #111.

## Evidence read

* Case study original and addendum, knowledge-base index and memory: read per the brief's start-of-Research rule (framing only; no regulatory claim is made here).
* Prior input dc1404abb (read-only worktree demo-sensor-ui-readiness-0620): two tracking files, research and state, 66 lines, zero tests run, no independent Review.
* Root ledger lines 1-80 read: dc1404abb missed the ledger path; ledger records the per-task discipline (prospective critique before install/test, true producer exit codes).
* Source scope: `src/core/src/zava_forward/core/sensor_view.py` (475 lines, bounded read model), `sensor_consumer.py` (1204 lines), `src/api/src/zava_forward/api/web/ops.js` (SENSOR_ROLES, sensorTable, sensorPanel, sensorDraftSection).
* Test scope and `def test` counts (static): core test_device_identity 38, test_live_readings 20, test_sensor_consumer_live 10; api test_quality_sensors 92, _c7 14, _e1 17, _e2 15, test_live_control 42, test_live_simulator 37.
* Files with MSSQL or skip markers: test_sensor_consumer_live, test_quality_sensors, _c7, _e1, _e2. Skips must be reported as skips, not passes.

## Constraints

* Focused tier, local only, no Docker/MSSQL/browser/cloud, pip only, no PYTHONPATH=mvp, env -u ZF_DATA, no src/ or docs/ edits, tracking-only write surface.

## Findings and risks

* Browser-based UI rendering is not covered by these unit suites; this verifies API and read-model contract only.
* Venv must be isolated at /tmp/venv-1288-1045 and removed afterwards; import paths verified inside this worktree.
