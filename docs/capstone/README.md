---
title: Capstone Working Set
description: Current presentation, reproducible sources, pitch, demo and rubric inputs
ms.date: 2026-10-29
ms.topic: how-to
---

## Start Here

Use the 54-slide Cowork v2 presentation. There is one current deck, not a
choice between the older executive and Cowork routes.

| Work | Current material |
| --- | --- |
| Present or review | [PowerPoint](./deck/zava-forward-cowork-v2-draft.pptx) and [matching PDF](./deck/zava-forward-cowork-v2-draft.pdf) |
| Edit and rebuild | [Source guide](./source/README.md), [54-slide manifest](./source/slides.json) and [native baseline](./source/baseline.pptx) |
| Find image inputs and provenance | [Asset catalog](./source/assets/catalog.json) and [retained media](./source/assets/media/) |
| Prepare the pitch | [Speaker notes](./pitch/speaker-script.md), [question bank](./pitch/questions-and-answers.md) and [pitch folder](./pitch/) |
| Prepare the demo | [Ten-minute runbook](./demo/runbook.md), including the under-two-minute executive hook and recovery route |
| Understand technology choices | [Decision register](./source/README.md#technology-decisions); main page 16 and appendix pages 31, 37, 46 and 47 |
| Inspect findings and checks | [Dated review](./source/review-2026-10-29.md), including the legal-status correction on page 3 and all-criteria evidence gaps |
| Recover previous work | [History and restore map](./history/README.md); original findings and authoring sources are retained |
| Continue thought leadership | [Existing paper package](./thought-leadership/everything-but-the-software/README.md), unchanged by this reorganization |

The PPTX and PDF are drafts for owner review. Prepared notes, native rendering
and local extraction do not establish rehearsal, human acceptance, measured
benefits or a fresh rubric score.

## What To Keep

Keep the complete source package and its builder dependencies. The JSON covers
all 54 slide records and notes; the pinned native baseline owns unchanged
layouts, relationships, themes and embedded graphics. JSON alone does not
reconstruct those native designs. The 36 separate media inputs make image
dependencies inspectable and editable.

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

Rehearse the retained 23:45 narration plan within the 30-minute presentation
slot, with a separate ten-minute demo. Build variants share their timing;
appendix answers are optional depth. Confirm the actual panel slot before
the final rehearsal rather than reviving a historical timing route.

Resolve the original image URL/prompt/licence gaps before new external reuse.
Complete the actual live-demo preflight, direct accessibility/navigation and
audience checks, remaining legal/privacy/product gates and the repository's
publication gates separately. The retained buttons use fixed slide jumps;
their historical "Return to caller" wording is not dynamic viewer history.

No deployment, data export, paid inference, spending approval, commit, push,
hosted rubric run or production acceptance is part of this reorganization.