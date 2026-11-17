---
title: Issue 432 details
ms.date: 2026-11-17
---

## Phase 1 detail

Inventory table columns: area, code symbol, test, state. Rows: per-call ledger join, request call and depth bounds,
limits and alerts, price evidence, billing reconciliation, accepted-outcome report, held-out batch runner,
resident reservation, legacy paths. Unproven: criteria 5 and 8. Smallest next step stated once.

## Phase 2 detail

The test reads the inventory section markers, extracts backticked `module.symbol` references under a fixed
allowlist table in the test, and checks each with `hasattr` or file existence. A second case builds an
in-memory ledger with no price or billing and asserts cost `Unknown` and reconciliation `unreconciled`.
