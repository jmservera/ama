---
title: Employee sensor charts demo evidence (issue 2193)
description: Evidence for the dual-axis Home sensors chart and the map card gauges on the synthetic demo
ms.date: 2026-11-21
ms.topic: reference
---

## Scope

Synthetic demo, desktop only (owner decisions 2026-11-18 and 2026-11-21). Refs #2193, #2118, #1288. The change is local and frozen; it is not deployed to `ca-cutover-test-demo-api` because no production change is authorised.

## Evidence

* Chart: Home sensors tab, one SVG with temperature on the left axis and relative humidity on the right axis, each with its own scale. Screenshot: [dual-axis chart](./home-sensors-dual-axis-chart.png) (stale fixture, showing the out of date note and dashed border).
* Gauges: [map card gauges](./map-card-gauges.png), rendered by the shipped `sensorGauges` for fresh, stale and withheld (nothing shown) inputs.
* Local Chromium run of the existing `checks.quality_sensors_browser_check` with axe 4.10.3: 43 checks passed, including "axe no serious/critical" on the retained readings state, with the chart present.
* Probe in the same fixture: solid temperature line with circles, dashed humidity line (`stroke-dasharray` 7px, 4px) with squares, text summary present, table visible, no horizontal overflow at 1440 px, zero running animations with reduced motion.
* Unit tests: `test_home_sensors_tab`, `test_accessibility_baseline`, `test_content_standard`: 70 tests OK.
* Web guidelines (fetched 2026-11-21 from the vercel-labs source) reviewed against the changed files: decorative key lines and scale text are `aria-hidden`, labels tied to meters, no `transition: all`, no outline removal, tabular numerals, no animation.

## Limits

The map card gauges were rendered through the real helper in a page, not through a live Leaflet map click. The live Azure app was not redeployed, so the live cohort of 20 homes was not observed with the new UI.
