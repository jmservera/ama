---
title: "Review: issue 1840 completed() classification"
ms.date: 2026-11-18
---

Executed once by the implementing worker (not the independent exact-head review the issue requires). Outcome: conformant for the focused scope; no material open findings.

* Behaviour: only `completed()` and its caller changed; `check_step` output is identical because the extracted block is unchanged. Existing Judge tests, including late restoration, active-MUTATED rejection and adverse precedence, pass.
* Residual: `completed()` also requires `before == pending`; a trustworthy mismatch with a non-pending precondition now reports INSUFFICIENT, already a gap in `check_step`.
* Routed work: independent exact-head review, full tier with external receipt, and PR to `test/assistant-old-image-sql-107` by the coordinator.
