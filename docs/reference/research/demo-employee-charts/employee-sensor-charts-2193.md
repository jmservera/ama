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

## Live observation 2026-11-21 (wave 2)

Playwright (Chromium, 1440x900, reduced motion, signed in with the demo test account, credentials read at runtime) against `ca-cutover-test-demo-api`; script [live_probe_2193.py](./live_probe_2193.py).

* The cases list returned 50 homes; 4 had at least two readings (ZF-2025-0030, 0031, 0032, 0041), the rest had fewer.
* Chart on ZF-2025-0031: left axis 6 to 6.8 degC, right axis 92 to 92.8 %RH, so the axes have independent scales. 12 readings; temperature solid with circles, humidity dashed (`7px, 4px`) with squares; key text names line style, marker and axis. Probe: [live-chart-probe.json](./live-chart-probe.json); screenshot: [live-home-sensors-chart.png](./live-home-sensors-chart.png).
* Alternatives: `aria-describedby` points at a text summary; a Recent readings table with 12 rows follows the chart.
* Reduced motion: media query matched, 0 running animations, no horizontal overflow.
* Map card (Dawn Brown home, opened from a keyboard-focused marker): latest reading text plus two `meter` gauges, temperature 7.5 degC on 0 to 40 and humidity 92.9 %RH on 0 to 100, each with a text label. Probe: [live-map-card-probe.json](./live-map-card-probe.json); screenshots: [top](./live-map-card-top.png), [gauges](./live-map-card-gauges.png). The card still scrolls (434 of 886 px) because the deployed build predates the reorder.
* Stale, offline and withheld states were not observed live: all four homes with data were fresh (under 15 minutes). They are covered by `test_home_sensors_tab`.
* Local at this head: 71 tests OK (`test_home_sensors_tab`, `test_accessibility_baseline`, `test_content_standard`); `python3 -m mypy` clean.

## Limits

The gauge reorder (gauges directly under Latest reading, new `MapCardGaugeOrder` test) is local and not deployed, because this wave authorises no production change; it is proven by test only. Stale, offline and withheld states are proven by tests only. No person-run assistive-technology test (not needed for the demo).
