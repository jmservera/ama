---
title: Plan for issue 80 round 1
description: Per-list CSV export wiring for staff lists
ms.date: 2026-11-03
---

## Phases

* [x] Phase 1: `core/list_export.py` safe cell and CSV writer; use it in `Store.export_csv`.
* [x] Phase 2: API routes for five list CSVs, kinds in `projection.STAFF_GET`, contractors denied.
* [x] Phase 3: Download links on visits, funding and handoffs screens.
* [x] Phase 4: tests (core unit, loopback API, role inventory), ruff, mypy, README.

Details: [phase details](../details/2026-11-03-excel-transition-80-r1-details.md).

## Critique (one pass, direct)

Verdict: proceed. Applied: reuse the JSON store calls so rows match; deny contractors on every export (matches cases.csv and the role inventory); no note row so header stays first; no AI path. Rejected: importing importer from api (violates dependency rule).

## Stacked slices

2: finance and stock queues, governance, resident/chat exports. 3: xlsx via API after #144. C4 thresholds: owner decision.
