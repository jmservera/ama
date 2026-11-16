---
title: Issue 1818 phase details
date: 2026-11-16
task_id: issue-1818
---

## P1

`sensor_map.summaries(db, home_ids, now, mssql=False) -> dict[str, dict]` keys: state, label, temperature_c, humidity_pct, observed_at, age_seconds, alert, calibrated(False), provenance. At most 100 ids, one grouped query, consent via `sensor_view.consent`, any exception yields `unavailable`. Helpers `restricted()`/`not_connected()` for fixed-state summaries. `insights.map_view(..., sensors=None)` attaches `sensor` to each point item only. Tests in `src/core/tests/test_sensor_map.py`.

## P2

Server provider: if user role in quality-evidence roles and assistants.sql, open one transaction, `authorize(db,user,"quality-evidence")` for staff row/scope, filter ids by case_ids/areas scope, call `summaries`. Else every item gets `restricted`. Tests in `src/api/tests/test_map_sensors.py`: role leakage, bounded query count, JSON-only store.

## P3

`MAP_SENSOR_STATES` labels, `sensorBadge(sensor)` text+symbol, home card rows "Sensor status", "Temperature", "Humidity", "Last reading", "Source"; maplist item adds status text; checkbox "Show only homes with stale, offline or alert sensors" (points mode, client-side, announced via live region).

## P4

`showcase_view.sensors` gains `freshness` (state, text), `latest_at`, `provenance`, `calibrated`. `demo.js` renders "Reading status" block: "Stored history, not live", last reading time UK, age text, "Synthetic demo data, not calibrated".

## P5

Run core+api tests, both browser checks, ruff, mypy.
