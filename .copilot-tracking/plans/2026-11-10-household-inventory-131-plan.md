---
title: Issue 131 case-local expected-household inventory primitive plan
ms.date: 2026-11-10
task_id: 131-household-inventory-1110
---

## Objective

Add the INITIAL opt-in primitive: a versioned, caller-supplied, append-only expected-household inventory with explicit report-version links bound by a server-derived digest, a pure declared-completeness and currentness view, and refusal-only consumers at the existing `resident_gate` and `scope_record`. Research: [research](../research/2026-11-10-household-inventory-131-research.md). Phase detail: [details](../details/2026-11-10-household-inventory-131-details.md).

## Phases

* [ ] P1 Core action, strict input, constants and privacy tuples in `resident_decisions.py`.
* [ ] P2 Pure `tenure_inventory_view`, `followup_view` integration, gate and scope consumers.
* [ ] P3 Focused Core tests (JSON base, inherited SQLite) and API tests (served route, current registry, canaries).
* [ ] P4 Bounded Core and API README text.
* [ ] P5 Focused validation: targeted tests, ruff, mypy, diff review; Review once.

## Constraints

* Only the existing resident route and `_operation` writer; no new endpoint, schema, UI, role, store, sqlstore, server or projection edit.
* No release path. A fully linked and current inventory never lifts `TENURE_HOLD`.
* Legacy unmanaged cases unchanged. No Legal, roster or approval claim.
* Owner focused-validation override: no blanket full or `--changed` gate; MSSQL not claimed.
* Single critique, single Review; findings become later work, no repair budget.

## Success

New tests pass on JSON and SQLite stores and through the served handler; baseline tests stay green; diff touches only the expected files.
