---
title: Capstone Authoring Source
description: Complete native-template and JSON editing contract, retained media and technology-decision evidence
ms.date: 2026-11-08
ms.topic: how-to
---

## Source Authority

| Input | Responsibility |
| --- | --- |
| [baseline.pptx](./baseline.pptx) | Immutable snapshot of the actual owner-supplied 54-slide deck at this reorganization; native layouts, sections, media, relationships and untouched content |
| [slides.json](./slides.json) | All 55 ordered records/notes, immutable baseline mapping, the added main-route deployment slide, exact text/bounds corrections and current narration |
| [assets/catalog.json](./assets/catalog.json) | Captured media in `media`; future-logo, journey and architecture projections in `additional_media`, with exact usage and SVG/native/PNG hashes |
| [assets/media](./assets/media/) | All 36 original embedded media files, not flattened pictures of whole slides |
| [Official product icons](./assets/official/README.md) | Fabric and Power BI source SVGs, native PNG derivatives, permitted-use guidance and archive provenance |
| [DT resident journey](./diagrams/discovery-journey/text-equivalent.md) | Editable Excalidraw, same-geometry SVG/PNG, deterministic generator and provision-linked method/pain/gain/decision trace |
| [Application and Azure architecture views](./diagrams/architecture/text-equivalent.md) | Original CxO Excalidraw for main page 12; full deployment frame on new main page 13; complete Bicep-grounded Azure source plus core frame for B10/page 38; native renders, generator, icon rights and explicit trust/acceptance limits |
| [Invoke-Capstone.ps1](../../../tools/capstone/Invoke-Capstone.ps1) | Current ExportSource, Build, Verify and native Render entry point |
| [Native shape helper](../../../tools/cowork-native-recovery/Invoke-StoryReview.ps1) | Existing XML/native-shape functions used by the current builder; its historical standalone workflow is not the current build command |
| [validation.json](./validation.json) | Compact delivery/verification receipt, not another build input |

The baseline hash is pinned in the manifest. The delivered PPTX is an output,
never an implicit fallback input. A complete rebuild needs the native baseline,
JSON, catalog, all referenced media and both scripts above. The old 18-slide
authoring inventory does not recreate the current deck.

### Single Added Main-Route Slide

Schema 2 inserts `S11A` at physical page 13, immediately after `S11`.
`number` is the current physical position, `part_number` is the stable
OOXML slide/notes part identity, and `baseline_number` selects the immutable
template. Existing parts 1-54 keep their names, IDs, actions and destinations;
new part 55 uses template 12. The builder supports only this declared insertion,
not arbitrary source packages or a new baseline pin.

The main route is pages 1-27, QX is page 28, and B01-B27 are pages 29-55.
Original pages 13-54 move one physical position without changing their codes.
The native product section includes the new slide. Original `TIMING` lines
remain source provenance; `CURRENT ROUTE TIMING` adds the operative 45-second
shift, giving 24:30 narration and 5:30 reserve in a 30-minute slot.
Financial graphics/arithmetic are untouched. Explicit index/topic/answer labels
are incremented without changing fonts, geometry or targets, including cost-page
footer numbers. Cost notes permit only the existing fixed status/navigation
corrections plus deterministic page-reference and current-route metadata;
no general cost-note edit permission is added.

## Current Autonomy and Product Story

The [CxO/story continuation](./review-2026-11-08-cxo.md) brings the architecture,
coded workflow and exact autonomy reasoning onto current main pages 9/12/15/17.
It aligns B04/B10/B19/B20 questions and corrects B27's stale "designed money
limits" wording against current source. A conceptual state-flow is not a
deployed LangGraph runtime, and prepared improvements do not demonstrate live
listening/composure or a higher score.

The [8 November review](./review-2026-11-08.md) records the exact requested
versus current autonomy, partial original task breadth, reactive/proactive
proposal surfaces, employee/resident follow-up channels and design-thinking
decisions. Decision 1 is historical #58 feasibility and a pending current
scoring rebuild, not the current five-helper generative engine. The optional
resident site is an added channel, not an original mandatory-portal request.

The review includes the fully retrieved dated Project 7 snapshot and a
refresh recipe. Update changing figures and source/live evidence before final
delivery; board Done includes not-planned work. Regenerate the deck and pitch
from the manifest, never by hand-editing the generated notes.

The later 8 November study update is on current pages 23/41 and their index
entry. It credits coauthor Isabel Cabezas Martin's execution/data collection
and distinguishes the OSF-registered base from the active unregistered
exploratory amendments. Selected 21/default 12, three models/five arms,
F1-F10 plus CR1 and all three implementation epochs are explicit.
Owner-reported completed steps are not independent replicates, a single
frozen implementation or newly reported efficacy results. The
[paper's current record](../thought-leadership/everything-but-the-software/README.md)
supersedes older paused/prospective status without rewriting its history.

## AI Consumption Evidence (#432)

The [dated source-only Tokenomics drafting insert](../../reference/resources/ai-tokenomics.md#pitch-drafting-insert-2026-10-31)
provides proposed slide/Q&A wording for the existing ledger extension, finite
dispatch limits, recoverable human review and billing-led accepted-outcome
report. It is not an applicable price, bill, measured cash value or live approval.
OD-51, actual reconciliation and an authorised held-out batch remain missing.

The old brief is now historical. Integrate approved wording through
`slides.json` and regenerate the deck/notes/question bank under this guide;
do not hand-edit generated pitch outputs or alter protected cost arithmetic.
This source-only delivery changes no generated deck, slide notes or rehearsal.

## Make An Edit

Edit [slides.json](./slides.json), selecting a record by physical `number`
and checking its `code`. Several main-story IDs have progressive build pages.

* `layout: baseline` retains native slide geometry from the pinned template.
* `layout: native` defines replacement content in `elements`, with retained
  header IDs in `keep_ids` and `headers`. Measurements are inches and points.
  Editable diagram primitives include `ellipse`, `roundRect`, `can` and `line`.
  A `polygon` has at least three `points` in 0-100 local coordinates; a `pie`
  has two distinct clockwise `angles` in degrees from 0 to less than 360.
  Optional `stroke`/`stroke_width` define a hex outline and its point width;
  `valign` is `t`, `ctr` or `b`. Invalid geometry, bounds or styles fail the build.
* `layout: text` makes uniquely matched text replacements; optional `box`
  changes only the identified frame bounds, not its native action target.
* `notes` retains the captured original. When present, `revised_notes` owns
  the current notes and takes precedence; original timing lines are retained.
* `sources` lists repository evidence required by a revision. A path is not
  proof that the underlying claim is current, approved or observed.
* `images` references catalog asset IDs with contained placement and alternative
  text. The builder preserves aspect ratio and verifies original/derived hashes.
  A journey asset's `source_native` and `source_native_sha256` also bind the
  editable Excalidraw; it is not replaced by a flattened image-only source.
* `content_date` dates generated pitch metadata; it is not legal or provider
  currentness verification.

Keep physical slide order, native link objects, source/version labels and
approval boundaries unless changing them is a separate explicit task.
New native layouts use the manifest and retained template headers. Change the
template pin only for a deliberate structural/template revision, never merely
because a generated content layout changes. Repeat validation for either case.
Do not silently re-export from the delivery file or replace the source JSON
with `ExportSource`: that initialization action starts from the 54-slide baseline,
not the current roadmap and prior content revisions.

Edit media only with a documented origin and reuse right. Update its catalog
hash deliberately and rerender every affected page. Asset extraction preserves
the supplied bytes, not an undocumented original photograph URL, generation
prompt, licence or subject consent. Those gaps are explicit in the catalog;
repository clearance is not universal new-publication clearance.

## Build And Review

Use the [root build commands](../README.md#rebuild). Every run writes to an
explicit external directory and checks:

* The pinned template, complete ordered manifest and every media input
* Exact expected package bytes: 293 captured baseline members plus six declared
  PNGs and four new slide/notes relationship members; four fixed metadata
  members declare the insertion without renumbering existing package parts
* All 55 nonempty note blocks, retained source timing lines and revised route windows
* Native navigation actions and unique shape IDs
* The six protected cost slides on pages 6, 11, 22, 33, 37 and 53; all financial
  evidence remains unchanged. Default protection permits only fixed
  navigation-note corrections. The owner-approved 8 November status-only
  revision permits a closed list of words/notes on baseline parts 21/52
  (physical 22/53), never calculations, other text, geometry or actions;
  current-route timing metadata does not change the original duration slots

The present baseline contains 108 fixed slide-jump actions. Preserve their
actual targets; neither their labels nor an older review establishes dynamic
Last Slide Viewed behaviour. Native viewer/keyboard interaction still needs
direct acceptance testing.

Native Windows Render produces a PDF and 55 PNGs plus measured text bounds.
The historical [Linux visual refresh](./review-2026-10-30.md#illustrated-visual-refresh-on-linux)
used the explicitly separate preview route below: all 54 pages rendered,
108 PDF jumps verified, all text present in 215 revised frames and the 40
untouched page renders pixel-identical to the Linux before-render.
These are not native PowerPoint bound metrics or accessibility acceptance.
Inspect changed pages and relevant neighbours, fix findings, and rerender.
The earlier
technology-page review had seven findings corrected. A later reader review
corrected inherited legal/forecast, navigation and demo-fallback passages and
opening inconsistencies. The legal-status page is the sixth visual revision.
The 29 October export had zero revised-text overflow and 264 inherited warnings.
The earlier 30 October roadmap export had zero revised overflow and 234 inherited warnings.
The earlier owner-corrected product/DT/future native export had zero revised overflow and 231 inherited warnings;
they are not erased or described as accessibility acceptance.

See the [dated review](./review-2026-10-29.md) for original findings and
qualitative coverage of all 20 criteria. Cost-slide graphics and arithmetic
remain unchanged; the historical note exceptions on baseline pages 32, 36 and 52 correct only
false Last Slide Viewed instructions. The builder checks that exact exception.

The [30 October review and owner correction](./review-2026-10-30.md) preserves
both the earlier candidate and the corrected product-first story. Page 8 explains
evidence -> hypotheses -> maps -> design/test; current page 14 shows the DT Coach's
resident journey. Pages 15-16 describe the built Workbench and bounded file/CLI
adoption. Fabric and Power BI are not current components: page 24 proposes
future history, measures and preview ontology context; page 25 separates current
verification, analytics comparison and an independent context experiment.
The [full proposal register](./roadmap-recommendations.md)
maps all 25 reviewed families into 22 grouped dispositions. This is not a
commitment to every option, a purchase or a new approved product requirement.

Captured `media.slides` records describe baseline usage; retained media can
remain necessary to reproduce the pinned baseline even when a revised layout
no longer displays it. `additional_media.slides` is verified against actual
generated relationships. Original 36 inputs remain unchanged. The two official
icons are placed only on future page 24. The DT journey is placed only on page
14; keep its native/SVG/PNG/generator/text-equivalent files together. The current
PNG is a local native `@excalidraw/cli` export of the editable 1600 x 560 scene,
not the earlier PowerPoint rasterization. No account or upload was used.
The slide owns its title, status and safety boundary; projected cell text is
20.2 pt and the proposed human-role labels are 15.4 pt. Page 40's complementary
value-proposition canvas uses editable native PowerPoint sectors and text.
Direct resident/staff and
projection/accessibility acceptance remain unperformed.

The architecture images are placed on pages 12, 13 and 38. Page 13 uses the
wide native `deployment` frame, including supporting services and gated options.
Page 38 uses the native `core` frame, not a scaled full poster.
Keep the complete Excalidraw/SVG/PNG, core/deployment derivatives, generator and text
equivalent together. Local Excalidraw CLI with existing Chromium generates
the PNGs; no account/upload or remote image model was used. The catalog pins
both source models and their exact derivatives. New package member names
reuse the builder's existing `roadmap-*` additional-media convention; this
internal prefix does not classify an architecture as future or deployed.
The full view's PaaS services are outside the VNet; production/background/
resident options remain distinct from the selected shared-API source view.

Build and Verify also generate current main-route speaker notes and appendix
Q&A under the run's `pitch/` folder. Publish the matching PPTX/PDF and those
two Markdown outputs together after review. Retain dated review evidence;
do not commit all temporary renders. The compact receipt binds the candidate
to the baseline, manifest, media catalog, builder and shared native helper.

The four text-source hashes use UTF-8 bytes of the manifest, media catalog and
two scripts with CRLF and lone CR normalized to LF. BOM and every other byte,
including significant whitespace and final newlines, are preserved; invalid
UTF-8 fails explicitly. The root `.gitattributes` already requires LF text
checkouts, so no additional rule is needed. Binary delivery, template and media
hashes remain exact, without normalization. Run Verify against the actual candidate and regenerate
the receipt from its successful report after any source change. Substituting
digests without verifying the source-to-delivery binding is not validation.

### Linux Preview

LibreOffice and Arial-compatible fonts are required. The preview refuses an
existing destination and never substitutes for the Windows Render action.
From the repository root, use a fresh external run:

```bash
Run="$(mktemp -d /tmp/ama-capstone-XXXXXX)"
python3 -m venv "$Run/venv"
"$Run/venv/bin/python" -m pip install -r tools/capstone/requirements.txt
pwsh -NoLogo -NoProfile -File tools/capstone/Invoke-Capstone.ps1 -Action Build -RepoRoot "$PWD" -OutputDir "$Run/build"
"$Run/venv/bin/python" -m tools.capstone.render_preview --input "$Run/build/zava-forward-cowork-v2-draft.pptx" --output-dir "$Run/preview"
```

The preview writes the matching PDF, 55 slide PNGs and a compact report with
source/PDF hashes. LibreOffice drops these slide-jump actions on import, so the
tool reads actual shape bounds, slide order and destinations from the candidate
PPTX, reconstructs the fixed PDF links, then verifies every destination and hit
region after saving. Differing destinations may not share a click region;
ambiguous overlaps fail before and after saving. The B04 index frame moves
up by 0.07 inch, retaining its font, height and destination while clearing B05.
Unsupported navigation fails explicitly; dynamic history
is never invented. Native PowerPoint viewing and direct keyboard/AT acceptance
remain separate checks.

Focused regressions:

```bash
pwsh -NoLogo -NoProfile -File tools/capstone/Test-NativeShapes.ps1 -RepoRoot "$PWD"
pwsh -NoLogo -NoProfile -File tools/capstone/Test-SourceHashes.ps1 -RepoRoot "$PWD"
pwsh -NoLogo -NoProfile -File tools/capstone/Test-DeckInsertion.ps1 -RepoRoot "$PWD" -CandidatePath "$Run/build/zava-forward-cowork-v2-draft.pptx"
PYTHONDONTWRITEBYTECODE=1 "$Run/venv/bin/python" -m pytest -p no:cacheprovider -q tools/capstone/test_render_preview.py
node docs/capstone/source/diagrams/discovery-journey/build-resident-journey.mjs --check
node docs/capstone/source/diagrams/architecture/build-architecture.mjs --check
node --test docs/capstone/source/diagrams/architecture/test-architecture.mjs
```

The current manifest explicitly names
`cost_status_revision: owner-approved-2026-11-08-status-only`.
The builder's fixed exception is absent by default and rejects any other
revision name. Verify compares the entire cost slide/note against only those
fixed substitutions and deterministic route metadata, and reports the exception instead of claiming all six
raw slide bytes are unchanged. Run the negative guards against a built candidate:

```powershell
./tools/capstone/Test-CostStatus.ps1 -RepoRoot $PWD.Path -CandidatePath "$Run/build/zava-forward-cowork-v2-draft.pptx"
```

The tests reject an unapproved revision, altered numeric text, geometry and
extra note words. This is authoring permission, not spend or operational
financial approval.

Use `Test-SourceHashes.ps1 -SemanticOnly` before regenerating the receipt.
Run its default mode afterward to check all four canonical source bindings and
the exact delivered PPTX hash against the verified receipt.

To regenerate a journey derivative, run the generator without `--check`, then
use `excalidraw render` locally with `--padding 0 --scale 1.5 --max-width 2400
--max-height 840 --fonts-url none`. Supply `--browser-path` if the existing
Chromium/Chrome binary is not on PATH. Render externally, inspect the result
and deliberately update all three catalog hashes before rebuilding.

## Technology Decisions

These are source-backed presentation explanations as of 2026-10-29, not new
ADR approvals, current provider-price checks or production acceptance.
"Not selected" describes this baseline, not universal product inferiority.

| Choice | Why / alternative not selected | Value And Revisit Test |
| --- | --- | --- |
| Shared Container Apps API | [ADR 0002](../../adrs/0002-pilot-readiness-architecture.md) favours fewer operating/state/retry boundaries; AKS and five independently deployed assistant workers add unproved operating need | Hypothesis: simpler controlled delivery. Split only for measured isolation, scale, long-running work or recovery requirements; page 38 |
| Azure SQL + Blob | [ADR 0002 data-store appraisal](../../adrs/0002-pilot-readiness-architecture.md) keeps transactional state/audit separate from file bytes. Shared JSON has concurrency weaknesses; Cosmos is a less direct fit for the retained relational gates. PostgreSQL remains a portability alternative needing audit/control engineering | Test correct transitions, version binding, persistence and recovery; no measured platform superiority claimed; page 38 |
| Entra plus API authorization | [Identity learning](../../adrs/0002-pilot-readiness-architecture.md) separates authentication from server-enforced role/case/field scope; shared passwords or browser hiding are not equivalent controls | Reduce duplicate identity handling without transferring professional or resident authority; page 38 |
| Rules before AI | [Deterministic ranking](../../adrs/0002-pilot-readiness-architecture.md) retains policy, arithmetic, freshness and release checks. Model-owned queue order or approvals were not selected | Reproducible decisions and explicit owners, not a claim of validated fairness or savings; page 17 |
| Conditional Decision 1 and generative inference | [Model-fit research](../../ideas/typesafe-system-one-agent-fit.md) and [behaviour specification](../../reference/research/decision-1-behaviour-specification.md) separate supplied-candidate/binary support from narrative generation; an exact field may only need a parser | Compare held-out quality, all review/correction effort, latency and complete cost; abstain or retain simpler work when benefit is unproved; page 32 |
| Owned chat threads; memory separately gated | [ADR 0004](../../adrs/0004-per-user-agent-chat-and-memory.md) retains case/subject isolation rather than shared case memory or automatically adopting preview managed memory | Follow-up help is conditional on privacy, retention and evaluation. Thread continuity is not persistent memory approval |
| Source-backed regulatory cards; conditional chat | [ADR 0005](../../adrs/0005-regulatory-compliance-assistant.md) does not make chat or fine-tuning the legal clock. Deterministic cards remain the comparator and manual path | Better source navigation must demonstrate comprehension value; currentness and named legal approval remain separate |
| IoT Hub Basic plus private Event Hub adapter | [ADR 0003](../../adrs/0003-journey-derived-capabilities-runtime-fit.md) and [IoT synthesis](../../reference/research/iot-sensor-analytics-research-plan.md) separate device identity/one-way intake from private keyless consumption. Standard device-control features and a complete streaming estate are not automatically needed | Bounded synthetic engineering is not live device, calibration, consent or safety evidence; page 47 |
| Selective Fabric analytics later | [Fabric assessment](../../reference/research/microsoft-fabric-fit-assessment.md) preserves reporting requirements, SQL ledger/workflow authority and a governed SQL/history + Power BI comparator. Dedicated always-on Fabric and operational SQL replacement are not recommended on current evidence | Potential reusable cross-source history, shared measures and repeated-report preparation. Require a named workload, approved data projection/capacity and a favourable quality/effort/freshness/full-cost comparison; page 48 |

Fabric mirroring does not inherit application permissions or automatically
retain the business-event/audit history. Fabric SQL ledger-creation limits
are not the same as the eligibility of current ledger tables for mirroring.
Capacity, private routes, licensing, source load and operations belong in the
cost comparison. The earlier USD 700 ceiling is not new Fabric funding; its
recorded execution authority expired, and current all-in headroom remains
Unknown/Blocked. No purchase, trial activation or data export follows.

The [current agents guide](../../../src/agents/README.md) retains a critical
unsupported-claim-with-valid-citation counterexample. Model feasibility,
human reviewer effectiveness and incremental benefit remain different claims.
Current source structure is the [five src distributions](../../../src/README.md),
not the retired application directories or five autonomous workers.