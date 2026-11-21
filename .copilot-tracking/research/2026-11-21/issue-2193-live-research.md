---
title: Issue 2193 research - employee sensor charts
ms.date: 2026-11-21
---

## Scope

Issue #2193 (demo, desktop only): Home sensors tab gets a combined temperature and relative humidity line chart with two independent vertical axes, plus a text and table alternative; the map home card shows latest readings, or gauges. Offline, stale and withheld states stay unchanged.

## Findings

* Home sensors tab: `sensorPanel` and `sensorBody` in `src/api/src/zava_forward/api/web/ops.js`. Payload `v.readings` (oldest first, window `v.max_readings.window`) has `observed_at`, `temperature_c`, `humidity_pct`; `v.latest`, `v.age_seconds`, `model.fresh`/`model.alerts` carry freshness. States withheld/offline/unavailable return no readings, so no chart renders there.
* Existing table `sensorTable` already lists the recent readings; a chart needs its own text summary and a "Show this chart as a table" details (pattern in `bars()` in `app.js`).
* SVG helper `svg()` is a global in `app.js`; `ops.js` loads before it, but calls happen at runtime so the helper is reachable.
* Map card: `showHome` in `app.js` fills `sensorValues` from `sensorReading(point.sensor)`; point.sensor has `temperature_c`, `humidity_pct`, `state`.
* Tests: `tests/test_home_sensors_tab.py` runs shipped JS in a Node mini DOM; web guard tests are `test_accessibility_baseline.py`, `test_content_standard.py`.
* Constraint: no push, no production change, so the live app `ca-cutover-test-demo-api` is not redeployed; live proof is limited to what the existing deployment shows.

## Planning readiness

Ready. Research disposition: executed.
