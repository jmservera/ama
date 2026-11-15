---
title: Issue 1238 F3 stale Pending supersede plan
ms.date: 2026-11-14
---

## Plan

* [x] Add `_supersede_stale_pending` called from `_res_service_forward_outcome` on `Acknowledged`, skipping in-flight attempts.
* [x] Update the retry test expectation to `["Superseded", "Acknowledged"]`.
* [x] Add tests: acknowledged retry supersedes (fields and persistence); non-acknowledged retry leaves Pending; in-flight attempt is not superseded.
* [x] Run targeted tests, `ruff check`, `mypy`.

## Critique (single pass)

* Does it weaken the Q6 two-person rule? No: that governs superseding without a later acknowledgement; here a recorded receipt on the same request and key is the evidence. Accepted.
* Late outcome for the superseded attempt is already refused and its receipt logged (existing test). Accepted.
* Verdict: proceed, no conflicts with confirmed decisions.
