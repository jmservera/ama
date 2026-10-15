---
title: Issue 107 R1 agents dispatch plan critique
ms.date: 2026-10-15
---

Critique executed once on the final candidate plan. Verdict: proceed with amendments applied directly.

* Risk: the new `provider` seam could change timeout and slot semantics in the API. Disposition: the slot semaphore and watchdog stay in `Assistants.execute` (they guard the SQL lease); the worker bounds its own slots independently. Applied.
* Risk: `shape_result` duplicated in agents would drift. Disposition: single pure function in core, shared. Applied.
* Risk: claiming the "model calls leave the api" criterion while the API still composes the provider. Disposition: state plainly that the call is made by agents code but still in the API process until #144; do not close #107. Applied.
* Risk: Azure queue adapter would add `azure` dependency to agents. Disposition: rejected; ports only, adapter deferred to #144.
* Conflict with confirmed decisions: none.
