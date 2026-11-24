---
title: Issue 2320 r4 changes
ms.date: 2026-11-24
---

Tier: focused. No src change, no deployment, Azure read-only.

Added: docs/reference/research/issue-2320-live-r4-2026-11-24.md and its probe scripts, JSON outputs and screenshot; README index entry; log entry.

| Criterion | Status |
| --- | --- |
| #2320 1 Profile briefing time | Proven (already ticked) |
| #2320 2 Briefing within 5 s, no 503 on a quiet system | Unproven: 5 of 5 within 0.9 s, but system not quiet and first-GET-after-change untested |
| #2320 3 Test proves read path avoids write lock | Unproven: existing test covers a repeated held GET only; needs src work |
| #2320 4 Live re-check with times | Proven (already ticked) |
| Forecast within 10 s or named state (#2304) | Proven for sample: 14 of 14 within 8.57 s, one named 503 |
| Briefing, retention, AI report | Briefing and retention proven; AI report 200 but 122.72 s |

Open: criteria 2 and 3 stay unticked; follow-ups ranked in state.
