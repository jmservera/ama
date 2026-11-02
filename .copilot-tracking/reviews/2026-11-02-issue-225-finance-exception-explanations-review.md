# Review: issue 225 finance exception explanations (2026-11-02)

Execution: once, post-implementation, self-review of the diff. Outcome: slice conformant; the issue stays open (Refs).

| Criterion | Status | Evidence |
| --- | --- | --- |
| Queue explains exceptions and unknowns | Proven (unit) | test_exception_explanations_name_decider_and_never_decide_payment, test_clean_match_is_not_a_payment_decision |
| Safe endpoint, nothing inferred | Proven (unit) | every row names the human decider; "Payment is made outside this system."; no controls |
| WCAG 2.2 baseline, keyboard | Partly | structural test only (focusable labelled regions, captions, no positive tabindex); no browser, axe or assistive-technology run; #151 acceptance is human |
| Design system, no simulator | Partly | reuses host table and panel; Fluent 2 conformance not assessed |

## Routed follow-ups

1. Browser keyboard and axe run for the finance screens (needs a browser scenario registry entry).
2. Separate approver, preparer and payment officer entry points only if #155 shows need.
3. Observed validation in #155; no real prices or budgets.
