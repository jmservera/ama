---
title: Issue 2320 live re-check on revision 0000064, research
ms.date: 2026-11-24
---

Disposition: executed (opening). Task: re-prove live that `GET /api/assistants/forecast` answers within 10 s or a named state (#2304), plus briefing, AI report and retention, on `ca-cutover-test-demo-api` (main b05eea4f7). Scope: synthetic demo, read-only Azure, authenticated GETs from Playwright, no deployment. Prior evidence: [r2 note](../../docs/reference/research/issue-2320-live-r2-2026-11-24.md).

Disposition: executed. Planning Readiness: Ready.

Findings (note to be written at docs/reference/research/issue-2320-live-r3-2026-11-24.md):

* Live app: revision 0000064 (image digest 257cd08d...) was created 13:48:50Z with 0% traffic; 0000065 (same digest, created 13:51:02Z) took 100% traffic and became Healthy at about 13:53. The brief named 0000064; the image under test is identical.
* Forecast: 13 live GETs on a signed-in session. 12 answered 200 in 3.5 to 8.6 s (last-good answers carry `stale_seconds`); one took 33.77 s (200). Early 503s at 13:51:43 to 13:52:10 came from other clients during start-up.
* Briefing: 5 of 5 GET 200 in 0.43 to 0.85 s, template, hold reason in body.
* Retention: 200 in 2.25 s from this session; another client got 503 sql-write-lock-busy at 13:57:46Z.
* AI report: 200 but 135.17 s.
* Container log: `/healthz` client-disconnect errors and an `/api/account/photo` 503 around the 33.77 s outlier show the process was saturated.

Tier: focused (no src change).
