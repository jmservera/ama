# Changes c1: review-fix cycle 1 (Refs #110)

Date: 2026-11-14.

* `src/core/src/zava_forward/core/sensor_consumer.py`: reading ID check uses `reading_id_for`.
* `src/core/src/zava_forward/core/synthetic/device_identity.py`: `verify_envelope` type and grid checks.
* `src/api/src/zava_forward/api/iot_stream.py`: `decode` verifies live-schema envelopes.
* `src/api/tests/test_iot_device_dedup.py` (new), `src/api/tests/test_iot_stream.py` (derived sensor in live test), `src/core/tests/test_iot_device_identity_schema.py` (type and grid cases).
* Validation: new, test_iot_stream, identity and consumer-live tests pass; mypy and ruff clean in src/core and src/api. test_live_simulator and test_diagnostic_log_privacy ran with no new failures. Full gate not run.
