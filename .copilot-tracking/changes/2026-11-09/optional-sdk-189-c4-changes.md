<!-- markdownlint-disable-file -->
# Issue 189 C4 optional streaming SDK import changes (2026-11-09)

Plan: [plan](../../plans/2026-11-09/optional-sdk-189-c4-plan.md). Refs #189 only. Source commit `96963f1aa4fece500156b05105c1e333dff5965e` on prospective record commit `3d3cfce56`.

## Changes

* `src/api/src/zava_forward/api/live_simulator.py`: `DeviceActivation` is imported under `TYPE_CHECKING`; `_sink` imports it lazily on the `iothub` branch and maps a missing module to `StreamError("IOT_SDK_MISSING")` (existing `Cannot run:` path, exit 2). `Limits`, `check_capacity`, estimates, guards, duration, auth and control state are untouched.
* `src/api/tests/test_live_simulator.py`: one focused test that the `iothub` sink reports `IOT_SDK_MISSING` (exit 2) when the streaming SDK is absent.
* No config, dependency, namespace fixture, check, CI, UI or product change; no `Any`, cast or ignore.

## Validation (demo-targeted tier; capture `/tmp/capture-189-c4-agyxLb`, manifest sha256 `853741b54e2669d0822ed16adb6e2fa04abbf17ed0f4dd51cacffa77f3e4408d`)

| Check | Result |
|-------|--------|
| Before: `test_api_install_prevents_scrubbed_server_child_writing_source_bytecode` (from `tools/`) | exit 1, 1 error, `ModuleNotFoundError: azure` via `server -> simulator_admin -> live_simulator -> iot_stream` (`repro-before.out`) |
| After: same test | exit 0, 1 test OK (`contract-after.out`) |
| `python3 -m unittest test_rpi_checks` (tools) | exit 0, 102 tests OK locally; hosted CI runs 103 because current main adds selector cases (not merged here) |
| `test_live_simulator test_simulator_admin test_live_control test_iot_stream test_iot_credential_hygiene test_sensor_consistency` (`PYTHONPATH=tests:../core/tests:../agents/tests`, owned venv with the declared SDK) | exit 0, 189 tests OK (a first run with a wrong path form errored on import of `test_auth`; rerun with the documented form passed) |
| ruff 0.17.1 `check` and `format --check` on the two changed files | exit 0, exit 0 |
| mypy 2.4.0 (API profile, from `src/api`) | exit 0, no issues in 202 source files |

Not run: browser check (the control UI and boot path are unchanged and the boot is proven by the contract test), full gate, global install, SQL, cloud, private data, models. Tested source sha256: `live_simulator.py` `5195ff4a828df67cbf1fadf9bc05aa2b11257c5c6757c38fff6b8fe4854da913`, `test_live_simulator.py` `ccf4cd0644bc8247b66b142a0c369f0434d1d70b571f1372b666f227223c9e78`.

## Cycle ledger

C1, C2, C3, C4 spent (4 of 5); one remains. Hosted CI for the new head remains required.
