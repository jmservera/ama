---
title: Issue 2193 changes, wave 2
ms.date: 2026-11-21
---

## Changes

* `src/api/src/zava_forward/api/web/app.js`: map card gauges placed directly under Latest reading, so the card needs no inner scroll to reach them (taken from unmerged 43c03d6f0f).
* `src/api/tests/test_home_sensors_tab.py`: `MapCardGaugeOrder` test, fails on the old order.
* `docs/reference/research/demo-employee-charts/`: updated note, `live_probe_2193.py`, two probe JSON files, three screenshots. Index row and log entry updated.

Classification: FULL tier (src change); the coordinator runs the gate. Local checks: 71 web tests OK, mypy clean. `rpi-checks.py --all` not run. No push, no Azure change (read-only live observation; no throwaway resources created).

## Criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Dual-axis chart, independent min/max | Proven live | left 6 to 6.8 degC, right 92 to 92.8 %RH; screenshot, probe |
| Text and table alternative | Proven live | `aria-describedby` summary; 12-row Recent readings table |
| Non-colour cues | Proven live | dashed humidity, circles vs squares, key text |
| Reduced motion | Proven live | media query matched, 0 running animations |
| Offline, stale, withheld states unchanged | Unproven live: all 4 homes with data were fresh; tests only | `test_home_sensors_tab` matrix |
| Map card readings or gauges | Proven live (two meters with text labels) | probe, screenshots |
| Gauge reorder in the map card | Unproven live: not deployed (no production change authorised); test only | `MapCardGaugeOrder` |
| Fluent 2 and WCAG baseline | Engineering checks only; person-run AT not needed for demo | baseline tests |
| test_accessibility_baseline, test_content_standard pass | Proven | 71 tests OK |
