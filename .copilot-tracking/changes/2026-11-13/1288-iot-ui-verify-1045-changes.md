# Changes: 1288-iot-ui-verify-1045

Status: complete. Base 3b05143179f83235c5b4e80e70aad99bdc44d83f. Tracking-only write surface; no src/ or docs/ edits. Refs #1288, #109, #110, #111.

## Preserved prior input

* dc1404abb files copied byte-identically (sha256 verified equal to the git blobs):
  * `.copilot-tracking/research/2026-11-13/sensor-ui-readiness-1288-0620-research.md` c35da55e41037620c1cff51b45406fc37c6775e3fa765d6a1b53c6b9deb21312
  * `.copilot-tracking/rpi-sessions/2026-11-13/sensor-ui-readiness-1288-0620-state.json` 04cdfb8978fe66bca75b354009ffeed9f7bda2ad22f3445f719e703a91bc9ed5

## Environment

* /tmp/venv-1288-1045 (python 3.12, `--system-site-packages` for the four Azure/aiohttp SDKs already installed system-wide), pip editable install of src/core, src/agents, src/api with `--no-deps`. First attempt with `--no-build-isolation` failed (no wheel in venv, exit 1); retried with default build isolation (build tooling only), exit 0. Critique-directed deviation recorded.
* Namespace package `__path__` lists the worktree src first, then the main checkout's editable path from system site-packages. Module origins confirmed in the worktree: `zava_forward.core.sensor_view` and `sensor_consumer` resolve to `/home/azureuser/source/ama-demo-wt/child-1288-iot-ui-verify-1045/src/core/src/zava_forward/core/`. Package `__path__` for core, agents, api: worktree path first.
* Environment unset: ZF_DATA, ZF_TEST_MSSQL, ZF_SENSOR_MSSQL. No Docker, MSSQL, browser, cloud or model calls. API modules test_quality_sensors_c7/_e2 use loopback sockets only (local).

## Results (producer exit codes captured directly with `$?`)

* Core, from src/core, `PYTHONPATH=tests`: test_device_identity, test_live_readings, test_sensor_consumer_live. Exit 0, Ran 68 tests, OK, 0 skips (38 + 20 + 10 per-module ok lines).
* API, from src/api, `PYTHONPATH=tests:../core/tests:../agents/tests`: test_quality_sensors, _e1, _e2, _c7, test_live_control, test_live_simulator. Exit 0, Ran 480 tests (sibling-module imports re-run shared test classes, so this exceeds the static count), OK (skipped=169).
* All 169 skips are `needs disposable SQL Server (ZF_TEST_MSSQL=1)`. Skips per module: test_quality_sensors 92, _e1 29, _e2 31, _c7 7 (sum 159; remaining 10 are inherited by classes imported across modules). test_live_control (42) and test_live_simulator (37) had 0 skips and ran entirely.
* SQL-backed Quality sensor paths were NOT exercised and are NOT claimed as passed; a disposable SQL Server run remains outstanding follow-up work.
* Browser rendering of ops.js was not run; this is API and read-model contract verification only.

## Cleanup

* /tmp/venv-1288-1045 and temporary logs removed.
