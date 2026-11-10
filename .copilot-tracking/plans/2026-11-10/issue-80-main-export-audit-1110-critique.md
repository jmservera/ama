<!-- markdownlint-disable-file -->
# Critique: issue #80 export audit plan (single pass)

Reviewed: plan and details for `issue-80-main-export-audit-1110`. Executed once; not repeated.

## Verdict

Proceed with direct amendments. No significant or divergent issue needs a user decision; no advice conflicts with a confirmed decision.

## Findings and dispositions

* Proof overreach risk: a passing browser check on Closed cases and form-schemas must not be read as evidence for other lists. Applied: the matrix proof level `B` is assigned only to the route a check actually drives; all others stay `S`, `A` or `N`.
* Role inventory test proves route role gates, not row correctness. Applied: matrix marks it as `A` (route and role gate) and never as row, filter or immutability proof.
* Ambiguity of "list": do not narrow to force "every". Applied: bullets and navigation stay `unknown` and the owner decision is stated exactly; no all-blocked claim.
* Environment contamination: system python resolves another checkout. Applied: owned venv with import-origin verification before any check.
* Heavy lock: one non-queued `flock -n` per browser check; BUSY or failure stops that check and is recorded as a true outcome, not retried.
* Scope drift: no source, test or fixture changes, no thresholds, no tick, no freshfive allowance. Applied as plan constraints; Root decides ticks and publication.
* Historical candidates `d8ce761a` and `9b2572cf` stay exclusions, not delivery proof.
