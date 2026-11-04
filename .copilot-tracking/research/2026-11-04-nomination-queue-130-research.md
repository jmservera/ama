---
title: Issue 130 nomination queue research
ms.date: 2026-11-04
---

## Delivery check

* Merged: #509 (unverified intake, correction, hazard refusal), #859 (read-only follow-up view), closure audit ticks C1, C6, C7, C12, C13, C15.
* Unmet: C2 (delivery not verified), C3 (reviewer and outcome), C4, C5 (automatic hazard routing), C8-C11, C14.
* Blocked on owner decisions OD-41/OD-42 (reviewer policy, representative authority): reviewer/outcome, dependent-decision graph.
* Prior follow-up rank 1 (unblocked): role-queue visibility of overdue nominations (#76). Evidence: `taskqueues.overdue_tasks` covers hazards, resident update and handoffs only; `nomination_follow_up` computes `next_update_overdue` but no queue shows it.

## Planning readiness

Ready for one slice: surface an overdue nomination `next_update` as a staff overdue task. Disposition: executed (code reading only).
