---
title: Issue 2237 retry research
description: Retry of the /api/retention 500 investigation from main 6a03928ccb
ms.date: 2026-11-22
---

Research disposition: executed. Planning Readiness: Ready.

* Prior note: [issue-2237-retention-500-live-2026-11-22.md](../../docs/reference/research/issue-2237-retention-500-live-2026-11-22.md).
* Retry evidence is recorded in that note under "Retry 2026-11-22T21" (probe result `retry-2026-11-22T21.json`).
* Live GET /api/retention on revision 0000053: 200 in 56 of 56 calls. Console log tail (300 lines) holds 18 `http-error` lines, none for /api/retention.
* Log Analytics query still refused from this host.
* Follow-ups seen incidentally (different issues): POST /api/chat/threads 500 `ProgrammingError` at 19:44 UTC; GET /api/ai/report 500 `FileNotFoundError` at 20:33 UTC.
