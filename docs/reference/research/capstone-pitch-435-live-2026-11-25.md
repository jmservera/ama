---
title: Capstone Tokenomics slide B28 and per-criterion status (Refs #435)
description: Owner-directed addition of the Tokenomics appendix slide B28 to the capstone deck, validation evidence and what remains unproven for issue 435 on the synthetic demo
ms.date: 2026-11-25
---

Scope: synthetic demo, desktop only. Owner decision 2026-11-25: add the Tokenomics slide to the capstone deck from the docs/capstone/pitch material. No Azure change was made, no credential was read and no source under `src/` changed (focused tier).

## What changed

* [The delivered deck](../../capstone/deck/zava-forward-cowork-v2-draft.pptx) now has 56 slides. Page 56 is appendix card B28, "What does an accepted proposal cost?", cloned from the B27 card structure. It states the unit (cost per accepted outcome above a quality floor, a proposal), the measured held-out batch (12 synthetic proposals, 2,522 tokens, usage only, #432, 2026-11-18), the gap (no price, no saving, no accepted-proposal count) and what is not claimed. Sources are the [Q&A brief](../../capstone/tokenomics-qa-brief.md) and the [#432 note](./ai-heldout-batch-432-live-2026-11-18.md).
* Placement: appended as page 56 so no existing page number or cross-reference moves. The S18 (page 22) notes now list B28 under related answers. B28 buttons: Topic jumps to slide 22, Return to caller jumps to the index (slide 28), as B27 does.
* [The PDF](../../capstone/deck/zava-forward-cowork-v2-draft.pdf) was regenerated with LibreOffice from the edited deck (56 pages).

## Validation (2026-11-25)

* `python-pptx` reload: 56 slides; slide 56 notes start "B28"; hyperlink relationships resolve to `/ppt/slides/slide28.xml` and `/ppt/slides/slide22.xml`.
* LibreOffice render of page 56 inspected: no overflow or clipping; all text readable.
* Package diff against HEAD: 303 to 307 members; only slide56 and notesSlide56 parts (with rels) added; no member removed; no media changed; `test_journey_icons_are_exact_six_step_presentation_assets` passes; `python3 -m unittest tools.test_capstone_pitch_docs` passes (6 tests).
* Claim scan: the slide and notes contain no price, saving or payback statement; USD 0.44 per home appears only as a labelled planning scenario.

## Limits

* The rebuild workflow could not run: PowerShell is not installed here, and the builder supports a single declared insertion. The deck was edited directly, so [slides.json](../../capstone/source/slides.json), [validation.json](../../capstone/source/validation.json) and the builder do not include B28, and a clean rebuild from source would drop it. Fold B28 into the manifest and builder before the next rebuild.
* The receipt hash in `validation.json` (`candidate_sha256`) no longer matches the delivered PPTX, so `Test-SourceHashes.ps1` delivery verification would fail until the receipt is regenerated (not run here: no PowerShell).
* The question-bank index (slide 28) has no B28 entry; the card is reached from the S18 notes and the speaker's own navigation. Native hyperlinks to B28 are not added.
* No rehearsal timing exists for B28; it is off the timed main route.
* The independent PowerPoint workflow validation and native PowerPoint rendering were not run.

## Per-criterion status

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Owner decides placement; deck rebuilt and revalidated if changed | Decision proven; revalidation partial | Owner decision 2026-11-25 to add the slide, recorded in the task brief (the 2026-11-13 decision is in the [placement draft](../../capstone/pitch/tokenomics-placement-draft.md)). Deck changed and validated by reload and render as above; not rebuilt through the PowerPoint workflow (limits above), so the criterion is not fully proven |
| 2 | Mentor confirms what Tokenomics meant | Cannot be proven for the demo | Needs the mentor; the repository holds only the owner's report. B28 states the unit as a method with gaps and shows no figure implying one was requested |
| 3 | Segment rehearsed in the timed route | Ticked in the issue; not re-proven | [Rehearsal notes](../../capstone/pitch/tokenomics-rehearsal-notes.md) record no performed timing; B28 adds none |
| 4 | Owner decides on a finite measured batch; spend authority recorded | Proven for the synthetic demo | Authority and batch recorded in the [2026-11-18 note](./capstone-pitch-435-live-2026-11-18.md) and the #432 note; B28 shows the 12-proposal usage result with its label |
| 5 | Deck challenged against the assessment guide | Ticked in the issue; not re-proven for B28 | The [challenge](../../capstone/pitch/capstone-assessment-challenge.md) covers the 55-slide deck, not the new card |
| 6 | Every Tokenomics statement sourced and labelled, no price, saving or payback claim | Proven for B28; not re-proven elsewhere | Claim scan above; notes carry evidence labels per statement |
