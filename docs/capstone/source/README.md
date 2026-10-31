---
title: Capstone Authoring Source
description: Complete native-template and JSON editing contract, retained media and technology-decision evidence
ms.date: 2026-10-31
ms.topic: how-to
---

## Source Authority

| Input | Responsibility |
| --- | --- |
| [baseline.pptx](./baseline.pptx) | Immutable snapshot of the actual owner-supplied 54-slide deck at this reorganization; native layouts, sections, media, relationships and untouched content |
| [slides.json](./slides.json) | All 54 ordered records/notes, native main-story roadmap layouts, exact text/bounds corrections and explicit current narration |
| [assets/catalog.json](./assets/catalog.json) | Captured media in `media`; future-logo and journey images in `additional_media`, with exact usage and SVG/native/PNG hashes |
| [assets/media](./assets/media/) | All 36 original embedded media files, not flattened pictures of whole slides |
| [Official product icons](./assets/official/README.md) | Fabric and Power BI source SVGs, native PNG derivatives, permitted-use guidance and archive provenance |
| [DT resident journey](./diagrams/discovery-journey/text-equivalent.md) | Editable Excalidraw, same-geometry SVG/PNG, deterministic generator and provision-linked method/pain/gain/decision trace |
| [Invoke-Capstone.ps1](../../../tools/capstone/Invoke-Capstone.ps1) | Current ExportSource, Build, Verify and native Render entry point |
| [Native shape helper](../../../tools/cowork-native-recovery/Invoke-StoryReview.ps1) | Existing XML/native-shape functions used by the current builder; its historical standalone workflow is not the current build command |
| [validation.json](./validation.json) | Compact delivery/verification receipt, not another build input |

The baseline hash is pinned in the manifest. The delivered PPTX is an output,
never an implicit fallback input. A complete rebuild needs the native baseline,
JSON, catalog, all referenced media and both scripts above. The old 18-slide
authoring inventory does not recreate the 54-slide deck.

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
with `ExportSource`: that initialization action starts from the baseline,
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
* Exact expected package bytes: 293 captured baseline members plus three declared
  PNGs (two future logos and the journey); only declared image relationships change
* All 54 nonempty note blocks and retained timing lines
* Native navigation actions and unique shape IDs
* The six protected cost slides on pages 6, 11, 21, 32, 36 and 52; notes may
  change only through exact navigation-sentence corrections, not calculations

The present baseline contains 108 fixed slide-jump actions. Preserve their
actual targets; neither their labels nor an older review establishes dynamic
Last Slide Viewed behaviour. Native viewer/keyboard interaction still needs
direct acceptance testing.

Native Windows Render produces a PDF and 54 PNGs plus measured text bounds.
The [current Linux visual refresh](./review-2026-10-30.md#illustrated-visual-refresh-on-linux)
uses the explicitly separate preview route below: all 54 pages rendered,
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
remain unchanged; the note exceptions on pages 32, 36 and 52 correct only
false Last Slide Viewed instructions. The builder checks that exact exception.

The [30 October review and owner correction](./review-2026-10-30.md) preserves
both the earlier candidate and the corrected product-first story. Page 8 explains
evidence -> hypotheses -> maps -> design/test; page 13 shows the DT Coach's
resident journey. Pages 14-15 describe the built Workbench and bounded file/CLI
adoption. Fabric and Power BI are not current components: page 23 proposes
future history, measures and preview ontology context; page 24 separates current
verification, analytics comparison and an independent context experiment.
The [full proposal register](./roadmap-recommendations.md)
maps all 25 reviewed families into 22 grouped dispositions. This is not a
commitment to every option, a purchase or a new approved product requirement.

Captured `media.slides` records describe baseline usage; retained media can
remain necessary to reproduce the pinned baseline even when a revised layout
no longer displays it. `additional_media.slides` is verified against actual
generated relationships. Original 36 inputs remain unchanged. The two official
icons are placed only on future page 23. The DT journey is placed only on page
13; keep its native/SVG/PNG/generator/text-equivalent files together. The current
PNG is a local native `@excalidraw/cli` export of the editable 1600 x 560 scene,
not the earlier PowerPoint rasterization. No account or upload was used.
The slide owns its title, status and safety boundary; projected cell text is
20.2 pt and the proposed human-role labels are 15.4 pt. Page 39's complementary
value-proposition canvas uses editable native PowerPoint sectors and text.
Direct resident/staff and
projection/accessibility acceptance remain unperformed.

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
"$Run/venv/bin/python" tools/capstone/render_preview.py --input "$Run/build/zava-forward-cowork-v2-draft.pptx" --output-dir "$Run/preview"
```

The preview writes the matching PDF, 54 slide PNGs and a compact report with
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
PYTHONDONTWRITEBYTECODE=1 "$Run/venv/bin/python" -m pytest -p no:cacheprovider -q tools/capstone/test_render_preview.py
node docs/capstone/source/diagrams/discovery-journey/build-resident-journey.mjs --check
```

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
| Shared Container Apps API | [ADR 0002](../../adrs/0002-pilot-readiness-architecture.md) favours fewer operating/state/retry boundaries; AKS and five independently deployed assistant workers add unproved operating need | Hypothesis: simpler controlled delivery. Split only for measured isolation, scale, long-running work or recovery requirements; page 37 |
| Azure SQL + Blob | [ADR 0002 data-store appraisal](../../adrs/0002-pilot-readiness-architecture.md) keeps transactional state/audit separate from file bytes. Shared JSON has concurrency weaknesses; Cosmos is a less direct fit for the retained relational gates. PostgreSQL remains a portability alternative needing audit/control engineering | Test correct transitions, version binding, persistence and recovery; no measured platform superiority claimed; page 37 |
| Entra plus API authorization | [Identity learning](../../adrs/0002-pilot-readiness-architecture.md) separates authentication from server-enforced role/case/field scope; shared passwords or browser hiding are not equivalent controls | Reduce duplicate identity handling without transferring professional or resident authority; page 37 |
| Rules before AI | [Deterministic ranking](../../adrs/0002-pilot-readiness-architecture.md) retains policy, arithmetic, freshness and release checks. Model-owned queue order or approvals were not selected | Reproducible decisions and explicit owners, not a claim of validated fairness or savings; page 16 |
| Conditional Decision 1 and generative inference | [Model-fit research](../../ideas/typesafe-system-one-agent-fit.md) and [behaviour specification](../../reference/research/decision-1-behaviour-specification.md) separate supplied-candidate/binary support from narrative generation; an exact field may only need a parser | Compare held-out quality, all review/correction effort, latency and complete cost; abstain or retain simpler work when benefit is unproved; page 31 |
| Owned chat threads; memory separately gated | [ADR 0004](../../adrs/0004-per-user-agent-chat-and-memory.md) retains case/subject isolation rather than shared case memory or automatically adopting preview managed memory | Follow-up help is conditional on privacy, retention and evaluation. Thread continuity is not persistent memory approval |
| Source-backed regulatory cards; conditional chat | [ADR 0005](../../adrs/0005-regulatory-compliance-assistant.md) does not make chat or fine-tuning the legal clock. Deterministic cards remain the comparator and manual path | Better source navigation must demonstrate comprehension value; currentness and named legal approval remain separate |
| IoT Hub Basic plus private Event Hub adapter | [ADR 0003](../../adrs/0003-journey-derived-capabilities-runtime-fit.md) and [IoT synthesis](../../reference/research/iot-sensor-analytics-research-plan.md) separate device identity/one-way intake from private keyless consumption. Standard device-control features and a complete streaming estate are not automatically needed | Bounded synthetic engineering is not live device, calibration, consent or safety evidence; page 46 |
| Selective Fabric analytics later | [Fabric assessment](../../reference/research/microsoft-fabric-fit-assessment.md) preserves reporting requirements, SQL ledger/workflow authority and a governed SQL/history + Power BI comparator. Dedicated always-on Fabric and operational SQL replacement are not recommended on current evidence | Potential reusable cross-source history, shared measures and repeated-report preparation. Require a named workload, approved data projection/capacity and a favourable quality/effort/freshness/full-cost comparison; page 47 |

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