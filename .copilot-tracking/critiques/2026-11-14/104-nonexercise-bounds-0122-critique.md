---
title: Issue 104 criterion 5 independent critique
ms.date: 2026-11-14
---

Executed once on the final candidate plan; verdict: Proceed with changes, all compatible and applied directly.

* Refusing only at `authorize` leaves legacy billable authorities usable: applied, `reserve_in` also holds `alert-unowned`.
* Changing the alert `route` would break the workbook parse and existing tests: applied, route unchanged.
* Rejecting unrecorded prices at `authorize` is redundant with `price-unknown` and breaks deferred-price tests: applied, check only for recorded non-synthetic prices.
* Schema change must not invalidate stored ledgers: applied via optional-field allow-list.
* No significant or divergent issue needed a user decision.
