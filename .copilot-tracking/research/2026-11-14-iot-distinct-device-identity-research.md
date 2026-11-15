# Research: #110 distinct IoT Hub identity, schema version, stable reading ID (2026-11-14)

Task: `iot-distinct-device-identity`. Research disposition: executed. Planning Readiness: Ready.

## Evidence

* `src/core/.../synthetic/sensor_identity.py`: `sensor_key(home)` is a collision-checked hash of the home ID; one sensor per home.
* `src/core/.../synthetic/device_identity.py`: `plan()`/`Manifest.validate()` require `device_id == "SYN-" + sensor_id`, home/sensor consistency and device/home one-to-one; per-device X.509, credentials only as references (ADR 0003 decision 6).
* `src/core/.../synthetic/live_readings.py`: `Reading` carried `device_id`, `schema_version` and a derived `reading_id` (`LIVE-{sensor}-{slot}Z`, a pure function of device and UTC slot, so replay-stable) but nothing validated them at generation or send time.
* `src/core/.../sensor_consumer.py` `_live_shape` already rejects unknown schema versions and a `reading_id` that does not match sensor and slot; `iot_stream.Binding`/`_bindings` already enforce device/home uniqueness at the receiver.
* `src/api/.../live_simulator.py` `send_slot` published readings without validating them and did not refuse duplicate homes.
* `infra/modules/iothub.bicep`: hub provisioning only; device identities are run-owned and created by `device_registry_azure` (no keys in Bicep). Repo-wide scan `test_iot_credential_hygiene` covers keys and connection strings.

## Gap

Producer-side enforcement: no refusal of missing/unsupported `schema_version`, missing/mismatched `reading_id`, forged device ID, or device/reading-ID collisions across a cohort. No cohort-level test of AC "distinct identity with schema version and stable reading ID".

## Decision

Keep the reading ID format (the consumer and SQL key depend on it). Add `Reading.validate`, `require_distinct`, `validate_row`; enforce in `Generator.reading` and `send_slot`.

## Not verified

Live Azure IoT Hub (no cloud run); AC-066 live-platform acceptance stays out of scope.
