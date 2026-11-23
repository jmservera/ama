---
title: Issue 2253 live r4 research
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready. The owner requires a code change and regression test.

Evidence: [live baseline json](../../docs/reference/research/issue-2253-live-2026-11-23/live-r4-before.json) and [png](../../docs/reference/research/issue-2253-live-2026-11-23/live-r4-before.png) from revision 0000027 (Healthy): ticks 16.8 px vs 16 px body, 0 overlaps, 18 circles, 1 touching marker pair.

Residual defects in `src/api/src/zava_forward/api/resident_demo/web/demo.js` `sensorChart`:

* The latest reading is always drawn, even when closer than `markerGap` to the previous marker, giving a touching pair.
* The "Latest stored" label is end-anchored at the divider, so with a short history it can run left over the 45 tick label (x up to 50).
