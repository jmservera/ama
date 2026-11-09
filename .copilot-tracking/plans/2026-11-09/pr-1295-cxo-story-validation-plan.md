<!-- markdownlint-disable-file -->
# PR 1295 CxO story PowerShell validation plan (2026-11-09, prospective)

Details: [phase details](../../details/2026-11-09/pr-1295-cxo-story-validation-phase-details.md). Research: [research](../../research/2026-11-09/pr-1295-cxo-story-validation-research.md).

## Scope

Run existing read-only/source-contract checks on frozen `399e31ac` with the isolated PowerShell 7.6.9. No deck content, financial, slide-count, navigation or protected-cost change. No full gate, no native PowerPoint.

## Phases

* [x] Phase 1: Build the candidate to an external scratch directory and run Verify.
* [x] Phase 2: Run Test-CostStatus on the built candidate, Test-SourceHashes (default and `-SemanticOnly`) and Test-NativeShapes.
* [x] Phase 3: Record exact commands, exits and counts in changes; failures are reported, not waived or fixed here.
* [x] Phase 4: Review, state and handoff; commit only these recovery artifacts.

## Boundaries

Scratch under `/tmp` only; the tracked tree must stay clean. Any failing check blocks and is reported with no false pass. No push, PR edit or merge. Original FAIL and interrupted-gate evidence and the first recovery report are preserved.
