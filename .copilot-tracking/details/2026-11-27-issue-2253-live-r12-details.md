---
title: Issue 2253 r12 plan
---

# Plan

* Phase 1: in `demo.js` sensorChart, compute label x-span and pick y=26 (top) or y=144 (bottom) whichever has no plotted circle or forecast square within the span; prefer top.
* Phase 2: extend `test_resident_sensor_chart_browser.py` with a high-value case on both metrics asserting no marker or square overlaps any text.
* Validation: the browser test, `test_accessibility_baseline.py`, `test_content_standard.py`, mypy in src/api, probe re-run. Tier FULL for src change is named by the brief but the complete gate is run by the coordinator; no rpi-checks --all.

# Critique (single pass)

Verdict: proceed. Findings applied directly: the bottom position must not collide with the x axis ticks (axis text is at left of x=56; label is right of it, y=144 text spans about 134-148, axis line at 150: acceptable); if both collide keep the top. No conflict with confirmed decisions; desktop only.
