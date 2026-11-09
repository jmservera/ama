<!-- markdownlint-disable-file -->
# Plan: PR 1295 source freshness (2026-11-09)

* Task: `pr-1295-source-freshness`; research: [.copilot-tracking/research/2026-11-09/pr-1295-source-freshness-research.md](../../research/2026-11-09/pr-1295-source-freshness-research.md); details: [.copilot-tracking/details/2026-11-09/pr-1295-source-freshness-phase-details.md](../../details/2026-11-09/pr-1295-source-freshness-phase-details.md); critique: [.copilot-tracking/reviews/2026-11-09/pr-1295-source-freshness-plan-critique.md](../../reviews/2026-11-09/pr-1295-source-freshness-plan-critique.md).
* Start: HEAD `6bcf10ee63518c0e157c73e42f574b1aae65b6d4`; owner remote `0bcf55da1` preserved; main `d4d6827fe` (read-only, not merged).
* Test tier: owner-selected demo-targeted checks. No `rpi-checks --all`. Correction budget: cycle 2 of 5.

## Scope

* Generation-only: regenerate `resident-journey.excalidraw` and `.svg` with the existing generator, update their two catalog hashes, rebuild/verify the delivered deck and receipt with the documented tools.
* Excluded: application, backend, security, journey narrative and `text-equivalent.md`, generator logic, the C1 notch, owner IoT/resident work, unrelated defects.

## Phases

* [ ] Phase 1: Baseline and pre-change identities
  * Record sha256 of the two assets, PNG, catalog, PPTX, PDF, receipt; record failing `--check` (already observed on HEAD and main).
* [ ] Phase 2: Regenerate and prove the diff
  * Run the generator; diff against pre-change files; prove only `line`, `sha256` and `localLink` metadata (native) and the SVG metadata line changed; geometry, text and topology identical by structural comparison.
  * Re-render the PNG in scratch with the documented CLI settings; keep the PNG only if byte-identical, otherwise record why a rebuild is required.
* [ ] Phase 3: Catalog, deck and receipt
  * Update the two catalog hashes from the regenerated files. Build and Verify with `Invoke-Capstone.ps1`; refresh `validation.json` and delivered files only where their bytes change, from tool output.
* [ ] Phase 4: Targeted validation
  * Journey `--check` (must exit 0), Build, Verify, Test-SourceHashes (semantic and default), Test-NativeShapes, Test-DeckInsertion, Test-CostStatus, render_preview with pytest, architecture build/update checks and node architecture/geometry tests. Re-observe slide and action counts.
  * Re-inspect pages 12 and 13 geometry/preview (C1 notch). State coverage honestly.
* [ ] Phase 5: Review and freeze
  * One review, changes record, state JSON, local commit with trailer, clean tree, no push.

## Acceptance

* Journey `--check` exits 0; Verify and hash checks pass; only intended source-reference changes; failures retained, no waiver.

## Stop conditions

* A required check fails for a reason not introduced here (record, do not mask); the diff includes any layout/text/topology change; the PNG differs unexpectedly; budget beyond five cycles.
