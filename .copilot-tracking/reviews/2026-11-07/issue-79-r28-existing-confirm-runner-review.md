---
title: Issue 79 r28 review
ms.date: 2026-11-07
---

Author-only Review, not independent. Execution: Complete. Outcome: Conformant with residual work.

* RV-001 High (independent, root): existing record, retry and race loser reported durability without a sync. Author-corrected and reproduced RED then GREEN; not independently re-confirmed. The independent finding is preserved.
* RV-002 Medium (independent, all three): runner reported a linked record as a refused `publish_failed`. Author-corrected with a distinct status; not independently re-confirmed.
* RV-003 Medium, residual: repeated retries under a persistent sync failure re-audit the uncertainty each time (honest, noisy).
* RV-004 Medium, residual: child 61f3ebe1 must propagate this root keeping `_private` ownership, `_remove` and `_confirmed`; code now overlaps, so expect a mechanical conflict. Route: coordinator.
* RV-005 Medium, residual: all publication evidence (FULL 799026a3) is historical on this head; a new FULL, independent exact-head review and hosted checks are required. #1258, #1259 and the two earlier Medium edge cases are untouched.
