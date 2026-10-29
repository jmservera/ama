---
title: Owner manual Q and A navigation review
description: Read-only review of HEAD-parent, committed, and uncommitted Cowork v2 PowerPoint changes.
date: 2026-10-28
---
<!-- markdownlint-disable-file -->

## Result

* Review complete. The requested question-index -> numbered answer -> question-index loop is structurally correct for all 27 questions. No dangling package relationships, wrong question destinations, lost slides, or new visual-layout defects were found.
* The commit activates navigation rather than adding the visible numbering: the B01-B27 labels, slide numbers, question index, answer content, and layout already existed in HEAD^.
* One new behavior/label warning affects every answer: "Return to caller" now always goes to index slide 27, not the last slide viewed. The existing presenter notes still promise the old behavior.
* The uncommitted file has eight changed ZIP entries but no additional question, navigation, layout, slide-order, or note-wording change. These changes are consistent with an Office save/proofing/view-state update.
* No original PPTX, existing YAML, docs, git index, commit, branch, or remote was modified. No rebuild or save was performed.

## Provenance

Source: `D:\ama\docs\capstone\deck\zava-forward-cowork-v2-draft.pptx`.
Branch: `jmservera/feat-presentation-qa-navigation`; no PR supplied.

| Version | Git revision | Bytes | SHA256 |
|---|---|---:|---|
| Before manual change | HEAD^ `e5f5eb51a7b3a84da7d052c82b802850ee2544d1` | 2618212 | `cff879250b4acf866859f7f259b12aecb0b731cca02e940d5cea8a33598b2577` |
| Committed manual change | HEAD `81e94efcf164e0a497e53dfb73c0a9e1e82ba62f` | 2397137 | `3221b2a485ddb9d4fc4477c0ab5f63fa36fa78d73a3a627838c5c4deac8aac6b` |
| Working manual change | Uncommitted working file | 2397249 | `2bab9b79de4352a1915dab04d1846a4c4be90f6889a2b9b6af4807e48a33d5f8` |

* Git blob bytes were hashed directly with `git show`, confirming the before and committed snapshots. The working snapshot hash matches the original working file.
* All three snapshots are in external scratch: `C:\Users\juanserv\.copilot\session-state\9980ca66-d38f-4f63-8e1d-bc92df820fc5\files\ppt-qa-review`.
* Comparison resolves `presentation.xml` slide IDs through presentation relationships before assigning displayed positions. All three have the same 54 stable IDs in the same order. Only after resolving these was it established that `slideN.xml` happens to be displayed position N in these files.

## Three-way delta

### HEAD^ -> HEAD

* 136 ZIP entry differences: 128 modified, 3 added, 5 removed. These are not 136 substantive edits.
* Slide 27: 27 existing shapes `Index B01` through `Index B27` gain shape-level click actions, each targeting its matching numbered answer.
* Slides 28-54: 27 existing `Footer navigation` shapes gain fixed links to slide 27.
* Slides 28-54: 27 existing `Return to interrupted calling slide` shapes change from `ppaction://hlinkshowjump?jump=lastslideviewed` to `ppaction://hlinksldjump`, with a slide relationship targeting slide 27.
* The 27 existing `Appendix topic destination` fixed links remain unchanged. No link-bearing shapes were added or deleted: 54 new click actions and 27 changed actions produce 108 current actions versus 54 before.
* No displayed slide text, order, shape IDs, z-order, or shape transforms changed. Notes on positions 7, 8, 13, 15, 22, and 51 have whitespace-only text differences; no note wording changed.
* Remaining changes: relationship/media renumbering and deduplication, removal of two unused image relationships/assets, empty text-run/empty-description cleanup, proofing/extensions, document/view metadata, and cached master/layout date fields refreshed from 24 to 28 October. No new media content was introduced. The two removed distinct assets had no XML use of their relationship IDs.
* Normalizing media references by content hash, excluding hyperlink actions, and ignoring Office-only/empty-run metadata leaves zero residual slide visual-XML differences. Shared master/layout differences are automatic date-field cache refreshes, not a design change.

### HEAD -> working file

* Exactly eight modified ZIP entries; none added/removed:
  * `docProps/app.xml`: total editing time.
  * `docProps/core.xml`: revision and modification timestamp.
  * `ppt/viewProps.xml`: editor view state.
  * `ppt/slides/slide9.xml` and `slide40.xml`: `dirty="0"` proofing flags.
  * `ppt/notesSlides/notesSlide14.xml`, `notesSlide22.xml`, and `notesSlide40.xml`: proofing flags, spelling markers, text-run segmentation, and end-paragraph formatting metadata.
* No slide text, note text, navigation target/action, media content, geometry, shape membership, z-order, or slide sequence change. Note part filenames are package identifiers, not displayed slide numbers.

## Findings and recommendations

| ID | Severity | Origin | Positions and shapes | Finding |
|---|---|---|---|---|
| N1 | warning | New in HEAD; unchanged working | 28-54, `Return to interrupted calling slide`, visible label `Return to caller` | All 27 buttons now jump to fixed index 27. This meets the requested index loop, but no longer returns to an arbitrary interrupted main slide. Example: enter B01 at 28 from main slide 10; this button targets 27, while its separate `Topic: S04 / slide 4` button targets 4, not 10. If the intended behavior is index-only, a future edit should relabel it `Back to questions`. If caller-history behavior must also remain, keep that as a distinct Last Slide Viewed action rather than conflating the two. No fix applied. |
| N2 | warning | Newly inconsistent in HEAD; text pre-existing | Notes on 28-54 | All 27 still say `Return to caller uses Last Slide Viewed to resume the interrupted main slide`. That instruction no longer matches OOXML. A future owner-authorized edit should align notes with the chosen navigation behavior. |
| N3 | info | Pre-existing copy; now stale after HEAD | 27, speaker notes and navigation footer | Notes still instruct the owner to add clickable internal links, and visible navigation instructions mention only typing a slide number plus Enter. The hyperlinks now exist; presenter guidance can acknowledge clicking as well as numeric jumping. |
| N4 | info | Pre-existing; unchanged | 26-54, geometry-check locations in scratch JSON | Automated geometry reports 347 warnings and 12 informational findings, zero errors. Results are exactly identical before and working. They include intentional full-bleed picture/scrims, near-edge top navigation, and compact gaps. Native renders show no new overlap/cutoff. These raw heuristic counts are not new navigation defects or accessibility acceptance. |
| R1 | warning | Source-rebuild risk, not a new deck defect | Extracted YAML for 27-54 | The skill extraction retains text, geometry, styles, and notes but emits no hyperlink/action fields for these shape-level actions. A YAML rebuild would not preserve these 108 navigation actions without explicit implementation and revalidation. Keep the manually edited PPTX and the navigation map as preservation evidence. |

No error-severity structural/navigation finding. N1 and N2 are related consequences of the same intentional fixed-index change, not separate broken destinations.

## Exact navigation invariant to remember

* This is the 54-slide Cowork v2 deck, not the historical 22-slide deck.
* Displayed slide 27 is the single question index, stable slide ID `4027`.
* For every integer n from 1 through 27, question `Bnn` on slide 27 targets displayed slide `27 + n`; that answer's visible B-number and the index's printed slide number must agree.
* Every answer's `Footer navigation` and currently labeled `Return to caller` must target fixed index 27 for the owner-requested index round trip. Current actions are fixed slide jumps, NOT Last Slide Viewed.
* Each separate `Topic:` button retains its fixed main-route destination listed below. A topic destination is not the question index and is not caller history.
* After insertion/reordering, re-resolve by stable slide ID and revalidate printed numbers; do not assume part filenames equal displayed positions.

## Complete question navigation map

All rows originate on index 27. `Back` applies to BOTH `Footer navigation` and `Return to interrupted calling slide`. `Topic` is the distinct `Appendix topic destination` button. All 27 printed question numbers, answer B-labels, 54 back links, and 27 topic-label/target pairs passed.

| Question | Index shape ID | Answer position | Answer stable ID | Back | Topic position |
|---|---:|---:|---:|---:|---:|
| B01 | 20975 | 28 | 4246 | 27 | 4 |
| B02 | 21175 | 29 | 4466 | 27 | 12 |
| B03 | 21196 | 30 | 4687 | 27 | 9 |
| B04 | 21070 | 31 | 4909 | 27 | 16 |
| B05 | 21085 | 32 | 5132 | 27 | 21 |
| B06 | 21316 | 33 | 5356 | 27 | 13 |
| B07 | 21343 | 34 | 5581 | 27 | 20 |
| B08 | 20980 | 35 | 5807 | 27 | 6 |
| B09 | 20986 | 36 | 6034 | 27 | 11 |
| B10 | 21218 | 37 | 6262 | 27 | 19 |
| B11 | 21241 | 38 | 6491 | 27 | 16 |
| B12 | 21020 | 39 | 6721 | 27 | 8 |
| B13 | 21031 | 40 | 6952 | 27 | 22 |
| B14 | 25950 | 41 | 7184 | 27 | 9 |
| B15 | 25824 | 42 | 7417 | 27 | 24 |
| B16 | 21526 | 43 | 7651 | 27 | 20 |
| B17 | 20993 | 44 | 7886 | 27 | 23 |
| B18 | 21560 | 45 | 8122 | 27 | 25 |
| B19 | 26092 | 46 | 8359 | 27 | 19 |
| B20 | 25767 | 47 | 8597 | 27 | 15 |
| B21 | 21371 | 48 | 8836 | 27 | 20 |
| B22 | 21400 | 49 | 9076 | 27 | 19 |
| B23 | 21430 | 50 | 9317 | 27 | 13 |
| B24 | 26019 | 51 | 9559 | 27 | 3 |
| B25 | 21101 | 52 | 9802 | 27 | 21 |
| B26 | 21118 | 53 | 10046 | 27 | 21 |
| B27 | 25885 | 54 | 10291 | 27 | 21 |

* Index visual grouping is deliberately not B-number order. Group membership and placement did not change.
* Recursive inspection included grouped shapes and text-run links. All 108 current actions are shape-level clicks; none are grouped-child links, text-run links, mouse-over actions, or external URLs. No additional actions were found in masters/layouts/other XML parts.
* Before: 27 Last Slide Viewed actions plus 27 fixed topic links. Current: 108 fixed internal slide jumps, zero Last Slide Viewed actions. No dangling relationships in any snapshot.

## Remaining slide order

Combined with index 27 and answer positions 28-54 above, this is the complete unchanged 54-slide sequence. Titles below are shortened identifiers, not proposed edits.

| Position | Stable ID | Content |
|---|---:|---|
| 1 | 10492 | More homes ready |
| 2 | 10694 | 15,600 homes to lift by 2030 |
| 3 | 10897 | Three clocks |
| 4 | 11101 | Homes stall between teams |
| 5 | 11306 | EPC C forecast, first build |
| 6 | 11512 | EPC C forecast, second build |
| 7 | 11719 | Six weeks of product work |
| 8 | 11927 | People who move a home forward |
| 9 | 12136 | Challenging the brief |
| 10 | 12346 | Prototype learning |
| 11 | 12557 | Stress-tested economics |
| 12 | 12769 | Meet the Workbench |
| 13 | 12982 | One-home service blueprint |
| 14 | 13196 | Backlog and epics |
| 15 | 13411 | Spreadsheet adoption |
| 16 | 13627 | Five assistants, one workbench |
| 17 | 13844 | Three security boundaries, first build |
| 18 | 14062 | Three security boundaries, second build |
| 19 | 14281 | Three security boundaries, third build |
| 20 | 14501 | Seven checkpoints |
| 21 | 14722 | Model inference and accepted value |
| 22 | 14944 | Everything But the Software |
| 23 | 15167 | Validate, pilot, scale |
| 24 | 15391 | Fund the validation gate |
| 25 | 15616 | One-home demo |
| 26 | 15842 | Close: more homes ready, control intact |

## Extraction and validation evidence

* ZIP CRC integrity passes for all three snapshots; all package-internal relationship targets exist.
* `validate_deck.py` passes on all three: 54 slides, all have speaker notes, zero property issues. No historical YAML count was used.
* `extract_content.py --resolve-themes --slides 27,...,54` produced 28 slide YAML files and a global style under external scratch `extracted-working`. The destination was new, not an overwrite of stale extraction. All files parse and have element lists and notes. Style includes 13.333 x 7.5 dimensions, Arial typography, resolved theme colors, and light/dark slide groups. Element-level styling is expected in this extraction; it is not a new defect. Extracted `title` metadata is empty because these are manually positioned title shapes; visible titles remain in elements.
* Native PowerPoint 16.0 COM was available. Opened snapshots with `ReadOnly=-1`, no window, macros disabled; exported images only; closed only review presentations without Save/SaveAs. Exported working slides 26-54, including one preceding neighbor; slide 54 is the end so no following neighbor exists.
* Also exported before/committed slides 27 and 28. Their decoded RGB pixels are exactly identical across before, committed, and working snapshots: link wiring changed, appearance did not.
* Native image filenames match displayed positions: `native-render-working\slide-026.jpg` through `slide-054.jpg` at 2000 x 1125. All 29 were visually inspected in five contact sheets; 27, 28, and 51 also inspected at full size. Index is dense but readable; no new cutoff, overlap, footer collision, or broken title-wrap treatment observed.
* Per-slide disposition: 26 has intentional full-bleed geometry warnings; 27 has N3 presenter-copy caveat; every slide 28-54 has N1/N2 return-label/note caveats. No additional slide-specific visual defect found in this targeted block.
* Geometry checks on 26-54 are exactly identical before and working: zero errors, 347 warnings, 12 info. The validator's top-level `slide_count: 54` describes the source deck; its `slides` list has the 29 requested positions.
* LibreOffice and pdftoppm unavailable; no installation attempted. Used native PowerPoint export instead of the uv-based pipeline. No deck/image upload or external vision service was used.
* Limits: structural OOXML inspection and local native export are NOT actual interactive Slide Show testing, keyboard/screen-reader accessibility acceptance, PDF-viewer link acceptance, or presenter rehearsal. Those remain owner checks. Property validation checks note presence, not the correctness of navigation wording.

## Preservation and next actions

* Retain the owner's PPTX as the current navigation source. Historical 2026-10-14 YAML is a different 22-slide deck, "Back the evidence. Keep the resident promise."; it was not read, synced, or rebuilt.
* Do not treat this targeted 28-slide extraction as a complete rebuild source. Shape-level actions are missing from extracted YAML. A future rebuild must explicitly preserve/recreate the 108-action map, keep all 54 slides, and repeat stable-ID/printed-number tests. Template-only builds discard original slides; they do not preserve these manual edits.
* Owner decision, not a blocker to this review: should `Return to caller` be renamed to clarify fixed index return, or should separate true caller-history functionality remain? Rehearse entry from the index and from an arbitrary main slide to make that distinction explicit.
* Machine-readable evidence: `manual-navigation-review.json`. Execution details: `..\changes\review-2026-10-28.md`. Bulky OOXML, extraction, validators, and images remain in the explicit external scratch directory.
