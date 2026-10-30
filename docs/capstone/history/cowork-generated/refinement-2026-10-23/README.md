---
title: IoT and Optional Resident Portal Presentation Refinement
description: Main-route IoT and optional resident self-service assessment integrated into the 54-slide Cowork v2 deck
ms.date: 2026-10-23
ms.topic: reference
---

## Current Files

Use the [revised PPTX](../../zava-forward-cowork-v2-draft.pptx) and
[native PowerPoint PDF](../../zava-forward-cowork-v2-draft.pdf).
The deck still has 54 slides, the same sections, slide IDs and navigation
labels. The planned timing is retained, not newly rehearsed. Retained Cowork
handoffs and original v2 exports remain unchanged. Unretained source
deliverables are described in their original handoffs, not presented as files
available in this checkout.

## Narrative Changes

| Slide | Change | Native preview |
| --- | --- | --- |
| 9, S08 | Portal is optional and under assessment, not rejected; test fewer avoidable calls and staff interruptions | [Slide 9](./slide-9.png) |
| 13, S12 | Same-home story preserves assisted routes and describes the portal as under assessment | [Slide 13](./slide-13.png) |
| 19, S16 final build | Main-route sensor/simulator -> IoT Hub Basic -> API checks -> SQL -> human review lane, explicitly not live | [Slide 19](./slide-19.png) |
| 33, B06 | Optional portal, resident choice and unchanged assisted routes; human validation is next, not already completed | [Slide 33](./slide-33.png) |
| 46, B19 | Distinguish locally tested offline consumption from roadmap live integration and explain post-retrofit monitoring value | [Slide 46](./slide-46.png) |

IoT is accepted exercise design under
[ADR 0003](../../../../adrs/0003-journey-derived-capabilities-runtime-fit.md#decision),
not verified live transport or analysis. A deterministic signal may request
human review; it never diagnoses a hazard, suppresses a resident report,
changes priority or releases a hold. Resident reports keep their independent
human safety route.

## Portal Evidence and Value Test

[Issue #441](https://github.com/jmservera/ama/issues/441) and its
[latest public comment](https://github.com/jmservera/ama/issues/441#issuecomment-6374724922)
were read on 2026-10-23. Owner-confirmed Option B reuses existing case/API
authority: portal/workflow first, any resident-answer task separately gated.
At retrieval, the issue remains open with a Research-stage integration
blocker and no published PR. The owner reports unpublished local work;
this presentation does not inspect or approve those candidate drafts.

The hypothesis is fewer avoidable status calls and longer uninterrupted
staff working periods, without shifting effort onto residents. Compare
interruption time, total handling/review effort, resident effort, access and
comprehension. No numerical savings, cash/headcount benefit or company
performance is claimed. Phone, email, letters, visits and accessible assisted
channels remain available without detriment; portal use is not works consent.

Per-message human review remains normative. Routine automation stays off
pending requirements-owner disposition and separate release approval.
Source ID `E441` records these boundaries in the portable evidence register.
The original 18-slide authoring contract, generated notes, brief and demo
commentary are updated prospectively; they are not presented as the full
native v2 build recipe or as current approved product requirements.

## Validation and Limits

The presentation packer passed structural validation. Native Windows
PowerPoint opened the candidate as 54 slides, rendered all five changed
slides at 1600x900 and saved the full PDF. Independent visual review found
one clipped IoT sentence and ambiguous target styling; both were corrected,
repacked and re-rendered. Parent inspection of the corrected affected slides
found no remaining clipping or overlap in the changed content.

The installed PPTX also passes the actual scorer's extraction: 54 slides,
54 speaker-note blocks and the unchanged slide-39 marker. Canonical XML
comparison against the prior committed deck identifies exactly five changed
slides and their five notes; every other package part, media file, section
and navigation relationship is preserved. The new native PDF has 54 pages
and contains the IoT and portal revisions. The scoring registry is unchanged.

These are targeted artifact checks, not all-slide redesign review,
accessibility conformance, projection testing, timed rehearsal, portal user
research, live IoT acceptance or a capstone score. No application code,
infrastructure, resident data, paid service calls, commit, push or hosted
scoring workflow was changed or executed for this refinement.
