---
title: Issue 2253 live r6 changes
ms.date: 2026-11-23
---

Refs #2253. Focused tier: only a test file under `src/api/tests/` changed; no `src` file; `rpi-checks.py --all` not run. No web file edited, so web-design-guidelines was not re-fetched.

Changes: `src/api/tests/test_epic149_child_ux_contracts.py` gains `test_resident_sensor_chart_geometry_with_dense_history`, which runs `sensorChart` from `demo.js` in node. Divergence: the test was drafted before this record was persisted. Validation: 16 tests OK; mutation `markerGap = 1` made it fail; ruff check, ruff format check and mypy clean.

Live state: revision `0000028` still serves the old image; no Azure change made.

| Criterion (issue "Expected") | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven live (r5) | 16.8 px against 16 px body, revision 0000028 |
| No overlap, "Latest stored" clear of the 45 tick | Unproven live; proven locally | stale live data draws no label; new test asserts label side and offset |
| Circle markers on stored readings | Proven live (r5) | 18 circles; local test asserts circles exist |
| Stored readings not one thick stroke | Unproven live; proven locally | live 1 touching pair on old image; new test asserts spacing of at least 9 units for 288 readings |
| Forecast squares still render | Unproven live; proven locally | new test asserts 3 squares |
| Narrow screens | Not applicable | desktop-only demo |
