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
Refs #2253. Focused tier: only a test file changed under `src/api/tests/`; no `src` code change; `rpi-checks.py --all` not run. The web-design-guidelines source was not re-fetched and no web file was edited.

Change: `test_resident_sensor_chart_behaviour_in_node` in `src/api/tests/test_epic149_child_ux_contracts.py` slices the real `sensorChart` out of `demo.js`, runs it under node with a stub DOM and asserts marker spacing, latest-marker retention, "Latest stored" anchor flip, and forecast square count. It skips when node is absent.

Validation: `test_epic149_child_ux_contracts` 16 tests OK; ruff check and format clean; mypy clean in `src/api`. Mutation checks: `markerGap = 0.1` and `roomLeft = true` each make the new test fail; `demo.js` restored (git shows no change).

| Criterion (issue "Expected") | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven live (r5) | 16.8 px against 16 px body; r5 probe, unchanged this round |
| No overlap, "Latest stored" clear of the 45 tick | Proven in source by executed code; unproven live | new node test: label end-anchored left of divider with room, start-anchored right of it near the left edge; live label not drawn (stale data), fix not deployed |
| Circle markers on stored readings | Proven live (r5) | 18 circles |
| Stored readings not one thick stroke | Proven in source by executed code; unproven live | new node test: 289 dense readings thinned, all gaps at least 9 units, latest marker kept; live image lacks `markerGap` |
| Forecast squares still render | Proven in source by executed code; unproven live | new node test: 6 forecast squares; live history stale so no forecast |
| Narrow screens | Not applicable | desktop-only demo |

No live Azure change or new probe was made this round.
