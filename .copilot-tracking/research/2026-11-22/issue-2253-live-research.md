---
title: Issue 2253 research (resident sensor chart)
ms.date: 2026-11-22
---

Research disposition: executed. Planning readiness: Ready.

* Chart code: `src/api/src/zava_forward/api/resident_demo/web/demo.js` `sensorChart`, styles in `demo.css`.
* Root cause 1: `.sensor-chart text{font:1.25rem ...}` sets the size in SVG user units (viewBox 480 wide) so text scales with the SVG width (about 2x at 1440 px), giving oversized labels.
* Root cause 2: 48 stored readings across the left half of the 414-unit plot sit about 4 units apart; circles r=3 plus a 2-unit line merge into a thick stroke.
* Planned fix: text 12 user units with SVG max-width 40rem; thin circle markers every few readings (always the latest); legend notes thinning.

Live reproduction (ca-resident-demo, 1440x900, synthetic resident, before the fix): `docs/reference/research/issue-2253-resident-chart-2026-11-22/before-live.json` and `before-live.png`. Rendered SVG scale 1.396; text 27.9 px against 16 px body text; 1 text overlap; 48 circles, 46 touching their neighbour.
