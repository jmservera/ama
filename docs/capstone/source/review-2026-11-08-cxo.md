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

The implementation commit is `35907670`; the owner-approved normal merge
completed as `b2009737`, incorporating main `fa7ae0c9` without conflicts.
No diagram-referenced infrastructure declaration or deck source changed.
The only changed diagram-evidence input is the API README; its bounded-chat
section is identical, so the diagram refresh changes provenance hashes,
not topology or claims. The final candidate needs a fresh gate and
independent exact-head assessment after that refresh.

The initial focused-gate attempt selected all runtime/resource groups because
the revision unnecessarily extended the shared builder's media-prefix list.
That attempt was stopped, not reported as passed. The final implementation
instead reuses the existing additional-media naming contract and restores the
builder exactly to main. Diagram IDs, content, hashes, visible meaning and
behaviour do not change; no gate rule or protection is weakened. A new
exact-head gate follows the packaging correction.

### Independent Story Review And Owner Disposition

The independent assessment of `08e4d3ca` is **FAIL**, retained rather than
replaced by the otherwise coherent narrative verdict. It found three Medium
consistency issues:

* Main 21/B25 52 and B26 53 still called admission controls proposed, while
  B27 correctly described their source-coded status.
* The page-16 SAY paragraph overclaimed a historical binary-support run;
  the cited observation establishes EPC selection, with support separately
  specified.
* B18/page 45 labelled its fallback "Recorded walkthrough", whereas the
  prepared route uses repository evidence, not a recording.

All three corrections are accepted. The owner explicitly approved a narrow,
tested status-wording/narration exception on protected cost pages, with every
financial number, calculation, currency, timing and action retained.
The builder requires that exact revision name, permits only fixed status
substitutions on 21/52, and compares all remaining slide/note bytes exactly.
Negative tests reject other numbers, geometry, notes and approval values.
It must report the status exception; raw-byte preservation of all six pages
is not claimed after that correction.

The historical model claim now distinguishes observed EPC selection from
specified binary support. The fallback label is "Repository evidence".
No new model run, recording, approval, price or accepted-value result follows.
The original FAIL and exact corrective assessment are preserved in PR evidence.
These shared authoring-guard changes require a fresh full local matrix; the
earlier partial receipt is historical, not publication evidence for this head.

## Later 8 November: IoT, Resident Site And Main Deployment Slide

### Communication Job And Audience Map

The owner explicitly selected an **added full Azure deployment slide on the
main route**, including supporting services and gated options, rather than
an appendix-only replacement. The mixed CxO/AMA panel setting retains the
planned 30-minute presentation and separate ten-minute demo. Exact attendees,
prior knowledge and actual projection conditions are unconfirmed. Seek the
next bounded validation question and accountable owners, not deployment,
service procurement, cost approval or increased autonomy.

| Group / preference | Needs and strongest proof | Trust risk / intended action |
| --- | --- | --- |
| Sponsor: Sergeant primary, Scientist secondary | Recommendation first; one source-grounded deployment map, an explicit 45-second increment and unchanged cost arithmetic | Reading every Azure label obscures the decision; agree the validation scope, owner and missing evidence |
| Technical/assurance: Scientist primary, Sergeant secondary | Receiving chain, SQL responsibilities, identity/network boundaries, source declarations and gates; exact mapping/link tests | Source existence is not accepted live integration or compliance; identify the next integration/control test |
| Resident/service perspective: Therapist primary, Scientist secondary | Own-case access, separate identity, assisted continuity and independent safety; retained brief and permission contracts | Synthetic journeys are not resident testimony or real consent; retain resident agency and test actual needs |
| Future-oriented sponsor: Evangelist secondary | Imagine reusable accepted history supporting reviewed quality decisions, after today's evidence | Materialized averages and sensor-linked L4 flags are not current functionality; approve a question, not an assumed benefit |

Use a deliberate sequence: recommendation -> people and case scope (S11) ->
deployment responsibility/gates (new S11A) -> resident journey (S12).
Keep the one factual core while changing register, not the facts.

### Narrative And Operative Route

**S11A claim:** Azure connects home evidence to an owned action, with explicit
integration and authority limits. The receiving chain is home sensors ->
Azure IoT Hub -> Event Hubs -> validated/idempotent intake -> SQL accepted
observations/history -> averages/analysis derived on read. No ADX/Fabric,
new standalone stream worker or household telemetry in Log Analytics is added.
The employee Workbench uses the case API; the separate synthetic resident
site targets the shared contract, not a proved live integration.

The main diagram includes SQL/Blob/conditional Foundry, private endpoints/
DNS, registry, Vault and Monitor, plus separately gated edge/token/background/
queue/model/simulator options. It distinguishes the five current evidence
helpers from the brief's Quality Verification sensor-checking/L4 flag target.
Sensor-to-helper linkage and persisted averages remain integration proposals.
Existing analysis functions do not establish a served analysis API or
Workbench integration; the service links are gated targets.
Neither an average nor a model response is a safety diagnosis or acceptance.

The new slide is **physical 13 / S11A / package part 55 / template 12**.
Existing baseline parts/IDs stay stable. Main pages become 1-27; QX is 28;
B01-B27 are 29-55; B10 is 38 and B19 is 47. Protected cost pages become
6/11/22/33/37/53. Native fixed links target the same existing parts, so their
physical destinations shift without retargeting the actions.
Visible index/answer/topic page labels are incremented consistently, including
the protected cost-page navigation footers. That exception changes no financial
number, formula, price, currency, frame geometry or action target.

The new 45-second slot is 11:40-12:25. Original narration slots and shared
progressive-build durations remain unchanged. The revised total is **24:30**,
leaving **5:30** in the planned 30-minute slot. Original `TIMING` windows
remain baseline provenance; `CURRENT ROUTE TIMING` is operative. This is a
budget, not a timed rehearsal or evidence that all reference notes can be spoken.

### Evidence Register And Prepared Challenges

| Claim | Evidence, inspected 8 November | Type / limit |
| --- | --- | --- |
| Required five business jobs, original L2-L4 and resident/professional/Finance rights | Original Case Study 48; addendum's later autonomy/optional resident qualifications | Case requirement and unsigned proposal, not present end-to-end acceptance |
| One-way IoT receiving route | `infra/modules/iothub.bicep`, API `iot_stream.py` and `sensor_ingestion.py`; retained IoT research synthesis | Source declarations/adapters; live device identities, routing, SQL acceptance and calibration remain gates |
| Accepted telemetry/history and derived averages | Core `store.py`, `sensor_analysis_store.py` and `sensor_analysis.py` | Retained observations and read-only analysis; no proved materialization service or automatic task from analysis |
| Current quality helper is evidence preparation | Core `assistants.py` registry/projection | Home/measures/quality/checklists/documents; does not establish sensor aggregates wired into the helper |
| Resident site and permission separation | Addendum optional service proposal; existing API/core/resident prototype contracts | Separate synthetic showcase; shared-case/managed identity, explicit grants/revocation, lawful basis, retention and real consent remain gates |
| Supporting services/options | Bicep-grounded editable diagram and text equivalent | Declared topology, not cloud inventory, GDPR/PAS compliance or provider processing-geography acceptance |
| Company/resident context | Company-profile research, including owner-confirmed not-for-profit status and labelled sector models | Unknown company details and modelled resident indicators are not findings from residents |

Prepared concise answers:

* **Why SQL rather than another telemetry platform?** The existing intake and
  relational store already own accepted observations and history. Reuse those
  contracts; a new analytics estate needs a measured workload and its own
  cost/control justification.
* **Are the averages stored today?** Observations are retained; averages and
  quality/sufficiency analysis are derived on read. Persistent materialization
  and helper integration remain proposals, not delivered functionality.
* **Does Quality Verification already flag automatically?** The original
  brief requests L4 raise-only flags. Today's quality helper prepares evidence;
  sensor-linked autonomous flags and their critical-miss/reviewer-load evidence
  remain separate scope and release gates.
* **Does the resident website share staff login or see every home?** No.
  External identity and explicit own-case/representative permission are
  separate; login is not works consent. Shared-case wiring is still gated,
  and assisted service remains available.
* **Are the Azure boxes compliant and live?** This is source-backed design,
  not acceptance evidence. Name the specific source/control, say what was
  checked, and identify the owner/test still required.
* **Can an average prove damp is resolved?** No. Aggregates do not replace
  calibrated readings, sufficient evidence or competent inspection. Resident
  hazard reports follow the independent human safety route.

### Delivery: Seven Observables

| Observable | Moment-specific adjustment |
| --- | --- |
| Posture | Face the room and settle before the S11A claim; do not deliver the decision while turned to the diagram |
| Gestures | Trace the sensor chain once, then mark resident permission separately; distinguish source-backed paths from dashed gates |
| Movement | Stay still for SQL responsibility and the authority limit; return toward the audience for the resident-journey transition |
| Language | Say “retained observations”, “derived on read”, “separate synthetic showcase” and “gated integration”; avoid “already deployed” |
| Voice | Slow briefly on the average/materialization distinction; finish the 45-second summary without reading the full service inventory |
| Facial expression | Listen neutrally to a challenge; restate the actual concern before answering, conceding an accurate limitation |
| Dress | Match the confirmed executive setting; avoid visual distractions competing with the dense deployment view |

### Complete Assessment-Guide Review

No new numeric score is assigned. Section floors remain A21/B21/C9/D9,
no criterion may be 1, and artifact submission/attendance remain independent.
The following is a preparation assessment, not a panel observation.

| Criteria | Package support / remaining evidence |
| --- | --- |
| A1 architecture; A2 trade-offs | Main deployment, stable contracts and deliberate SQL reuse support explanation. Scaling, failure-domain and alternative workload evidence must still be demonstrated |
| A3 security/compliance/RAI | Identity, permissions, private endpoints and separate decisions are visible; live isolation/threat-control tests and legal/privacy approval remain unproved |
| A4 implementation | Source-coded intake/storage and partial helper breadth are disclosed; source gates do not establish complete live sensor/resident end-to-end functionality |
| A5 operations/cost | Supporting Monitor and unchanged financial arithmetic remain; measured reliability, complete billing and accepted business-value denominators are still required |
| A6 AI/evaluation; A7 autonomy | Current five-helper proposals are distinguished from original L2-L4 targets and deterministic state control; no measured model advantage or higher authority is invented |
| B1 structure; B2 calibration; B6 written craft | Added main-route responsibility map follows the application concept and precedes resident experience; readable rendered assets/navigation remain delivery checks |
| B3 demo/hook; B5 timing | Existing under-two-minute hook/recovery and revised 24:30 plan remain preparation; actual execution/time discipline needs rehearsal |
| B4 Q&A; B7 evidence | Prepared answers and exact source/type limits support depth; live composure and action-ready measured results cannot be generated from a deck |
| C1 discovery; C2 listening; C3 influence/honesty | Case stakeholders, resident agency and missing evidence are explicit; actual discovery/listening and the accountable human decision remain unobserved |
| D1 substance; D2 publish-readiness; D3 dissemination | This architecture/deck change adds no experimental outcomes, reviewer acceptance, artifact submission or new dissemination evidence |

### Focused Delivery Checks

Source insertion checks, six refusal mutations, 32 native-shape checks,
canonical hash semantics and ten PDF-navigation regressions pass. Build,
Verify, final media bindings, Linux render and affected-page visual checks
are recorded below after execution. No heavy publication gate is claimed by
these component checks; the parent workflow owns exact-head publication.

#### Final Delivery And Corrections

The final Build/Verify passes with **55 slides and nonempty notes, 108
unchanged fixed actions/destinations, 303 package members** (293 original
baseline members, six declared PNGs and four new slide/notes members).
The four exact structural metadata changes insert part 55 after physical
12 and retain every original section/slide ID. Of the baseline members,
186 remain byte-identical; all 107 expected revisions match the generated
source contract. The baseline file itself remains pinned at
`2bab9b79de4352a1915dab04d1846a4c4be90f6889a2b9b6af4807e48a33d5f8`.

The insertion regression verifies all 27 visible answer numbers and
extracts 30 required service/boundary terms from the actual new slide's notes
and image alternative text. All six protected cost pages pass exact expected
content checks and negative mutations for numbers, geometry, notes and
unapproved status. Status-word exceptions remain on physical 22/53;
navigation footer changes are on 33/37/53. Original duration slots,
financial numbers/currencies, arithmetic and action objects remain unchanged.
The operative route clock is 24:30, not a preserved 23:45 running clock.

Local review of the first complete deck identified two diagram-copy issues:
Quality was only named in notes rather than visibly among the five helpers,
and “read-only” ambiguously covered intake that appends observations.
The final diagram explicitly includes Quality, labels the existing API
telemetry/averages responsibility, and limits read-only/no-task wording to
analysis. Its footer labels sensor-to-Quality a gated target. The diagram
owner also separated token-only Blob from the digest arrow to evidence Blob.
No topology, new service adoption or runtime action follows those corrections.
The final notes explicitly say existing functions do not establish a served
analysis API or Workbench integration.

LibreOffice 24.2.7.2 renders all 55 pages; every one of the 108 PDF
destinations/hit regions is verified and unambiguous. Actual words are
present in all 427 inspected revised/native navigation text frames.
There are zero new non-native word-bbox hints; 128 deduplicated hints
reproduce words/positions in prior delivered pages. These are not native
PowerPoint bounds or accessibility acceptance. The first broad bbox check
reported duplicated/inherited hints as failure; that raw result is retained
outside the repository, not presented as a successful native bound test.

After aligning the added page, 25 original pages are pixel-identical.
The 29 changed existing pages are the CxO page, QX and all appendix pages
with updated physical-number labels; the new deployment page is additive.
Visual inspection covered 12/13/14/28/33/37/38/47/53/55. All 55 final PNGs
are identical to the visually reviewed corrected preview: the last update
changes notes only. The main full projection is approximately 12.1-point
minimum text, and CxO approximately 12.0; the selected core directs readers
to the full-size editable technical detail and main page 13.

The final delivery is
[PPTX](../deck/zava-forward-cowork-v2-draft.pptx) plus
[PDF](../deck/zava-forward-cowork-v2-draft.pdf), regenerated
[speaker notes](../pitch/speaker-script.md) and
[27 answers](../pitch/questions-and-answers.md), with
[compact source/delivery bindings](./validation.json).
Final PPTX SHA-256:
`7cf5abf93936aaa3b676c766479e91327a79c1746215a3a837be37b906acbc64`.
Final PDF SHA-256:
`09de4170ed89a845da9ffd61bc36e211a770f4d96944952e795e649187cf14cc`.

The focused checks also include 32 native-shape checks, canonical source/
receipt hashes, ten PDF regressions and the diagram owner's 14 final
source/browser/geometry checks. `javaldx` emits its inherited startup warning
but rendering succeeds. Native Windows PowerPoint, actual projector/
keyboard/assistive-technology, rehearsal, resident/staff, legal/privacy and
production acceptance remain separate. No numeric score, cloud change,
paid inference, commit, push or heavy publication gate was performed by this
presentation work.
