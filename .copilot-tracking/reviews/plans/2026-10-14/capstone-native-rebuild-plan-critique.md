---
title: Capstone Native Rebuild — Independent Plan Critique and Communications Handover
ms.date: 2026-10-14
---

# RPI Plan Critique: Capstone Native Rebuild

## Metadata

* Task ID: capstone-native-rebuild-2026-10-14.
* Plan: .copilot-tracking/plans/2026-10-14/capstone-native-rebuild-plan.md.
* Phase details: .copilot-tracking/details/2026-10-14/capstone-native-rebuild-phase-details.md.
* Research: .copilot-tracking/research/2026-10-14/capstone-native-rebuild-research.md.
* Critique execution status: **Complete**.
* Verdict: **Revise — three Medium findings, no Critical, High or Low findings.**
* Assessment count: this is the one independent final-candidate plan critique.
  No agent was launched and no repeated critique is requested.
* Contributor: requested AMA Presentation Communications Strategist.
* Only authored asset: this file. Plan, sources, deck, README files, tenant,
  application, authentication and existing working assets are unchanged.

## Inputs and Criterion Boundary

The confirmed owner asks the strategist and PowerPoint builder to rebuild the
capstone and replace its process-map image with native editable PowerPoint
boxes, with aligned title tops and common body starts. Preserve 22 slides,
all substantive evidence and controls, Zava branding, customer-first argument,
the existing publication workstream and truthful limits. There are no removals
or additional slides. Automatic continuation is already authorized; there is
no routine clarification or new budget request.

Read the complete plan, phase details, supplied research, original case,
addendum, company research, knowledge-base index, docs/reference/memory.md,
complete assessment guide, docs/capstone/README.md, canonical PPTX text and
all notes, and the SVG. Relevant current PRD, ADR, MVP, infrastructure,
service registry/review code and measurement/transition sections were also
read. Source references and their boundaries are registered below.

Canonical source:
docs/capstone/deck/zava-forward-executive-draft.pptx, 22 slides.
Read-only stdlib ZIP/XML extraction was used. Notes were checked through
slide relationships, not assumed from filename numbering: slide 13 points to
notesSlide22.xml; slides 14–22 point to notesSlide13.xml–notesSlide21.xml.
**This is valid existing packaging, not a discovered notes corruption.**
The old source contains stale 11 October / v0.13 / pinned-#58 proof wording;
the current worktree head is cabe05c. Runtime source, serving image and
documentation head are different provenance identifiers.

Decisions/dependencies assessed: P01-T01 → P01-T02 → P02-T01; parent owns
source claims, final asset inspection and publication; builder owns generated
shapes, measured geometry and fresh exports. Working output remains exclusively
under .copilot-tracking/ppt/2026-10-14/zava-forward-capstone-rebuild/.
Only the parent delivers the final byte-identical validated PPTX to the
canonical path and updates indexes/log/#68. No runtime deployment, auth work,
paid inference, application test change or specialist substitution is implied.

Boundary: assess planning credibility, supply communications content, and
review repository evidence against every guide criterion and floor. This is
not a new runtime verification, formal requirements review, legal-currentness
review, official rubric score, visual inspection of a rebuilt deck, rehearsal,
human acceptance or approval of a customer investment.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner native-map and peer alignment request | Covered in candidate | Named text shapes, TOP anchors, title/body geometry, no map picture; implementation specification below |
| Retain 22, additions zero, removals none | Covered | Plan scope and P01-T02; original-to-refreshed content inventory below |
| Mixed CEO/CIO/CFO, customer-first, planned 15 minutes | Covered by this P01-T01 contribution | Audience map, all-slide copy/notes and timing below |
| Current proof versus proposed design | Partial before disposition | Sources named, but no exact generated-claim oracle; PC-001 |
| Full notes/count/integrity regression | Partial before disposition | Note existence does not test correct topic/source association; PC-003 |
| Demo hook and recovery, no speculative capability | Partial before disposition | Demo timing requested but permitted demonstration mode and failure route unspecified; PC-002 |
| Five capabilities, owners, reactive/proactive, workflow core | Covered, concretized here | Native map specification and semantic inventory below |
| Safety, resident choice, professional/financial authority | Covered | Preserve on slides and in notes; never replace with generic “human in loop” |
| Full guide, all floors, separate pitch/artifact acceptance | Covered by this critique | All 20 criteria and floor analysis below; no numerical scoring |
| Generated geometry and full-deck fresh exports | Covered | Builder-owned in P01-T02; parent independently inspects final assets |
| P02-T01 final bytes, sources, publication, one Review | Covered | Parent ownership stays locked; publication is not product acceptance |
| Current PRD/ADR acceptance and residual RV-001/RV-002 | Covered as open | Operator proof does not close requirements, staff, human, quality or value gates |
| Private/pip tooling recovery | Accepted dependency | Parent separately restores tooling; this review needs neither python-pptx nor uv |

## Verdict

**Revise**, not Blocked. The candidate has sufficient evidence and the right
scope, specialist sequence, native-shape requirements and validation ownership.
Its remaining credibility risks are specific acceptance-contract omissions,
not reasons to remove native shapes, requested specialists or existing
controls. Apply the three direct corrections below and use the integrated
handover to proceed to P01-T02 without a second critique. Completing the deck
will not establish panel readiness or full product acceptance.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Replace generic proof checks with an exact claim-status oracle

* Related IDs: Functional Requirements; Acceptance Criteria; P01-T01;
  P01-T02 semantic checks; P02-T01 source-claim validation.
* Evidence: the canonical PPTX slides 11/12/17/19/21 and associated notes
  still frame proof around pinned #58 and v0.13. Current infra/README.md,
  “Five-assistant version: current handover”, and
  .copilot-tracking/reviews/logs/2026-10-14/five-assistant-live-delivery-review.md
  establish a different, precisely bounded milestone. The candidate asks for
  current proof and observed/open checks but does not enumerate the
  must-pass propositions or contradictions.
* Concern: “five real assistants” or “durability passed” can silently become
  staff acceptance or retained-old-data claims. Conversely, keeping only
  “narrow feasibility” obscures delivered work. Ordinary assistant authority
  is absent; proactive is off; the synthetic audit/recommendation baseline
  was explicitly reset before the new unchanged-state checks.
* Impact: CEO, CIO and CFO could approve the wrong next gate on an inaccurate
  statement of present capability, authority or cost.
* Smallest useful change: parent adopts the truth oracle and retained-content
  inventory below as P01-T02/P02-T01 acceptance evidence. Refresh all slide
  copy, notes and dates together, including optional appendices; distinguish
  current requirement status from historical acceptance.
* Action owner: planning parent for source truth/disposition; builder renders
  the supplied wording, not a new interpretation of runtime proof.
* Exact resolving evidence: final slide/relationship-resolved-notes extraction
  with each oracle proposition mapped to slide/source, zero unqualified
  full-acceptance/production/active-scan claims, source/image/revision match,
  clear reset-versus-post-reset preservation distinction, and a parent
  recorded source-claim check. No additional cloud call is required.
* Decision route: **direct planner correction**. Owner intent already fixes
  the scope and boundaries; no significant/divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Fix the demonstration mode before building the proof-point slide

* Related IDs: 15-minute goal; P01-T01 demo/recovery; P01-T02 notes;
  B3/B5 and no-cloud/no-paid-execution constraints.
* Evidence: current infra/README.md records normal serving assistant authority
  absent and proactive off after finite operator QA. The canonical slide 7
  notes say to show “actual executed scope” or use an illustrative trace.
  Candidate details request demo/recovery timing without specifying a
  callable, authorized live path or choosing evidence playback.
* Concern: a builder/presenter could script Generate, Verify or Accept clicks
  that are unobserved, disabled or require new paid authority; an illustrative
  recovery could also be mistaken for recorded execution.
* Impact: avoidable demo failure or a false human/operational acceptance claim;
  B3 asks for a clear outcome hook and graceful recovery, not fabricated live
  capability.
* Smallest useful change: adopt slide 12's **recorded, repository-evidence
  walkthrough**, maximum 110 seconds, and the bounded recovery script below.
  Slide 7 stays explicitly illustrative. No live inference, login, source
  verification or controlled action is part of this deck rebuild.
* Action owner: parent selects the local public evidence view and validates
  its claim; builder supplies native proof summary and recovery notes;
  presenter later rehearses separately.
* Exact resolving evidence: slide 12 and notes say “recorded operator-service
  proof, 14 October”; a 110-second sequence and ≤15-second recovery pivot
  are present; the script contains no fresh model/API/auth operation and
  never describes playback as live. If no public output artifact exists,
  show aggregate receipt only, not invented output or private receipts.
* Decision route: **direct planner correction**. It implements existing
  authority limits without asking for spending or changing application scope.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Notes regression must validate semantic association, not merely presence

* Related IDs: Acceptance Criteria “All22slides have notes” and “text and image
  integrity”; P01-T02 regression; P02-T01 final inspection.
* Evidence: current source slide 13's actual notes target is notesSlide22.xml;
  subsequent slides' note filenames lag their slide numbers. Source text and
  notes are sound when the relationships are followed. The candidate
  specifies note count/integrity but not relationship-aware topic checks.
* Concern: ordinal note copying can create a well-formed 22-note deck with
  finance notes on the map, transition notes on finance, and shifted sources
  thereafter. A count/text-presence test would pass.
* Impact: presenter says the wrong claim and the scorer receives the wrong
  explanation/source beside a slide. This is a semantic regression, not a
  cosmetic filename concern.
* Smallest useful change: builder binds each refreshed slide's notes by
  stable slide identity/relationship, then checks a topic and source sentinel
  for every slide against the 22-slide handover below. Parent inspects the
  final relationship-resolved extraction. Renumbering notes files is neither
  required nor sufficient.
* Action owner: builder for generated association regression; parent for final
  notes/source acceptance. No transfer of locked validation ownership.
* Exact resolving evidence: a 22-row report of slide index/title, actual
  notes relationship, topic sentinel and source references, all matching.
  Include map→five capabilities/proactive-off, finance→fictional cash example,
  proof→five calls/6884/open gates, closing ask→planning-only. Verify the
  delivered copy equals these checked working bytes.
* Decision route: **direct planner correction**, no user response.

## Strengths and Residual Risk

The candidate correctly preserves 22 slides, authoring sources, native
editability, font/geometry checks, fresh whole-deck exports and parent
publication control. Its exact “none” removals and prohibition on silently
replacing original case/memory/legal snapshots protect the evidence chain.
Preserve both requested specialists; this strategist contribution is complete,
while the requested powerpoint-builder remains P01-T02.

Accepted residuals are already explicit in the plan: PowerPoint/font fidelity,
real timed rehearsal and live Q&A need later human observation; RV-001 owns
real staff/session/source/accessibility acceptance, RV-002 semantic/value
evaluation. Those are not defects to fix by deck-only claims or another
critique. A7 may remain an assessment vulnerability because the implemented
service is deliberately bounded proposal generation, not demonstrated
independent autonomous reasoning. Do not expand authority to chase a score.

## Audience and Outcome Summary

**Audience/setting:** a mixed CEO/CIO/CFO council pitch about Zava North Homes,
with Assets/Programme/control-owner concerns represented. Fifteen minutes
including the short evidence demonstration and a little room for challenge;
optional appendices are not a second main story. Treat attendees as the
customer stakeholders, not as people to whom a fictional company lecture is
needed. Case data and operating evidence remain labelled.

**Known starting point:** original five-agent request, spreadsheet-coordinated
programme, 60,000-home case scale, owner-confirmed not-for-profit purpose.
Unknown: actual audience knowledge, operating bottleneck, delegations,
baseline outcomes and affordability. Do not assume a stakeholder's personality
or prior endorsement. No direct resident/employee research has been supplied.

**Requested action:** endorse preparation of the next bounded acceptance/value
proposal; nominate/confirm accountable owners, evidence needed and an agreed
return date. Not permission to deploy, spend, procure, enable scans, make
resident contact, approve work, submit funding or roll out to production.
The technical exercise was already delivered under its own scoped authority;
this pitch must not ask to “prove real AI/SQL exists” as if that had not happened.

**One-line argument:** “We can now show five bounded proposal paths on real
services. The next decision is whether they help people deliver safe,
resident-accepted homes better than the same controlled workflow without AI.”

## Recommended Archetype Strategy

Use a deliberate sequence, not an averaged style or fixed personality labels.

| Audience need / primary and secondary preference | Needs to hear | Trust/attention risk | Strongest available proof | Intended action / emotion |
| --- | --- | --- | --- | --- |
| CEO/Assets: Control, then Connect/Create | Decision first; resident promise; one owned journey; what stops unsafe scale | Cloud tour, generic transformation, inflated delivery or grant claims | Case request, retained human/resident gates, connected journey and explicit stop conditions | Sponsor the evidence stage; confidence without false reassurance |
| CIO/Digital: Compute, then Control | Exact changed runtime boundary, identities/contracts, failure and stale-source handling, what is not proved | Target diagrams presented as deployed estate; “all tests passed” without scope | Image05/revision12 receipt, independent SQL content/restart evidence, ADR runtime and current service contract | Own assurance evidence and supportable next gate |
| CFO/Finance: Compute, then Control/Connect | Gross cash versus grant states; whole-life/review cost; no new appropriation | Token count called money saved, grant opportunity called cash, historical cap called a quote | Explicit fictional home arithmetic; measured call/token count with no currency guarantee; paired-value design | Require scoped affordability and cost evidence, retain independent authority |
| Programme/resident/safety interests: Connect, then Compute | Safe/non-digital contact, no inferred consent, capacity, manual routes, named escalation | Treating concerns as resistance; claims that role agents represent residents | Requirement/control evidence and declared gaps, not invented testimonials | Co-design and later directly test burden, clarity and safeguards |
| Mixed room, Create moments | Tangible better future without new ungrounded capability promises | Vision floating free of evidence or an artificial urgency claim | Same-home illustrative journey linked to concrete next tests | See the opportunity, then choose the evidence gate |

Sequence: decision and resident purpose (1–2); evidence and reasoning (3–6);
tangible journey and people (7–8); inspectable mechanism and actual proof
(9–13); affordability/value (14–16); owners, gates and choice (17–18).
Use “the outcome is” at opening/close, “the evidence shows / does not show”
at proof, “imagine this home” only on the labelled illustrative journey,
and “let us understand what residents and staff need” at adoption.

## Evidence Register and Claim Oracle

References below are workspace-relative. IDs are local handover shorthand,
not claims of approval. Each final notes section must expand its referenced
IDs into paths, section names, date and status.

| ID | Source and sections | Classification / allowed use |
| --- | --- | --- |
| S01 | docs/case_study_48_original.md, Business Challenge; Architecture Brief; Expected Outcomes | Original 10 September request; 60,000-home case, five pressure points, not achieved benefits |
| S02 | docs/case_study_48_addendum.md, Business Challenge; Executive Assessment; Digital Foundation; Where Agents Fit; Recommended Executive Decision | Maintained 14 October synthesis and proposed controls; bottleneck/outcomes not verified company findings |
| S03 | docs/reference/research/company/company-profile-research.md, Confirmed Company Information; Role and Decision Map; Priority Company Gaps; Evidence Limitations | Owner-confirmed not-for-profit; modelled company/resident/finance attributes are not company facts or delegations |
| S04 | docs/reference/research/company/agent-request-challenge.md, Summary and capability sections; docs/reference/research/company/agent-what-if-study.md, method and revised verdicts, as carried in S02 | Sector-informed role-agent hypotheses, not employee interviews or resident testimony |
| S05 | docs/reference/research/company/pilot-measurement-challenge.md, Owner Decision; Proposed Measurement Design; Freeze/Analysis; Guardrails | Proposed comparisons and protected outcomes, not executed experiments |
| S06 | docs/case_study_48_addendum.md, EXA-002/003/004/005/007/008/010/011/012/013/015; Numerical Targets and Attribution; Subsequent Application Exercise Builds | Historical selected exercise assumptions; explicitly fictional costs/terms, not budgets, awards or current open authority |
| S07 | docs/prds/zava-forward-retrofit-programme-demonstrator.md, v0.14 front matter; component contracts; threat model; Five Reactive and Proactive Assistants; orchestration; evaluation; current handoff | Current candidate, 47 FRs/61 ACs; fresh requirements review and amended owner acceptance open; CON-009/AC-057 full acceptance not passed |
| S08 | docs/adrs/0002-pilot-readiness-architecture.md, Five-Assistant Exercise Runtime; Fresh Ledger and Synthetic Coverage Learning; current delta | Current lean proposal runtime, explicit reset, image/source/revision-linked service proof; proposed readiness estate separate |
| S09 | infra/README.md, Five-assistant version: current handover | Exact serving/source/model/SQL/restart receipt and authority-off state, 14 October; no fresh cloud inspection in this task |
| S10 | .copilot-tracking/reviews/logs/2026-10-14/five-assistant-live-delivery-review.md, Completed Work; Validation; RV-001/RV-002; Outcome | Technical Review Complete / Residual work, not blanket product conformance |
| S11 | mvp/README.md, Honest limits; Five retrofit assistants; Operator authority; current delivery paragraphs; mvp/zavaforward_mvp/assistants.py, REGISTRY/RULES/capture/eligible/review | Source and documented implementation; captured metadata/category citations, not unrestricted document reading, human source review or semantic entailment |
| S12 | docs/adrs/0001-azure-architecture.md, Hybrid M365 and Excel transition; Options still to compare; provisional appraisal | Proposed transition/full topology and historical illustration, not current deployment or scored customer platform choice |
| S13 | docs/ideas/typesafe-system-one-agent-fit.md, pinned #58 feasibility/parallel experiment, as carried in S02/S07 | Historical separate Decision 1 selection/generation evidence; not the provider for the five new service calls; no new evaluation results |
| S14 | docs/capstone/README.md; docs/reference/method/ama-capstone-assessment-guide.md; docs/reference/memory.md | Publication/storage map, complete official guide, owner communication preferences; these are distinct from observed pitch/score evidence |
| S15 | docs/capstone/deck/zava-forward-executive-draft.pptx; docs/capstone/deck/agents-in-retrofit-process.svg | Existing 22-slide content/relationship-resolved notes and map semantic source, not proof of future operation |

**Exact current-proof oracle (parent verifies final source claims):**

1. Current documentation/source context is cabe05c; runtime source is
   cd14b3b379026a87ebfa3e9058ac10c0df7888eb, not cabe05c.
2. Image05 is assistants-20261013-05, manifest
   sha256:e0254cb3a0599c21802f0b6515f975550cf00ddce4849d04fd3fa3d50683af20,
   serving ca-forward-test-api--0000012. Short forms on screen; exact forms
   in notes. Do not rename historical revisions.
3. The owner explicitly reauthorized the synthetic database reset on
   14 October after the earlier cancellation. Previous exercise
   recommendations/audit were reset, not preserved by migration. Retain
   generator/60,000-stock lineage; the new programme baseline is 980 cases,
   38 booked visits and 11 actual privately bound tenant staff. Do not publish
   their identities. Counts are exercise context, not real resident activity,
   staff use or programme success.
4. Five distinct registered operator service paths returned citation-validated
   ready proposals through real Azure OpenAI deployment standard, model
   gpt-4.1-mini-2025-04-14: five calls/attempts, 6884 total tokens, 15 ledger
   events. These are not Decision 1 calls or five independent autonomous agents.
5. Against that new baseline, independent controlled-domain hashes stayed
   unchanged by proposal generation, and full assistant-table content,
   outputs and usage survived an actual serving-revision restart. This is
   stronger than row-count equality, weaker than disaster recovery/restore.
6. Bounded operator QA ended. Normal serving assistant authority is absent;
   proactive scans are off. A registered capability is not current standing
   authority. Neither proactive enablement nor new calls are authorized here.
7. Citation validity means permitted source/provenance binding, not semantic
   correctness or competent source verification. None of the five has human
   verification/acceptance recorded by that operator exercise.
8. Real staff-browser/API, role/human/source/accessibility acceptance,
   semantic calibration, paired task value and operational outcomes remain
   open (RV-001/RV-002). PRD v0.14 remains a candidate. Do not mark AC-057
   or full requirements/product/pilot/production acceptance passed.
9. No observed doubled throughput, lower bills, secured £40m, programme
   savings, cost per accepted home, currency-cost cap, production selection
   or corporate investment approval follows. Token allowance is not a
   currency guarantee; historical EXA-012 and the scoped #58 override are
   not a new funding commitment.
10. Source-level automated contract tests are evidence of tested boundaries,
    not a live staff session or panel behaviour. No new score is inferred from
    cabe05c's historical rubric update or from successful CI.

No new legal date, statutory period, funding-round status or legal compliance
claim is needed in the refreshed slides. Preserve the independent hazard
route, source-register and human legal/control-owner approval boundary as
design requirements. If the parent later introduces consequential legal
claims, consult docs/reference/regulatory/README.md and the applicable
official source first; this task has not refreshed legal currentness.

## Narrative and Builder Handover — All 22 Existing Slides

**Status:** strategist-recommended implementation copy, not stakeholder-approved
narrative or delivery acceptance. Parent may adopt compatible dispositions
under existing authority. Each physical slide is retained; no new slide is
added. Existing subjects remain on the same slide numbers to simplify
regression. Refreshed copy replaces stale wording rather than adding another
layer of disclaimers. Use source/status footer plus full references in notes.

### Planned route and timing

| Main slide | Seconds | Cumulative |
| --- | ---: | ---: |
| 1 | 35 | 0:35 |
| 2 | 25 | 1:00 |
| 3 | 35 | 1:35 |
| 4 | 35 | 2:10 |
| 5 | 30 | 2:40 |
| 6 | 35 | 3:15 |
| 7 | 65 | 4:20 |
| 8 | 40 | 5:00 |
| 9 | 35 | 5:35 |
| 10 | 30 | 6:05 |
| 11 | 45 | 6:50 |
| 12, including evidence demo and recovery | 110 | 8:40 |
| 13 | 60 | 9:40 |
| 14 | 50 | 10:30 |
| 15 | 35 | 11:05 |
| 16 | 50 | 11:55 |
| 17 | 45 | 12:40 |
| 18 | 35 | 13:15 |

Reserve 75 seconds for one council challenge and 30 seconds for normal
transition/contingency: **15:00 total**. The demo's failure pivot is inside its
110 seconds, not an extra allowance. Slides 19–22 are optional reference
appendices, not timed additions to the main route. Their suggested response
durations below replace available discussion time or follow the pitch.
This is planning arithmetic, not a timed rehearsal.

### Slide 1 — Back the evidence. Keep the resident promise.

* **Message:** endorse a bounded next evidence stage, not autonomous rollout.
* **On-slide:** “60,000 homes. Safe, resident-accepted handovers.”
  “Today: endorse the next acceptance-and-value proposal.”
  “Real service proof now. Human and value gates next.”
  Footer: “Proposal only — no new spending or production authority.”
* **Layout:** bold resident-outcome headline left; single decision panel right.
  Retain Zava identity, cream/forest palette and original mission emphasis.
  Avoid a product logo wall or an invented resident quotation.
* **Notes:** “The outcome is not more agent activity. It is a home handed over
  safely, with the resident's decision respected and the evidence accepted.
  Five bounded service paths now have real technical proof. I recommend
  preparing the next acceptance-and-value proposal, with named owners and
  stop tests. This is not a spending, deployment or production decision.”
* **Transition:** “The original request identifies five genuine pressure points.”
* **Sources / time:** S01, S02 Executive Assessment, S03 confirmed status,
  S09–S10 / **35s**.

### Slide 2 — Five pressure points. One accepted home.

* **Message:** keep the five requested capabilities accountable to the same endpoint.
* **On-slide:** five short steps: “Choose homes / Assess & design /
  Prepare funding / Coordinate works / Verify & hand over”.
  “Measure accepted outcomes, not messages or drafts.”
* **Layout:** five peer native stage boxes, short aligned titles, no agent avatars.
  Below, one destination marker “Safe + resident-accepted + evidence-complete”.
* **Notes:** “You asked for help with prioritisation, assessment, funding,
  coordination and quality. That request remains the spine of the proposal.
  Doubling delivery and reducing bills were ambitions in the original case,
  not outcomes this exercise has established. A better draft does not
  manufacture a survey, a crew, consent or cash.”
* **Transition:** “We challenged what each end-to-end request actually contains.”
* **Sources / time:** S01, S02 Where Agents Fit / **25s**.

### Slide 3 — Each request needs rules, people and bounded AI.

* **Message:** the research changed task allocation, not the resident objective.
* **On-slide:** “Rules: gates, clocks, eligibility, versions.”
  “People: policy, consent, professional and financial decisions.”
  “AI: reconcile, prepare, draft, flag.”
  Footer: “Eight role-agent research instruments — not employee interviews.”
* **Layout:** three equal columns with common title/body starts, not a Venn
  diagram implying interchangeable authority.
* **Notes:** “Eight sector-informed role-agent perspectives challenged the
  request; they are research instruments, not the company's staff or
  approvers. Each request combines deterministic controls, accountable
  decisions and narrower text/evidence tasks. Richer inputs do not remove
  those boundaries. The binding delivery constraint is still unknown:
  capital, competent capacity, access or quality may dominate coordination.”
* **Transition:** “Three examples explain why that changes the build.”
* **Sources / time:** S02 Challenge of Requested Agents, S04 / **35s**.

### Slide 4 — Fix the prerequisite before adding the assist.

* **Message:** safe assistance depends on controlled inputs and separate decisions.
* **On-slide:** “Rank homes → approved policy + sourced facts.”
  “Offer a slot → committed capacity + resident choice.”
  “Draft funding → accepted evidence + separate ledger states.”
  “A slot is not consent. A form is not funding.”
* **Layout:** three request→prerequisite native cards; align request title,
  dividing line and body baseline. No dense paragraph screenshots.
* **Notes:** “Ranking weights are policy, not a model's choice. A schedule
  requires competent committed capacity and an informed resident decision.
  A funding pack needs the right evidence, route and Finance review.
  Application, award, claim and cash are different. These research hypotheses
  explain the prerequisite controls; they are not measured company bottlenecks.”
* **Transition:** “The shared foundation makes those prerequisites visible.”
* **Sources / time:** S02 Digital Foundation, S04 capability challenges / **35s**.

### Slide 5 — Change the handoffs, not the whole company.

* **Message:** modernise coordination around existing people and systems.
* **On-slide:** “Keep: teams, suppliers, useful systems.”
  “Add: one case, owned transitions, evidence, bounded assistance.”
  “Excel becomes reporting after a controlled transition.”
* **Layout:** KEEP/ADD panels with equal title regions; connected home motif
  between them. Do not imply current systems have already been integrated.
* **Notes:** “The proposal is a programme control and evidence layer, not
  replacement of the housing organisation. Keep useful systems, teams and
  suppliers. Introduce an owned case and a controlled transition from source
  spreadsheets to API-fed reporting. Neither the integration nor the reduction
  in duplicate effort is accepted simply because it appears in the design.”
* **Transition:** “A handoff becomes useful when its contract is explicit.”
* **Sources / time:** S02 modernisation objective, S07 boundary, S12 transition
  / **30s**.

### Slide 6 — Every handoff needs an owner and a next action.

* **Message:** observable work starts with a work contract, not a dashboard.
* **On-slide:** six equal cells: “Owner + receiver / State / Entry, exit,
  pause / Blocker + next action / Evidence version / Decision + reason”.
  “Sent ≠ accepted. Completed ≠ handed over.”
* **Layout:** 3×2 native grid with identical fixed title/body regions and
  reading order. Use concise noun phrases rather than all-caps mini-essays.
* **Notes:** “The sender retains chase responsibility until the receiver
  accepts. Record the next action, resident-update owner and relevant clocks.
  Material evidence changes reopen dependent reviews, not unrelated sibling
  decisions. Recording itself costs effort; include it in the value test.
  Hazard intake remains independent of routine handoff waiting.”
* **Transition:** “Follow that contract through one home.”
* **Sources / time:** S02, S05 Freeze/Analysis, S06 EXA-002/008/013,
  S07 lifecycle / **35s**.

### Slide 7 — One home shows the journey we still need to prove.

* **Message:** the connected target is broader than the observed service proof.
* **On-slide:** “1 Resolve conflicting evidence → 2 Agree scope, choice,
  funding and capacity → 3 Deliver; inspect; return defects → 4 Accept
  handover; close finance separately.”
  Persistent label: “Illustrative exercise journey — not an executed
  end-to-end customer outcome.”
* **Layout:** four native stages over one fictional home; amber hold/return
  branch, with human owners. Do not use green checkmarks on unexecuted stages.
* **Notes:** “Imagine one home with conflicting EPC sources. The dependent
  decision waits for a named resolver. Competent assessment and design,
  resident measure choice, funding and capacity precede work release.
  Returned evidence may reveal a defect: an independent authority sends it
  back, then accepts corrected work. Resident handover and financial closure
  are separate. This is the required connected story, not proof those steps
  have all run. The current technical receipt later proves proposal generation
  and durability, not physical delivery or this whole workflow.”
* **Transition:** “The resident and crew make that journey possible.”
* **Sources / time:** S06 EXA-002/003/005/007/008/015, S07 lifecycle and
  acceptance contract / **65s**.

### Slide 8 — A resident is not a scheduling variable.

* **Message:** choice, supported contact and real capacity precede release.
* **On-slide:** “Resident: clear options; safe phone, letter or assisted route;
  measure-specific choice.” “Delivery: committed crew, competence, materials;
  named liaison.” “Preferences ≠ consent. Silence/no-access ≠ refusal.”
* **Layout:** two generous panels, equal top-aligned titles; a separate
  “Human hazard route — never wait for AI” strip. No resident testimonials.
* **Notes:** “Let us understand what residents and staff need before calling
  a journey usable. No compulsory portal. Disclosed adjustments are not a
  licence to share diagnoses. Staff review communications and own exceptions;
  the service does not automatically send, book or instruct. Missed access
  calls for investigation, not inferred withdrawal or deprioritisation.
  Direct human research and accessibility acceptance remain outstanding.”
* **Transition:** “Trust also needs an explanation another person can inspect.”
* **Sources / time:** S02 service design, S06 EXA-004/005/007/011,
  S07 coordination contract, S10 RV-001 / **40s**.

### Slide 9 — Show the decision trace, not just an AI explanation.

* **Message:** source, rule, reviewer and change history make a decision inspectable.
* **On-slide:** “Know: source + evidence version + unknowns.”
  “Decide: rule + result + reviewer + reason.”
  “Change: authority + dependent re-review + preserved history.”
  “New source ≠ approved new policy.”
* **Layout:** three aligned trace cards, with a single return arrow for changed
  evidence. Do not imply whole-system compliance or external audit anchoring.
* **Notes:** “A generated explanation cannot substitute for source and approval
  records. Retain the applicable versions, reason, reviewer and timestamp.
  Changed sources invalidate dependent reviews. Legal and professional
  interpretations need accountable review before rules change; the repository
  is dated evidence, not a self-updating legal authority. Current assistant
  citations bind captured categories/metadata, not proof every conclusion is
  supported by a document passage.”
* **Transition:** “The workbench sits beside the systems that supply those facts.”
* **Sources / time:** S02 regulatory service design, S07 contracts/orchestration,
  S11 capture/review and honest limits / **35s**.

### Slide 10 — One workbench beside the systems you keep.

* **Message:** retain source ownership while connecting case work.
* **On-slide:** “Existing sources → validated intake → shared case →
  role queues and supported channels.”
  “Excel reports. Existing services retain their authority.”
  Label: “Target context — integrations are not all delivered.”
* **Layout:** native three-zone context, sources on left flowing into case,
  people/channels on right. Solid arrows mean intended controlled direction,
  not observed live integrations; label unbuilt links “proposed”.
* **Notes:** “The arrow is from source material into validated intake, not an
  uncontrolled write-back loop. The case connects home, building and package
  context with roles and evidence. Residents and suppliers need supported,
  scoped exchange, not open access to the internal staff workbench.
  Housing/repairs integrations, M365 document channels and import transition
  remain proposals or unverified. An integration picture is not a deployed
  connection receipt.”
* **Transition:** “The API is the authority boundary, not the model.”
* **Sources / time:** S07 context/component contracts, S11 limits,
  S12 transition / **30s**.

### Slide 11 — Let models propose; keep decisions on the controlled path.

* **Message:** the existing lean runtime preserves a separate human/domain write path.
* **On-slide:** “Staff / permitted task → API → source snapshot → bounded
  model proposal → human source review.”
  Separate lower path: “Authorized domain action → deterministic gates →
  SQL + audit.”
  “Model cannot approve, send, book, pay or clear a hold.”
* **Layout:** native two-lane control diagram. One shared deployed runtime,
  not five services or a separate deployed worker estate. Distinguish
  “observed proposal/SQL boundary” from “broader assurance still open”.
* **Notes:** “The current exercise reuses the existing workbench, API, SQL
  and model connection. Calls occur outside case/database locks. Typed
  validation and source permissions surround the model; proposal review only
  changes proposal/audit state. Human source verification must precede
  acceptance, and proposal acceptance still is not work or financial approval.
  The broader proposed queue/private-network/durable-worker estate is not
  this deployment. Manual case work remains available when assistance fails,
  expires or is disabled. Full identity, leakage, restore and role assurance
  are separate evidence gates.”
* **Transition:** “Here is what we can actually substantiate today.”
* **Sources / time:** S07 contracts/orchestration, S08 runtime, S11
  REGISTRY/capture/review, S10 / **45s**.

### Slide 12 — Five real proposal paths. No delegated decisions.

* **Message:** observed operator-service integration is real; human/value acceptance is open.
* **On-slide:** native proof receipt with three rows:
  “Real provider: 5 distinct ready proposals · 5 calls · 6,884 tokens.”
  “Real SQL: controlled state unchanged; proposal contents survived restart.”
  “Current: authority absent · proactive OFF · human/value gates OPEN.”
  Footer: “Recorded 14 October · image05 / e0254cb3 · revision12 ·
  synthetic baseline: 980 cases / 38 visits / 11 staff bindings.”
* **Layout:** large outcome numbers, not a screenshot of a log or raw model
  answer. Two visually explicit columns “Observed” and “Still to prove”.
  Use full provenance in notes, not microscopic on-slide digest strings.
  Preserve AI task-fit/Decision 1 discussion in notes and appendix 19.
* **Notes / evidence demo, total 110s:**
  * 0–15: “The hook is evidence assembly without changing the controlled
    case. This is recorded operator-service proof, not a live staff demo.”
  * 15–40: point to the five-path receipt and registered names in S10/S11:
    stock, assessment, funding, coordination and quality; all returned
    distinct citation-validated ready proposals from Azure OpenAI standard /
    gpt-4.1-mini-2025-04-14. Show only aggregate/public repository evidence.
  * 40–70: show the receipt's independent SQL/content/restart result.
    “Generation left the controlled domain unchanged; persisted proposal
    contents and usage survived the actual revision restart. The old
    recommendations and audit were deliberately reset before this new
    baseline; this was not an unchanged-history migration.”
  * 70–95: “Ready means a valid, unreviewed proposal. It does not mean
    correct, source-verified by a human, accepted or useful. This bypassed
    neither the staff-session gate nor professional decisions: it was
    operator service execution, not staff browser/API acceptance.”
  * 95–110: “Five calls prove integration, not savings or autonomy. QA ended;
    normal authority is absent and scans are off. Next are human acceptance
    and a fair value test.”
* **Recovery:** if the local evidence view fails, pivot within 15s:
  “The evidence view is unavailable; this native summary reports the
  recorded receipt, not a live run. The result is five proposal paths and
  durable contents. Staff, semantic and value acceptance remain open.”
  Stay inside 110s by shortening the middle walkthrough. Do not retry
  inference, sign in, enable scans, reset data, manufacture source-review
  clicks or display private native receipt/output files.
* **Transition:** “Now place those bounded capabilities in the whole process.”
* **Sources / time:** S08–S11, full claim oracle above / **110s including
  demo/recovery**, not an observed rehearsal.

### Slide 13 — Five assists. One controlled journey.

* **Message:** capabilities prepare evidence; workflow and people retain progression and decisions.
* **On-slide:** use the native map specification below. Title plus
  “Workflow controls progression. People retain decisions.”
  Mandatory prominent label: “Design + implemented contracts; proactive OFF.”
* **Layout:** full-width native editable five-column stage/owner/capability/
  request/proactive/core map. No embedded SVG/PNG/PDF diagram. All peer titles
  and corresponding bodies share explicit tops and reserved heights.
* **Notes:** “Each column serves a process stage, not an autonomous manager.
  A person may request help under effective authority. A future authorized
  event or scheduled check could create an owned review item after rules
  determine eligibility; scans are currently off. Data owners/Assets,
  competent technical roles, Finance, the resident/Programme/contract
  authority and independent QA retain their respective decisions.
  Funding spans planning through claims and cash. Hazards go directly to
  the human service; neither an empty model result nor a queue delays intake.
  Failure, stale evidence and expired authority preserve controlled state and
  an owned manual path. Fewer gaps and less rework are value hypotheses.”
* **Transition:** “The financial boundary is as important as the technical one.”
* **Sources / time:** S02 Agentic Architecture Brief, S07 five contracts,
  S11 actual registry, S15 SVG semantics, S09 off-state / **60s**.

### Slide 14 — See cash before optimism.

* **Message:** an award or claim is not cash, and fictional economics are not a budget.
* **On-slide:** “£20,000 gross base cash before grant receipt.”
  “£7,500 fictional grant → £12,500 provider base if received.”
  “If contingency spent: £22,000 gross / £14,500 provider exposure.”
  “Application ≠ award ≠ claim ≠ cash.”
  Persistent label: “Fictional EXA-010/015 — not a workbench price or award.”
* **Layout:** one waterfall-like native bridge without misleading subtracting
  grant before receipt; gross bar remains visibly labelled. Secondary
  contingency line, not another competing claim.
* **Notes:** “These are the selected home-cost fixtures, not a company budget,
  grant allocation, liquidity position or approved scheme calculation.
  Before receipt the gross base cash exposure remains twenty thousand.
  Whole-life technology, integration, training, review, assurance, financing,
  support and exit cost need their own appraisal. Five calls and token limits
  do not establish a currency cap or cost per accepted home. The historical
  exercise budget and scoped #58 override are not today's appropriation.”
* **Transition:** “Affordability also depends on making transition usable.”
* **Sources / time:** S06 EXA-010/012/015 and attribution; S03 not-for-profit;
  S09 finite authority / **50s**.

### Slide 15 — Make the first change small enough to learn.

* **Message:** supported staged adoption must avoid permanent dual entry.
* **On-slide:** “Co-design tasks → shadow one-way import → supported task
  walkthroughs → controlled switch and rollback.”
  “Named owners. No permanent dual entry. No compulsory portal.”
  Footer: “Proposed transition; direct human validation outstanding.”
* **Layout:** four aligned native cards; role name in fixed owner band and
  action below. Use “proposed” by roles, not unverified delegation.
* **Notes:** “Programme and workbook owners establish tasks and baseline.
  Data owners reconcile and own quarantine. Team leads support role tasks;
  these walkthroughs are proposed, not a rehearsal already completed.
  Digital and work owners agree exit tests and rollback before changing the
  write path. Excel can then report from the controlled API. Count training,
  recording and transition burden, and test accessible/non-digital routes
  with people rather than declaring a scan score to be acceptance.”
* **Transition:** “The benefit test must distinguish a better process from better AI.”
* **Sources / time:** S12 transition, S06 EXA-004/011, S07 simplicity,
  S10 RV-001 / **35s**.

### Slide 16 — Prove the programme. Test the AI separately.

* **Message:** a fair counterfactual, not a dashboard, establishes incremental value.
* **On-slide:** “Programme: matched existing teams; frozen cohort; same events;
  accepted handovers and whole-chain cost.”
  “Task: same inputs; manual/rules versus assistance; quality, net human effort,
  latency and cost.”
  “Include unfinished/withdrawn homes. Safety, choice, quality, equity and
  cash are not trade-offs.”
* **Layout:** two equal comparison panels and a protected-outcomes strip.
  No invented results chart; proposed targets must not look achieved.
* **Notes:** “Compare changes against an instrumented pre-period and concurrent
  matched delivery, logging shared staff/suppliers and displacement. The
  twelve-month reconstruction is context, not the counterfactual by itself.
  At task level pair the same inputs and count gathering, preparation,
  review, correction, re-review and shifted burden. Proposed 20% cycle-time
  and 25% coordination-effort reductions remain hypotheses, not ratified or
  measured benefits. Cycle time is assessment-to-ready-to-install; accepted
  handover is separate. Freeze definitions/thresholds before measurement;
  keep the simpler path if AI fails value or quality tests.”
* **Transition:** “That tells us what the next gate must ask for.”
* **Sources / time:** S05, S02 Pilot Success/Measurement, S07 evaluation and
  parallel-experiment intake, S10 RV-002 / **50s**.

### Slide 17 — Earn the next gate; do not repeat the last proof.

* **Message:** proceed from delivered technical evidence to human and value evidence.
* **On-slide:** four equal gate cards:
  “1 Confirm: current requirements, owners, authority.”
  “2 Accept: real staff/session, source review, roles, accessibility.”
  “3 Compare: semantics, net effort, cost, recovery.”
  “4 Decide: continue, simplify or stop.”
  “Recorded operator proof is an input — not production approval.”
* **Layout:** left-to-right gates, a small “technical receipt available”
  marker beneath, no green completion badges on open gates.
* **Notes:** “Historical v0.12 exercise approval does not approve the v0.14
  candidate. Confirm requirements and actual delegations. RV-001 requires
  representative staff with real sessions, roles, source verification and
  accessible manual/failure paths. RV-002 requires semantic grading and paired
  human-effort/quality/cost evidence. Expand restart proof to the necessary
  recovery/restore evidence where appropriate. Return with explicit passed,
  failed, blocked and not-run results; the owner then decides within a
  separately scoped authority. Do not reopen delivered technical work merely
  to simulate acceptance.”
* **Transition:** “Here is the decision I ask this council to make.”
* **Sources / time:** S07 current handoff, S10 RV-001/RV-002, S09–S11 /
  **45s**.

### Slide 18 — Endorse the next evidence proposal.

* **Message:** make a clear planning-only choice with named responsibilities.
* **On-slide:** “CEO / Assets: sponsor + accountable owners.”
  “CIO / Programme: human, permission and recovery evidence.”
  “CFO: whole-life affordability + scoped authority review.”
  “Agree the return date and stop tests.”
  Footer: “No new procurement, spending, rollout or production authority.”
* **Layout:** three equal executive panels; one clear decision ribbon.
  Finish on the resident promise, not an architecture diagram or score.
* **Notes:** “The recommendation is yes to preparing the next bounded
  acceptance-and-value proposal, not yes to autonomous rollout. Confirm
  owners and delegations, require fair alternatives and whole-life costs,
  and agree a return date rather than inventing one. If a critical control
  fails or authority is absent, stop that activity. If AI adds no net value,
  simplify it. We have real service evidence; now let assistance earn its
  place in safe, resident-accepted handovers.”
* **Transition:** “Which gate would you most need resolved before supporting
  the next proposal?” Then listen; use optional appendices only as needed.
* **Sources / time:** S02 recommendation, S03 role map/unknowns, S07,
  S10 / **35s**.

### Slide 19 — Technical challenge: bounded does not mean fully assured.

* **Message:** disclose runtime limits and the evidence required for stronger claims.
* **On-slide:** three aligned panels:
  “State: versions, fenced attempts, reservations; content restart observed.”
  “Trust: permitted sources, current role checks, independent review;
  real-session assurance open.”
  “Operate: owned manual path; performance, restore, quality and unit cost open.”
* **Layout:** readable three-column native cards, not a cloud service inventory.
* **Notes:** “Threats include source injection, cross-role leakage, stale
  approvals and duplicate or lost transitions. Application controls—not a
  prompt alone—constrain proposals. SQL controls claim/lease fences and finite
  shared liabilities; timeouts do not mean zero usage and billing is not
  exactly once. Local SQL/browser tests and deployed content-restart receipts
  are different evidence. No measured Azure scale load, full restore,
  production SLO or externally anchored whole-system audit is established.
  Present runtime still shares in-memory domain mechanisms described in
  the MVP limits; proposed queue workers/private topology remain distinct.
  Decision 1 is a separate candidate-selection/screening design with historical
  narrow evidence; it did not power the five new GPT proposal calls.
  Held-out calibration, alternatives on quality/latency/cost and independent
  human source labels remain required. Structured trigger predicates do not
  establish autonomous reasoning; A7 is not claimed complete.”
* **Sources / optional response:** S07 threats/evaluation/orchestration,
  S08 runtime, S11 limits, S12 full-topology distinction, S13 / **60–90s**.

### Slide 20 — Council challenge: the objections we welcome.

* **Message:** defend the recommendation without hiding reversal conditions.
* **On-slide:** “Why not improve Excel? Test equal scope and controls.”
  “Why not launch now? Human, semantic and value gates are open.”
  “What budget? No new commitment; scoped whole-life appraisal.”
  “What if AI fails? Manual workflow remains; simplify the task.”
* **Layout:** four top-aligned Q&A blocks with short answer lead-ins; full
  response/reversal conditions in notes rather than tiny on-slide text.
* **Notes:** “Restate the challenge before answering. Excel improvement is a
  fair comparator, not a straw man. Power Apps/Dataverse would be greenfield;
  company tenant/licensing/support fit is unverified. Azure is the exercise
  choice, not proof of the best customer investment. Five proposals prove
  integration, not five approved agents running a service. No new budget is
  approved here; cost includes review and operational burden. Choose the
  simpler path when assistance adds no net value. Unknown answers get an owner
  and evidence route, not a confident guess.”
* **Sources / optional response:** S02 options/economics, S03 gaps, S05,
  S07, S09–S12 / **30–60s per actual question**, not four rehearsed speeches.

### Slide 21 — Read the evidence label before the claim.

* **Message:** separate strong technical evidence from the open pitch and adoption gates.
* **On-slide:** “Request ≠ result. Research instruments ≠ residents.”
  “Exercise fixtures ≠ company performance or budgets.”
  “Observed operator proof ≠ human, semantic or value acceptance.”
  Footer: “As at 14 October · legal currentness not refreshed · live pitch,
  rehearsal and thought-leadership evidence still required.”
* **Layout:** three evidence-category cards plus a simple acceptance-boundary
  footer. No pass/fail score visual that implies panel grading.
* **Notes:** “Full source, section, date and status references accompany each
  slide. PRD v0.14 awaits fresh review and amended owner acceptance. Current
  source cabe05c is not the runtime source. The complete rubric informs this
  handover, but slides and plan arithmetic do not prove live presence,
  listening, under-two-minute delivery, Q&A, autonomous reasoning, business
  outcomes or Section D dissemination. No pitch or thought-leadership folder
  was present in the inspected capstone tree. A single separate thought
  leadership submission and masterclass attendance evidence remain owner
  responsibilities; existing deck notes are not submission/dissemination proof.”
* **Sources / optional response:** S01–S15 as applicable; S14 all guide
  criteria/floors / **45s**.

### Slide 22 — Compare equivalent routes before selecting a winner.

* **Message:** production platform choice must earn customer value, not follow the capstone preference.
* **On-slide:** three option columns:
  “Improve current workflow / Greenfield business platform / Azure-led hybrid”.
  Four comparison rows: “Mandatory controls / Transition + access /
  Support + recovery / Whole-life cost”.
  Common result: “Equivalent-scope evidence still needed — no winner scored.”
* **Layout:** native table, 18pt target, concise cells “To verify / To price /
  To test”, not the original cramped seven-row paragraph table. Preserve the
  full seven original dimensions in notes.
* **Notes:** “Compare workflow/evidence, permissions, migration, integration,
  resident access, whole-life cost and readiness on the same journey and
  controls. Include safety hold, withdrawal, missing evidence and failed
  integration. Confirm tenant, workbook quality, skills, licences and
  support; no Dataverse or Dynamics estate is available for assumed reuse.
  The Azure-led hybrid is the provisional exercise direction. Historical
  architect-proposed weights/scores are not customer-approved comparative
  evidence. A safety/privacy/consent/approval failure is a gate, not a score
  that another attractive feature can offset. Select the supportable option
  that meets controls at justified whole-life cost, even if simpler.”
* **Sources / optional response:** S02 implementation options, S07 options
  gate, S12 transition/appraisal, S03 unknowns / **60s**.

### Retained-content and note-association inventory

The 22-slide handover retains each original slide's substantive topic at the
same physical index: request/mission (1), five asks (2), research reversal
(3), prerequisite examples (4), shared foundation (5), work contract (6),
connected journey (7), dignity/capacity (8), decision trace (9), system context
(10), control flow (11), task fit and technical proof (12), map (13), fictional
cash (14), supported change (15), two comparisons (16), gates (17), decision
(18), technical limits (19), council challenge (20), provenance (21), options
(22). This is not content-preservation by byte equality: copy is intentionally
modernised and old observations are explicitly relabelled.

Preserve the old slide 12 supplied-candidate/Decision 1 versus generation
distinction in slide 19 notes; current GPT service proof must not replace it
with a false model-equivalence claim. Preserve the original slide 22 seven
comparison dimensions in its notes. No historical acceptance, source caveat,
resident/manual route, safety boundary or funding state is removed merely to
make room. The actual relationship-linked source notes, not ordinal filenames,
are the preservation baseline. Each of these 22 topic labels plus the notes'
source IDs is a semantic regression sentinel for PC-003.

## Native Map Implementation Specification — Slide 13

**Required result:** a full-width, readable, editable PowerPoint process map.
Existing SVG/PNG remain references only. No diagram image, cropped fragments,
single flattened vector, giant paragraph or hidden text layer substitutes for
native elements.

Use the canonical widescreen aspect ratio; inspect actual cx/cy rather than
trusting the existing misleading `type="screen4x3"` attribute. It is about
13.333 × 7.5 inches. Values below describe a 13.333 × 7.5 canvas; scale x
coordinates proportionally if preserving the exact existing EMUs. Do not
change the whole deck's aspect ratio accidentally.

* Content x = 0.45–12.883. Five columns of width approximately 2.375 with
  0.14 gutters; x positions approximately 0.450, 2.965, 5.479, 7.994, 10.508.
* Title y=0.40, height=0.48, ≥28pt. Short status/subtitle y=0.99,
  height=0.30. Keep logo/footer clear.
* Stage boxes y=1.42, height=0.45, 17–18pt. Short native arrow connectors
  occupy gutters, do not run through owners or imply autonomous release.
* Owner text y=1.98, height=0.72, 16pt, max three compact lines.
* Capability card background y=2.80, height=3.04. Every capability title
  textbox y=2.90, height=0.78, 17pt bold, same insets; reserve this full
  region for all five whether title wraps to one, two or three lines.
* On-request label y=3.77, height=0.27, 16pt; body y=4.10,
  height=0.65, 16pt. Proactive label y=4.83, height=0.27, 16pt;
  body y=5.16, height=0.60, 16pt. Shorten to the copy below if wrapping
  fails; do not shrink, clip or vertically centre. Label itself can say
  “Review trigger • OFF” if needed to fit the column.
* Full-width core band y=6.00, height=0.44, 16pt:
  “Workflow core: rights • versions • gates • human approvals • audit •
  retries • manual recovery”. This is deterministic infrastructure, not a
  sixth supervisor agent.
* Boundary lines y=6.53, height≈0.52, 16pt over two short full-width lines:
  “Checks OFF now; future eligibility → named human queue. Funding:
  application ≠ award ≠ claim ≠ cash.”
  “Hazard → human service now, never wait for AI. Value remains a hypothesis.”
  Source/footer below without collision.

| Peer element | Choose homes | Assess & design | Prepare funding | Coordinate works | Verify & hand over |
| --- | --- | --- | --- | --- | --- |
| Capability title | Stock Prioritisation | Assessment Preparation | Grant & Funding Evidence | Works & Resident Coordination | Quality Evidence Review |
| Human owner | Assets: policy; data owners: verify | Assessor + coordinator: independent sign-off | Finance: validate, approve, submit | Resident: choice; Programme: release | Independent quality authority: accept |
| On request body | Explain facts; query conflicts | Prepare sourced survey/design pack | Draft source-linked evidence pack | Draft update; suggest crew slots | Assemble evidence; raise gaps |
| Proactive body, OFF now | Missing/conflicting stock facts | Missing/changed survey or design | Missing inputs or changed terms | Unaccepted handoff; overdue update | Missing/conflicting quality evidence |

The on-slide short labels retain all five capabilities; notes list canonical
IDs from S11 and detail source categories/permissions, registered purposes
and synthetic predicates. The diagram expresses the process/design contract;
it does not claim actual broader document analysis or professional assessment
delivery. In particular current sources include permitted metadata/hashes,
not arbitrary document/photo content. Scheduled/event initiation is proposed
or implemented-but-disabled contract behaviour, not observed paid scanning.
Funding's lane spans planning through later claims/cash and is not a gate
that automatically approves work. Programme release also requires current
technical evidence, resident measure choice, funding/budget and committed
competent capacity; contract authority alone instructs suppliers.

**Builder-generated checks (retain locked ownership):**

1. Name stage, owner, capability-title, request-label/body and proactive-label/
   body shapes by peer index and semantic purpose. Native filled backgrounds
   must be separately editable. Connectors are native, with correct arrow
   direction and clear endpoints.
2. For each peer row assert identical y, height, font setting and insets in
   the generator. Every relevant text frame has explicit TOP anchor.
   Do not use a centred text frame with a top-aligned paragraph as a substitute.
   Report actual EMUs and any deliberate ≤1pt rounding tolerance.
3. No automatic text shrinking, hidden overflow or cropped paragraph.
   Measure one-, two- and three-line headings against the reserved title
   region; body frames must start at equal y regardless of heading length.
   Apply the same pattern to peer cards elsewhere in the deck.
4. Native map has zero process-diagram picture shapes; any retained branding
   picture must be explicitly identified as branding, not excluded silently.
   Extract five capability names, five stages, owners, on-request help,
   OFF-labelled triggers, deterministic core and hazard/funding boundaries.
5. Check map body ≥16pt, main body target18pt, main titles ≥28pt, intentional
   reading order and adequate contrast. Native text is not itself accessibility
   conformance; retain a full text-equivalent description in actual slide notes.
6. Export the complete fresh 22-slide deck and individually inspect slide 13
   at presentation size. Alignment/contrast/wrapping/overlap are rendered
   properties as well as XML properties. The coordinates above are a starting
   implementation spec, not proof that the built output fits.

## Full Capstone Guide Assessment — Evidence, Not Scores

Use docs/reference/method/ama-capstone-assessment-guide.md in its entirety.
All 20 criteria are five points each; A and B each carry seven criteria/35
points, C and D each three/15. The table is a coverage/gap analysis, **not**
an official or predicted score. A–C are live panel judgements; D is assessed
before panel day by two assigned reviewers. A plan and a passing render do
not establish any section floor.

| Criterion | Repository evidence and handover contribution | Missing evidence / honest assessment boundary |
| --- | --- | --- |
| A1 Architecture, modularity & scalability | S07 component contracts, S08 runtime, S12 target architecture; slides 10/11/19 distinguish state/proposal/failure domains | Production scale path, measured Azure load and full isolation remain unproved. Diagram completeness is not deployed scalability |
| A2 Trade-offs & patterns | S02/S12 equivalent options, staged transition, deterministic versus proposal allocation; slides 3/4/19/22 | No customer-approved comparable whole-life cost/fit appraisal. Presenter must defend rejection/reversal reasoning live |
| A3 Security, compliance & responsible AI | S07 illustrative threats and source/role controls; S08/S11 proposal/review boundaries; slides 8/9/11/19 | Real staff roles/leakage, human source verification, legal/DPO/control-owner approvals and full assurance are open. No compliance certification |
| A4 Implementation completeness | S09/S10 five real operator paths and durable SQL results, S11 runnable implementation; slide 12 | Full connected workflow, actual staff browser/API and human acceptance not established; CON-009/AC-057 not passed. Proactively disclose scope |
| A5 Operations: observability, reliability, performance & cost | S09 usage/restart evidence, S08 finite reservations, S07 SLO method/targets; slide 19 | No complete deployed SLO/load/restore series, unit-of-business-value cost or comprehensive latency evidence. Tokens are measured; currency cost/value is not |
| A6 AI design & evaluation | S07 defined evaluation protocol, source validation, failure catalogue; S11 task contracts; five real model calls | Model alternatives are not compared on held-out cost/latency/quality; no calibrated semantics or paired human effort results. Provenance is not entailment |
| A7 Agentic autonomy & orchestration | S07 bounded graph, S08 registered task/lease pattern, S11 static routing and deterministic predicates; slides 11/13/19 | Service invocation/trigger scripts do not demonstrate the guide's autonomous reasoning/handoff/reflection bar. Scans off. Do not claim excellent autonomy or weaken controls to chase it |
| B1 Narrative structure & argument | Existing deck and this 22-slide problem→evidence→recommendation argument; slides 1–18 | Live coherence not observed. Final rendered deck and delivery may differ from this plan |
| B2 Audience calibration & register | Owner memory, audience map, executive-to-technical transitions and optional appendices | No observed pitch to this council. Communication preferences are hypotheses, not fixed types or interviews |
| B3 Demo & executive hook | Slide 12 recorded outcome receipt, ≤110s plan and ≤15s recovery; slide 7 illustrative connected journey | No timed demo/recovery execution or audience comprehension evidence. Recorded evidence is not live staff functionality |
| B4 Q&A composure & depth | Slides 19/20/22 plus concise challenge responses below | No live challenge responses beyond prepared material. Scripted answers do not demonstrate composure or depth |
| B5 Pace, presence & time discipline | 795s main plus 105s question/contingency plan; moment-specific coaching below | No timed human rehearsal, actual pacing, presence or room recovery. Planning arithmetic is not rehearsal |
| B6 Written communication | Canonical deck with notes, docs/capstone/README.md and linked PRD/ADR/MVP; all-slide concise copy and notes association tests | Rebuilt source/export/notes, navigation and human/font inspection still to be validated; this critique is not generated asset acceptance |
| B7 Evidence & data storytelling | Exact bounded receipt, fictional cash bridge, evidence oracle and controls on denominator/status | No measured company baseline, attributable outcome or accepted-home unit cost. Do not make an unmeasured value chart or misleading certainty claim |
| C1 Discovery & business framing | Original case; owner not-for-profit context; role hypotheses, company gaps, hypothetical value and counterfactual design | Direct staff/resident discovery, company cost of inaction, quantified attributable value/constraints absent. Role instruments are not real engagement |
| C2 Listening & disagreement | Restate–clarify–answer–check pattern and question prompts below | No recorded live exchange or restated real challenge. Cannot claim active listening from a script |
| C3 Influence & intellectual honesty | Clear planning-only recommendation, unprompted off-state/open-gate disclosure and reversal conditions | Actual influence/handling “I don't know” under challenge requires live evidence; no stakeholder commitment or approval invented |
| D1 Substance & originality | Reusable contracts/learning exist in project sources and could support one authored synthesis | No Section D artifact or real engagement evidence supplied in inspected tree; deck/repository content is not automatically the submitted artifact |
| D2 Craft & publish-readiness | Sources and storage guidance exist; deck notes may support a future paired submission | No named complete separate artifact reviewed by the two assigned reviewers. Deck alone is insufficient; artifact deadline/submission not evidenced |
| D3 Dissemination & reach | Storage map defines publication/submission evidence | No real beyond-cohort publication, filing or delivery link/date/acceptance. A PR, AI-generated plan or internal deck rebuild does not prove reach |

### Floors and submission conditions — no compensating averages

| Official condition | Required evidence / present disposition |
| --- | --- |
| A ≥21/35 | Technical evidence exists, but seven live scores are unavailable; no A-floor conclusion |
| B ≥21/35 | Deck/narrative support exists; live delivery/demo/Q&A/rehearsal unavailable; no B-floor conclusion |
| C ≥9/15 | Business framing is documented; live consultative behaviour unavailable; no C-floor conclusion |
| D ≥9/15 | No submitted separate artifact/reviewer evidence in scope; D floor not evidenced and missing artifact risks Incomplete |
| No individual criterion may score 1 | No panel scores exist here; cannot certify any individual floor. In particular absence of pitch/D evidence must stay visible |
| Thought leadership artifact submitted | Submission is a graduation requirement, not a low-score substitute. No submission evidence inspected |
| Required number of masterclasses attended | Guide names attendance as a floor but does not give a count here; owner/programme evidence needed. Do not invent a count or infer attendance from repository work |

Section D requires exactly one suitable artifact submitted no later than two
weeks before the panel, assessed by two non-panel reviewers whose scores are
averaged; the panel receives it five business days beforehand. Formats are
white paper/guidance (~2,000+ words), blog (~800+ words, published/formally
submitted), reference implementation with purpose/architecture/setup/limits
README, submitted IP disclosure, or delivered community/conference session
with materials and notes/recording. A slide deck must be paired with notes,
a recording or delivered session; notes do not by themselves prove submission,
original engagement or dissemination. AI assistance is permitted, while the
candidate must own and defend the insight, evidence and recommendation.

The official guide's floors precede the outcome bands: Distinction 90–100,
Merit 78–89, Pass 66–77, Not Yet Met below66, **only after all floors clear**.
No such outcome is inferred here. The repository gate's missing-asset zeros
and committed-artifact parsing rules in docs/capstone/README.md are an
automation policy, not invented live panel scores. B6 capstone documentation
and Section D are separate deliverables.

Overlapping evidence must also stay separate: an incidental demo transport
failure concerns B3 recovery, not automatically A4 completeness; a real
implementation gap may affect A4. Q&A answer depth is B4, listening and
handling disagreement C2. Neither score can be assumed from the other.
Architecture, deck and actual pitch each need the complete-guide challenge;
this critique assesses architecture evidence and planned communication, not
a pitch that has not happened.

## Delivery Guidance for Moments That Matter

Use the seven observables purposefully, not as personality theatre.

| Moment | Posture / gestures / movement | Language / voice / facial expression / dress |
| --- | --- | --- |
| Opening, slides 1–2; Control + Connect | Upright and still for the decision; one open-hand gesture toward the resident outcome, no pacing | “The outcome is…” then the planning-only ask. Low, clear pace and pause after the boundary. Warm, serious expression. Council-appropriate professional dress, not theatrical “tech disruptor” styling |
| Journey, slides 7–8; Connect + Create | Open stance, trace the home once; turn back toward audience rather than talk to the screen | “Imagine this home” with explicit illustrative label; accessible ordinary words, slightly more vocal range. Concern is legitimate, not resistance. Warmth without invented resident emotion |
| Proof, slides 11–13; Compute + Control | Deliberate movement only to point to Observed versus Open; measured small gestures | “The evidence shows…” and “It does not show…”. Slow down at “operator, not staff acceptance”. Neutral, candid expression; avoid triumphal excitement over five calls |
| Cash, slide 14; Compute | Stand still; one contrast gesture for before versus after receipt | Distinguish pounds from tokens, base from contingency, fixture from budget. Pause at “not cash yet”. Do not smile through affordability concerns |
| Challenge/recovery; Compute + Connect | Stop clicking, face questioner, hands relaxed, no defensive lean or frantic movement | Restate the question, answer the known part, identify unknown/owner/next evidence and check the answer addressed it. Use the short recovery statement without blaming the room or calling playback live |
| Decision, slide 18; Control + Connect | Return to still, open posture; intentional pause invites a response | Repeat action, owner and date-to-agree; calm rising energy, not pressure. Maintain the same professional register/dress as opening; no artificial urgency or implied endorsement |

### Concise challenge responses and reversal conditions

* **“Are the five agents running?”** “Five registered operator proposal paths
  returned real model outputs and persisted them. Ordinary authority is
  absent and proactive scans are off. Staff and value acceptance are next.”
* **“Is this a real demo or a simulation?”** “The receipt is a real recorded
  operator/model/SQL/restart result on synthetic data. The one-home delivery
  story is illustrative. Neither is a live staff acceptance session.”
* **“Why not just fix Excel?”** “We should test that at equivalent scope.
  Source authority, permissions, evidence and handoff controls must work.
  Choose the simpler supported route if it meets them at lower whole-life cost.”
* **“You have not proved savings.”** “Correct. Five calls do not prove savings.
  Pair the same tasks and count all human review, correction and operating
  costs before claiming incremental value.”
* **“What happens when the model misses a hazard?”** “Model output cannot
  suppress independent human hazard intake, set its clocks or clear a hold.
  No negative flag is reassurance. That route must work without AI.”
* **“Why Azure?”** “It is the approved exercise direction with actual runtime
  evidence, not proof of best customer procurement. Comparable customer
  control fit and whole-life cost remain open.”
* **“Have residents approved this?”** “No resident evidence or approval has
  been supplied. Direct, accessible co-design and task testing are required;
  role-agent perspectives do not replace them.”
* **“What does ready mean?”** “A typed, citation-valid, unreviewed proposal.
  A person must verify its sources before acceptance; even that does not
  approve works, consent, quality, claims or payment.”
* **“Can you guarantee the bill?”** “No. Finite calls/tokens bound usage
  exposure but are not a currency guarantee. New scope needs effective
  pricing, liability and authority review.”
* **“Did you preserve all old data?”** “No. The owner authorized the synthetic
  database reset; previous exercise recommendations/audit were reset.
  Against the new baseline, independent controlled-domain and full assistant
  contents survived generation/restart as recorded.”

For unexpected challenges: “Let me check I have your concern right…”.
Then distinguish known evidence from assumption. “I do not know; the owner
and evidence needed are…” is preferable to invented precision. Confirm
whether the question was answered before offering an appendix.

## Evidence Gaps, Risks and Near-Term Decision

No input gap blocks this presentation work. There is no new owner question.
Audience knowledge and panel date are unknown; this handover therefore gives
a clear mixed-room route and leaves real timing/submission dates to the owner.

Immediate next decision: parent adopts the compatible claim/demo/notes
dispositions and dispatches the already requested powerpoint-builder to
P01-T02. The builder receives this entire 22-slide handover, not only slide 13.
The parent then owns final claims/assets/publication and one implementation
Review; do not reconvene this critique.

Near-term evidence work remains separately owned:

* Owner/representative staff: real-session, source-verification, role/manual/
  failure/accessibility work under RV-001, with genuinely effective scope.
* Programme/Data/QA/Finance: semantic grading and paired net-effort/quality/
  latency/cost work under RV-002; preserve adverse or inconclusive results.
* Presenter/owner: actual timed pitch/demo/recovery and unscripted Q&A
  observation, not AI-simulated rehearsal.
* Candidate/programme: one real thought-leadership submission, reviewer and
  dissemination evidence, panel scheduling and masterclass attendance.
* Legal/DPO/control owners: verify current applicability and governance before
  consequential legal/data/operating adoption. No fresh legal assurance here.

## Recommended Next Action

* Highest-impact finding: **PC-001**.
* Action owner: planning parent, then builder within generated-output ownership.
* Smallest next action: add the exact claim oracle, non-live demo contract and
  relationship-aware 22-row notes regression to the accepted dispositions,
  then proceed directly to P01-T02.
* User response required: **No**. No significant/divergent choice is unresolved.
* Completion claim allowed after implementation: validated rebuilt deck and
  published byte equality, within the recorded checks. Not “panel ready”,
  “rehearsed”, “human accepted”, “benefits proven” or “production approved”.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-14/capstone-native-rebuild-plan.md](.copilot-tracking/plans/2026-10-14/capstone-native-rebuild-plan.md) | Candidate plan; parent applies direct dispositions |
| [.copilot-tracking/details/2026-10-14/capstone-native-rebuild-phase-details.md](.copilot-tracking/details/2026-10-14/capstone-native-rebuild-phase-details.md) | Phase/task contracts and locked validation ownership |
| [.copilot-tracking/research/2026-10-14/capstone-native-rebuild-research.md](.copilot-tracking/research/2026-10-14/capstone-native-rebuild-research.md) | Reused evidence and implementation constraints |
| [.copilot-tracking/reviews/plans/2026-10-14/capstone-native-rebuild-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-14/capstone-native-rebuild-plan-critique.md) | Single critique and all-slide communications/native-map handover |
| [docs/capstone/deck/zava-forward-executive-draft.pptx](docs/capstone/deck/zava-forward-executive-draft.pptx) | Sole canonical executive deck, 22-slide source |
| [docs/capstone/deck/agents-in-retrofit-process.svg](docs/capstone/deck/agents-in-retrofit-process.svg) | Existing reference semantics; not the rebuilt slide medium |
| [.copilot-tracking/reviews/logs/2026-10-14/five-assistant-live-delivery-review.md](.copilot-tracking/reviews/logs/2026-10-14/five-assistant-live-delivery-review.md) | Bounded actual operator proof and RV-001/RV-002 |
| [docs/reference/method/ama-capstone-assessment-guide.md](docs/reference/method/ama-capstone-assessment-guide.md) | Complete criterion, floor and submission boundary |

## Next Steps

Active planning parent: incorporate PC-001–PC-003 directly, record their
dispositions and pass this complete handover to the requested
powerpoint-builder for P01-T02. Preserve parent final-asset/source/publication
ownership and builder generated-shape/geometry/export ownership. Continue to
P02-T01 and the single post-implementation Review after actual validation.
No repeat critique, live call, new budget or user response is required.
