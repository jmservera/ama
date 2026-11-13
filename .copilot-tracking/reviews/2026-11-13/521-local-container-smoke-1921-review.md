---
title: Issue 521 local container smoke review
ms.date: 2026-11-13
---

Independent code-review, executed once. Outcome: Conformant with limits.

* Finding: plan checkboxes P1 to P5 stale. Resolved by ticking them.
* Image digests and timings were not independently re-run by the reviewer; the redeploy itself, hosted CI and Azure behaviour remain unobserved (see changes file Limits).
* Routed work: after PR #1542 merges, re-run the smoke on the new main before the redeploy if the source changed.
