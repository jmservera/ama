<!-- markdownlint-disable-file -->
# Plan: PR 1295 validation correction (2026-11-09)

* Critique: [.copilot-tracking/reviews/2026-11-09/pr-1295-validation-correction-plan-critique.md](../../reviews/2026-11-09/pr-1295-validation-correction-plan-critique.md) (Revise, applied).
* Task: `pr-1295-validation-correction`; research: [.copilot-tracking/research/2026-11-09/pr-1295-validation-correction-research.md](../../research/2026-11-09/pr-1295-validation-correction-research.md); details: [.copilot-tracking/details/2026-11-09/pr-1295-validation-correction-phase-details.md](../../details/2026-11-09/pr-1295-validation-correction-phase-details.md).
* Start: HEAD `53ff9757930242795d321626a0301f4a948449c7`; owner remote `0bcf55da1` preserved; main `76db469b1` (read-only comparison, not merged).
* Test tier: owner-selected demo-targeted authoring checks only. No blanket gate, no `rpi-checks --all`.
* Correction budget: five total; this plan uses cycle 1 of 5 and stops early when resolved.

## Scope decisions

* Journey check failure: confirmed main defect (#1283 changed `agent-request-challenge.md`; no PR file is a generator input). No source change. Record failure, publication gap and a separate fix draft with reproduction, acceptance, dependencies and dedup.
* Page 12: confirmed PR-introduced geometry defect. Fix the CxO scene (`application-boundary` outline and caption position) and its derivatives.
* Page 13: crossing not reproduced (1 px near-contact only). No change; recorded.
* Page 46 font glyph, native PowerPoint, AT, projector, rehearsal: out of scope and unverified.

## Phases

* [ ] Phase 1: Failing regression first
  * Add a geometry test that fails on the current CxO source: boundary and frame outlines (rectangles without owned container text, and lines) in the two capstone drawings must not intersect any text box; inherited `docs/architecture` crossings are out of scope.
  * Run it before the fix and record the failure.
* [ ] Phase 2: Source fix
  * Allow `line` in `test-architecture.mjs` only for the named closed boundary outline and assert it is closed (critique 2).
  * Round-trip check of the polygon through the Excalidraw restore path; label the PDF a Linux preview (critique 4, 5).
  * Add an editable closed-outline primitive to `build-architecture.mjs`; replace the `application-boundary` rectangle by the notched outline; move `sensor-caption` to x 290, width 700.
  * Regenerate CxO native and SVG with the existing generator; render the PNG with the existing local Excalidraw CLI settings; leave Azure derivatives byte-identical.
* [ ] Phase 3: Contract and delivery set
  * Update `text-equivalent.md` and the three `cxo-architecture` catalog hashes (native, SVG, PNG).
  * Build with `Invoke-Capstone.ps1`, run Verify, regenerate the Linux preview PDF with the existing render tool, and copy the matching PPTX, PDF, speaker script and Q&A to the delivery paths only where their bytes changed.
  * Update `validation.json` only from Verify and preview reports (candidate/PDF/catalog and both pitch hashes, counts; qualify unreproduced preview metrics). No expected-hash edits by hand.
* [ ] Phase 4: Targeted validation and visual inspection
  * Run Verify (build and delivered), Test-NativeShapes, Test-SourceHashes (semantic and default), Test-DeckInsertion, Test-CostStatus, `test_render_preview.py`, `build-architecture.mjs --check`, `update-architecture.mjs --check` and the node architecture/geometry tests; run the journey check and record its expected failure.
  * Inspect pages 12, 13 and 38 images (all three use the changed or sibling architecture assets) and the diff; state coverage honestly.
* [ ] Phase 5: Review, state and commit
  * One self-review with independent-review input; changes record; state JSON; KB index/log only if a KB file changes (none expected).
  * Commit locally with Conventional Commit and trailer; clean tree; no push.

## Acceptance

* New regression fails before and passes after the fix; existing 14 node checks keep passing (plus the new one).
* Page 12 shows no outline crossing text; page 13 and the other pages are unchanged in bytes except where the catalog hash demands.
* Native PPTX editability, 55 slides, 108 navigation actions, notes and cost evidence preserved.
* Journey failure remains recorded with fix draft; no waiver.

## Stop conditions

* Stop and record a blocker if the rendered PNG cannot be produced with the existing tooling, if Verify fails for a reason this change did not introduce, or if the budget would exceed five cycles.
