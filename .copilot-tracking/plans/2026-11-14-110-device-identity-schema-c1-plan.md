# Plan c1: review-fix cycle 1 (Refs #110)

Date: 2026-11-14.

* [x] `sensor_consumer._live_shape` calls `live_readings.reading_id_for`.
* [x] `iot_stream.decode` calls `verify_envelope` for live-schema rows, mapping errors to `StreamError`.
* [x] `verify_envelope` requires a string `observed_at`, zero seconds/microseconds and 5-minute grid for v1 (1-minute for v2).
* [x] New `src/api/tests/test_iot_device_dedup.py`: decode plus `SensorConsumer.process` redelivery (`replay=True`, one row per key), tampered redelivery `IDENTITY_CONFLICT`, decode refusals. Update the existing live decode test to a derived sensor ID.
* [x] Focused tier only: affected unit tests, mypy and ruff with /tmp caches in src/core and src/api. Critique: compatible, no divergence.
