---
title: Review for issue 80 round 1
description: One-pass review of the per-list CSV export slice
ms.date: 2026-11-03
---

Review executed once. Outcome: slice conformant to plan; issue stays open.

## Checks

* Same store calls as JSON lists; contractors 403 on all exports; role inventory passes.
* Formula injection neutralised, including the existing cases.csv. No AI provider involved.
* Export is one-way: no import path; test confirms store unchanged.
* Dependency rule holds (api imports core only).

## Unmet acceptance criteria

* C2: partly met. Not exported: finance queue, stock queue, checklists, governance, resident, chat and form surfaces; no xlsx from the API; packages and work orders have no screen link.
* C4: unmet, owner decision (ADR 0001).
* C1 and C3 remain ticked from PR #303.

## Routed findings

* Slice 2 exports for remaining lists; accessibility and browser check of new links; web xlsx after #144; owners' thresholds.
* Security-sensitive (role-gated export): needs independent review and the coordinator gate.
