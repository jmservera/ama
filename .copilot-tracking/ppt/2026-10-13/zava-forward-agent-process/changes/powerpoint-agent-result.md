<!-- markdownlint-disable-file -->
---
title: PowerPoint agent result
ms.date: 2026-10-13
---

Status: complete (working output only; canonical deck untouched).

## Output

* Output: `.copilot-tracking/ppt/2026-10-13/zava-forward-agent-process/slide-deck/zava-forward-executive-draft.pptx`, 22 slides
* Source SHA256: `6ae671851a456b3f1482b0b24af09be2b836900c1d8eccc5a13fa929c1c268da` (21 slides; identical to canonical `docs/capstone/deck/zava-forward-executive-draft.pptx`, unmodified)
* Output SHA256: `1ec522efef1338875b60288fe58b61a50fa514f4427e26d3f69a1e2b950bb911`
* Content: `content/slide-013/content.yaml` (PNG placement full-slide, alt text, footer, logo, 3.7k-character notes with talk track, text equivalent, evidence)
* Staging: `slide-deck/staging/staged.pptx` (source plus one blank slide at position 13, footer counters 14 to 22 renumbered)
* Build: `build_deck.py --source staged.pptx --slides 13` (no --template, no content-extra scripts, no uv)

## Executed checks

* Slide count 21 to 22; slide 13 title "Five assists. One controlled journey."; status "PROPOSED DESIGN" visible in diagram and footer.
* Preservation: for all 21 original slides, shapes (type, name, geometry, text), notes text, image relationships and layout match the source; only footer counter digits differ. Masters 1/1, layouts 11/11.
* Notes: no slide has empty notes (22/22). Original slide 12 notes unchanged.
* `validate_deck.py`: 0 errors, 0 warnings, 1 info (partial content directory, expected). Output in `slide-deck/validation/deck-validation-report.md`.
* Real LibreOffice PDF export (`deck.pdf`) and pdftoppm images: `slide-deck/validation/slide-12.jpg`, `slide-13.jpg`, `slide-14.jpg`, plus `all-NN.jpg` thumbnails of all 22.
* Visual inspection by the agent of slides 12, 13, 14: slide 13 has no clipping or overlap; footer sits below the last diagram line without collision; Zava logo clear of the title. Initial footer position (7.20 in) was tight and was moved to 7.26 in, then re-exported.
* Observation (not a defect of this change): slides 12 and 14 show wide letter spacing in the LibreOffice render because Aptos is not installed; unchanged from source.

## Not run (distinct)

* Model-based vision validation (`validate_slides.py`): Unavailable, no SDK/model setup; not claimed as passed.
* PyMuPDF `render_pdf_images.py`: Unavailable (module missing); pdftoppm used instead.
* Rendering in real PowerPoint with Aptos: Deferred to owner.
* User acceptance, staff validation, rehearsal timing: Not performed.

## Rubric contribution (qualitative, no score)

* A1/A3/A6/A7: one idea per slide, bounded autonomy, proposal versus deployment distinction, source labels in notes and footer.
* B1/B2/B6/B7: value tests as measures per capability in notes, human approval owners on slide, benefits stated as unmeasured hypotheses.
* Residual: text equivalent is in notes and alt text only; diagram text is image-embedded (editable SVG source exists).

## Parent actions

Replace the canonical deck only after reviewing the output; no git, PR or outside-root changes were made.
