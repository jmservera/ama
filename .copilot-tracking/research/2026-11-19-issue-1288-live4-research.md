---
title: Issue 1288 live round 4 research (Refs #1288)
ms.date: 2026-11-19
---

Task: issue-1288-live4. Demo only, desktop, FOCUSED tier. Research disposition: reused (rounds 1 to 3, 2026-11-18) plus a live and local delta. Planning Readiness: Ready.

* First unticked criterion is 3 (Quality AI snapshot consumes the identical reading IDs). Source already exists on main (PR 1331, then later work); local tests prove it, see the third note. No code gap found; a live proof needs a model call, which is held (call_allowance 0, no release record).
* Delta to re-check: local focused tests at head 06188c533, active revision, simulator job presence.
