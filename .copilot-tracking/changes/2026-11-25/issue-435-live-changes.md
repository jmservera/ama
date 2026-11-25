---
title: Changes for issue 435 tokenomics slide (live 2026-11-25)
ms.date: 2026-11-25
---

## Changes

* `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`: added appendix slide B28 (page 56) and its notes; S18 notes list B28 under related answers. Direct python-pptx edit (script not retained); no rebuild workflow available.
* `docs/capstone/deck/zava-forward-cowork-v2-draft.pdf`: regenerated with LibreOffice (56 pages).
* `docs/capstone/README.md`, `docs/reference/README.md`, `docs/reference/log.md`: updated.
* `docs/reference/research/capstone-pitch-435-live-2026-11-25.md`: new evidence note.

## Divergences

* Manifest, builder and validation receipt were not updated (no PowerShell; builder supports one insertion): stated as a limit and follow-up.

## Validation

Focused tier. Reload (56 slides), render inspection of page 56, package diff (no media change), `tools.test_capstone_pitch_docs` (6 OK), `test_journey_icons_are_exact_six_step_presentation_assets` OK. No `src` change, so no full tier; `rpi-checks.py --all` not run. Hosted CI not observed (no push).

## Per-criterion table (issue 435)

| # | Criterion | Proven? | Basis |
| --- | --- | --- | --- |
| 1 | Placement decided; deck rebuilt and revalidated if changed | Partly | Decision 2026-11-25 (brief); deck changed, reload and render validated; PowerPoint workflow rebuild not run |
| 2 | Mentor confirms meaning | Unproven | Needs the mentor |
| 3 | Rehearsed in timed route | Unproven here | No performed timing exists; B28 is off the timed route |
| 4 | Batch decision and spend authority | Proven (demo) | 2026-11-18 note and #432 evidence |
| 5 | Deck challenged against guide | Not re-proven for B28 | Challenge covers the 55-slide deck |
| 6 | Statements sourced and labelled, no price, saving or payback | Proven for B28 | Claim scan; labelled evidence in notes |
