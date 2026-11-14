# Review: device identity, schema version, stable reading ID (Refs #110)

Date: 2026-11-14. Execution: executed once. Outcome: conformant for the focused tier.

* AC "distinct IoT Hub identity with schema version and stable reading ID": generator output verifies per home; shared gateway, foreign device, absent schema and non-canonical reading ID are rejected; redelivery yields an identical reading ID and body, which the existing consumer appends idempotently.
* No secrets or transport change. Behaviour of existing readings is unchanged (same ID string).
* Open item for later: `api/iot_stream.Binding.validate` does not yet require `sensor_id == sensor_key(home_id)`; deferred because existing tests use non-derived fixtures. Hosted CI and independent review remain pending.
