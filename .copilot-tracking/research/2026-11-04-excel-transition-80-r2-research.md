---
title: Issue 80 round 2 research
description: Delivery status and slice choice after PR 1019
ms.date: 2026-11-04
---

Research disposition: reused (round 1 research) plus re-check. Planning readiness: Ready.

## Delivered already

* PR 303: importer library, ticks C1 and C3.
* PR 1019: formula-safe CSV for cases, packages, work orders, handoffs, visits, funding.

## Unmet criteria

* C2: finance queue, stock queue, checklists, governance, resident, chat and form surfaces have no export; no xlsx via API (blocked by the api-may-not-import-importer rule).
* C4: owner decision, not code.

## Slice choice

Slice 2: CSV for the finance queue (finance roles and managers) and stock conflict queue (managers). Both reuse the JSON store calls, so role limits match. Role-gated data egress: security-sensitive, so independent review and coordinator gate are required; the author did not run the gate.
