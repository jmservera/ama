# Details: IoT fleet identity evidence slice (issue 110 r1)

## Phase 1: add tests

* File: `src/api/tests/test_iot_stream.py`, new class `FleetIdentityTests`.
* Test 1: three consented synthetic homes, `replay(..., Replay(fault="burst", end_slot=3))`. Assert three distinct device IDs equal to `SYN-` plus sensor ID, non-empty `schema_version` and `reading_id`, unique (sensor_id, reading_id) keys, identical keys and wire bytes on a second replay.
* Test 2: `decode` accepts each frame under its own binding and raises `IOT_DEVICE_BINDING_MISMATCH` when a reading arrives under another device's identity.

## Validation (focused tier)

* `python -m unittest test_iot_stream test_iot_credential_hygiene` from `src/api` with `PYTHONPATH=../core/tests:../agents/tests:tests`.
* `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-110` on the test file.
