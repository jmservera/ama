---
title: Issue 82 remaining gate family readiness research (2026-11-06)
ms.date: 2026-11-06
---

* Pins: branch feat/remaining-gate-family-readiness-82 at parent-81 integration head d4d33c7ec (tree 096d2a639), origin/main bb3a3b03c (read-only, unchanged), ignored-inclusive clean. Eventual child work targets parent 81, not main. Parent observations are not main acceptance. Earlier adverse records (RV-001 and others) are untouched; the Low sibling-source annotation is deliberately not taken.
* Governing requirement: PRD FR-008 (docs/prds/zava-forward-retrofit-programme-demonstrator.md). BRD FR-008 (material-change invalidation) is distinct; BRD RULE-001/002 inform existing booking rules; BRD FR-026 governs eligibility.
* Delivered (gates.py): safety release (C3 ticked), booking funding/safety/resident/evidence, and quality, each with `GateRule` source/date/version/reviewer (all exercise fixtures, reviewer "Unreviewed exercise rule").
* Controlled transition traced: `Store.advance` (store.py ~600, READY to BOOKED) runs `require_safety_clear`, `require_resident_clear`, `require_booking_gates` (GateResults), then `require_booked_capacity` (procurement.py ~627). The last one is a deterministic predicate but raises bespoke `ValueError`/`PermissionError`; it yields no pass/fail/unknown result and carries no rule provenance. That is the genuine C1/C4 gap.

## Family map

| Family | Existing server predicate | Gap | Readiness |
| --- | --- | --- | --- |
| Capacity | `_evidenced_capacity`, `_existing_capacity`, `_committed_used`; evidence, period, scope/contract version, hash, accepted-by manager, deficit | No GateResult/provenance; raises | Ready: existing approved semantics |
| Authority (contract) | `_contract_authority` (named manager, contract version, supplier, action, scope, validity, revoked) | Same; raises PermissionError, coupled to capacity at booking | Ready as a tightly coupled pair |
| Finance | `_financial_authority` -> `grants.require_authority`; budget/commitment approvals | Thresholds and finance sign-off owned by Finance; not a pre-transition gate here | Blocked on a human rule |
| Eligibility | None in server (store.py only mentions a Grants Officer check as text) | BRD FR-026 requires a Finance-approved versioned rule set; non-social conditions stay unknown until verified | Blocked: no rule, thresholds or approver; smallest decision is Finance naming the rule set and approver |

* Authentication stays separate: actors come from the trusted staff record; no change to identity, roles, authority entries or persistence.
* Planning Readiness: Ready for the capacity (+ coupled authority) increment; eligibility and finance stay visibly unreviewed and blocked.
