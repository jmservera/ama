---
title: Issue 2237 retry critique (one pass)
ms.date: 2026-11-22
---

Verdict: proceed with a docs-only plan.

* A fix without an observed cause would guess; the earlier note shows skipping malformed records would hide due retention items. Rejected, consistent with the prior decision.
* Widening the log-query access is an Azure estate change outside the owner's authorisation. Rejected.
* Incidental 500s on other routes are noted, not fixed here.
