<!-- markdownlint-disable-file -->
# Plan: issue #80 qualified audit correction

Research: `.copilot-tracking/research/2026-11-10/issue-80-qualified-audit-1110-research.md`. Details: `.copilot-tracking/details/2026-11-10/issue-80-qualified-audit-1110-details.md`. Critique: `.copilot-tracking/plans/2026-11-10/issue-80-qualified-audit-1110-critique.md`.

## Objective

Documentation-only: supersede two incorrect claims in the original audit (inventory totals; literal grep as absence proof) with a dated corrected supplement, and map rows and gaps to the Root-adopted planning minimum. Originals stay byte-identical.

## Phases

* [ ] Phase 1: write the supplement `.copilot-tracking/audits/2026-11-10/issue-80-qualified-audit-1110-supplement.md` (correction table, control trace, M1-M4 mapping, limits, remaining scope, Root decisions).
* [ ] Phase 2: write the changes file with exact documentary changes and confirm originals unchanged by `git diff` against `5d94c710`.
* [ ] Phase 3: one Review, then the external handoff `ROOT/handoff-80-qualified-audit-1110.md`, local commit, canonical chain.

## Constraints

No fetch, merge, rebase, source, test, dependency or config change; no runtime or browser run; no push, PR or GH mutation; thresholds human/open; C2, C4 and #73 stay open; no source allowance created.

## Success criteria

Totals stated as eleven distinct CSV paths plus progress variant (twelve entries), nine controls located, three not located; "not located by static literal search and bounded construction trace; generic/dynamic controls not ruled out" used consistently; seven genuine records and a verify exit 0.

## Additive plan 2026-11-10 (provenance qualification)

* [ ] Add dated qualification notices (insert after the title only; bodies untouched) to the original matrix, research and review, linking the supplement `.copilot-tracking/audits/2026-11-10/issue-80-qualified-audit-1110-supplement.md`.
* [ ] Correct the "only web consumers" statements in the qualified research and supplement to the inspected scope, listing `role-screens.js` consumers.
* [ ] Qualify "no GH operation" in the qualified changes file to no GH mutation, disclosing read-only `gh api user` lookups.
* [ ] Order: implement-start, edits, standalone validation, implement-done, then the single Review creates a new review artifact, review-done, commit, commit-complete, verify.
* Constraints: documentation only; no source, runtime, fetch, push or GH mutation; C2, C4 open; M1-M4 unchanged.
