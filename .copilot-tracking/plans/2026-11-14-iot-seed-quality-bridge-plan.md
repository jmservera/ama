---
title: IoT seed to Quality UI bridge plan
task_slug: iot-seed-quality-bridge
date: 2026-11-14
---

## Plan

* Add `src/api/tests/test_iot_seed_to_quality_ui_bridge.py` reusing `test_quality_sensors.Seed` with a fixed clock and `Generator(seed=184)` rows.
* Cases: generator values reach the home card exactly and deterministically; home card latest and readings equal the AI snapshot source and citations; read and snapshot do not mutate readings, cases or tasks and make no provider call or socket connection; consent withheld shows no values; CO2 is not invented and moisture maps to humidity.
* Fully annotated for strict mypy; ruff check and format clean.
* Validation: unittest, ruff, mypy from `src/api`; no `.pyc` tracked; commit locally, no push.

## Critique (single pass)

Scope is test-only, no source change; the CO2 gap is stated, not papered over. Accepted.
