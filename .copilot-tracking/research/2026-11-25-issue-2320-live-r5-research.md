---
title: Issue 2320 live re-check on revision 0000069, research
ms.date: 2026-11-25
---

Disposition: executed (opening). Task: re-prove live on `ca-cutover-test-demo-api` revision 0000069 (created 2026-11-25T14:18:52Z, 100% traffic, only revision, Healthy; deployed main 1154ce605) that `GET /api/briefing` never answers 503 sql-write-lock-busy. Scope: synthetic demo, desktop Chromium via Playwright, read-only Azure, no deployment. Fix code only if it still fails. Tier: focused unless src changes. Prior evidence: [r4 note](../../docs/reference/research/issue-2320-live-r4-2026-11-24.md).

Disposition: executed. Planning Readiness: Ready.

Findings (note: docs/reference/research/issue-2320-live-r5-2026-11-25.md): revision 0000069 still logged `GET /api/briefing status=503 cause=sql-write-lock-busy` at 14:22:04Z and 14:25:39Z (the second matches a client "Failed to fetch" in the first probe attempt); the probe then saw 18 of 18 briefing calls answer 200 but with elapsed times up to 20.42 s (10 of 16 over 3 s). Root cause in `Store.briefing` (`src/core/src/zava_forward/core/store.py`): the cache is keyed on `self.version`, so any write by another client misses it, and the miss path runs `run_text_task` then `self.audit`, which write under the SQL write lock (`sp_getapplock`, 15 s timeout, retries). A lock held by other clients (forecast job, other callers on the shared demo) turns that into a 503. #2358 only fixed the held-denial repeat GET. Tier: FULL applies because src changes.
