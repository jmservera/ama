---
title: Issue 2253 r12 research
---

# Research

Disposition: executed. Planning Readiness: Ready.

Prior notes (r1-r11, docs/reference/research/issue-2253-live-*) re-prove the shipped fix with a mid-range synthetic resident. The browser test `src/api/tests/test_resident_sensor_chart_browser.py` only measures temperature near 6 C.

New angle: the "Latest stored" label sits at a fixed y=26 (`demo.js` sensorChart). Readings near the top of the scale (humidity 95 percent maps to y=17) draw circles and forecast squares through the label. Reproduced in Chromium 1440x900 with the probe `docs/reference/research/issue-2253-live-r12-2026-11-27/probe_label_collision.py`; output in `probe-before.txt` (10 failing cases: dense, short, one, two and day histories, both metrics, value 95; mid and low values are clean).

This breaks the issue's expected result "no overlap" for stored markers and forecast squares against the label. Fix: choose the label's y (top or bottom of the plot) so it clears plotted points in its x span.
