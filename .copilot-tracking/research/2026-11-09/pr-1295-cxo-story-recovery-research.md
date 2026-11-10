<!-- markdownlint-disable-file -->
# PR 1295 CxO story recovery research (2026-11-09)

Task: `pr-1295-cxo-story-recovery`. PR-only lane, no proven issue mapping (issue 435 is not mapped; no issue is closed or ticked).
Research disposition: executed. Planning readiness: Ready.

## Identity

* Seed and PR head: `b671116d571b76ebbbc9e277a791e67f781609cd` (branch `docs/capstone-cxo-story`, base `main`).
* Fetched `origin/main`: `b46a9ad9a9619db535368d1b2cbbddec8110e122`; merge base `fa7ae0c9`.
* Local recovery branch `docs/demo-recovery-pr1295-1109`, clean at start.
* Hosted `gh pr checks` on the head: all pass (rubric 78/100 vs baseline 78/100). Review decision empty; no closing references.

## Original evidence found

* No original actual RPI plan/details/changes records for this PR are tracked in the branch. The original evidence that survives is the in-branch [story review](../../../docs/capstone/source/review-2026-11-08-cxo.md) and the PR body. Nothing is backfilled.
* Adverse evidence retained as stated there and in the PR body: independent assessment of `08e4d3ca` was FAIL (three Medium consistency findings, corrected in the head); the first focused-gate attempt was stopped and not passed; the owner-directed full local gate was interrupted, not passed. No passing full receipt exists. This recovery does not treat any of these as passing evidence.

## Main drift

`origin/main` moved 32 files since the merge base; the only non-tracking paths are `tools/rpi-checks.py` and `tools/test_rpi_checks.py`. No file under `docs/capstone`, `docs/architecture`, `src` or `infra` cited by the deck changed, so no merge was needed for story currency.

## Claim-to-source comparison (read-only)

* Gates, advance, auth, resident field catalog, receiver role, Foundry module and ACA auth locators in the architecture text equivalent resolve to the claimed declarations (gates.py 105, store.py 635, auth.py 34 and 101, resident_preview.py 24, iothub.bicep 147, main.bicep 328, containerapps.bicep 221). All local links resolve; three Microsoft Learn links were not fetched.
* Employee chat and AI consumption README anchors exist (api README 707, core README 94).
* Per-slide financial figures (currency amounts and percentages) are identical to main for all 54 slides. Package has 54 slides and the PDF has 54 pages. Slide 53 differs from main, consistent with the documented owner-approved status wording exception; slides 21/52 status changes sit in the guarded status substitution, not in slides.json figures.
* The deck states that the demo is prepared material, device ingestion is source/synthetic evidence only, and the graph is conceptual. These match the source. No claim of live AI, IoT acceptance or compliance was found that source contradicts. No mock is presented as actual AI.

## Gaps and limits

* `pwsh` is unavailable, so `Test-CostStatus.ps1`, `Test-SourceHashes.ps1`, `Test-NativeShapes.ps1` and the Build/Verify pipeline were not re-run; recorded results in `validation.json` are historical, not recomputed here.
* No native PowerPoint, keyboard/assistive-technology, projector or human rehearsal evidence exists. Human rehearsal remains separate.
* The independent exact-head reassessment of the three corrected Medium findings is a coordinator task.

## Conclusion

No concrete directly coupled consistency bug was confirmed. No deck change, no `ama-mentor-deck` load and no PowerPoint authoring pipeline run is justified.
