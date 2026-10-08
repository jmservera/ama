---
title: Capstone Deliverables and Storage Map
description: Where every capstone asset must be stored so the rubric gate can find and score it, and what scores 0 until it exists
author: AMA programme
ms.date: 2026-10-07
ms.topic: reference
---

The rubric gate scores only what is committed to this repository. A criterion
that needs an artifact which has not been committed is recorded as 0 by the
gate, not by the model. Rules are in
[rubric.json](../../.github/rubric/rubric.json) and the artifact registry in
[artifacts.json](../../.github/rubric/artifacts.json); the criteria come from
the [Capstone Assessment Guide](../reference/method/ama-capstone-assessment-guide.md).

## Storage map

| Rubric section | Asset | Store it at | Format the scorer reads |
| --- | --- | --- | --- |
| A1 to A7 | Business requirements | `docs/brds/` | Markdown |
| A1 to A7, B6, C1 | Product requirements | `docs/prds/` | Markdown |
| A1 to A3, B6 | Architecture decision records | `docs/adrs/` | Markdown |
| A1, A3 to A7, B6 | Solution code, tests, README and diagrams | `src/` and `mvp/` (see the registry globs) | Source files |
| A1, A3, A5 | Infrastructure as code | `infra/` and `prototype/deploy/*.bicep` | Bicep, Terraform |
| B1, B2, B6, B7 | Final capstone deck, with speaker notes | `docs/capstone/deck/` | `.pptx` (slide and notes text) |
| B1 to B5, B7, C2, C3 | Pitch rehearsal and Q&A transcripts, timing notes, demo script and recovery notes, restated-challenge examples | `docs/capstone/pitch/` | `.md`, `.txt`, `.vtt` |
| D1 to D3 | Thought leadership artifact | `docs/capstone/thought-leadership/<artifact-name>/` | `.md`, `.txt`, `.vtt`, plus `.pptx` as support |

Recordings (video or audio) are not read by the scorer. Commit the transcript
or written notes next to the recording and link the recording from them.

## Thought leadership artifact (Section D)

Commit exactly one artifact folder, `docs/capstone/thought-leadership/<artifact-name>/`,
with a `README.md` that states the format, the audience, the engagement evidence
and where it is published or submitted.

| Format | What to commit in the folder |
| --- | --- |
| White paper or architecture guidance | The paper, 2,000+ words, structured and sourced |
| Technical blog post | The post, 800+ words, plus the publication or submission link and date |
| Reference implementation or accelerator | A `README.md` covering purpose, architecture, setup and known limitations, linking the repository that holds the working code |
| IP disclosure or patent filing | The disclosure document and the submission reference |
| Community or conference session | Published materials, written notes or a transcript, and a link to the recording |
| Slide deck | Never enough alone. Commit written notes or a transcript with it |

D1 to D3 score 0 until a text artifact exists in this folder. D3 stays at the
bottom band until a real publication, filing or delivery beyond the cohort is
recorded with its link and date. BRDs, PRDs and code never count toward Section D.

## What scores 0 or is capped until it exists

| Criteria | Needs at least one of | Without it |
| --- | --- | --- |
| B1, B2, B7 | Capstone deck or pitch transcripts | 0 |
| B3 to B5, C2, C3 | Pitch transcripts and notes (demo, Q&A, timing) | 0 |
| D1 to D3 | Thought leadership artifact | 0, and the outcome is Incomplete |
| B6 | Capstone deck, plus the documentation already in the repository | Capped at 3 |

Because every Section D criterion and most of Section B score 0 today, the
Section B and D floors fail. Scores rise only as the assets above are committed.
Masterclass attendance is a floor in the guide but is not repository evidence
and is not scored by the gate.
