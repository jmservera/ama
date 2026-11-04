---
title: Issue 130 nomination overdue queue plan
ms.date: 2026-11-04
---

## Plan

* [x] Add nomination `next_update` to `taskqueues.overdue_tasks` (read-only, named owner or Unknown).
* [x] Test boundaries: past, today, Unknown or invalid date, no owner, closed case, no mutation.
* [x] Run focused tests, ruff, mypy; no gate, full suite or benchmarks.

Details: [details](../details/2026-11-04-nomination-queue-130-details.md). Tier: focused (no security, infrastructure, SQL schema or deployment change).

## Stacked later slices (not started)

1. Reviewer and outcome record after OD-41/OD-42.
2. Dependent re-review links once a dependent decision type exists.
3. Automatic hazard onward routing (needs independent hazard owner decision).
