---
title: Critique issue 2303 r73 plan
ms.date: 2026-11-25
---

Executed once on the final candidate. Verdict: proceed, amendments applied directly.

* A per-call memo is safe. The result depends on the user, the store state and the ordered-distinct case ids, all fixed during one call, and the memo lives in the call frame, so there is no cross-request staleness or authorisation leak.
* Amendment: key on `tuple(dict.fromkeys(case_ids))` to match the function's own de-duplication.
* Risk: three distinct sets still cost about 3 x 1.9 s. Accepted; the aim is a large cut (73 s to roughly 10 s). The live figure can only be measured after a deployment, which this task does not perform.
* Rejected as out of scope: a cross-request cache (staleness against withheld values) and rewriting the 980-case scan.
