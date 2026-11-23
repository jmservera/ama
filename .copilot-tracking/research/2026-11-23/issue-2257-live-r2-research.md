---
title: Issue 2257 live research, pass r2 (revision 0000055)
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

Merged on main: retry (#2261, #2283), sensor-overlay hardening (#2292). Live API 0000055 (created after #2292) runs the hardening: its log shows `map sensor summary unavailable exc=ProgrammingError`. Fresh-session probe 8 of 8 passed; reset recovery proven; briefing 503 carries `cause=sql-write-lock-busy`. Full findings: `docs/reference/research/issue-2257-live-r2-2026-11-23.md`.

Gap: the overlay log line omits the SQLSTATE class, so the lock cause is inferred, not proven. Options: add class logging (src change, FULL tier, owner redeploy needed) or leave as a follow-up.
