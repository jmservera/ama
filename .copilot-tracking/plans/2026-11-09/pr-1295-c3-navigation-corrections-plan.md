<!-- markdownlint-disable-file -->
# Plan: PR 1295 C3 coupled current navigation/currency defects (2026-11-09)

* Task: `pr-1295-c3-navigation-corrections`; research: [.copilot-tracking/research/2026-11-09/pr-1295-c3-navigation-corrections-research.md](../../research/2026-11-09/pr-1295-c3-navigation-corrections-research.md); details: [.copilot-tracking/details/2026-11-09/pr-1295-c3-navigation-corrections-phase-details.md](../../details/2026-11-09/pr-1295-c3-navigation-corrections-phase-details.md)
* Start: HEAD `58229b8d30fc0019794ce4f98956beef6f0ea1e2`; owner remote `0bcf55da1` preserved; main `f3532b02c` merged normally (no rebase, force or push).
* Test tier: owner-selected demo-targeted checks. No `rpi-checks --all`. Correction budget: cycle 3 of 5 (C1, C2 retained).

## Scope

* F1 `Update-RouteNote`: one explicit baseline-to-physical mapping covering `page N`/`pageN`, `index N`/`indexN`, `slide N` and plural ranges, endpoints mapped, delimiters kept, part 55 untouched, below 13 unchanged.
* F2 architecture guide paragraph qualified as 14 October baseline versus 8 November source-coded depiction; no live deployment claim.
* F3 KB index rows 852 and 909 qualified to 55 slides/current numbering; dated historical 54 claims kept; log entry appended.
* F4 R09 anchors to 33/253/327.
* Regenerate only dependent notes, pitch question bank, delivered PPTX/PDF, `validation.json` hashes.
* Excluded: `slides.json`, visible slide text, protected cost XML, financial numbers, TIMING lines, historical records, new protected-financial editing, broad native rewrite.

## Phases

* [ ] Phase 1: Integrate main
  * Merge `origin/main` `f3532b02c` into the clean branch (ordinary merge commit). Preserve both append-only histories if a real conflict appears.
* [ ] Phase 2: Mapping fix and literal tests
  * Replace the page/slide regex with a single mapping function and add table-driven literal tests to `Test-DeckInsertion.ps1`. Prove the new tests fail on the pre-change function and pass after.
* [ ] Phase 3: Regenerate and prove the package delta
  * Build; compare pre/post packages member by member: expect only the five note parts to change. Prove 55 slides/notes, 108 actions, presentation order/IDs/sections, every click `r:id`/target versus baseline, reciprocal slide-note ownership, non-empty notes, duplicate ZIP entry refusal, protected cost bytes and unaffected slides/images.
  * Refresh pitch Q&A, delivered PPTX and PDF (fresh preview), and `validation.json` from tool output.
* [ ] Phase 4: Documentation
  * F2, F3, F4 edits and a dated log entry; update `ms.date` only where content changes.
* [ ] Phase 5: Targeted validation
  * Verify (build and delivered), Test-DeckInsertion, Test-CostStatus, Test-NativeShapes, Test-SourceHashes (semantic and default), render_preview plus pytest, build-architecture/update-architecture `--check`, node architecture and geometry tests, journey `--check`.
* [ ] Phase 6: Review and freeze
  * One post-implementation review, changes record, state JSON, local commit with trailer, clean tree. No push.

## Acceptance

* Literal mapping table passes; the 5 affected notes change as predicted and nothing else; receipt, catalog and delivered hashes equal recomputed values; all failures retained; native, visual, AT, rehearsal and live approvals remain unproven.

## Stop conditions

* Any package change outside the five note parts; a protected financial byte change; a required check fails for a cause introduced here; a change outside existing owner exceptions (freeze that item and name the owner decision).
