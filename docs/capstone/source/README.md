---
title: Capstone Authoring Source
description: Complete native-template and JSON editing contract, retained media and technology-decision evidence
ms.date: 2026-10-29
ms.topic: how-to
---

## Source Authority

| Input | Responsibility |
| --- | --- |
| [baseline.pptx](./baseline.pptx) | Immutable snapshot of the actual owner-supplied 54-slide deck at this reorganization; native layouts, sections, media, relationships and untouched content |
| [slides.json](./slides.json) | All 54 ordered slide records and original notes; six native-layout revisions and explicit current narration corrections |
| [assets/catalog.json](./assets/catalog.json) | Every embedded media member, retained file, SHA-256, slide usage and provenance/clearance limit |
| [assets/media](./assets/media/) | All 36 original embedded media files, not flattened pictures of whole slides |
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
* `layout: text` makes explicit, uniquely matched text replacements.
* `notes` retains the captured original. When present, `revised_notes` owns
  the current notes and takes precedence; original timing lines are retained.
* `sources` lists repository evidence required by a revision. A path is not
  proof that the underlying claim is current, approved or observed.

Keep physical slide order, native link objects, source/version labels and
approval boundaries unless changing them is a separate explicit task.
For a native layout beyond the revised pages, make a deliberate template
revision and update its pin and source manifest, then repeat validation.
Do not silently re-export from the delivery file or replace the source JSON
with `ExportSource`: that initialization action starts from the baseline,
not the current five-slide revision.

Edit media only with a documented origin and reuse right. Update its catalog
hash deliberately and rerender every affected page. Asset extraction preserves
the supplied bytes, not an undocumented original photograph URL, generation
prompt, licence or subject consent. Those gaps are explicit in the catalog;
repository clearance is not universal new-publication clearance.

## Build And Review

Use the [root build commands](../README.md#rebuild). Every run writes to an
explicit external directory and checks:

* The pinned template, complete ordered manifest and every media input
* Exact expected package bytes, including unchanged relationships and themes
* All 54 nonempty note blocks and retained timing lines
* Native navigation actions and unique shape IDs
* The six protected cost slides on pages 6, 11, 21, 32, 36 and 52; notes may
  change only through exact navigation-sentence corrections, not calculations

The present baseline contains 108 fixed slide-jump actions. Preserve their
actual targets; neither their labels nor an older review establishes dynamic
Last Slide Viewed behaviour. Native viewer/keyboard interaction still needs
direct acceptance testing.

Render produces a PDF and 54 PNGs plus measured text bounds. Inspect the
changed pages and relevant neighbours, fix findings, and rerender. The current
technology-page review had seven findings corrected. A later reader review
corrected inherited legal/forecast, navigation and demo-fallback passages and
opening inconsistencies. The legal-status page is the sixth visual revision.
The final export has zero revised-text overflow and 264 inherited bound warnings;
they are not erased or described as accessibility acceptance.

See the [dated review](./review-2026-10-29.md) for original findings and
qualitative coverage of all 20 criteria. Cost-slide graphics and arithmetic
remain unchanged; the note exceptions on pages 32, 36 and 52 correct only
false Last Slide Viewed instructions. The builder checks that exact exception.

Build and Verify also generate current main-route speaker notes and appendix
Q&A under the run's `pitch/` folder. Publish the matching PPTX/PDF and those
two Markdown outputs together after review. Retain dated review evidence;
do not commit all temporary renders. The compact receipt binds the candidate
to the baseline, manifest, media catalog, builder and shared native helper.

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