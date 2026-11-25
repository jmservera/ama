---
title: Issue 2320 live r8 review
ms.date: 2026-11-25
---

Review executed once on the changed scope. Outcome: conformant for the changed scope; open items routed as follow-ups.

* Behaviour: a cached busy answer is per-user key, 10 s, labelled as not recorded; a successful record clears it. Cases changing within the TTL are reflected after it expires; accepted and documented.
* Concurrency: reads and writes of `_briefing_busy` happen under `store.lock`.
* Tests cover first fallback, reuse, expiry and clearing.
* Limits: no live proof (not deployed); lock holder unidentified; the SQL wait still holds `store.lock` for the first miss.
* Human review: tier FULL gate and independent review remain with the coordinator; no approvals are claimed.
