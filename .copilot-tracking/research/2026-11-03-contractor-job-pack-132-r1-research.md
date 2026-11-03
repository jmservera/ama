---
title: Issue 132 round 1 research
ms.date: 2026-11-03
---

## Delivered already (disposition: reused)

* Contractor-scoped work order view with no vulnerability reason: `procurement.py` `_wo_view`, `projection.py` allow-lists (needs_notice, named contact).
* Versioned checklists and independent acceptance: `quality.py` (`CHECKLISTS`, `submit_quality`, `_independent`, `accept_quality`). Appointment outcomes: `OUTCOMES`.
* No merged PR names #132 (only audit PRs #613 and #614). An issue comment records the readiness review: a staff-only slice is feasible but the owner has not waived the #116 identity dependency.

## Gaps

* No job pack projection with design version; no worker-confirmation receipt; no offline or no-show recovery rules; no escalation route; no intake decision record.

## Planning readiness: Ready

Smallest coherent slice: pure core rules with tests, no persistence, no API, no contractor writes. Does not touch security, infrastructure, SQL or deployment code (no gate by this slice).
