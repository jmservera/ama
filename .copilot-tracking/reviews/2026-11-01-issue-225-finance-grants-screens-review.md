# Review: issue 225 finance and grants screens (2026-11-01)

Execution: once, post-implementation, self-review of the diff against the acceptance criteria. Outcome: slice conformant; criteria 4 and 5 not fully proven, so the PR uses Refs.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Invoice queue compares quantities, scope, version, budget, milestone evidence; explains exceptions and unknowns | Proven (unit) | test_invoice_lines_compare_scope_quantity_budget_milestone |
| Funding route, template and constructed field draft show conflicts and reviewed evidence | Proven (unit) | test_funding_draft_shows_conflicts_and_evidence_without_submission |
| Safe endpoint is a reviewed export or readiness view; nothing inferred | Proven (unit) | readiness panel "Not ready" default, no-control assertions |
| WCAG 2.2 baseline, textual state, keyboard | Unproven | native semantics (table caption, th scope, focusable scroll region) only; no browser or axe run, and #151 acceptance is human |
| Design system components (#150), no role simulator | Partly | reuses host panel/table patterns; no simulator; Fluent 2 conformance not assessed |
| Tokenomics: AI economics section | Proven (design only) | usage-to-billing, Total Cost of AI components, booked-value status, Unknown defaults |

## Copilot review round 2

All four threads valid and fixed (line total wording, unverified milestone reference, unchecked queue exceptions Unknown, unreadable form review keeps readiness and holds Unknown). Original Review outcome preserved; focused tests and ruff pass.

## Routed follow-ups

1. Browser keyboard and axe check for both screens (criterion 4).
2. Observed validation in #155; no real prices or budgets.
3. The host `/api/ai/report` is manager-only, so the Grants and Evidence Officer sees Unknown cost by design.
