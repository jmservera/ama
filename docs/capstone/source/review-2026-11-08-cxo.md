---
title: Capstone Story and Application Architecture Review
description: Main-route design argument, appendix question alignment, CxO and Azure architecture views, and evidence needed for stronger live criteria
ms.date: 2026-11-08
ms.topic: reference
---

## Recommendation

Present an argument for selective automation, not a tour of the technology:

> Keep case control in explicit rules. Use bounded AI where interpreting
> evidence helps. Give people an owned next action and retain their decisions.
> Compare the result with the same workflow without AI before extending authority.

This continues the merged [autonomy review](./review-2026-11-08.md).
The original brief already specified task-level L2-L4 autonomy, resident
consent and professional/Finance approval. A deterministic part of an
agent's business responsibility need not be implemented by a generative model.
Five business jobs do not require five independently deployed applications.
The current five helpers are evidence proposals; full drafting, L3 coordination
and L4 quality flags remain distinct scope/authority increments.

The owner requested direct updates to the existing deck, notes and Q&A plus
two original editable Excalidraw views. Preserve all 54 physical pages,
numbered index/answer links, actual fixed destinations, progressive builds,
23:45 narration plan and six protected cost pages. This is prepared material,
not a rehearsal, user endorsement or a promised rubric increase.

## Audience And Outcome

Mixed customer CXOs and the AMA panel need one factual core with changing depth.
Lead with the recommendation (Sergeant), connect it to resident choice and
staff work (Therapist), show methods/options/limits (Scientist), and describe
conditional future value only after the evidence (Evangelist).
The intended action is agreement on the next validation question, accountable
roles and evidence required before a costed plan. This is not a production,
legal, spending or platform-purchase approval.

## Four Criteria To Strengthen

The [assessment guide](../../reference/method/ama-capstone-assessment-guide.md)
scores these live. The 81-to-77 AI readiness reassessment on PR #1283 did not
establish that the written improvements had been removed. Prepared clarity
can improve the package, but cannot manufacture observed listening or composure.

| Criterion | Material improvement | Practice and evidence still needed |
| --- | --- | --- |
| B1 Narrative structure and argument | Opening recommendation; explicit rules-only, rules-plus-AI and wider-automation alternatives on page 9; application map on 12; one-case causal example on 14; exact levels on 16 | Present the recommendation before the service inventory. A listener should be able to repeat the problem, choice, reason, unproved value and next decision |
| B4 Q&A composure and depth | First disclose the core design on the main route; retain mechanisms, constraints and reversal tests in B03/B04/B10/B14/B27 | Practise new variations, not only the written bank: cheaper rules, wider autonomy, supplier outage, different household authority and an unsupported AI answer. Record actual answers, challenged assumptions and follow-up owners |
| C2 Active listening and disagreement | Give the presenter a restate/clarify/answer/evidence/return pattern; prepare concessions without scripting the audience's reaction | Let the question finish. Restate the actual concern and confirm it when ambiguous. Concede a valid point without inventing agreement; only a real exchange can demonstrate this |
| C3 Influence and intellectual honesty | Defend a clear recommendation; disclose incomplete task breadth and missing benefit evidence before being asked; identify where the simpler option wins | Explain what evidence would change the recommendation. Say what is unknown and name how/with whom it will be resolved; do not turn a caveat list into indecision |

Useful unscripted challenges include:

* "If most of this is rules, why use AI at all?" Compare evidence interpretation
  and all human review effort against the rules/template path.
* "Why not activate the requested L4 quality flags?" Distinguish raise-only
  flags from acceptance; explain the critical-miss, false-flag and reviewer-load
  evidence needed, rather than calling the original boundary unsafe.
* "Does one login let AI see everything?" Separate company sign-in, application
  roles, case/field permission and the minimum-necessary model projection.
* "Can you already use our OneDrive files and real sensors?" Separate controlled
  file tooling from a live connector, and authored device ingestion from
  accepted live operation.
* "What would make you remove AI?" A worse accepted result, extra total effort,
  unsafe omissions or an unfavourable full-cost comparison are valid reasons.

For the other live communication criteria, rehearse the under-two-minute
outcome hook and recovery route (B3), the actual timed route with discussion
reserve (B5), and movement between executive and technical depth (B2).
No fictitious recording, transcript, audience approval or timing is added.

## Main Story And Appendix Depth

Keep the same order and time allocation; concise fragments replace material
within existing slots instead of adding the complete appendix to the talk.

| Main page | Claim and supporting depth | Why it belongs here |
| --- | --- | --- |
| 1 / S01 | One owned workflow, selective AI and the next validation decision | Establish the recommendation before the build tour |
| 9 / S08 | The brief's bounded levels, options and the chosen rules-plus-AI mechanism; B03/B14 depth | Explain the product judgement, not merely that the brief was challenged |
| 12 / S11 | CxO application view: people/login/roles, Workbench/API, records/evidence, files/devices and scoped advice; B10 depth | Give non-technical listeners a model of the application before service names |
| 13 / S12 | Resident journey and assisted choice; B06/B12 depth | Show why controlled handoffs matter, without presenting desk research as testimony |
| 14 / S13 | One fictional source conflict: coded gates route the owner; optional AI prepares a proposal; a person acts; B14/B27 depth | Explain the deterministic state-flow and the AI branch on the main route |
| 15 / S14 | Controlled file adoption and manual continuity; B02/B04 depth | Separate a usable transition increment from an unproved live M365 connector |
| 16 / S15 | All five requested/current levels and task-fit of rules, decision models and generation; B03/B04 depth | Make reductions, partial scope and historical Decision 1 visible before challenge |
| 17-20 | Trust boundaries and meaningful review, not a new model-controlled workflow | Connect controls to resident/professional/Finance decisions |
| 22-24 | Delivery learning, separately qualified future proposal and evidence-led next step | Keep a running experiment or Fabric opportunity separate from proved current value |
| 25-26 | Same-home outcome demo/debrief and close | Demonstrate the argument, not an unrelated feature inventory |

The "graph" is a conceptual rendering of coded gates, queues and controlled
transitions. Current code does not contain a deployed LangGraph/GraphState
runtime owning programme decisions. In
[gates](../../../src/core/src/zava_forward/core/gates.py), unknown never passes;
[advance](../../../src/core/src/zava_forward/core/store.py) checks gates,
safety, resident authority and capacity; [task queues](../../../src/core/src/zava_forward/core/taskqueues.py)
derive an owned next action.
The [employee chat contract](../../../src/api/README.md#employee-chat-with-bounded-skills-530)
has one chosen skill and one bounded model call, with no router, tool loop,
booking or domain-write tool.

## Appendix Audit

All 27 answer pages and their index entries were inspected for question/topic
alignment and usefulness. Four answer headlines had drifted into action
statements rather than matching their index questions:

| Code / page | Previous issue | Reconciled question |
| --- | --- | --- |
| B04 / 31 | Index asks where mechanisms fit; answer headline says Decision 1 must beat the baseline | Where do rules, decision models and generation fit? |
| B10 / 37 | Index asks why separate agent deployments were rejected; headline/body give a narrow shared-API technology choice | How is the full application architecture organised? Shared-API/split rationale remains supporting detail |
| B19 / 46 | Index asks about sensors/AI diagnosis; answer headline is a safety conclusion | How do device readings support decisions safely? |
| B20 / 47 | Index and headline use different future-platform questions | When would Fabric add value beyond SQL? |

B03 and B13 were already semantically aligned after the previous revision.
Other shortened index labels remain equivalent to their questions. No action
destinations are changed to compensate for wording. B10's fixed Topic link
still returns to the security view on page 19; B20's still returns to adoption
on page 15. "Return to caller" is an inherited fixed action, not a promise of
dynamic viewer history.

B27 also contained a substantive stale claim: currency/task/period and
request-call/depth bounds were described as merely designed. The
[current consumption contract](../../../src/core/README.md#ai-consumption-ledger-432)
contains source-coded durable admission bounds. The revision distinguishes
those controls from missing actual prices, named live approvals, complete
billing reconciliation and unjoined historical/resident accounting.
No new financial or AI activation follows.

This is an alignment/story review, not fresh currentness certification of
every retained operational/regulatory/cost claim. Historical price assumptions
and protected cost calculations are retained. Refresh changing evidence
before final presentation.

## Two Architecture Views

The [editable views and text equivalent](./diagrams/architecture/text-equivalent.md)
separate the CxO application model from the full Azure reference architecture.
Both are original drawings, using the cited Learn pages only for composition.
The full view uses official labelled Azure icons without copying either
reference solution or adding its services by analogy.

The simple view is an application/data-scope concept, not a deployment or
network map. Corporate login does not grant every application/data right.
Residents use separate identity and explicit own-case grants. AI receives
permitted task facts, not an unrestricted database or document feed.
M365 and device integrations remain labelled and gated.

The technical view is based on Bicep and a bounded System Architecture
Reviewer source analysis. It must distinguish:

* Current shared-API assistance from conditional/deferred queue workers
* Direct-demo ingress from the separately gated production edge
* PaaS services outside the VNet from their private endpoints inside it
* Human sign-in from workload managed identities
* Source-authored controls from actually verified live controls
* Resource region from model-processing geography, privacy approval and
  compliance acceptance

The diagram supports compliance evidence; it does not certify compliance,
retention, a lawful basis, provider terms or safe autonomous decisions.
Original historical diagrams and their dated evidence remain unchanged.

## Assessment And Validation

Apply the complete rubric, not only its total: A/B/C/D section floors are
21/21/9/9, no criterion may be 1, and the thought-leadership artifact/submission
requirements remain separate. Source-backed diagrams support A1-A3 and the
deliberate workflow/AI distinction supports A7; neither proves production
implementation completeness, measured model advantage or greater autonomy.
Written package improvements support B1/B2/B6 and preparation for B4/C2/C3.
Section D's human reviews/publication and actual live evidence remain unfilled
where the retained record says so.

The completed build, exact source/delivery bindings, changed-page inspection,
navigation checks and independent review dispositions are recorded here
after execution. Passing mechanical checks do not demonstrate rehearsal,
projection/keyboard/assistive-technology acceptance or housing benefit.

### Component Checks And Corrections

Build/Verify preserve 54 ordered slides and nonempty notes, 108 actual
fixed-jump actions, timing and all six protected cost slides/calculations.
The package contains 293 baseline members plus five declared PNGs.
Seven new Node source-contract tests, 32 native-shape checks, canonical
source-hash semantics and nine PDF-navigation regressions pass.

The Linux preview renders all 54 pages and verifies every destination and
hit region without overlaps. All 349 revised text frames retain their
complete words within declared bounds using 1.5-point tolerance.
Ten pages change visually (9/12/14/16/27/31/37/46/47/54); 44 remain
pixel-identical to the previous delivered Linux PDF. Page 1 changes
narration only. Page 22's existing caveat gets a text-box height correction,
with unchanged wording and pixels. No experimental data or result is added.

The first preview exposed wrap/overlap in the new page-16/page-54 copy and
an inherited page-22 glyph overrun. Shortened wording and larger appropriate
text bounds resolve these without shrinking type or changing timing.
The original failed comparison and previews remain in the external session
run; they are not relabelled as successful validation.

The System Architecture Reviewer found no substantive topology defect in the
new technical assets, but identified a source-locator error: Flow 10's
permission link named the Event Hub entity at line 77 rather than the receiver
assignment. It is corrected to line 147. The original source inventory,
precision findings and corrective assessment remain retained separately.
This is assisted source critique, not architecture adoption or cloud acceptance.

Excalidraw CLI 0.2.0 uses existing Chromium locally. The full reference PNG
includes editor frame chrome; the core frame is exported separately and the
SVG omits editor chrome while retaining the same nodes/flows.
LibreOffice 24.2.7.2 emits a `javaldx` startup warning but successfully renders
the deck. Neither that preview nor the local measures are native Windows
PowerPoint, keyboard/AT, projector or human acceptance.

Independent exact-head storytelling/source assessment and the fresh focused
publication gate remain separate. The owner approved a normal latest-main
merge before final publication; no rebase or force-push is authorised.
