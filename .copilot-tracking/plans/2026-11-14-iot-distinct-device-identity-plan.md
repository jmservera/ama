# Plan: #110 distinct device identity enforcement (2026-11-14)

* [x] Phase 1: add `Reading.validate`, `require_distinct`, `validate_row` to `live_readings.py` (fixed error codes).
* [x] Phase 2: call validation in `Generator.reading`; refuse duplicate homes and invalid rows in `live_simulator.send_slot`.
* [x] Phase 3: tests: `src/core/tests/test_iot_device_identity_enforcement.py` (cohort of 40 homes, schema version, replay stability, collisions, no credential material) and two `send_slot` tests in the API suite.
* [x] Phase 4: unit tests, mypy, ruff check and format in `src/core` and `src/api`.

Critique: executed once (self-review): no conflicts; reading ID format unchanged for consumer compatibility.
