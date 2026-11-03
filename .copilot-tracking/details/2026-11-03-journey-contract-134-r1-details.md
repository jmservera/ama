# Details: same-home journey trace, slice 1 (Refs #134, R1)

* `src/core/src/zava_forward/core/journey_trace.py`: `journey_trace(entries, case_id)` returns events, five stage rows, intervals, order findings, decision domains, shared actors, `independent_decisions`, `complete`, and constructed-fixture labels.
* Stage mapping: EPC conflict = `stock_comparison` with field `epc`; correction = `stock_query_resolve` of that query id; decisions = resident, technical sign-off, quality acceptance, Finance disposition; handover = `quality_handover`; closure = `finance_payment_status`.
* Intervals: seconds between first events of adjacent stages, else `Unknown` with a reason.
* Isolation: entries whose `case` differs are ignored; building records are not read.
* Tests: `src/core/tests/test_journey_trace.py` (8 tests; real JSON store audit entries for stages 1 and 2, ledger-shaped entries for later stages; `buildings.blockers` control).
