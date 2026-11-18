# Research: per-device Hub identity, schema version, stable reading ID (Refs #110)

Date: 2026-11-14. Base: fe9a4d8ba. Disposition: executed. Planning Readiness: Ready.

* `live_readings.Generator` already derives `sensor_id` per home (`sensor_identity.sensor_key`), `device_id = "SYN-" + sensor_id`, a `schema_version` (v1 five-minute, v2 one-minute) and `reading_id = LIVE-{sensor}-{slot}Z`; `SensorConsumer` appends on (sensor_id, reading_id) idempotently.
* `device_identity.DeviceIdentity.validate` enforces the identity shape; `api/iot_stream.decode` binds the Hub-authenticated device to the row.
* Gap: no single check that a message's device identity, schema version and reading ID agree with the home; the reading ID rule was inline in the dataclass. API test bindings use non-derived fake sensor IDs, so tightening `iot_stream.Binding` is out of scope.
