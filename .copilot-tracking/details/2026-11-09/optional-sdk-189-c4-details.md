<!-- markdownlint-disable-file -->
# Issue 189 C4 optional streaming SDK import phase details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/optional-sdk-189-c4-plan.md).

## P2 Edit (`src/api/src/zava_forward/api/live_simulator.py`)

* Import `TYPE_CHECKING` from `typing`; replace line 35 with `if TYPE_CHECKING: from .iot_stream import DeviceActivation`; annotate `IotHubSink.__init__(activation: "DeviceActivation")`.
* In `_sink`, after the `stdout` branch, `try: from .iot_stream import DeviceActivation` and `except ModuleNotFoundError: raise StreamError("IOT_SDK_MISSING") from None`. The rest of `_sink` is unchanged.
* The existing `Cannot run: IOT_SDK_MISSING` handler path (`StreamError`, exit 2) reports the absence; no new broad handler.
* `Limits`, `check_capacity`, estimates, guards, duration, auth and control state are untouched.

## P3 Validation (from `src/api` unless stated; owned `mktemp` capture directory with raw cmd, stdout, stderr and exit files)

* Before: `python3 -m unittest test_rpi_checks.GateTests.test_api_install_prevents_scrubbed_server_child_writing_source_bytecode` from `tools/` fails (captured).
* After: same test passes, then the whole `test_rpi_checks` module from `tools/`.
* Add one focused test in `tests/test_live_simulator.py` only for the new explicit missing-SDK mapping (blocked import), plus a check that importing `simulator_admin` with the Azure SDK modules blocked succeeds.
* `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_live_simulator tests.test_simulator_admin tests.test_live_control tests.test_iot_stream -q` in an owned venv having the declared SDK.
* `ruff check`, `ruff format --check` on the affected files and `mypy` (`files` from `pyproject.toml`) with ruff 0.17.1 and mypy 2.4.0 in the owned venv; install only if the selected command proves the profile missing.
* Browser: one controlled synthetic run of the simulator control check only if the control boot needs reconfirmation (the harness contract already boots the server).

## P4 Records

Raw outputs and `hashes.sha256` remain outside the repository; concise records, the tested source hash and the ledger (spent 4, remaining 1) go in the changes, review and handoff.
