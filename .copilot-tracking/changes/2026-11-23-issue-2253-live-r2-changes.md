---
title: Issue 2253 live r2 changes
ms.date: 2026-11-23
---

Files: [research note](../../docs/reference/research/issue-2253-live-r2-2026-11-23.md), live probe json and png under `docs/reference/research/issue-2253-live-2026-11-23/`, and these RPI records. No source, Azure or data change. Tier: focused (no `src` change). Tests: `test_epic149_child_ux_contracts` 15 OK.

| Criterion (issue "Expected") | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven | 16.8 px against 16 px, live revision 0000026 |
| No overlap of "Latest stored" and the 45 tick | Proven | 0 text overlaps |
| Circle markers on stored readings | Proven | 8 circles |
| Stored readings not one thick stroke | Proven | 1 touching pair (latest marker) noted |
| Narrow-screen text rule | Unproven | desktop-only demo, out of scope |
