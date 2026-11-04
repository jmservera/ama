---
title: Plan for issue 80 round 2
description: Finance and stock queue CSV export
ms.date: 2026-11-04
---

## Phases

* [x] Phase 1: server routes `/api/finance.csv` and `/api/asset/stock-queue.csv`, kind mapping to existing `finance_queue` and `stock_queue` projections.
* [x] Phase 2: download links on finance queue and asset board screens.
* [x] Phase 3: tests (registry, row parity, role parity), role inventory, README.

Details: [phase details](../details/2026-11-04-excel-transition-80-r2-details.md).

## Critique (one pass, direct)

Verdict: proceed. Reuse store calls so a 403 from the store stays a 403; no AI; no importer import. Stacked next: checklists, governance, resident and chat; xlsx after #144; C4 owner decision.
