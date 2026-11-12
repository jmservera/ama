---
title: Issue 435 current capstone deck assessment changes
ms.date: 2026-11-12
task_id: current-capstone-assessment-435-1112
---

## Files changed

* Added `docs/capstone/pitch/current-deck-assessment-2026-11-12.md`: identity and agreement table, A1-D3 judgement table with page evidence, floors and overlap rules, 16-row Tokenomics register, routed findings F1-F6, criterion position.
* Edited `docs/capstone/pitch/README.md`: one link and a sentence stating the assessment is not a score or approval.
* Appended a 2026-11-12 entry to `docs/reference/log.md`; no earlier entry rewritten.
* Added RPI artifacts: research, plan, details, critique, state, this changes file and the review.

## Divergences and amendments

* Plan critique PC-001 to PC-004 applied (working-file hash comparison, regex inventory over all 55 pages, note-comparison wording, no installation). Execution divergence: during authoring, page citations for pages 18-21 were corrected after a title check (page 21 is the seven-checkpoint slide, not cost; security and architecture cited as pages 18-20).
* The knowledge-base index `docs/reference/README.md` does not list pitch files individually (the placement draft is absent too), so it was not edited.

## Validation (focused documentation tier)

* All relative links in the new file resolve; ASCII scan clean; no em dashes.
* Working-file `git hash-object` equals the identities in the research for the PPTX, PDF, manifest, generated script and answers; the builder file is unchanged (`git status` shows no modification).
* `git status --short` shows only the two edited docs plus untracked RPI artifacts and the new assessment.
* Not run: deck build or render, native PowerPoint, rehearsal, runtime tests, complete gate, hosted CI (nothing published).

## Correction 1 (after original commit 9dd2c2427e46)

* Defect introduced by this assessment: register row T12 attributed page 44 (B16) to E05. The delivered PPTX shows `Sources: E06 · E07 · E13` on the slide and only E06, E07 and E13 in its notes (page identified by B16 content; E-codes read with standard-library XML extraction). Row T12 now cites E06, E07, E13 and notes that E05 is not cited there; class "Designed control, not live". Row T4 (page 22, E05) and finding F3 are unchanged.
* Validation: only the assessment file differs in the working tree; protected deck, PDF, manifest, builder and notes hashes unchanged; guide coverage rows unchanged; no link added.

## Correction 2 (after d65c72cc0ab9)

* N1 from the independent assessment: T14 cited E05; page 55 visible text and notes carry no E-code. Row now cites the source line (API bounded-skills and core consumption guides) and class "source-contract statement, not an E05 citation".
* Same defect class, found while verifying: T13 (page 54) said unlabelled; the source line cites E19, E04, E09. Corrected. No other row re-audited (no broad audit).
* Validation: only the assessment file differs among protected/docs paths; PPTX and other protected hashes unchanged; no link added.
