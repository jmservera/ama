---
title: Issue 130 nomination follow-up view plan
ms.date: 2026-11-03
---

## Plan

* [x] Add `nomination_follow_up` and attach it in `followup_view` (core, computed, not persisted).
* [x] Unit test: ready record, legacy record with missing owner/route, overdue, Unknown due date, no mutation.
* [x] Document in `src/core/README.md`.
* [x] Run focused tests, ruff, mypy; no gate, full suite or benchmarks.

Details: [details](../details/2026-11-03-nomination-follow-up-130-details.md). Tier: focused (no security, infrastructure, SQL or deployment change; the view is computed after load).

## Stacked later slices (not started)

1. Role-queue item for overdue or unacknowledged nominations (#76).
2. Human reviewer and outcome record after OD-41/OD-42 policy.
3. Dependent re-review links once a dependent decision type exists.
