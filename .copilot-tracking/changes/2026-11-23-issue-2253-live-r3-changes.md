---
title: Issue 2253 live r3 changes
ms.date: 2026-11-23
---

Files: [research note](../../docs/reference/research/issue-2253-live-r3-2026-11-23.md), live probe json and png under `docs/reference/research/issue-2253-live-2026-11-23/` (`live-r3-0000027.*`), README index row, log entry, and these RPI records. No source, Azure or data change. Tier: focused (no `src` change); no tests run. Refs #2253.

| Criterion (issue "Expected") | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven | 16.8 px against 16 px, live revision 0000027 |
| No overlap of "Latest stored" and the 45 tick | Proven | 0 text overlaps; label not drawn on current data |
| Circle markers on stored readings | Proven | 18 circles |
| Stored readings not one thick stroke | Proven | 1 touching pair at the right edge noted |
| Legend "Solid line with circles" and forecast squares | Unproven here | outside the probed element; r1 capture covers them |
| Narrow-screen text rule | Unproven | desktop-only demo, out of scope |
