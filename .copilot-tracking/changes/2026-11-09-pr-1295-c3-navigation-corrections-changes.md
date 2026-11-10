<!-- markdownlint-disable-file -->
# Changes: PR 1295 C3 navigation corrections

Plan: `.copilot-tracking/plans/2026-11-09/pr-1295-c3-navigation-corrections-plan.md`. Frozen start `58229b8d30fc0019794ce4f98956beef6f0ea1e2`; ordinary merge of `origin/main` `f3532b02c` (commit `26d2e8785`, clean, no rebase or force). Correction budget: cycle 3 of 5 (C1, C2 retained; two remain; no extension inferred).

## Changes

* `tools/capstone/Invoke-Capstone.ps1`: added `Convert-BaselineSlideNumber` (baseline 13 to 54 move up one, others unchanged) and `Update-BaselineNavigationNumbers` (one regex for `page(s)`, `slide(s)`, `index`, optional space, `-`, en dash and `/` range endpoints). `Update-RouteNote` applies it to every part except 55; timing logic unchanged.
* `tools/capstone/Test-DeckInsertion.ps1`: literal independent table (13 cases including B13/page40, index/page27, `index 27`, S19/page22, `pages 23-24`, below-13 and part 55 unchanged) and `Update-RouteNote` checks for parts 55 and 40.
* `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`: regenerated; exactly five members differ from the C2 package (`notesSlide27/40/47/53/54.xml`; QX, B13, B20, B26, B27). SHA-256 `949e2077...fa7fca`.
* `docs/capstone/deck/zava-forward-cowork-v2-draft.pdf`: fresh Linux LibreOffice preview; all 55 page images byte-identical to the C2 preview. SHA-256 `e1476330...0504`.
* `docs/capstone/pitch/questions-and-answers.md`, `speaker-script.md`: regenerated (hash line; Q&A lines for the five changed notes).
* `docs/capstone/source/validation.json`: candidate, builder, preview PDF, speaker script and Q&A hashes from actual files; scope note extended. Manifest, catalog and native helper hashes unchanged.
* `docs/architecture/README.md`: sensor-ingestion paragraph now separates the 14 October baseline from the 8 November source-coded chain; no live deployment claim.
* `docs/reference/README.md`, `docs/reference/log.md`: current 55-slide row and numbering, `ms.date`, appended log entry. The dated 2026-10-29 54-slide entry is retained as history.
* `docs/capstone/source/diagrams/discovery-journey/text-equivalent.md`: R09 anchors `#L33`, `#L253`, `#L327` (verified against actual headings).

## Verification (logs external, scratch `/tmp/ama-pr1295-c3`)

* Fail-before: old function fails 4 of 6 literal cases; new passes all.
* Package proof: 303 unique members, 55 slides, 55 non-empty reciprocal notes, 108 actions with every `r:id` and destination equal to baseline, presentation order, sldIds and sections equal baseline plus the inserted S11A, protected cost slides and notes byte-equal, only five notes differ.
* Duplicate ZIP entry (304 entries, 303 names): Verify exit 1, "Package member set differs".
* Verify (candidate and delivered) exit 0; Test-DeckInsertion (source and candidate) exit 0; Test-CostStatus exit 0; Test-NativeShapes 32 checks; Test-SourceHashes exit 0; render_preview pytest 10 passed; journey, architecture and technical `--check` exit 0; node architecture and geometry tests exit 0.

## Adverse records retained

* Test-DeckInsertion first run exit 1 (PowerShell array unrolling in my table; fixed with commas).
* Package-proof script had two harness bugs (`/>` serialization, sldId comparison); not package defects.
* Test-CostStatus first call omitted the mandatory `-CandidatePath` (exit 1); rerun exit 0.
* First duplicate-ZIP fixture attempt failed in the generator (BadZipFile) and was rebuilt.

## Divergences and frozen items

* Frozen for owner decision: `docs/capstone/demo/runbook.md:109` baseline page numbers; QX manifest sentence "All 54 page numbers" (`slides.json:3029`, protected manifest, hash unchanged).
* Native PowerPoint, visual, assistive-technology, owner-notch, rehearsal and live approvals remain unproven; no all-55 human acceptance claim.
