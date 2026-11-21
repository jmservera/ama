---
title: Issue 2193 changes
ms.date: 2026-11-21
---

## Changes

* `src/api/src/zava_forward/api/web/ops.js`: `sensorChart` dual-axis SVG line chart in Home sensors with text summary, key and out-of-date note.
* `src/api/src/zava_forward/api/web/app.js`: `sensorGauges` meters in the map home card.
* `src/api/src/zava_forward/api/web/style.css`: chart and gauge styles.
* `src/api/tests/test_home_sensors_tab.py`: `createElementNS` shim, heading expectation, new chart and state test.
* Evidence: `docs/reference/research/demo-employee-charts/employee-sensor-charts-2193.md` and two screenshots.

Classification: FULL tier (src change); the coordinator runs the gate. `rpi-checks.py --all` not run.

## Criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Dual-axis chart (independent min/max) | Proven locally | screenshot, probe |
| Text and table alternative | Proven locally | summary text, existing Recent readings table, tests |
| Non-colour cues | Proven locally | dashed line, markers, key text |
| Reduced motion | Proven locally | no animation, 0 running animations |
| Offline, stale, withheld unchanged | Proven locally | test matrix; stale shows note; no chart for withheld/offline |
| Map card readings or gauges | Proven for helper; not via live map click | gauges screenshot |
| Fluent 2 and WCAG baseline | Engineering checks only (axe, baseline tests); no person-run AT test (not needed for demo) | check output |
| test_accessibility_baseline and test_content_standard pass | Proven | 70 tests OK |
| Seen on live app ca-cutover-test-demo-api | Unproven: not deployed (no production change authorised) | n/a |
