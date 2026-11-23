---
title: Issue 2253 live r6 research
ms.date: 2026-11-23
---

Refs #2253. Research disposition: executed. Planning Readiness: Ready.

Findings:

* Live `ca-resident-demo` still serves revision `ca-resident-demo--0000028` (created 2026-11-23T12:31:09Z, 100% traffic), image digest unchanged since r5. The `markerGap` fix is on main but not in that image, so r5 live results stand (see `docs/reference/research/issue-2253-live-2026-11-23/live-r5-0000028.json`). No redeploy is authorised for this goal.
* The issue body has no tick-list; the "Expected" sentences are the criteria. Unproven live in r5: no overlap of "Latest stored", no thick stroke, forecast squares. Owner-only items: none; deploy is a coordinator action.
* Gap a test can close: `test_resident_sensor_chart_text_and_markers_stay_legible` only greps demo.js strings. No test executes `sensorChart` and asserts geometry; the browser check needs a live server and browser.

Decision: add a node-executed regression test of `sensorChart` using dense history (288 readings) and a short history, asserting marker spacing, latest marker at the divider, three forecast squares, and the label flip.
