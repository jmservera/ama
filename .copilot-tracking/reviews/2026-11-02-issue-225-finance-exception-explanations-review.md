# Review: issue 225 finance exception explanations (2026-11-02)

Execution: once, post-implementation, self-review of the diff. Outcome: self-review only; engineering evidence; WCAG/AT acceptance pending. The issue stays open (Refs).

| Criterion | Status | Evidence |
| --- | --- | --- |
| Queue explains exceptions and unknowns | Unit-tested (`tests.test_finance_grants_screens`: 12 tests; with `tests.test_content_standard`: 25 tests; node harness, run 2026-11-02, OK) | test_exception_explanations_name_decider_and_never_decide_payment (grouping, Line 1, no_budget, unknown row Unknown), test_invoice_level_exception_is_grouped_across_lines, test_clean_match_is_not_a_payment_decision |
| Safe endpoint, nothing inferred | Unit-tested (same run) | decider per known code, Unknown for unknown codes, "Payment is made outside this system.", no controls; roles cross-checked with FINANCE_APPROVERS in src/core controls.py |
| WCAG 2.2 baseline, keyboard | Partly | structural test only (focusable labelled regions, captions, no positive tabindex, no button/input/select nodes); no browser, axe or assistive-technology run; #151 acceptance is human |
| Design system, no simulator | Partly | reuses host table and panel; Fluent 2 conformance not assessed |

## Routed follow-ups

1. Browser keyboard and axe run for the finance screens (needs a browser scenario registry entry).
2. Separate approver, preparer and payment officer entry points only if #155 shows need.
3. Observed validation in #155; no real prices or budgets.
