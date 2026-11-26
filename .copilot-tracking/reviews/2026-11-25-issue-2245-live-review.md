---
title: Review for issue 2245 (2026-11-25 live run)
ms.date: 2026-11-26
---

Review executed once on the changed scope. Outcome: conformant for the changed scope.

* Source change is limited to outcome mapping and two reply strings; the reason stays in the receipt and logs. Budget-limit wording is unchanged; guard denial and token failure keep the unavailable wording.
* Existing tests that expected `provider-unavailable` for ledger holds were updated deliberately; targeted agents, api and core chat tests pass.
* The research note states no live proof of the new wording (not deployed) and no proof of why the reservation went unsettled; the table does not overstate either.
* Routed follow-ups: (1) settle or expire stale reservations so one slow SQL write cannot poison a day's budget; (2) identify the SQL lock holder; (3) deploy and re-probe the wording.
* Human approvals and hosted CI remain required; none claimed.
