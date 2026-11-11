---
title: Inventory-managed staff intake and independent QA 132 extension E2 plan
ms.date: 2026-11-11
---

Refs #132. Test-only. At most two cases in `src/api/tests/test_staff_intake_api.py`.

* [x] Phase 1: add helpers `declare_inventory` (real route, `Unknown` inventory) and `assert_held` (409, inventory reason and `TENURE_HOLD`), importing `TENURE_HOLD` from Core.
* [x] Phase 2: case A, capture then hold then acknowledge then independent QA accept refused, also after restart; record stays `Submitted`; inventory view stays `Unknown`.
* [x] Phase 3: case B, capture then accept then hold then handover refused with state `Accepted`; later capture while held records `Submitted` and its accept is refused.
* [x] Phase 4: focused validation, one critique, one review, freeze commit.

Details: [details](../../details/2026-11-11/inventory-qa-132-e2-details.md). Not touched: application code, permissions, manifests, infrastructure, memory, evidence pack, shared log, issues, PRs.
