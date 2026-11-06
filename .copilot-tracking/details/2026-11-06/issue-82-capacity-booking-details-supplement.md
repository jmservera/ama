---
title: Issue 82 capacity-at-booking details supplement (2026-11-06)
ms.date: 2026-11-06
---

Supplements the d688 details file (left byte-identical). Semantics, tests and validation are in `../../plans/2026-11-06/issue-82-capacity-booking-plan-supplement.md`.

* Files: `gates.py` (rule and function), `procurement.py` (`CapacityGateError`, `_evidenced_capacity` sites, `require_booked_capacity`), `test_quality_procurement.py` (shared `Flows`).
* Unknown/Fail mapping is by explicit exception state, never message text. `appointments.py` callers of `_existing_capacity` inherit the subclass unchanged (still ValueError).
* Out of scope: finance, eligibility, other authority actions, persistence of the pass result, API or schema.
