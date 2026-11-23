---
title: Issue 2253 live r7 changes
ms.date: 2026-11-23
---

Refs #2253. Tier: src web file changed (`src/api/src/zava_forward/api/resident_demo/web/demo.js`), so the targeted web contract tests ran; the full gate (`rpi-checks.py --all`) was not run per the brief and is left to the coordinator. The web-design-guidelines source was not re-fetched: the change alters no markup, style or copy, only the y arithmetic of SVG marks.

Changes: `sensorChart` gains `yFor(value)`, which clamps plotted y to the 10..150 plot area for stored points, the forecast anchor and forecast squares. `test_resident_sensor_chart_geometry_with_dense_history` now also feeds a 60 C and -30 C reading plus a 99 C forecast and asserts every mark stays within 10..150. Exact values remain in the description and table.

Validation: 64 tests across the epic149, accessibility baseline and content standard modules OK; 303 `test_resident*` tests OK (9 skipped); removing the clamp made the new assertion fail; ruff check, ruff format check and mypy clean. No Azure change.

| Criterion (issue "Expected") | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven live (r5) | 16.8 px against 16 px body, revision 0000028 |
| No overlap, "Latest stored" clear of the 45 tick | Unproven live; proven locally | r6 label-side test; r7 clamp keeps out-of-range marks off the ticks |
| Circle markers on stored readings | Proven live (r5) | 18 circles; local node test |
| Stored readings not one thick stroke | Unproven live; proven locally | r6 spacing test; live needs the new image deployed |
| Forecast squares still render | Unproven live; proven locally | node test asserts 3 squares, in range |
| Narrow screens | Not applicable | desktop-only demo |
