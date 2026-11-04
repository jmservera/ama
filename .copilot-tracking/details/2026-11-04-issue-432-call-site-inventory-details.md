---
title: "Details: #432 provider call-site inventory"
ms.date: 2026-11-04
---

* Test file: `src/api/tests/test_ai_call_site_inventory.py` (api tests can see core, agents and api sources).
* Inventory maps file to status: `ledger`, `own-accounting`, `counts-only-sink`.
* Tests: all call sites classified; only the two resident files lack the ledger join; the ledger site still reads usage, completes the ledger entry and carries configuration.
* No runtime, price, budget, cost or knowledge-base change.
