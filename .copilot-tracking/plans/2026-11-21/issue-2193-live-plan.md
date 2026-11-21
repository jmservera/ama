---
title: Issue 2193 plan
ms.date: 2026-11-21
---

* [ ] P1 `sensorChart(v, model)` in `ops.js` and call from `sensorBody` before the recent readings table.
* [ ] P2 Chart text summary and "Show this chart as a table" details reusing `sensorTable`.
* [ ] P3 `sensorGauges` in `app.js` map card, below the latest reading text.
* [ ] P4 CSS in `style.css` (chart, dashed and marker cues, meters).
* [ ] P5 Tests in `test_home_sensors_tab.py`; run accessibility baseline and content standard tests; mypy/ruff not needed (JS/CSS only).
* [ ] P6 Browser proof with Playwright on a local app with synthetic data; criteria table in changes record.

Tier: FULL (src change); the coordinator runs gates.
