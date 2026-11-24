---
title: Issue 2304 live r64 changes
ms.date: 2026-11-24
---

No `src/` change; focused tier (live proof and documentation only). Files: research note `docs/reference/research/issue-2304-live-r64-2026-11-24.md`, probe and outputs in `docs/reference/research/issue-2304-live-r64-2026-11-24/`, index and log entries.

## Per-criterion table

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Profile where the time goes | Proven on an equivalent run; live trace unproven (SQL private) | `issue-2304-forecast-live-2026-11-23.md` |
| 2 | Forecast within bound or named state, never a silent hang | Proven live, caveat: one 27.11 s 200 under load, 10 of 11 calls within 10 s | research note, runs 1 to 3 |
| 3 | Counting-connection test | Proven, 5 `ForecastStatements` tests OK | local run 2026-11-24 |
| 4 | Live re-check with elapsed time | Proven on revision 0000064 | research note |

Briefing 200 (0.07 to 0.44 s), AI report 200 (67.96 s), retention 200 (2.43 to 3.23 s; one named busy 503 at 19.16 s under load).

Issue action: tick all four and close with a comment (see review).
