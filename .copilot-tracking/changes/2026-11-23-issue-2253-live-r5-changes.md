---
title: Issue 2253 live r5 changes
ms.date: 2026-11-23
---

Refs #2253. Focused tier: no `src` file changed; `rpi-checks.py --all` not run. The web-design-guidelines source was not re-fetched; no web file was edited.

Changes: new live probe and evidence under `docs/reference/research/issue-2253-live-2026-11-23/` (probe_r5.py, live-r5-0000028.json and png) plus these RPI records. The fix itself is already on main (#2258, #2305) and is not in the live image.

Validation: `resident_sensors_browser_check.py` 0 FAIL; `test_epic149_child_ux_contracts` 15 OK. Live probe on revision 0000028 as in the research record.

| Criterion (issue "Expected") | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven live | 16.8 px rendered against 16 px body |
| No overlap of labels, "Latest stored" clear of the 45 tick | Axis labels proven live (0 overlaps); "Latest stored" unproven live | live data is stale, label not drawn; code guard and test pass locally; fix not deployed |
| Circle markers on stored readings | Proven live | 18 circles |
| Stored readings not one thick stroke | Unproven live | 1 touching pair live; the replacement fix is not deployed (no `markerGap` in served demo.js); local check passes |
| Forecast squares still render | Unproven live | no forecast for stale history; local check PASS (6 forecast rows) |
| Narrow screens | Not applicable | desktop-only demo |
