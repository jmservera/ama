---
title: IoT seed to Quality UI bridge research
task_slug: iot-seed-quality-bridge
date: 2026-11-14
refs: "#165, #1288"
---

## Scope

Prove seeded synthetic home telemetry flows deterministically into the Quality UI home card and the AI quality-evidence snapshot, without mutating working records and without live Azure IoT Hub.

## Evidence

* Issue #165 (synthetic data epic): the live simulator and backfill are tied to the shared home stock; the read model lives under #1288.
* `src/core/.../synthetic/live_readings.py`: `Generator(seed).reading(home, moment).row()` is a pure seeded function of (seed, home, slot). Channels are temperature_c, humidity_pct and sunlight_wm2 only.
* `src/core/.../sensor_view.py`: `view` (employee home card, `GET /api/cases/{id}/sensors`, rendered by `web/ops.js` `sensorPanel`) and `capture_source` (AI snapshot source) share one capture. `UNITS` holds temperature_c and humidity_pct only; the module forbids inventing variables.
* `src/core/.../assistants.py`: `Service.sensors` and `Service.snapshot("quality-evidence", ...)` consume it. Consent per home gates values.
* Existing seed harness: `src/api/tests/test_quality_sensors.py` (`Seed`), local mock provider, no network.

## Findings

* No CO2 channel exists anywhere in the generator or read model. Moisture is represented by relative humidity (`humidity_pct`, `%RH`). The contract test therefore asserts moisture=humidity_pct, temperature=temperature_c, and that CO2 is absent and not invented, rather than fabricating a CO2 feed.
* No Azure dependency is needed: rows are inserted directly in the retained `sensor_reading` contract shape.

Planning readiness: Ready.
