---
title: Issue 2320 live re-check on revision 0000067, research
ms.date: 2026-11-24
---

Disposition: executed (opening). Task: re-prove live on `ca-cutover-test-demo-api` revision 0000067 (created 2026-11-24T15:34:05Z, 100% traffic, the only revision) after the forecast release-reference fix (#2364, Refs #2304) that briefing, forecast, retention and AI report answer within a stated bound. Scope: synthetic demo, desktop Chromium via Playwright, read-only Azure, no deployment. Prior evidence: [r3 note](../../docs/reference/research/issue-2320-live-r3-2026-11-24.md).

Tier: focused (no src change).

Disposition: executed. Planning Readiness: Ready.

Findings (note: docs/reference/research/issue-2320-live-r4-2026-11-24.md): briefing 5 of 5 200 in 0.28 to 0.90 s; forecast 14 calls all within 8.57 s (13 x 200, one named 503 unavailable at 8.49 s); retention 200 in 2.49 s; AI report 200 in 122.72 s; no sql-write-lock-busy in the last 300 log lines. Criteria 2 and 3 remain unproven.
