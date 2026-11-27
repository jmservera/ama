---
title: Capstone Working Set
description: Current presentation, reproducible sources, pitch, demo and rubric inputs
ms.date: 2026-11-27
ms.topic: how-to
---

## Start Here

Use the current Cowork v2 presentation and select its "Demo-first pitch"
custom show. It contains 17 selected slides, begins the employee-site demo
at 00:30 and returns to the business argument at 02:20. Prepared narration
and demo finish at 13:00; questions and recovery have 2:00 within 15 minutes.
The full 56-page deck and PDF remain the source-backed reference package.
B28 is now part of the [manifest](./source/slides.json) and builder, so a
clean rebuild preserves the measured Tokenomics evidence.

Physical slide 6 also shows the full Azure planning range, including AI;
slide 7 retains its dated counters in a readable grid. The separate
"Discovery and UK sovereignty" custom show takes six additional confirmed
minutes. Its timed chapters are in the integrated script; do not spend the
two-minute question reserve on the full secondary show.

| Work | Current material |
| --- | --- |
| Present or review | [PowerPoint](./deck/zava-forward-cowork-v2-draft.pptx) and [matching PDF](./deck/zava-forward-cowork-v2-draft.pdf) |
| Edit and rebuild | [Source guide](./source/README.md), [56-slide manifest and pitch route](./source/slides.json) and [immutable 54-slide native baseline](./source/baseline.pptx) |
| Find image inputs and provenance | [Asset catalog](./source/assets/catalog.json), [retained media](./source/assets/media/) and [official Fabric/Power BI sources](./source/assets/official/README.md) |
| Prepare the pitch | [Timed speaker script with embedded demo runbook](./pitch/speaker-script.md), [question bank](./pitch/questions-and-answers.md) and [Tokenomics Q&A brief](./tokenomics-qa-brief.md) |
| Prepare the demo | [Timed demo script](./demo/runbook.md): complete 1:50 panel route, optional eight-minute walkthrough and two-minute question/recovery reserve |
| Understand the discovery and journey | [DT Coach method, pain/gain and decision trace](./source/diagrams/discovery-journey/text-equivalent.md), [editable Excalidraw](./source/diagrams/discovery-journey/resident-journey.excalidraw) and [PNG](./source/diagrams/discovery-journey/resident-journey.png); main pages 8 and 14 |
| Understand what comes next | [Future roadmap and proposal crosswalk](./source/roadmap-recommendations.md); future Fabric/Power BI and agent-context proposal only near the close on pages 24-25 |
| Understand technology choices | [Decision register](./source/README.md#technology-decisions); main page 17 and deeper appendix comparisons |
| Understand the application and full Azure topology | [CxO concept](./source/diagrams/architecture/cxo-architecture.svg), [new main-route deployment projection](./source/diagrams/architecture/azure-deployment.svg), [full reference](./source/diagrams/architecture/azure-architecture.svg) and [editable sources/text equivalent](./source/diagrams/architecture/text-equivalent.md); main 12/13 and B10/core frame 38 |
| Improve the story and challenged criteria | [CxO/story review](./source/review-2026-11-08-cxo.md); main-route recommendation/state-flow/autonomy, appendix alignment and real rehearsal evidence still needed |
| Review the demo-first refresh | [27 November evidence, narrative and full assessment review](./source/review-2026-11-27.md); retained history, current-source/detailed-live distinctions, costs, study findings and validation gaps |
| Explain UK boundaries and sovereign options | [Dated service matrix and possible migration path](../architecture/environment-region-quota-strategy.md#uk-data-boundary-and-sovereign-migration-options-2026-11-27); public controls, local replacements, preview limits and separate identity/model/provider checks |
| Explain brief fidelity and the evolving product | [8 November autonomy/story review](./source/review-2026-11-08.md): exact requested/current levels, three help modes, historical Decision 1, optional resident access, design-thinking decisions and refreshable progress snapshot |
| Inspect findings and checks | [30 October illustrated visual refresh](./source/review-2026-10-30.md#illustrated-visual-refresh-on-linux), earlier roadmap findings on the same page and preserved [29 October review](./source/review-2026-10-29.md) |
| Recover previous work | [History and restore map](./history/README.md); original findings and authoring sources are retained |
| Continue thought leadership | [Current coauthored paper package](./thought-leadership/everything-but-the-software/README.md): owner-confirmed OSF base, ongoing unregistered exploratory amendments, independent execution and three implementation epochs; not experimental outcome proof |

The PPTX and PDF are drafts for owner review. Prepared notes, native rendering
and local extraction do not establish rehearsal, human acceptance, measured
benefits or a fresh rubric score.

The revised story moves from a visible owned next action to its business
purpose, resident choice, architecture, task autonomy, controls and cost.
It then connects the delivery failures and completed exploratory study to a
bounded validation decision. Original L2-L4 responsibilities, full task
breadth, trigger mode and accepted live behaviour remain distinct.
No faster retrofit, grant award or resident saving is claimed.

## What To Keep

Keep the complete source package and its builder dependencies. The JSON covers
all 56 slide records and notes; the pinned 54-slide native baseline owns unchanged
layouts, relationships, themes and embedded graphics. JSON alone does not
reconstruct those native designs. Keep the 36 captured media inputs and the
two official future-roadmap icons, each with original SVG and PNG derivative,
and the DT journey's editable Excalidraw, SVG, PNG, generator and text equivalent.
The catalog pins every input and approved new-image placement. Neither Fabric
nor Power BI is a current product component; pages 15-16 explain the built
Workbench and existing bounded adoption tools without those logos.

Keep the new application/Azure architecture sources together: two editable
Excalidraw models, full SVG/PNG derivatives, the Azure core and deployment projections,
generator, source/rights trace and text equivalent. The CxO map is a logical
application/data view; the Azure view distinguishes network endpoints,
managed services, current source realization and separately gated options.
No picture is a live inventory or compliance/data-residency attestation.

Keep pitch and demo material together with the same deck revision. Do not edit
the generated speaker notes or Q&A independently of the source manifest.
Only actual rehearsal/delivery records should be described as transcripts.

The historical 18-slide brief, seven editable Excalidraw diagrams, original
Azure icon sources and earlier native recovery inputs are under
[history](./history/README.md). They are not another current build route.
The 15 approved redundant exports were archived and restored before removal;
their exact paths and hashes are in the
[cleanup receipt](./history/reorganization-2026-10-29.json).

## Rebuild

From the repository root in PowerShell 7.4 or newer, choose a new external
directory for each build. Build and Verify do not require Office. Render
requires installed Windows PowerPoint.

```powershell
$Run = Join-Path $env:LOCALAPPDATA ("ama/capstone-runs/" + [guid]::NewGuid().ToString('N'))
./tools/capstone/Invoke-Capstone.ps1 -Action Build -RepoRoot $PWD.Path -OutputDir $Run
./tools/capstone/Invoke-Capstone.ps1 -Action Verify -RepoRoot $PWD.Path -OutputDir $Run
./tools/capstone/Invoke-Capstone.ps1 -Action Render -RepoRoot $PWD.Path -OutputDir $Run
```

The run produces a PPTX, native PDF/PNGs, verification reports and synchronized
pitch notes. Review those outputs before replacing the delivery files. Heavy
previews stay outside the checkout. See the [source guide](./source/README.md)
for the editing contract and [compact validation receipt](./source/validation.json)
for the current delivery identity.

On Linux, use the [explicit preview route](./source/README.md#linux-preview)
after Build. It renders all slides with LibreOffice and restores the 108 PDF
slide jumps from the actual PPTX. This is not native Windows PowerPoint
validation. The current refresh restores the illustrated timeline on page 3,
the resident touchpoint map on page 14 and the editable pain/gain canvas on
page 40, with coordinated visual refinements on ten other pages. The question
index also separates two formerly overlapping click regions without changing
their destinations.

## Rubric Inputs

The [artifact registry](../../.github/rubric/artifacts.json) selects exactly
the current deck path with a 20 MB allowance. It also reads Markdown, text
and VTT material under both `pitch/` and `demo/`. Source inputs and history
are not substitute current pitch evidence. Thought-leadership registration
is unchanged. PDFs and images do not substitute for PPTX speaker notes.

Local checks use the real PPTX extractor and deterministic registry/gate
tests. Hosted scoring uses trusted configuration from base `main`; the new
demo-folder registration takes effect there only after the registry update
is integrated. No recorded score is manually changed.

## Next Work

Rehearse the generated script and its complete 1:50 demo. The default
15-minute pitch includes the demo and question reserve; no ten-minute demo
is added to it. Use the longer runbook only when a longer slot is confirmed,
finishing navigation at eight minutes and preserving its two-minute reserve.
The original slide timing lines are historical reference provenance.
Record actual timings, questions and failures only after a run.

Resolve the original image URL/prompt/licence gaps before new external reuse.
Complete the actual live-demo preflight, direct accessibility/navigation and
audience checks, remaining legal/privacy/product gates and the repository's
publication gates separately. The retained buttons use fixed slide jumps;
their historical "Return to caller" wording is not dynamic viewer history.

No deployment, data export, paid inference, spending approval, commit, push,
hosted rubric run or production acceptance is part of this reorganization.