# Research: issue 1818 live walkthrough (2026-11-19)

Opening note. Unmet criterion: 5 (live Azure IoT Hub -> SQL -> UI map walkthrough). Criteria 1-4 are ticked.

## Findings

* Only criterion 5 is unticked. Existing notes ([2026-11-18 walkthrough](../../../../docs/reference/research/issue-1818-live-iot-map-walkthrough-evidence-2026-11-18.md), [2026-11-19 re-observation](../../../docs/reference/research/issue-1818-live-20261119-2026-11-19.md)) already prove it for the demo.
* The 2026-11-19 note says the receiver register fix is "not on main". That is stale: `git log -S"INSERT INTO sensor_register"` on `src/core/.../sensor_consumer.py` returns `e91b6fa81` (#2105, on this branch's base) and `infra/README.md:4318` lists `dbo.sensor_register`.
* No code gap remains. The only code route would be SQL/receiver grants, which is FULL tier and out of scope for a worker.
* Planning readiness: Ready (evidence-only change).
