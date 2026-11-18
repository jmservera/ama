# Changes: device identity, schema version, stable reading ID (Refs #110)

Date: 2026-11-14.

* `src/core/src/zava_forward/core/synthetic/live_readings.py`: `reading_id_for` helper; `Reading.reading_id` uses it.
* `src/core/src/zava_forward/core/synthetic/device_identity.py`: `verify_envelope` with fixed codes DEVICE_ENVELOPE_MISMATCH, SCHEMA_VERSION_REQUIRED, READING_ID_MISMATCH.
* `src/core/tests/test_iot_device_identity_schema.py`: five tests (distinct identities, schema per cadence, stable redelivery ID, shared or foreign identity, missing schema or unstable ID).
* Validation (focused tier): new tests 5/5; test_live_readings, test_sensor_consumer_live, test_device_identity, test_sensor_stream pass; mypy and ruff clean in src/core. Run with PYTHONPATH pointing at this worktree because the editable installs resolve to another checkout. Full gate not run.
