# Research: issue 225 finance exception explanations (2026-11-02)

Task: issue-225-finance-exception-explanations (parent: issue-225-finance-grants-screens, PR 657 merged). Disposition: reused and extended (focused). Planning Readiness: Ready.

## Evidence

* Merged slice 1 (`finance-invoices`, `finance-funding` in `role-screens.js`) shows exception messages verbatim only. Review of slice 1 routed two follow-ups: keyboard and semantics proof (criterion 4) and exception explanation. `docs/reference/research/ux/atlas-screen-trace.md` row for Finance and Grants promises "Exceptions explained before any export or readiness block".
* `core/finance.py match_invoice` emits fixed codes: ambiguous_commitment, no_commitment, duplicate, over_commitment, no_budget, over_budget, not_in_scope, quantity, no_milestone. Invoice-level codes are replicated per line, so the screen must group them.
* Issue criterion 1 requires the queue to "explain exceptions and unknowns"; `docs/reference/research/ux/customer-journeys/finance.md` and atlas O16/O17 are desk hypotheses, validation stays in #155.
* Content standard (`content-standard.md`, `test_content_standard.py`) audits `role-screens.js` copy; plain language, textual state, no payment or award inference.

## Decisions

* Add a read-only "Exception explanations" table per checked invoice: exception, where it applies, plain meaning, what the match did not check, who decides. Unknown codes degrade to an Unknown explanation.
* Unchecked invoices state exceptions are unknown; no exceptions found is never presented as a payment decision.
* Add node-harness structural checks for keyboard and semantics (focusable scroll region, no positive tabindex, no controls, labelled tables). Not a substitute for assistive-technology testing.
* No server change, no controls, no real prices.
