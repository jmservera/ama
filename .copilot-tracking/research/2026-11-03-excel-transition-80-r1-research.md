---
title: Issue 80 round 1 research
description: Delivery status and slice choice for Excel transition export wiring
ms.date: 2026-11-03
---

Research disposition: executed. Planning readiness: Ready.

## Delivered already

* PR #303 (merged): `src/importer` import preview, quarantine with human approval, supersession history, CSV and read-only xlsx export with history, read-only comparison. Ticks C1 and C3.
* `GET /api/cases.csv`, `/api/continuity/export` and progress CSV existed. Issue comments (2026-10 closure audit) record C2 and C4 as unmet.

## Unmet criteria

* C2: every list offers Excel or CSV export. Only cases, progress and continuity had one. Dependency rule: api may not import importer, so api needs its own formula-safe writer in core.
* C4: owners set staged transition thresholds. Owner decision, not code.

## Findings

* `Store.export_csv` wrote raw cells, so a resident or address value starting with `=` would be a live formula in Excel.
* Contractors are denied `/api/cases.csv`; the role inventory test requires every route to be listed and non-staff denied.
* Visits, funding and handoffs have screens; packages and work orders have API lists only.

## Slice choice

Slice 1 (this PR): formula-safe CSV for packages, work orders, handoffs, visits and funding, staff only, plus links on three screens and the cases.csv fix. Later slices: finance and stock queues, governance, resident and chat surfaces, xlsx via API after #144; C4 owner decision. Touches role-gated data egress (security-sensitive); focused tier only, gate not run by the author.
