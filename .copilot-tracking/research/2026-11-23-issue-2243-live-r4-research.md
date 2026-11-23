---
title: Issue 2243 research r4
ms.date: 2026-11-23
---

Disposition: executed (live probe) plus code read. Planning Readiness: Ready.

* Code: `expires_at()` in `assistant.py` reads `ZF_DEMO_EXPIRES_AT`; `aoai.py` calls it on every path. Fix merged (#2249).
* Live: revision 0000028 at 100%, env expiry 2028-01-01T00:00:00Z, deployment `resident-mini` capacity 10 (10 requests, 10000 tokens per minute). Probe at 16:12 UTC: both free-text questions HTTP 200, labels "AI suggestion, not approved" and "AI-generated"; log lines show model token counts.
* Registry `crcutovertestrzsrg` has public access disabled; a rebuild/roll from this host is not possible without an estate change, which this goal does not authorise.
* Gap: tests cover the topic path past the default expiry but not the free-text path (`answer_question`).
