# Issue #188 research: ingestion and backfill consistency

* Task: issue-188-ingestion-consistency; Research disposition: executed; Planning Readiness: Ready.
* Existing evidence (src/core):
  * `sensor_consumer.py`: `SensorConsumer.process` admits backfill (`reading-v2`) and live-sim rows into `sensor_reading`; identical row replays (`replay=True`), changed values in an existing slot reject as `IDENTITY_CONFLICT`; `retained_envelopes` returns both schemas per home, ordered by `observed_at`.
  * `synthetic/sensor_consistency.py`: `report`/`weather_report` compare against an independent reference with declared `Tolerance`; they need a reference series and do not read the store.
  * Tests: `test_sensor_consumer_live.py` (replay, mixed series), `test_sensor_handover.py` (statistical seam against a reference).
* Gaps against #188 criteria:
  1. No helper ingests a window and reports accepted, replayed and rejected counts, so window idempotence was only shown per row.
  2. No store-backed continuity check for the combined home series without a reference.
* Boundary: synthetic evidence only; not calibration, physical accuracy or live acceptance. Tolerances are caller-declared, not approved operational tolerances.
