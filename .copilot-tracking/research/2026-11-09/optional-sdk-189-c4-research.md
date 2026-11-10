<!-- markdownlint-disable-file -->
# Issue 189 C4 optional streaming SDK import research (2026-11-09)

Task `optional-sdk-189-c4`; parent `type-applicability-189-c3`. Refs #189 only. Research disposition: executed (read-only; scratch capture outside the repository). Base HEAD `d3810ffe489a6ceb048bfb35a14fca1f504bd1e7`, tree `2d25fcde42d67e23f070e4cf9d49c11341daa7b5`; fetched `origin/main` `1464b4d850a89aaaf835ba8a9ad98d38aeb1fdd6` (selector, tool, rubric and tracking advancement only; no merge needed while hosted CI is pending).

## Actual hosted failure

PR 1313 run 42654739930, job 129290232250, `GateTests.test_api_install_prevents_scrubbed_server_child_writing_source_bytecode` (tools tests: 103 run, 1 error). The real api install step is replayed (`venv --without-pip` plus the no-bytecode pth), so no Azure SDK is present, and the real design-system harness launches `zava_forward.api.server`. Boot fails: `server.py:22` imports `simulator_admin`, `simulator_admin.py:21` imports `live_simulator`, `live_simulator.py:35` imports `iot_stream`, `iot_stream.py:13` imports `azure.eventhub`, giving `ModuleNotFoundError: No module named 'azure'`.

## Local reproduction before any fix

The same test run from `tools/` at the frozen head reproduces the identical chain (exit 1, 1 test, 1 error; capture `/tmp/capture-189-c4-*`, `repro-before.out`). It is the existing contract, not a generic stress.

## Dependency boundary findings

* The #189 admin controls (`simulator_admin`) need only the pure `live_simulator.Limits` and `check_capacity`. Before #189 the server never imported `live_simulator` or `iot_stream`, so the coupling is newly introduced by this workstream.
* `live_simulator` already imports `azure.iot.device` lazily inside `_sdk_client`. Its only SDK-coupled import is `from .iot_stream import DeviceActivation` (line 35): an annotation on `IotHubSink.__init__` and one construction in `_sink` on the `--sink iothub` branch. `DeviceActivation` is a pure frozen dataclass, but `iot_stream` itself imports four SDK modules at module level and is the real streamer/receiver (`HubReceiver`, etc.), so it must keep its hard import.
* `pyproject.toml` lists the SDKs as base dependencies of the distribution, but the maintained contract (and the owner brief) requires the employee API to boot without them; the SDK is only needed when the live publisher is selected.
* `live_simulator.main` has a final `except Exception` returning fixed code `SIM_FAILED` (exit 4); an unhandled lazy `ModuleNotFoundError` there would hide the missing dependency, so it needs a narrow, explicit mapping.
* Tests import `DeviceActivation` from `iot_stream` directly; no test patches `live_simulator.DeviceActivation`.

## Options

1. Move `DeviceActivation` to a new pure module: broader extraction, touches `iot_stream`, tests and docs; rejected as larger than needed.
2. Lazy-import `iot_stream` where the real publisher is selected, keep the annotation under `TYPE_CHECKING`, convert a missing module in `_sink` to the fixed `StreamError("IOT_SDK_MISSING")` (printed by the existing `Cannot run:` handler, exit 2). Smallest, typed, no catch-all, no behaviour change for limits, estimates, guards, duration, auth or control state. Chosen.
3. Install the SDK in the test or CI profile: forbidden (hides the dependency); namespace fixture/check/CI unchanged.

## Scope and cycle

C4 is explicitly authorised by the coordinator: four of five cycles spent after C4, one remains. Source limited to `src/api/src/zava_forward/api/live_simulator.py` and, only if needed, one focused test in `src/api/tests/test_live_simulator.py`. No product UI, auth, activation or cloud change; web-design-guidelines review not applicable (no web file changes).

## Planning Readiness

Ready.
