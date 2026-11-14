# Changes: #110 distinct device identity enforcement (2026-11-14)

* `src/core/src/zava_forward/core/synthetic/live_readings.py`: `Reading.validate`, `require_distinct`, `validate_row`; `Generator.reading` validates.
* `src/api/src/zava_forward/api/live_simulator.py`: `send_slot` refuses duplicate homes (`DEVICE_ID_COLLISION`) and validates each wire row before send.
* `src/core/tests/test_iot_device_identity_enforcement.py` (new, 15 tests); `src/api/tests/test_live_simulator.py` (2 tests).

Validation (worktree sources via PYTHONPATH because editable installs point at another checkout): core targeted 95 OK (1 skip) plus new/live reading 41 OK; API live simulator, IoT stream and credential hygiene 96 OK; mypy, `ruff check`, `ruff format --check` clean in `src/core` and `src/api`. Hosted CI and the full gate not run.
