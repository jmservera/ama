<!-- markdownlint-disable-file -->
# Iteration 4 — evidence-led executive story

## Task and scope

Deck authoring, build and QA only, within this tracking workspace. The parent
owns published-file removal/replacement, catalog/log/scorer and independent
final review. No git operations, published deck edits or nested agents.
Direct Python / pip only; no uv or uv-managed pipeline.

## Grounding read

Original case, maintained addendum, reference README and memory, company
profile, agent-request challenge, pilot-measurement challenge and complete
capstone guide. Installed powerpoint skill, PPTX skill and shared PPTX
instructions read. Existing 21-slide YAML and evidence register inspected.

## Authoring completed

Rewrote main slides 1–17 as a customer-first argument:

1. 60,000-home mission and the five-agent request.
2. Eight role-agent instruments, explicitly not employee interviews.
3. Discovery reversal and three request/discovery/consequence/build chains.
4. Minimum shared foundation, not total company or operating-model replacement.
5. Owners, lifecycle states, timestamps, blockers, accepted handoffs and evidence.
6. Constructed one-home story, informed resident choice and actual capacity.
7. Inspectable decision trace: source/version/rule/reason/reviewer/event/override.
8. System context and controlled action flow, native editable shapes/connectors.
9. AI authority boundary, honest fictional cash, supported Excel transition.
10. Separate programme and AI contribution tests, named-owner gates and limited ask.

Removed current-review assertions from appendix 20. Prior reviews remain
historical and do not approve iteration 4. Technical/objection/options appendices
retained as on-demand material. Main architecture sources now feed the workbench
left-to-right; workbench output serves people/reporting, not source authorities.

## Build and QA

First build: direct installed build script succeeded, 21 slides. Installed
PPTX properties and default geometry validators each reported zero issues.
PowerPoint COM export produced slide-001.jpg through slide-021.jpg at 1600×900
in slide-deck/validation-iteration-4.

Visual bug hunt found issues the structural validators cannot detect:

* Error: card text overflow on slides 4, 7, 10, 14 and 17.
* Warning: dense/tight or marginal card text on slides 3, 9, 11, 13 and 16.
* Error: slide 5 displayed literal `\n` because of single-quoted YAML strings.
* Warning: card first paragraphs were centered by default, inconsistent with
  left-aligned body text throughout the rewritten main slides.
* Planning warning: first main narration was 1,976 words, above the 1,950 target.

Fixed by shortening visible copy, making card alignment/line-spacing/padding
explicit, reducing card sizes to readable 19–24pt where required, correcting
YAML escapes and trimming narration. No validator thresholds were relaxed.
Second build and full image review resolved all listed card issues. An additional
PowerPoint rendered-text containment check found two textboxes with bounds
larger than their declared boxes (slide 5 title; slide 17 closing line), even
though the images remained legible. Corrected their height/font size while
preserving default geometry spacing.

## Final observed verification

**Status: complete for authoring/build/QA scope.**

* Final output: `slide-deck/proper-warm-executive-draft.pptx`.
* 21 slides: main 1–17, on-demand appendix 18–21.
* Main spoken script: **1,920 words**, approximately **13.71 minutes at 140 wpm**.
  Appendix: 543 words. Count uses word tokens in notes before `Evidence:`,
  excluding source references and the explicitly non-spoken demo/recovery cue.
  This is a planning estimate; no timed oral rehearsal is claimed.
* Installed `validate_geometry.py`: **0 errors, 0 warnings, 0 info** across 21
  slides, with unchanged defaults: 0.5-inch margin, 0.3-inch gap, 0.2-inch clearance.
* Installed `validate_deck.py`: **0 errors, 0 warnings, 0 info** across 21
  slides; count and required speaker notes verified.
* PowerPoint rendered-text containment: **0 findings** across all 21 slides.
  Check compares real rendered text bounds with its owning shape, tolerance
  one point. Concurrent COM read/export initially produced a cleanup
  `Presentation.Close: Object does not exist` error after reporting zero;
  repeated serially and completed with exit 0. Final export and artifact unaffected.
* All 21 1600×900 images refreshed, exact names `slide-001.jpg` through
  `slide-021.jpg`; six contact sheets refreshed from those images.
* Direct image review completed across all slides; fix-and-verify included
  adjacent slides. Final changes 5/17 rechecked with 6–8 and 18–20.
* 152 native editable PowerPoint shapes; zero picture shapes. Diagrams are not
  flattened screenshots. Main YAML and generated PPTX text agree.
* No literal newline escape, lorem/ipsum/xxxx placeholder text found.
* SHA-256:
  `b48462222c5aec9d3f49c747ea373683c784b7f36aa84460bc3fcdfb8f156130`.

### Final visual disposition

| Slide | Final finding / disposition |
|---|---|
| 1 | No remaining issue; mission opening and request remain legible. |
| 2 | No remaining issue; five request cards fit with consistent left alignment. |
| 3 | Dense first-pass wording simplified; no remaining card overflow. |
| 4 | First-pass chain overflow fixed; all three causal chains readable. |
| 5 | Literal escape and title containment fixed; thesis/cards clear. |
| 6 | No remaining issue; six work-contract fields aligned and readable. |
| 7 | Overflow fixed; all four one-home stages and exception are visible. |
| 8 | No remaining issue; resident choice and capacity remain separate. |
| 9 | Tight card copy shortened; all trace fields retained. |
| 10 | Overflow fixed; source → workbench → people/report arrows correct. |
| 11 | Tight nodes simplified; AI returns to staff, action flows through API. |
| 12 | No remaining issue; selection/generation and authority boundary clear. |
| 13 | Cash card overflow fixed; fictional labels and conditional net funding clear. |
| 14 | Overflow fixed; four supported transition stages readable. |
| 15 | No remaining issue; programme and AI comparisons remain distinct. |
| 16 | Tight gate copy simplified; named role owners retained. |
| 17 | Card overflow and closing-text containment fixed; limited ask clear. |
| 18 | No remaining issue; on-demand technical assurance caveats legible. |
| 19 | No remaining issue; alternatives and reversal conditions retained. |
| 20 | No remaining issue; historical review no longer presented as current approval. |
| 21 | Dense by design, on demand; full-size table readable, no clipping. |

Visual findings above are direct image review, not Copilot SDK vision-model
results. The uv-managed pipeline and SDK vision step were not run; installed
Python validators and the requested PowerPoint exporter were used instead.
No outstanding authoring/geometry/PPTX/render blocker remains.

## Files changed and generated

Modified: `content/slide-001/content.yaml` through `slide-017/content.yaml`,
`content/slide-020/content.yaml`, `content/global/style.yaml`,
`research/primary-research.md`, `research/evidence-register.md`.
Created: this iteration-4 execution log and
`slide-deck/validation-iteration-4/` property/geometry JSON and reports,
per-slide check JSON, 21 exported JPGs and six contact sheets.
Rebuilt: `slide-deck/proper-warm-executive-draft.pptx`.

No published file, scorer, docs catalog, knowledge-base log or git was changed.

## Open decision evidence

Measured benefit, current-state baseline, whole-life cost, real user acceptance,
production assurance, formal owner authority and timed oral rehearsal remain
open. Independent final narrative review is the parent's next task.

## Independent review and publication follow-through

The independent AMA Presentation Communications Strategist review in
`research/subagents/storytelling-review-iteration-5.md` passed the narrative
and all 21 rendered slides without blockers. Applied its three precise
editorial findings: restored "application" in the original funding ask,
named assisted versus usual delivery explicitly in the programme comparison
and its notes, and removed binary/three-class detail from the main narration.
The detailed task-fit limitation remains in the evidence register.

Rebuilt and exported again after those edits. Both installed validators
report zero issues across 21 slides; reviewed the amended slide 2 and slide 15
images directly. The final spoken main notes contain 1,919 word tokens before
`Evidence:`, about 13.71 minutes at 140 words/minute; this remains an estimate,
not a rehearsal. Updated `research/final-pptx-text-and-notes.md` using the same
extractor as the rubric, then verified expected decision-trace, application
and comparison text is present in the published package.

Published only `docs/capstone/deck/proper-warm-executive-draft.pptx`, with
SHA-256 `bb857cb474ad03c38a29c26af052556a4933ef6cdf762cd6bf0eaa53862d2e03`,
identical to the final working build. Removed the owner-requested duplicate
from `docs/presentations/` after closing only that already-saved PowerPoint
presentation. The separate mentor deck was not changed.

The capstone is detected by the registry. The scorer repair is separate:
positive `:slideN` PPTX citations now resolve to the changed file. Ordinary
PR runs still load the gate from `main` until owner-approved merge; no live
score file has been manually altered or fabricated.
