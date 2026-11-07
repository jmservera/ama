# Issue 82 capacity-at-booking correction details supplement

Date: 2026-11-06 (UTC). Refs #82.

## Discriminators

* Unknown (None): no active order, or an order not in APPOINTED state (evidence of a booked order is absent). Refuses.
* Fail and Unknown from `_evidenced_capacity` are unchanged from r1.
* Structured rethrow at the commitment check happens only when the capacity handler produced the sole missing item (`len(missing) == 1`), using the typed error, never its message.

## Selectors

* `test_quality_procurement.JsonFlows` and `SqlFlows` `-k booking_` and `-k single_order`; `MssqlProcurement` inherits them and is executed only in the later FULL run.
* Controls: `test_gates`, `test_consultation_controls`, full `test_quality_procurement` Json/Sql/HandoverBlockers.

## Out of scope

API or persistence of Pass, other families, named review, activation of the rule.
