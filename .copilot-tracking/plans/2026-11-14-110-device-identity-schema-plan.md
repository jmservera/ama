# Plan: device identity, schema version, stable reading ID (Refs #110)

Date: 2026-11-14.

* [x] Extract `live_readings.reading_id_for(sensor_id, observed_at)` as the single idempotency-key rule.
* [x] Add `device_identity.verify_envelope(device_id, row)`: device is `SYN-` plus the sensor derived from the home, schema version is a live version, reading ID equals the canonical key.
* [x] Add `src/core/tests/test_iot_device_identity_schema.py`.
* [x] Focused tier: core unittest subset, mypy, ruff check and format with /tmp caches. No importer or api change. Critique: compatible, no divergence.
