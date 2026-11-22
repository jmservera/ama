---
title: Issue 2257 verify-fixed research
ms.date: 2026-11-22
---

Research disposition: executed. Planning Readiness: Ready.

* Main already fixes the client: commit 0234e8e79d (#2261) added `fetchReadRetrying`, used by `api()` for the `/api/map` read.
* Deployed revision `ca-cutover-test-demo-api--0000053` recovers from an aborted first `/api/map` (443 markers, no message) and loaded 443 markers in 8 of 8 fresh sign-ins.
* Gap: the unit test exercises the helper with `/api/law/alerts` only; nothing pins the map path to the retrying read.
* Cause stays inferred (replica scale-in and probe timeouts coincide with the window); no request-level trace exists.
* Full evidence and per-criterion status: [docs/reference/research/issue-2257-verify-live-2026-11-22.md](../../../docs/reference/research/issue-2257-verify-live-2026-11-22.md).
