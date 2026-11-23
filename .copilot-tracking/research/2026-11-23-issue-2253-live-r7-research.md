---
title: Issue 2253 live r7 research
ms.date: 2026-11-23
---

Refs #2253. Research disposition: executed (read r6 research, changes and review first). Planning Readiness: Ready.

Findings so far:

* r6 added a node-executed geometry test for temperature with in-range data only. Its covered cases are dense history and a short history.
* Gap: `sensorChart` in `demo.js` maps values to `y = 150 - (v - min) / (max - min) * 140` with no clamp. A stored or forecast value outside the fixed axis (temperature -10 to 45 C, humidity 0 to 100 %) draws outside the 10..150 plot, over the tick labels or off the 180-unit viewBox. The core sensor policy allows flagged out-of-range readings, so this is reachable.
* Owner-only items: none. Live re-proof needs a deploy and is not part of this angle.
