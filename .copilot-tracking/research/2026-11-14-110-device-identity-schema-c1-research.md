# Research c1: independent review findings (Refs #110)

Date: 2026-11-14. Disposition: executed. Planning Readiness: Ready.

* Review `independent-direct-110-device-24ebcaeb7.md`: `verify_envelope` had no production caller; `SensorConsumer._live_shape` hardcoded the reading ID format; no end-to-end dedup proof; `observed_at` grid not enforced.
* `iot_stream.decode` is the production decode path for Hub messages and already holds the authenticated `device_id`. Seeded packet rows use other schema versions and non-derived sensor IDs, so verification applies only to `LIVE_VERSIONS` rows.
* Editable installs resolve to another checkout; tests run with PYTHONPATH on this worktree.
