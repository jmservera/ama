---
title: Issue 2304 live r67 changes
ms.date: 2026-11-24
---

Changes: documentation and evidence only. Added the research note `docs/reference/research/issue-2304-live-r67-2026-11-24.md`, its probe, JSON outputs and screenshots, and the RPI tracking artifacts. No source change, no deployment, no Azure resource created (nothing to delete). Tier: focused (documentation and evidence).

Live result on revision 0000067: 11 forecast calls, all under 10 s (max 9.37 s, one named 503, ten 200). ForecastStatements tests: 6 OK.

## Per-criterion table

| # | Criterion | Proven / unproven | Basis |
| --- | --- | --- | --- |
| 1 | Profile where the time goes | Unproven live (proven on an equivalent run on 2026-11-23) | SQL public access is disabled, so no live statement trace |
| 2 | Forecast answers within a bound or named state | Proven live on 0000067 | 11 of 11 calls under 10 s |
| 3 | Counting-connection test | Proven | 6 tests OK |
| 4 | Live re-check with elapsed time | Proven on 0000067 | Research note timings |

Issue ticks: already all ticked; none changed.
