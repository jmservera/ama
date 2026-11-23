---
title: Issue 2243 review r3
ms.date: 2026-11-23
---

Review executed once on the diff (aoai.py, test, docs). Outcome: conformant for the stated scope.

* `HTTPError` is checked before `URLError` (its parent), so 429 is not shadowed.
* Existing generic path unchanged (browser check and `OSError` test still apply).
* No message text logged.
* Open work routed later: owner raises `resident-mini` capacity; roll a rebuilt image; re-probe the free-text path after the ledger hourly window.
