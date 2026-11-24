---
title: Issue 2320 live re-check on revision 0000061, research
ms.date: 2026-11-24
---

Disposition: executed. Planning Readiness: Ready.

Task: prove live on ca-cutover-test-demo-api revision 0000061 the briefing GET without the write lock (#2320), the spent-allowance close and chat call cap (#145, #2245), the AI-hold notice, and the retention and forecast endpoints. Scope: synthetic demo, read-only Azure plus authenticated GETs from Playwright; no deployment, no throwaway resource; sign-in values read at run time, never printed.

Findings (full evidence in [the note](../../docs/reference/research/issue-2320-live-r2-2026-11-24.md)):

* Briefing repeat GET 0.08 to 0.16 s in 12 of 12 calls, no 503 (baseline 11 to 14 s).
* Forecast 503 after 13 to 17 s twice; write-lock-busy 503 on a chat thread create; other demo traffic present.
* Chat cap hold seen live (`call-budget-limit`); allowance-close after restore needs a restore drill, not authorised.
* #145 backup criterion remains production-only (Local redundancy, 14 days).

No src change is needed to record this; tier is the focused tier.
