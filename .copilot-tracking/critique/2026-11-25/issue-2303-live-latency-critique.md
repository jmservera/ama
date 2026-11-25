---
title: Issue 2303 latency critique (2026-11-25)
ms.date: 2026-11-25
---

Critique executed once on the final candidate plan. Verdict: proceed with amendments, all compatible, applied directly.

* Risk: a cached `ai_eval` snapshot freezes measured latencies. Disposition: accepted; the report is scripted evidence, and the response shape is unchanged.
* Risk: stale result after a golden change. Disposition: key includes golden SHA-256.
* Risk: existing test patching `chat_eval.run_eval` returns stale data. Disposition: key includes function identity.
* Risk: cold request still slow. Disposition: warm thread at start; first request waits on the single flight; residual risk stated in the changes record, not hidden.
* Risk: unbounded growth. Disposition: bounded to 8 keys.
* Scope guard: no response shape change, no Dockerfile change, no Azure change.
