---
title: Capstone Deliverables and Storage Map
description: Where every capstone asset must be stored so the rubric gate can find and score it, and what scores 0 until it exists
author: AMA programme
ms.date: 2026-10-13
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
| B1, B2, B6, B7 | Capstone deck, with speaker notes | `docs/capstone/deck/` (sole published executive deck; no duplicate in `docs/presentations/`) | `.pptx` (scorer reads slide and notes text) |
| B1 to B5, B7, C2, C3 | Pitch rehearsal and Q&A transcripts, timing notes, demo script and recovery notes, restated-challenge examples | `docs/capstone/pitch/` | `.md`, `.txt`, `.vtt` |
| D1 to D3 | Thought leadership artifact | `docs/capstone/thought-leadership/<artifact-name>/` | `.md`, `.txt`, `.vtt`, plus `.pptx` as support |

Recordings (video or audio) are not read by the scorer. Commit the transcript
or written notes next to the recording and link the recording from them.

The [Zava Forward council proposal](./deck/zava-forward-executive-draft.pptx)
is the executive capstone artifact. The owner retired its duplicate in
`docs/presentations/` on 2026-10-11; that folder still holds the separate
mentor presentation. The filename retains its draft status: production
approval, measured benefits and live pitch evidence remain separate gates.

The deck was detected in PR #61, but the scorer's `:slideN` references did not
match the deterministic gate's text-only anchor parser. This discarded its
proposed B1, B2, B6 and B7 changes and left misleading missing-deck baseline
rationales in the comment. See the
[gate repair and activation boundary](../../.github/rubric/README.md).
Do not treat a saved-scorecard replay as a fresh score for the revised deck.

## Agents in the Retrofit Process (2026-10-13)

The PowerPoint Builder added the map as slide 13 of the
[22-slide council proposal](./deck/zava-forward-executive-draft.pptx), after the
AI-authority boundary and before the CFO example. All 21 original slides,
notes, masters, layouts and images are retained; moved page counters are
renumbered. The new slide includes an alternative description, a full text
equivalent, source references and a suggested 45-60-second talk track in notes.

The published copy passed notes/count checks, new-slide geometry checks and
original-content preservation comparisons; fresh slides 12-14 were inspected
from a LibreOffice export. PowerPoint/Aptos font fidelity, model-SDK vision
validation, human acceptance and timed rehearsal are not claimed as passed.
The historical 2026-10-11 working content is the earlier 21-slide version;
use the current canonical deck as the source for partial rebuilds with the
[new slide content](../../.copilot-tracking/ppt/2026-10-13/zava-forward-agent-process/content/slide-013/content.yaml).
The [partial-build helper](../../.copilot-tracking/ppt/2026-10-13/zava-forward-agent-process/build_agent_slide.py)
also embeds the YAML image description, which the shared builder alone ignores.

![Five bounded assists across choosing homes, assessment/design, funding, works coordination and quality/handover, with on-request help, proactive review triggers and separate human owners.](./deck/agents-in-retrofit-process.png)

The [vector process map](./deck/agents-in-retrofit-process.svg) illustrates the
proposed design, not five autonomous managers or a claim that every capability
is deployed. The workflow owns progression and accountable people retain
policy, resident choice, technical acceptance, work release, grant submission,
quality acceptance and payment. Funding spans preparation through later
claim/cash reconciliation; an award is not a receipt, and reviewed funding,
budget, resident choice and capacity precede work release.

| Bounded capability | Staff-requested help | Proactive review trigger, not an approval | Intended improvement and value test |
| --- | --- | --- | --- |
| Stock Prioritisation | Explain source-bound candidate evidence; propose reconciliation of conflicting records, never change ranking policy or queues | New/conflicting stock/EPC evidence or an eligible freshness review | Fewer data blind spots; compare reconciliation time, critical conflicts found and homes still viable after survey |
| Assessment Preparation | Pre-fill a survey/design pack from sourced facts, never invent site observations | Changed, missing or stale assessment evidence | Less review/rework; compare returns, reapprovals and assessment-to-ready time, retaining separate assessor/coordinator sign-off |
| Grant and Funding Evidence | Draft a source-linked application or evidence pack; rules own eligibility and calculations, Finance owns review/submission | Changed terms or missing evidence routed for human review, never silent activation of a new rule | Fewer pack gaps; compare first-time evidence acceptance, rejection/rework and time to claim; award/claim/cash stay separate |
| Contractor and Resident Coordination | Draft an update or suggest slots within committed capacity; no auto-send, instruction, booking or consent inference | Unaccepted handoff or missed resident-update commitment to an owned queue | Clearer ownership; compare coordination effort per accepted home, failed visits and unowned handoffs, preserving resident choice and independent work release |
| Quality Evidence Assurance | Assemble evidence for independent review; raise missing or contradictory evidence, never accept or clear | New quality evidence, missing items or anomaly signals within a registered task | Earlier reviewed defect signals; compare evidence rework, first-time acceptance and missed critical defects |

Proactive means an authorized event or scheduled check makes a task eligible.
The deterministic task registry selects rules, bounded AI or human handling;
only permitted, source/version-bound tasks may produce an unreviewed draft or
raise-only flag to a named human queue. Structured freshness, deadlines and
readiness are rules, not evidence of agent reasoning. Any hazard uses the
independent human safety route immediately; a negative model result never
suppresses intake or changes its clocks. Failed/stale/disabled assistance
preserves controlled state and an owned manual route.

All improvement claims are hypotheses. Paired comparison with the same
rules/manual workflow counts preparation, review, correction and shifted
burden alongside critical errors, latency, cost and uncertainty. Narrow live
model integration, fixture tests and diagram arrows do not prove all workflow
capabilities, proactive deployment, calibrated quality or measured benefit.
The [draft closure review](../reference/research/gap-analysis-next-build.md#draft-experiment-closure-review-2026-10-13)
keeps absent #58 capabilities and current-infrastructure verification explicit.

Content is grounded in the [addendum agent map](../case_study_48_addendum.md#agentic-architecture-brief),
[agent request challenge](../reference/research/company/agent-request-challenge.md#summary)
and [PRD bounded-agent pattern](../prds/zava-forward-retrofit-programme-demonstrator.md#bounded-agent-orchestration-pattern).
No new requirement, authority, numerical benefit or operational approval is
introduced. The diagram's intended contribution to A1/A3/A6/A7 and B1/B2/B6/B7
is explanation of fit, triggers, controls and value tests, not a fresh rubric
score or panel-readiness claim. Live pitch/rehearsal and the complete rubric
floors remain separate.

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

Missing pitch and thought-leadership evidence still prevents the associated
criteria and floors from being satisfied. A deck alone cannot clear them.
Scores rise only as the assets above are committed and assessed.
Masterclass attendance is a floor in the guide but is not repository evidence
and is not scored by the gate.
