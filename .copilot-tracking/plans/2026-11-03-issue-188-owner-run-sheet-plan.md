# Issue 188 plan: owner run sheet (2026-11-03, r1)

Details: [details](../details/2026-11-03-issue-188-owner-run-sheet-details.md)

## Stacked slices

* Slice 1 (merged, #847): demo finds its fixtures.
* Slice 2 (this PR): owner run sheet for the live Azure SQL check. [x]
* Slice 3 (owner-gated): execute the run sheet after a live Hub stream.
* Slice 4 (blocked): real pinned climate in the demo.

## Critique (single pass, self)

Verdict: proceed. Documentation only; no code or credential path added; the sheet forbids secrets, separates read-only from write access and ties ticking to recorded evidence. No criterion is ticked.

## Validation (focused)

* Git diff and ASCII review. No executable change, so no tests beyond the checks script.
* Gate, benchmarks and full suites not run.
