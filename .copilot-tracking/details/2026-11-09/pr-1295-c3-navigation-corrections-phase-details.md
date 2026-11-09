<!-- markdownlint-disable-file -->
# Phase details: PR 1295 C3 (2026-11-09)

## Phase 1

* `git merge --no-ff origin/main -m "chore: merge main into PR 1295 recovery branch"`; author/committer repository-local noreply identity; Copilot trailer. Confirm clean tree first.

## Phase 2

* In `Invoke-Capstone.ps1` add `Convert-BaselineSlideNumber` (`13..54` +1, otherwise unchanged) and `Update-BaselineNavigationNumbers` using a single `[regex]::Replace` with `(?i)\b(pages?|slides?|index)( ?)(\d+)(?:([-\u2013/])(\d+))?\b` (critique finding 1 adds the `/` endpoint separator, e.g. QX `pages 9/16` to `9/17`). `Update-RouteNote` calls it for every part except 55. Nothing else in the function changes (timing append stays).
* `Test-DeckInsertion.ps1`: before the `-not $CandidatePath` return, a literal table of input/expected pairs, each written as constants independent of the production regex: `B13/page40, index/page27 and fixed topic S19/page22` to `...page41, index/page28 ... S19/page23`; `index 27` to `index 28`; `pages 23-24` to `pages 24-25`; `pages 1-22` to `pages 1-23`; `page 12`, `index 12`, `pages 5-12` unchanged; `page 54` to `page 55`; `page 55` unchanged; part 55 through `Update-RouteNote` unchanged; single application only (`index page 27` to `index page 28`, one shift).
* Fail-before proof: run the same table against the pre-change function body from `git show HEAD:tools/capstone/Invoke-Capstone.ps1` in scratch; record the failures.

## Phase 3

* Build to `/tmp/ama-pr1295-c3/post-build`. Python `zipfile` comparison with pre-build: changed member list, notes parts, protected parts 6/11/21/32/36/52 slide bytes, all other bytes. Independent check script reads baseline and candidate: slide count/order/sldId/rId, sections, hyperlink `r:id` plus resolved target per click, notes relationships both directions, duplicate names, ZIP duplicate refusal (build an adversarial copy with a duplicate entry and prove refusal by the existing `Verify`/package reader).
* Content proof independent of the production transformation (critique finding 2): a Python check holds literal hand-written (old fragment, new fragment) pairs for QX, B13, B20, B26, B27; expected note text is the pre-build note with exactly those literal substitutions; every other note part, including cost parts, part 55 and all unchanged notes, must be byte-equal to the pre-build candidate.
* Recompute both pitch hashes, PDF hash and preview-source hash against the receipt and pitch candidate hash lines (critique finding 5).
* Copy the candidate PPTX and generated Q&A/speaker files to the repo; run `render_preview` on the delivered candidate; compare page images with the C2 preview; replace the delivered PDF with the fresh preview; update `validation.json` bindings (candidate, builder, preview source and PDF hashes, notes about metrics scope).

## Phase 4

* `docs/architecture/README.md` 263-267: replace with a dated qualified paragraph; keep ADR link.
* `docs/reference/README.md` rows 852 and 909 and `ms.date`; `docs/reference/log.md` append `## [2026-11-09] update | ...`.
* `docs/capstone/source/diagrams/discovery-journey/text-equivalent.md` line 264 anchors.

## Phase 5

* Commands in the plan; all logs in scratch; adverse outcomes recorded.

## Phase 6

* One review record, changes record, state JSON; commit `fix(capstone): ...` with trailer; clean tree check.
