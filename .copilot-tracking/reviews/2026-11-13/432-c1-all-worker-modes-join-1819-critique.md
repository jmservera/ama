---
title: Issue 432 per-call join across all worker modes critique
ms.date: 2026-11-13
---

Critique executed once by `rubber-duck` before code. Verdict: Revise. All findings compatible with confirmed direction, applied directly.

* F1 retry scenario infeasible after provider failure (held settlement blocks the next reservation; a permitted call blocks reclaim, `assistants.py:1377`). Applied: retry is a returned first attempt whose lease expires (`expire`), then reclaim at fence 2 and a returned second call; provider-failure stays a separate mode.
* F2 settlement carries meter id only; root/attempt come from the reservation. Applied: the definition binds the call through its reserved row, asserts no output row immediately after a failed or fenced call, then asserts the later root-level output separately in the retry test.
* F3 independent expected values for every `call_join` caller (chat, legacy included). Applied: expected root, attempt, configuration, prompt computed from independent inputs, not from the observed reservation.
* F4 legacy content-free. Applied: distinct system, input and response canaries.
* F5 exact report baselines. Applied: before/after deltas and exact counts, no `>= 1`.
