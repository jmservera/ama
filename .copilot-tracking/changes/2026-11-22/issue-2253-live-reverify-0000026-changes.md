---
title: Issue 2253 reverify changes (revision 0000026)
ms.date: 2026-11-22
---

Tier: focused (no src change; FULL not triggered). Changes: third-run section in `docs/reference/research/issue-2253-resident-chart-2026-11-22.md`, evidence files `reverify-live-0000026.json` and `.png`, a log entry. Azure was read only (revision list and show); no resource was created or changed. Refs #2253.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven | 16.8 px against 16 px live on `ca-resident-demo--0000026` |
| No overlap of 'Latest stored' and tick 45 | Proven | 0 text overlaps; reverify-live-0000026.png |
| Circle markers on stored readings per legend | Proven | 8 circles; legend says circles mark some readings |
| Stored readings not one thick stroke | Proven (1 touching pair, latest marker) | reverify-live-0000026.png |
| Narrow-screen rule | Unproven, out of scope | desktop-only demo, not browser-tested |

No defect remains. The issue has no checkboxes to tick.
