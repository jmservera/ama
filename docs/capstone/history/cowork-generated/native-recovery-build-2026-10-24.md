---
title: Native Cowork Cost Recovery Build
description: Execution log and handoff for the six-slide native cost recovery
ms.date: 2026-10-24
ms.topic: reference
---
<!-- markdownlint-disable-file -->

## Task and Status

Task: build-deck, export and validate the owner's existing 54-slide native
presentation. Status: complete for requested artifact generation and scoped
validation; independent presentation acceptance remains outstanding.

Branch `docs/capstone-cowork-story` was reused. Staged and unstaged changes
were preserved. No stash, reset, branch switch, commit, push, deployment,
inference, issue update or spending activation was performed.

Inputs: the current `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`,
the six-page map in `COWORK-BRIEF.md`, and the recovered calculations in
`evidence/ai-cost-evidence.md`. The 18-slide source inventory and older YAML
decks were not used to reconstruct the 54-slide deck.

## Method and Execution

* Loaded the PowerPoint builder and native PPTX editing skills. Verified native
  PowerPoint 16.0 through Windows COM; zero presentations were initially open.
* Authored `content/recovery.json`, a JSON content manifest, and
  `Invoke-Recovery.ps1`. This is an intentional exception to the generic YAML
  shape-rebuild pipeline: native package editing preserves the owner-selected
  layouts, themes, charts, sections, media, relationships and return actions.
* Copied original PPTX/PDF into `slide-deck/original.pptx` and `original.pdf`
  before building. Updated only slide parts 6, 11, 21, 32, 36 and 52 and their
  six notes. Existing main-route TIMING lines were retained.
* Initial validation caught a malformed script help-comment delimiter; fixed
  before any deck edit. First native PDF export rejected the two-argument COM
  `ExportAsFixedFormat` call; native `SaveAs` PDF format 32 succeeded.
* Native rendering exposed slide 11 number wrapping and slide 32 formula/ledger
  overlap. Shortened chart labels with a shared GBP axis and moved the formula
  into the free right column. Native text bounds then caught slide 6 grant-tile
  wrapping; shortened its label without removing conditional wording.
* Rebuilt and rerendered after repairs. No font family substitutions were made;
  selected font sizes were adjusted to fit existing native geometry.
* Exported a 54-page PDF and 18 native 1600 x 900 PNG previews covering every
  changed slide plus one predecessor and successor. Inspected all six changed
  slides individually and the adjacent-slide contact sheet. Generated full
  54-slide, six-changed-slide and 18-adjacent-slide contact sheets from the PDF.
* Used isolated `uv run --no-project --with ...` dependencies for PDF/image and
  skill property validation; did not modify the repository environment metadata.
* Confirmed canonical originals still matched the saved originals, then copied
  the validated PPTX/PDF into the requested canonical paths.

## Changes by Page

| Page | Restored content |
| --- | --- |
| 6 | USD 6,873 whole-cohort inference scenario; GBP works and conditional grant remain visibly separate |
| 11 | GBP 6,082/home works benchmark and conditional GBP 3,041/home grant; separate fictional package and other sensitivities retained |
| 21 | USD 0.44/home inference scenario, assumed task/token/rate inputs, USD 6,873 cohort, doubled USD 0.88/home, unknown accepted cost |
| 32 | Preserved dated ledger; separate P + USD 6,872.9856 future appraisal and planned-home denominator; no envelope double count |
| 36 | Exact works/grant calculation plus evidence-pack explanation; fictional GBP 20,000 base, GBP 22,000 envelope and cash-flow arithmetic retained |
| 52 | Exact token and inference workings; accepted-outcome TCA unknown; money/request controls remain proposed and not run |

All six notes include source IDs, assumptions and limitations. Funding notes
retain the eligible home/measure, assessment, cost/completion evidence,
application, award, claim and cash chain. Historical secondary pricing dated
2026-10-23 is not a verified current deployment price. No full-project TCO,
guaranteed grant, additional income, saving, payback or issue #435 acceptance
is established.

## Validation Evidence

* `slide-deck/package-validation.json`: pass; 54 slides, 54 note parts, all
  27 Last Slide Viewed actions. Only the 12 intended slide/note parts differ;
  every other ZIP member is byte-identical, including presentation order,
  sections, relationships, masters, media and unchanged slides/notes.
* `slide-deck/validation/deck-validation-results.json` and report: builder skill
  `validate_deck.py`, zero issues across 54 slides; all notes present.
* `slide-deck/validation/pdf-arithmetic-validation.json`: 54 PDF pages, restored
  text checks pass, exact Decimal arithmetic pass, all 54 note parts nonempty,
  27 PDF static links and a PDF structure tree present.
* `slide-deck/validation/native-navigation-validation.json`: native PowerPoint
  readback confirms all 27 caller buttons use `ppActionLastSlideViewed` (5).
* `slide-deck/validation/delivery-validation.json`: delivered canonical bytes
  equal the validated pair; hyperlink elements match on all 54 slides, and
  presentation section/order metadata is unchanged. New local links resolve.
  Four historical broken links in the append-only knowledge log and existing
  Markdown diagnostics in the knowledge index/log were left unchanged.
* `slide-deck/validation/native-text-bounds.json`: changed text fits after
  repairs. Unchanged slide 6 shape 27758, the large `88`, reports a 3.25 pt
  width excess; its native preview is visibly intact and it was not edited.
* `slide-deck/validation/slide-NNN.png`: native previews for 5-7, 10-12, 20-22,
  31-33, 35-37 and 51-53. `contact-changed-six.png`,
  `contact-adjacent-18.png` and `contact-all-54.png` are current contact sheets.

Reproduce the package build/check from the repository root:

```powershell
pwsh -NoProfile -File .copilot-tracking/ppt/2026-10-24/cowork-cost-recovery/Invoke-Recovery.ps1 -Action Build -RepoRoot /home/jmservera/source/ama
```

Native rendering uses that script's `Render` action under Windows PowerShell,
with `RepoRoot` set to the WSL Windows/UNC path. The script closes only its own
candidate presentation and does not quit the user's PowerPoint application.

## Delivered Files

* `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`
  SHA-256 `39659a3ad9974f802a8418177a9ca0ca8daf7478e71cd82d04cd7677d9ad2cc0`
* `docs/capstone/deck/zava-forward-cowork-v2-draft.pdf`
  SHA-256 `b816f3f2282ffad4e0afd41cc39ba76a6871bc62c2292c5a62129a4864bd9a9c`

Also modified presentation status in `COWORK-BRIEF.md`, the source handoff
README, the generated-output README, the dated correction record, the knowledge
index and append-only knowledge log. Earlier adverse findings remain intact.

## Remaining Gates

Native COM rendering, property checks and visual inspection are scoped artifact
checks, not an independent storytelling review, timed rehearsal, interactive
keyboard/screen-reader test, projection test, accessibility conformance,
Finance/funder approval, current primary-price verification, live-system
acceptance, hosted score or publication clearance. Native history-sensitive
return actions are not equivalent PDF behavior; PDF readers retain static
topic links or their own history. No independent vision/model invocation was
performed. The LibreOffice-dependent aggregate pipeline was replaced with
native PowerPoint rendering and the skill's property validator, not reported
as a completed LibreOffice pipeline. Parent/owner should conduct independent
visual/storytelling review and the normal approval gates before external use.
