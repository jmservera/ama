---
title: Issue 2257 r3 research
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Revision 0000055 is still the live revision (Healthy). Ten fresh sign-ins at 11:45 to 11:48 UTC: 10 of 10 loaded 443 markers, 0 "Map unavailable", 0 `requestfailed`, every `/api/map` 200. Result: `docs/reference/research/issue-2257-live-r3-2026-11-23/probe-result-114822.json`. With r2 (8 of 8) that is 18 of 18 on the hardened revision.
* The deployed image predates #2300 on `main`, so the retry button added there is not live; its live effect stays unproven.
* Gap: the overlay warning logs only the exception class, so the lock cause is inferred from a briefing 503 tag (r2). `is_write_lock_busy` already exists in core.

## Decision

Add the same cause tag to the overlay warning, with one focused unit test. This is a src change (FULL tier); no `rpi-checks.py --all` here.
