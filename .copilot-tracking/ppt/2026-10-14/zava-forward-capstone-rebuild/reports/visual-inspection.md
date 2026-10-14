---
title: Local rendered-asset inspection
ms.date: 2026-10-14
status: complete
---
<!-- markdownlint-disable-file -->

# Inspection method and scope

Inspected the actual fresh LibreOffice 22-page PDF/JPG exports through four
generated contact sheets. Also opened individual 2000×1125 images for slides
11, 12, 13, 14, 15, 16, 19 and 22, focusing on dense, native-map, control,
proof, cash and comparison layouts. Reopened affected/final contact sheets
after repairs. This is the builder's local image inspection, not paid SDK
vision validation, a human PowerPoint session, rehearsal or formal
accessibility/product acceptance.

All image references below are under `../slide-deck/validation/`.

## Per-slide findings after repair

| Slide | Actual image | Severity/status | Inspection finding |
| --- | --- | --- | --- |
| 1 | `slide-001.jpg` | info, resolved | Decision panel body reduced from 28 to 25pt, not autofitted; complete acceptance-and-value wording fits. Dark-brand palette and boundary/footer clear. |
| 2 | `slide-002.jpg` | info | Five stage titles share top/reserved height; all body starts align. Accepted-home endpoint clearly separate. |
| 3 | `slide-003.jpg` | info | Rules/People/AI peers top-aligned, common body baseline. Research-instrument caveat legible. |
| 4 | `slide-004.jpg` | info | Three prerequisite cards align. Plus signs on their own lines are intentional text; control statement clear. |
| 5 | `slide-005.jpg` | info | KEEP/ADD title/body rows align on dark section; no implied delivered integration. |
| 6 | `slide-006.jpg` | info | Six-cell grid readable, row titles and body starts consistent; second-row wrapping fits. |
| 7 | `slide-007.jpg` | info | Native arrows confined to gutters; hold/return human-owner band and illustrative status retained. No completion badges or executed-home implication. |
| 8 | `slide-008.jpg` | info | Two peer titles and bodies align; separate consent/access and human hazard statements clear above footer. |
| 9 | `slide-009.jpg` | info | Source/decision/change trace peers align. Long Change body wraps without clipping. Policy boundary distinct. |
| 10 | `slide-010.jpg` | info | Source/case/people zones aligned. Arrows clear of words. Target/proposed integration status visible. |
| 11 | `slide-011.jpg` | info | Two-line main title is entirely rendered in reserved area; no lane-label collision. Proposal and domain lanes visibly distinct, all peer starts align. Lower lane extended for comfortable body fit. |
| 12 | `slide-012.jpg` | info | Observed and Still-to-prove rows align. Five calls/tokens/events and open authority/acceptance boundaries readable; provenance and synthetic-context footers do not collide. |
| 13 | `slide-013.jpg` | info, resolved | Native five-column map checked full-size. Shortened OFF labels no longer wrap into trigger bodies; assessor/coordinator owner now fits two lines. All stage/owner/title/request/trigger rows align and all words are visible. Core, funding/cash, hazard and OFF status legible; only picture is logo. Dense margins are intentional. |
| 14 | `slide-014.jpg` | info | Gross cash bar remains labelled before grant receipt; two subordinate scenarios align. Fictional status and application/award/claim/cash distinction unambiguous. |
| 15 | `slide-015.jpg` | info | Controlled-switch title renders over three lines while other headings use two. Reserved title block keeps **all four body starts identical**, with no collision; verified individually full-size. |
| 16 | `slide-016.jpg` | info | Programme and paired-task panels readable and aligned. No invented results chart; protected-outcomes strip clear. |
| 17 | `slide-017.jpg` | info | Four open gate cards share title/body starts. Second body wraps more but fits. Technical receipt is input, not approval. |
| 18 | `slide-018.jpg` | info, resolved | Executive cards align. Closing restriction moved upward after a 0.02/0.04in frame-only footer intersection was detected; final rectangles do not intersect and footer is clear. |
| 19 | `slide-019.jpg` | info | Two-line title and three assurance cards remain separated. All card text including longer Trust body is fully visible; Decision 1 separation readable. |
| 20 | `slide-020.jpg` | info | Four Q&A blocks readable and aligned by row. Increased card height for wrapped affordability answer; no overflow. |
| 21 | `slide-021.jpg` | info | Evidence-category peers align. Legal-currentness/pitch/Section-D boundaries clear. Long source-only footer remains in its own line. |
| 22 | `slide-022.jpg` | info, resolved | Retained original table removed through safe build hook. Entire option comparison now native editable boxes/text. Greenfield header rewrapped; all headers and cells fit, no old content visible. |

## Structural and rendering cross-checks

* All 311 nonempty native text frames render their expected words within
  their own frames (0.5pt tolerance); final failures: zero.
* Final text-frame rectangle intersections: zero; off-slide shapes: zero.
* All 56 peer rows have exact matching saved tops/heights/insets/fonts.
* All nonempty text frames are TOP-anchored and fixed size.
* Forest/cream and dark-on-moss/warm retain readable contrast in actual
  rendered assets. This is not a formal WCAG conformance claim.
* All 22 original-brand logo placements and counters present; current
  footers say 14 October and actual /22 indices.
* Default geometry heuristics still flag deliberate branding/footer edge
  bands and compact gaps. All 180 findings retained and classified in
  `shared-geometry-dispositions.json`; zero errors, zero unresolved local
  visual blocker. Generic checker is not claimed clean.

## Remaining limitations

Native PowerPoint may lay out fonts differently. Explicit installed Liberation
Sans avoids the local missing-Aptos fallback; parent/human native font review
remains appropriate. No model vision calls, real rehearsal, staff/human
acceptance, accessibility task acceptance, semantic evaluation or value
experiment was performed. The deck's exact claims remain tied to the adopted
repository receipt, not a newly inspected Azure environment.
