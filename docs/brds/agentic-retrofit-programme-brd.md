---
title: Agentic Retrofit Programme Business Requirements Document
description: Business requirements for safe, resident-centred and financially controlled retrofit delivery
author: AMA Research Team
ms.date: 2026-10-14
ms.topic: reference
brd_id: "BRD-2026-AMA48-001"
status: "draft"
version: "0.17.0"
owners: ["AMA Research Team"]
reviewers: ["Executive Director of Assets (proposed sponsor)", "Named Zava North Homes control owners (to be confirmed)"]
created_date: "2026-09-11"
last_updated: "2026-10-14"
business_goal_ids: ["BG-001", "BG-002", "BG-003", "BG-004", "BG-005", "BG-006", "BG-007", "BG-008", "BG-009", "BG-010", "BG-011", "BG-012"]
business_goal_smart_status: "fail"
fr_to_ac_coverage_threshold_pct: 80.0
diagram_format: "none"
lineage:
  supersedes: []
  superseded_by: []
requirement_id_prefixes:
  fr: "FR"
  ac: "AC"
  nfr: "NFR"
  con: "CON"
  br: "RULE"
---

## Document Status

Version 0.17.0 is a candidate amendment for fresh business/requirements
review, not a newly accepted BRD. It keeps the v0.16.0 owner direction that
real AI, real SQL and actual Azure deployment apply to each subsequent
accepted application exercise build, and adds four business requirements
(FR-045 to FR-048), three open decisions (OD-41 to OD-43) and refinements to
FR-008, FR-017 and FR-037 from the 2026-10-14 customer journey atlas and the
sensor data-flow design in ADR 0002. FR-048 captures in-use monitoring data
and keeps it an input to human review only. The
atlas is desk research by role-agent instruments, not user validation; see
Customer Journey Evidence. The historical PRD v0.12.0 acceptance does not
approve this amendment or operational use.

| Field | Value |
| --- | --- |
| Initiative | Agentic Retrofit Programme Delivery |
| Organisation | Zava North Homes |
| Programme | Zava Forward |
| Region | North of England |
| Portfolio | 60,000 homes |
| Executive sponsor | Executive Director of Assets, supported by the Chief Executive |
| Status | Draft for business validation |
| Source | [Original Case Study 48](../case_study_48_original.md) and [Case Study 48 Addendum](../case_study_48_addendum.md) |
| Proposal source | [Case Study 48 Addendum](../case_study_48_addendum.md) |
| Recommended decision | Build an end-to-end non-production demonstrator, then authorise controlled operational validation; no portfolio-wide rollout or capital acceleration approval |
| Owner decision | 2026-09-26: frame the programme as agent-led modernisation of the existing retrofit model, with agents taking on coordination, chasing, re-keying, reconciliation and evidence assembly while people keep decisions |

> [!IMPORTANT]
> Quantified benefits, portfolio baselines, approval thresholds and internal
> operating arrangements remain unvalidated unless this BRD identifies them as
> case-study facts. Sector-informed recommendations require confirmation by the
> association and affected residents before approval.

The original case study remains the record of the request. This BRD translates
the addendum into proposed requirements, not evidence of approval or achieved
benefits.

On 26 September 2026 the requirement set was relabelled to the canonical BRD
taxonomy described under Requirement Identifier Scheme: business goals (BG),
functional requirements (FR), acceptance criteria (AC), non-functional
requirements (NFR), imposed constraints (CON) and business rules (RULE). The
earlier identifiers BR-001 to BR-068 and OBJ-01 to OBJ-12 remain valid as
legacy aliases, because other project documents and the change log cite them;
the Legacy Identifier Map resolves each one. The prefix BR is not reused. The
relabelling did not change what any requirement asks for. Four legacy rows
(BR-046, BR-048, BR-062 and BR-066) were split into single-obligation requirements,
and six constraints were extracted from the regulatory and case-study context.

The legacy BR-059 to BR-068 rows came from the 26 September 2026 agent request
challenge and the modelled customer profile. They cover eligibility and
funding route, tenure, hazard awareness, vulnerability data, contractor
instructions and contract data, quality assurance by absence of flags, sensor
validity and separate PAS 2035 sign-offs. The addendum's reference to 42
controls describes the earlier BRD baseline.

The working presentation line is "Ready, steady, retrofit." The identity is not
cleared for legal, trademark, domain or resident-facing use. It must not be used
in hazard, complaint, safeguarding or consent communications.

## Executive Summary

The association needs to increase the pace of domestic energy-efficiency
improvements while protecting resident safety, meeting applicable statutory
response times, preserving resident choice, maintaining retrofit quality and
operating within financial and supplier capacity.

A small team holds retrofit assessment, grant, procurement, resident consent
and quality assurance together through spreadsheet-based coordination. This
does not establish that administration is the binding delivery constraint.
Readiness work must distinguish coordination failures from capital, competent
staff, supplier, property, resident and technical constraints.

The proposed solution is agent-led modernisation of the existing retrofit
model. Existing teams, suppliers, professional roles and systems remain. The
agents take on manual coordination, chasing, re-keying, reconciliation and
evidence assembly through the digital foundation they need: a shared property
record, explicit lifecycle stages, named handoff owners and deterministic
controls for safety, consent and approvals. Bounded AI may recommend, draft,
reconcile and flag, but is not the default solution to every workflow.
Accountable people retain authority for safety, technical approval, resident
consent, investment, procurement, grant submission, payment and quality
acceptance.

The programme will not be approved on delivery volume alone. It must demonstrate
safe property progression, valid and accessible resident decisions, committed
delivery capacity, evidence-based grant reporting, controlled quality and an
affordable portfolio trajectory.

For the capstone presentation, Zava North Homes is treated as the real
customer case and attendees are addressed as its stakeholders in their actual
roles. The records constructed for the exercise do not establish actual
company performance, resident outcomes, systems or operating decisions.

The immediate investment request is a capped readiness stage followed by
an end-to-end non-production demonstrator and separately authorised shadow and
live validation. The underlying retrofit capital case and the incremental
technology case require separate appraisal. A five-agent rollout, GBP 40
million of secured grant and doubled throughput are not approval assumptions.

## Board Decision Narrative

For the AMA learning programme, each accepted application exercise build
means a delivered prototype, PoC or MVP, including updates of Zava Forward.
It must use actual Azure hosting, real SQL state (the existing Azure SQL
realization) and at least one registered real generative or decision-model
task in the exercised path. Continue the generated 60,000-home stock and
retained 980-case programme lineage; test cohorts are not replacement MVPs.
Documentation, unit/CI tests and non-delivery development checks may use
local state/mocks, but cannot satisfy application delivery. This learning
requirement is separate from production options and attributable benefits.

Zava North Homes does not have a spreadsheet problem. It has a delivery
control problem that spreadsheets make harder to see. A small team coordinates
property evidence, professional approvals, resident decisions, supplier
capacity, grant records and quality assurance across fragmented records. The
result is avoidable chasing, repeated data entry, unclear ownership and weak
visibility of the constraint preventing each home from progressing.

The stakes are material. The provisional scenario contains 15,600 homes below
EPC C and implies 3,900 accepted completions a year over four full delivery
years. At the illustrative GBP 20,000 cost per home, that is a GBP 312 million
programme before the association has validated the cohort, delivery capacity,
grant award, match funding or affordability. Moving unreliable information
faster would amplify risk rather than create value.

We recommend that the Board sponsor a complete end-to-end demonstrator of the
target operating model, followed by controlled operational validation. The
demonstrator will connect one property journey from readiness and assessment
through resident engagement, supplier coordination, quality evidence, grant
reconciliation and portfolio reporting. It will use constructed exercise
records or approved de-identified cases in a non-production environment, so
the architecture can be built, tested and demonstrated without exercising
live authority over a resident, contractor, payment, grant claim or safety
decision.

The proposition is not five autonomous agents replacing existing teams. It is
one controlled property lifecycle with bounded agents removing coordination,
chasing, re-keying, reconciliation and evidence-assembly work. Deterministic
controls govern safety holds, consent status, eligibility, approvals, funding
and lifecycle transitions. Agents may reconcile records, draft from approved
evidence, recommend within committed capacity and raise exceptions. Named
people retain every consequential decision.

The first demonstration must prove value to the people doing the work. A user
should be able to see which homes need attention, why each is blocked, who owns
the next action and when the resident should receive an update. The system
should pre-populate sourced facts, assemble draft evidence packs and route
exceptions instead of asking staff to maintain parallel spreadsheets. Success
is less manual effort and fewer avoidable failures per accepted handover, not
the number of agent features shown.

The Board is asked to approve the direction and the conditions for a capped
demonstrator, not the full capital programme or portfolio rollout. Before any
live validation, accountable owners must approve the lawful measurement basis,
data protection assessment, safety and resident guardrails, technical
authority, supplier capacity, funding position, operating cost and stop
criteria. The demonstrator must disclose known gaps and show tested fallback
when an agent, model, integration or data source fails.

The programme will return with evidence in three forms:

* a working architecture that completes representative property journeys
  end to end and exposes its state, decisions, handoffs and failures;
* a task-level comparison showing whether each agent capability improves
  quality, review time and cost over deterministic workflow alone; and
* an operational validation plan showing how attributable value, resident
  experience, safety, quality, affordability and scale readiness will be
  measured against current delivery.

This is more ambitious than a collection of disconnected pilots and safer than
an immediate portfolio rollout. It builds the complete architecture needed to
demonstrate the future service, while preserving a separate evidence gate
before the association exposes residents, staff, suppliers or capital to live
consequences.

## Evidence Classification

The BRD uses four evidence classes:

| Classification | Meaning |
| --- | --- |
| Case-study fact | Stated operating context, not independently verified company evidence |
| Sector-informed recommendation | A proposed requirement derived from the addendum, housing-sector practice or specialist review |
| Planning assumption or value hypothesis | An illustrative cost, target, schedule or benefit requiring validation; a source claim is not an observed outcome |
| Unknown company detail | Information the association must validate before approval |

## Business Context and Background

### Source Context and Original Request

* The association manages 60,000 homes in the North of England.
* It intends to improve every property toward EPC C by 2030 under a proposed
  standard.
* It must respond to emergency hazards and damp and mould within applicable
  Awaab's Law timescales.
* Retrofit assessment, grant applications, contractor procurement, resident
  consent and quality assurance are managed by a small team using spreadsheets.
* Delivery is described as far behind plan.
* The proposed programme includes prioritisation, assessment drafting, grant
  preparation, contractor and resident coordination, and quality verification.
* The Executive Director of Assets approves investment.
* Residents control consent.
* Finance submits grant applications.
* The original request describes a Retrofit Coordinator approving drafted
  PAS 2035 assessments.

Following the addendum, the proposed model instead makes competent assessors,
designers, coordinators and evaluators responsible for their respective
professional outputs. Software may prepare sourced factual inputs and check
completeness; it cannot invent observations or substitute for assessment.
The applicable PAS edition, funding rules and role responsibilities must be
confirmed before the pilot.

### Regulatory Timing

The local legal corpus was retrieved on 19 September 2026. Awaab's Law Phase 1
came into force on 27 October 2025 for emergency hazards and significant damp
and mould hazards. Phase 2 guidance states 30 November 2026, but the
implementing instrument is not in the corpus and must be verified before
activation. Phase 3 scope and commencement remain unconfirmed.

The government response of 1 April 2026 sets a final SRS MEES policy position:
one qualifying metric by 1 April 2030 and a second by 1 April 2039, subject to
transition and exemption arrangements. The corpus does not yet evidence the
direction, revised RSH standard and commencement needed to treat the policy as
an in-force landlord duty. Consultation-stage requirements are historical
where the final response differs.

The addendum and supporting research record WH:SHF Wave 3 grant spend by
31 March 2028 and delivery to September 2028. No allocation to Zava North
Homes is evidenced. Readiness must verify any award and its applicable
conditions rather than assume a currently open application round. Existing
hazard response and eligible grant delivery must not wait for the new platform.

The funding route also varies by place. The WH:SHF technical annex (January
2025, converted 19 September 2026) allocates a share of Wave 3 capital by
formula to the Greater Manchester (5.7%) and West Midlands (7.8%) combined
authorities through integrated settlements
([local snapshot](../reference/regulatory/retrofit-standards-and-funding/warm-homes-social-housing-fund-technical-annex-2025.md),
Page 3 and Page 5, Table 3). Homes there follow a devolved route rather than a
competitive national bid. Of the two, only Greater Manchester is in the North
of England. Whether Zava North Homes owns stock there is an unknown company
detail. The same annex notes that "in scope", meaning EPC D or below, does not
necessarily reflect scheme eligibility (Page 3, footnote 1). FR-026 therefore
treats eligibility and route as versioned rules, not as a ranking input.
Non-social homes may make up to 30% of an application's homes only under
stated conditions. That rule has been verified only in the Greater Manchester
Combined Authority copy of the scheme guidance
([Housing Association Primer](../reference/research/sector/housing-association-primer.md#grant-treatment-of-non-social-homes)).
Check the national DESNZ guidance before relying on it.

Regulatory applicability, commencement dates and current guidance must be
verified against official sources at each approval and implementation stage.
Legal interpretation remains outside the authority of programme automation and
this BRD.

### Sector Context

The supporting research identifies recurring sector pressures:

* Incomplete or conflicting property and compliance records
* Competing safety, repairs, maintenance, development and retrofit investment
* Scarce competent retrofit and supply-chain capacity
* Variable contractor evidence and subcontractor visibility
* Resident trust, accessibility and consent challenges
* Weak cross-team handoffs
* Grant deadlines, match funding and evidence conditions

These are sector-informed hypotheses, not established company facts.

The [Modelled Customer Profile](../reference/research/company/company-profile-research.md#modelled-customer-profile),
added on 25 September 2026, models Zava North Homes as a merged northern
group with majority stock-transfer heritage. Its values are modelled estimates
from sector medians and national rates, not company facts. Three of them
change what the requirements must cover:

* Mixed tenure. About 2,940 shared ownership homes and about 1,750 right to
  buy leaseholders are modelled. For these homes retrofit is usually an
  improvement, and responsibility, consent and cost recovery depend on each
  lease
  ([Housing Association Primer](../reference/research/sector/housing-association-primer.md#retrofit-responsibility-in-shared-ownership-and-leasehold-homes)).
* Recorded versus actual vulnerability. National rates imply about 34,800
  rented households with a long-term illness or disability. The share the
  association records is unknown and probably much lower, so recorded flags
  cannot be treated as complete.
* Below-C range. The modelled range is about 15,000 (25%) to 15,600 (26%)
  homes below EPC C. A separate Karbon-based scenario gives about 13,800. The
  scenarios use different bases and are not merged.

## Customer Journey Evidence

On 2026-10-14 the nine company role instruments published a
[customer journey atlas](../reference/research/ux/customer-journeys/customer-journey-atlas.md)
with 28 stage-based maps, three subjourneys and 24 agent opportunity
hypotheses. It is desk research and divergent ideation, not user observation,
approved requirements or measured company data. This BRD uses it only to find
business-control gaps. Every journey pain, gain and request remains a
sector-informed hypothesis until OD-41 is closed.

| Journey theme | Existing coverage | Disposition in v0.17.0 |
| --- | --- | --- |
| Continuity: tell the story once | FR-017, AC-023 | AC-023 now limits reuse to a stated purpose and recipient; FR-045 adds representative authority |
| Resident-controlled coordination | FR-012, FR-013, FR-014, RULE-006 | FR-046 separates an offer from a confirmed commitment and records household constraints, deferral and pause |
| Evidence that carries context | FR-008, FR-028, RULE-017 | AC-011 now states that reused evidence never transfers an approval |
| Nomination, prioritisation and challenge | FR-037, RULE-005 | AC-065 now requires preserved original account, owned review, correction and re-review of dependent decisions |
| Accountable recovery after closure | FR-015, FR-029, FR-030, CON-004 | FR-047 keeps complaint remedy, defect and household-level lease or charge disputes open after package progress |
| Controlled source-to-rule change | FR-038, FR-039, FR-040, RULE-021 | No change; the journey confirms the existing human-owned activation control |
| Effort shifted to residents, staff or suppliers | RULE-019, Benefits Validation Register | No change; review, correction, resident and supplier effort are already counted |
| Portfolio narrative, analytical supervision and cash rehearsal (opportunities O10, O18 to O20) | Out of scope for this phase | Exploratory later scope; initial programme supervision stays deterministic |

The journey outputs do not widen agent authority. The twenty-four
opportunity hypotheses are candidates for test design in the PRD and ADR, not
approved features. A useful non-AI comparator remains required for each, and
CON-007 still applies to every delivered application build.

## Problem Statement and Business Drivers

### Problem Statement

The association cannot establish a credible path to faster retrofit delivery
while critical decisions, evidence and handoffs are spread across spreadsheets
and teams, and much of the coordination rests on a small team. This creates a
risk that
delivery targets are pursued without reliable property data, explicit safety
holds, accessible resident decisions, committed supplier capacity, controlled
PAS 2035 progression, verified grant value or an affordable investment
trajectory.

The programme must first establish which constraints limit accepted outcomes
and which agent capabilities add value compared with matched existing delivery
without agents. Faster administration alone does not prove that physical
delivery can increase. If Phase 0 shows supplier or competent-assessor
capacity is the binding constraint, agents cannot create that capacity; their
value is in forecasting, scheduling within confirmed capacity and evidence
flow.

### Cross-Functional Challenge to the Five-Agent Request

A structured review challenged the original architecture from asset,
programme, finance and grants, resident engagement, building safety,
procurement and frontline housing perspectives. On 26 September 2026 a second
review added the Data and Performance Lead. The eight role agents tested each
requested agent's "owns end-to-end" line for its real problem, cheaper
alternatives, bounded AI fit, required foundation, value test and stop
criteria. The findings are recorded in the
[Agent Request Challenge](../reference/research/company/agent-request-challenge.md).
These `company-*` role profiles are research instruments grounded in the
case-study evidence and sector research, not the capstone attendees
themselves. Their convergence is a sector-informed hypothesis, not proof of
company stakeholder agreement.

No perspective supported five end-to-end agents as an implementation
commitment. Each request combines three kinds of work: deterministic control
work, accountable human decisions, and a smaller set of tasks where bounded AI
helps. The requested decomposition assigns technology to five visible
activities before the association has established the binding delivery
constraint, authoritative data, controlled lifecycle, professional capacity,
supplier commitments, resident journey or defensible financial baseline. It
also combines responsibilities that require different authorities while
duplicating evidence, reconciliation, exception and reporting capabilities
that should be shared.

The underlying requirement is to establish the digital foundation that agents
need, so existing teams and decision makers can answer:

* Where each home is in the retrofit lifecycle
* How long it has remained at that stage
* What prevents progression
* Who owns and has accepted the next decision
* When the resident will receive the next update
* Whether the binding constraint is data, capital, professional capacity,
  supplier capacity, resident access, technical complexity, quality or
  administration
* Whether completion means activity, installation or a safe,
  resident-accepted and evidence-complete handover

The five proposed agents should therefore be treated as hypotheses:

| Original proposal | Cross-functional challenge | Proposed disposition |
| --- | --- | --- |
| Stock Prioritisation Agent | No verified address-level baseline, data-confidence model or approved cohort policy exists. Once weights are agreed, ranking is arithmetic; eligibility is a rules question. Ranking may conceal missing safety, building, planned-maintenance or resident information, and recorded vulnerability flags are probably incomplete. | Defer live use. Test a transparent, versioned scoring model and deterministic eligibility rules (FR-026) in shadow mode as a digital-foundation module. Limit AI to reconciliation, extraction from free text and plain-language explanation. |
| Assessment Agent | Software cannot perform missing observations. The request merges the Retrofit Assessor's survey ownership and the Retrofit Coordinator's review into one approval. | Replace with bounded assessment preparation: source-backed factual pre-population, evidence assembly and omission checks for separate competent sign-offs. |
| Grant and Funding Agent | The GBP 40 million remains an opportunity rather than an evidenced award. Reporting is a data-lineage problem, and the funding route may be a formula allocation rather than a bid. | Implement the grant ledger, versioned eligibility and route rules, reconciliation and approval controls first. Pilot drafting only for an evidenced award or open route. |
| Contractor and Resident Coordination Agent | Supplier utilisation and resident choice have different interests, authorities, information needs and escalation routes. An agent cannot secure consent, and a drafted contractor message could act as a client instruction or variation. | Split in two. Resident side: deterministic decision record, human-owned service, bounded drafting and routing only. Contractor side: suggestions within committed capacity, with instructions reserved to the contract manager. |
| Quality Verification Agent | Documentary completeness or normal sensor readings cannot establish physical quality, resident satisfaction or safe closure. The main risk is a pack with no flags being read as proof of quality. Contractors must not accept their own evidence. | Rename as evidence assurance and anomaly flagging. Flags can only add work to a human queue. Competent people retain inspection, acceptance, remediation and closure authority. |
| Programme supervisor | An AI orchestrator cannot safely enforce undefined states, gates, authority limits or exception routes. Chaining agents compounds errors and hides accountability. | Implement deterministic workflow, queues, clocks, audit and escalation first. Consider later summarisation and recommendation support only. |
| Damp-and-mould loop | Hazard awareness can arise in any channel, including retrofit surveys and contractor visits, and the statutory clock runs from awareness. Retrofit tooling must not own the statutory response. | Link to the existing repairs and hazard service with an awareness timestamp (FR-003, RULE-003). Permit only a raise-only signal scan feeding human triage. |

The dependency-first proposition is:

1. Verify the current property and resident journey using twelve months of
   property-level cases.
2. Establish common property and building identifiers, authoritative sources
   and data owners.
3. Define lifecycle states, mandatory gates, decision authorities,
   material-change rules and accepted-handover criteria.
4. Implement closed-loop handoffs, common exception controls, queue ageing and
   property-to-portfolio reporting.
5. Validate professional, supplier, resident-service, assurance and financial
   capacity for the pilot.
6. Compare process redesign, existing-platform configuration, deterministic
   workflow and bounded AI in shadow mode.
7. Authorise only capabilities with attributable value and acceptable
   safety, resident, quality, financial and operational performance.

The proposed evidence, team and bounded-assistant design for this work is
defined in the
[Retrofit Flow and Constraint Discovery Brief](./retrofit-flow-discovery-brief.md).

The leading non-agent comparator is a Frontline Property Progress and Handoff
View for one pilot locality. It would show the controlled property timeline,
current stage, age, blocked reason, live appointments, relevant repairs and
complaints, named owner, accepted handoff, next action and promised resident
update. It would also flag unowned, overdue, conflicting and reopened work
without becoming a second system of authority.

If readiness evidence supports bounded AI, the first candidates are:

* An Evidence-to-Claim Assurance Assistant combining assessment preparation,
  quality evidence checks and grant-pack reconciliation
* A Supplier Delivery Assurance Assistant reconciling contracted capacity,
  work-package demand, evidence obligations, subcontractor performance and
  material changes

Neither candidate may exercise safety, professional, resident-consent,
procurement, investment, payment, grant-submission, quality-acceptance or
defect-closure authority.

The 26 September 2026 challenge breaks these candidates into five recurring
bounded capabilities. All five are recommend, draft or raise-only functions,
and none needs end-to-end ownership. Each needs a non-agent comparator and a
stop criterion under RULE-019. The tests below are sector-informed proposals
for Phase 1 shadow mode. Owners must ratify the thresholds before measurement
begins. Every capability test samples unsupported-claim rate, explanation
fidelity and automation-bias indicators. Any unsupported eligibility, consent,
safety or evidence claim accepted by a reviewer undetected, or automation-bias
indicators breaching owner thresholds, pauses that capability under RULE-024.

| Capability | Where it came up | Non-agent comparator | Proposed shadow test | Proposed stop criterion |
| --- | --- | --- | --- | --- |
| Reconcile records and flag missing data | Stock prioritisation, assessment preparation, grant ledger | Rules-based cohort model and data-quality reports | Run a past cohort through the spreadsheet selection, the rules model and the rules model with AI. Measure homes still viable after survey, critical conflicts found, override rate, reproducibility and time to cohort | Any home dropped without human review, any statutory hazard routed through ranking, or no gain over the rules model on missed critical exceptions once review effort is counted |
| Read unstructured evidence against fixed checklists | Assessment pre-fill, quality evidence, grant claim packs | Per-measure evidence checklist at the payment gate | Pre-fill 30 to 50 homes alongside the manual process. Run evidence checks on past homes and seeded defects alongside human reviewers | Any unsourced site observation, any safety-critical defect missed that humans caught, false flags that overwhelm reviewers, or checking that takes as long as doing the work |
| Draft content from controlled records | Resident, contractor, grant and Board content | Templates and staff drafting | Rebuild the last funder return and recent resident and contractor messages with and without AI drafting | Net review time falls by less than 25%, or any unsupported eligibility, evidence or consent statement reaches a reviewer undetected |
| Route inbound messages to staffed queues using fixed categories | Resident channel, contractor messages, damp intake | Scripted triage and a single contact log | Route one patch's messages in parallel with staff. Report results by age, disability, language and channel | Any safeguarding or hazard message misrouted, or gaps between resident groups widen |
| Raise-only signal scanning | Missed hazard reports, missed handoffs, defect patterns | Mandatory hazard question on every form, and sampling rules | Scan past repairs notes, complaints, surveys and contractor notes, and compare hits with human triage | Any output delays, suppresses or closes a clock, or review load exceeds triage capacity |

Typed decision models that return closed-set answers and probabilities, rather
than generated text, are an implementation option under research for the
routing, evidence-reading and signal-scanning capabilities
([IDEA-001](../ideas/typesafe-system-one-agent-fit.md)). This is an
unvalidated proposal, not a requirement.

### Sponsor Discovery Questions

The following questions continue Method 1 scope discovery. Answers must be
supported by company evidence rather than sector assumptions.

| Priority question | Evidence requested | Decision unlocked |
| --- | --- | --- |
| Where was elapsed time lost between candidate identification and accepted handover during the last twelve months? | Property-level stage entry, exit, pause and reopen dates; delay reasons; queue owners; decision times; manual effort | Binding-constraint definition and options appraisal |
| When a resident reports a missed retrofit appointment and worsening mould, where is the account recorded once and who accepts the next decision? | Current contact journey, repair and hazard route, handoff acceptance, next-update ownership and frontline visibility | Frontline view, exception and resident-service design |
| Which PAS 2035 and assurance roles are available, competent and committed by month for the proposed pilot? | Named role model, competence scope, internal and supplier capacity, evidence and approval responsibilities | Technically credible pilot scope |
| What survey, installation and quality capacity is contractually committed rather than forecast? | Contracts, frameworks, work packages, locality and monthly capacity, subcontractors, contingency and performance evidence | Supplier strategy, cohort size and mobilisation decision |
| Has the association received an executed award supporting any part of the GBP 40 million opportunity? | Award, eligible-property schedule, match funding, spend and claim deadlines, payment profile and clawback conditions | Grant workflow, affordability and benefit case |
| Which pilot buildings have unresolved safety, shared-system, planned-maintenance or property-condition dependencies? | Building register, accountable owners, current evidence, open actions and progression-blocking conditions | Safe cohort and sequencing rules |
| Which system, if any, is authoritative for property identity and EPC records, and what share of homes has a physical stock-condition survey from the last five years? | System inventory, UPRN coverage, survey dates and data owners | Data readiness and prioritisation model (RULE-015) |
| When an assessor, installer or liaison officer spots damp, mould or another hazard, how is it reported, and does the system record the awareness date separately from the logging date? | Current reporting routes, case fields, damp and mould volumes, backlog and Phase 1 compliance | Hazard referral design (FR-003, RULE-003, OD-29) |
| Does the housing management system record tenure and lease type for each home, and what share is verified? | Tenure and lease fields, verification status, shared ownership model and right to buy lease dates | Owner decision routes (FR-015, OD-27) |
| Which local authority areas contain the stock, and does any fall within a combined-authority integrated settlement? | Stock by local authority, funding route per scheme and co-funding sources | Funding route and eligibility rules (FR-026, FR-027, OD-26) |
| Which contracts and frameworks would the pilot use, and who is the named contract manager and authority limit for each? | Contract forms, expiry dates, data obligations, leaseholder contributions and delegated authority | Contractor control and award gate (RULE-008, FR-022, OD-30) |
| Can the association supply twelve months of no-access and withdrawal records, with reasons, by channel and adjustment need? | Appointment outcomes, withdrawal reasons, channels and adjustment records | Replacement of no-access and refusal planning assumptions (OD-08) |

### Owner-Provided Direction on Sponsor Discovery Questions (2026-10-03)

The programme owner gave the directions below on 2026-10-03 in response to
the Sponsor Discovery Questions. These are owner statements and planning
directions, not verified company evidence, system records or completed
company research. Several explicitly substitute a modelled or illustrative
estimate for data the owner has not yet supplied; those are labelled
accordingly and do not close the related Open Decision.

| Question | Owner direction, 2026-10-03 | Evidence status |
| --- | --- | --- |
| Elapsed time lost between candidate identification and accepted handover | Owner accepts the cause is "a mix of everything" and is content to proceed without separating causes for now. | Owner-accepted ambiguity; no stage-level records supplied. OD-01 and OD-18 stay open; the binding-constraint analysis still needs real stage data. |
| Missed appointment and worsening mould, account ownership | Owner directs a new escalation control: after more than 5 missed appointments for the same case, escalate for investigation of the root cause and a fix. | Owner design direction, not existing practice evidence. Added to the draft as a proposed RULE-006 control; Housing and repairs leads must ratify it and its handoff targets (OD-09). |
| PAS 2035 and assurance roles for the pilot | Owner asked the company-role agents to decide, intending to request engagement of these roles at an upcoming presentation. The Housing Retrofit Programme Manager role-profile agent proposes six named roles with their PAS 2035 function and the monthly evidence needed to confirm each; see "PAS 2035 role-profile hypothesis" below. | Role-profile hypothesis for the sponsor's presentation request, not confirmed company staffing. OD-06 and OD-33 stay open pending named people, certification and committed capacity. |
| Survey/install/quality capacity: contracted vs forecast | Owner asked for an educated guess; no sector benchmark or company record in the repository supports a defensible locality-level capacity estimate. | Declined: no evidence base exists to model this responsibly. OD-10 and OD-30 stay fully open; contract and framework capacity data is still required. |
| GBP 40 million grant opportunity, award status | Owner states an award has been executed, covering roughly half of the homes that could have received it. | Owner-provided direction; exact award terms, eligible-property schedule, match funding, deadlines and clawback conditions are not yet supplied. OD-11 and OD-26 stay open for the documented award evidence. |
| Pilot building safety/shared-system/condition dependencies | Owner asked for a statistical model; the repository holds no building register or portfolio geography to ground a per-building estimate. | Declined: no evidence base exists to model this responsibly. OD-04 and OD-22 stay fully open; the building register and accountable owners are still required. |
| Authoritative property/EPC system and 5-year stock-condition survey coverage | Owner asked for a statistical estimate. The Provisional Sector Benchmark Pack's "Rolling stock surveys" line (12,000 homes per year for a five-year cycle) is a stronger-practice comparator target, not an observed completion rate; if the association already ran at that cadence, a five-year rolling cycle would in principle cover the full 60,000-home portfolio, but no evidence confirms the association runs at, below or above that rate, and no authoritative system has been named. | Illustrative benchmark-derived reference point only, explicitly not company evidence. OD-03 and OD-26 stay open for the named system and the real survey-coverage figure. |
| Hazard reporting route and awareness-date tracking | Owner describes current practice: a hazard is reported to the team via a written description from the technician, or by phone from the resident; when a resident reports it, a technician then attends to audit the mould's severity. | Owner-provided description of current practice. Confirms a reporting route exists but does not state whether the system records the awareness date separately from the logging date, or the volumes and backlog. OD-29 stays open for that remaining evidence. |
| Tenure/lease type recording and verified share | Owner asked for a statistical model; the repository holds no tenure-mix survey or verification-rate benchmark to ground a defensible estimate (the existing company-profile tenure split is itself labelled an estimate, not a verified share). | Declined: no evidence base exists to model this responsibly. OD-27 stays fully open; the housing-management-system fields and verification status are still required. |
| Local authority areas containing the stock, and combined-authority settlement overlap | Owner asked for a statistical model; the repository holds no stock-by-local-authority breakdown to ground an estimate. | Declined: no evidence base exists to model this responsibly. OD-26 stays fully open; stock geography by local authority is still required. |
| Contracts and frameworks the pilot would use | Owner states the pilot would use all of the association's current contracts and frameworks, not a subset. | Owner-provided direction; named contract managers, authority limits, expiry dates and data obligations per contract are not yet supplied. OD-30 stays open for that detail. |
| No-access and withdrawal history, 12 months | Owner asked for a statistical model. The Provisional Sector Benchmark Pack already carries a first-appointment no-access planning assumption (10% central, 5% to 15% sensitivity) and a resident refusal/withdrawal planning assumption (5% to 10%), both sourced to sector data, not company records. | Illustrative sector-benchmark substitute only, explicitly not company evidence. OD-08 stays open for the association's own 12-month records by reason, channel and adjustment need. |

#### PAS 2035 role-profile hypothesis (role-profile agent output, 2026-10-03)

The Housing Retrofit Programme Manager role-profile agent proposed six roles
for the sponsor's presentation request. This is a role-profile hypothesis for
requesting engagement, not a statement of Zava North Homes' current
staffing; no named individuals, headcounts or capacity figures are asserted.

1. **Retrofit Coordinator** - owns the PAS 2035 pathway, risk-path decision
   and design release; typically an internal or long-term named role,
   distinct from the Assessor. Monthly evidence: named competent person(s),
   certification validity, live concurrent-home caseload against a stated
   per-FTE capacity ceiling.
2. **Retrofit Assessor** - owns the site survey sign-off, separate from
   Coordinator review; commonly contracted or supplier-provided. Monthly
   evidence: certification, surveys signed off, confirmation no person holds
   both roles that month.
3. **Retrofit Adviser/Designer** - produces the property-specific measure
   design requiring competent sign-off; often an external consultant.
   Monthly evidence: design approvals issued, qualification currency,
   caseload.
4. **Retrofit Evaluator** - independent post-installation technical
   verification, independent of the installer; typically contracted. Monthly
   evidence: inspections completed, pass/defect rate, sampling percentage.
5. **Installer-side quality role (PAS 2030-certified installer/site
   supervisor)** - delivers and self-evidences installation only, cannot
   approve compliance; always supplier-provided. Monthly evidence:
   certification scope, committed versus delivered capacity, defect and
   reopen rate.
6. **Named programme assurance (Building Safety Lead liaison and independent
   reviewer)** - holds safety-hold release and escalation authority; should
   sit independently of delivery. Monthly evidence: holds raised and
   released, review turnaround.

Confirmation that all six are available, competent and committed each month
remains the Phase 0 readiness gate (OD-06, OD-33) before pilot mobilisation.

### Business Drivers

* Protect residents from emergency hazards, damp, mould and unintended retrofit
  consequences.
* Meet in-force regulatory duties and prepare for confirmed future requirements.
* Establish an evidence-based portfolio trajectory toward improved energy
  performance.
* Increase delivery capacity without reducing quality or bypassing human
  authority.
* Improve access to eligible grant funding while controlling match funding,
  cash exposure and clawback.
* Preserve resident agency, accessibility, trust and complaint rights.
* Protect asset value, financial capacity and board assurance.

## Business Objectives and Success Metrics

| ID | Legacy ID | Objective | Measure | Baseline | Target and timeframe | Status |
| --- | --- | --- | --- | --- | --- | --- |
| BG-001 | OBJ-01 | Improve portfolio energy performance | Number and percentage of homes below EPC C | Provisional sector benchmark: 15,600 homes, or 26%; modelled range about 15,000 to 15,600 | Board-approved annual reduction through 2030 | Replace with company data |
| BG-002 | OBJ-02 | Increase safe retrofit throughput | Homes reaching accepted handover per year, with reopened defects shown separately | Actual throughput unknown; 3,900 per year is a required-trajectory scenario, not a baseline | Indicative pilot: at least 50 accepted handovers from 80 to 100 candidates; approve portfolio trajectory separately | Pilot and trajectory proposals |
| BG-003 | OBJ-03 | Protect resident health and safety | Controlled progressions with unresolved safety evidence | Unknown | Zero | Proposed |
| BG-004 | OBJ-04 | Meet hazard response obligations | Cases meeting applicable response and resident-update times | Unknown | 100% within applicable requirements | Proposed |
| BG-005 | OBJ-05 | Preserve resident control | Work started without valid agreement or authorised exception | Unknown | Zero | Proposed |
| BG-006 | OBJ-06 | Improve quality | Right-first-time acceptance and material defect rates | No sector average; 90% initial target for scenario testing | Board-approved thresholds before rollout | Planning assumption |
| BG-007 | OBJ-07 | Improve grant conversion | Opportunity, award, claimable and cash values | GBP 40 million opportunity; owner reports an executed award covering roughly half of potentially eligible homes, but award evidence is not supplied | Separate, reconciled reporting for every funding stream | Owner-reported, not documented; no controlled status change |
| BG-008 | OBJ-08 | Maintain affordability | Minimum liquidity and covenant headroom | Sector warning comparators only; provider position unknown | Remain within board-approved tolerances | Requires company data |
| BG-009 | OBJ-09 | Improve resident outcomes | Energy-cost, comfort, satisfaction and complaint measures | Repairs 73.6%; listens and acts 61.6%; complaint handling 35.5% | Validated improvement without increased harm | Provisional sector medians |
| BG-010 | OBJ-10 | Improve accountability | Exception handoffs accepted by a named human owner | Unknown | 100% accepted or escalated within approved times | Proposed |
| BG-011 | OBJ-11 | Reduce avoidable coordination effort and delay | Primary cycle-time measure: assessment-to-ready-to-install elapsed time. Also measure manual coordination hours per accepted home, net of review and assurance. Report accepted handover separately as an outcome. | Measure in Phase 0 using a comparable cohort | Owner-confirmed proposed pilot improvements: at least 20% lower cycle time and 25% fewer coordination hours per accepted home against the measured baseline | Owner-delegated reviewer requested changes before draft-target ratification; endpoint direction recorded, OD-18 remains open |
| BG-012 | OBJ-12 | Demonstrate proportionate technology value | Incremental benefit, whole-life cost, draft accuracy, overrides and critical exceptions versus non-agentic alternatives | Establish options and shadow-mode baseline | Positive attributable value before scale; zero autonomous controlled approvals and no missed critical exceptions in agreed tests | Proposed scale gate, not proof of zero live risk |

Every FR, RULE and NFR requirement row carries one canonical identifier, its
legacy alias, the business goals it supports and one or more acceptance
criteria. Identifiers are stable and are not renumbered after deletion or
reordering.

BG-002 to BG-005 and BG-011 have measurable targets and timeframes, although
the BG-002 and BG-011 targets remain unvalidated proposals. BG-001 and BG-006
to BG-010 and BG-012 do not yet state a numeric target, a timeframe or both,
because the value depends on company data or a board decision: OD-01 for
BG-001, OD-13 and OD-18 for BG-006, OD-11 for BG-007, OD-12 and OD-15 for
BG-008, OD-08 and OD-18 for BG-009, OD-09 for BG-010 and OD-18 for BG-012.
These goals fail the SMART check until the owners supply the values. This BRD
does not invent them.

No objective will be considered achieved solely because an automated action was
completed or an installation volume increased. On 4 October 2026 the owner
directed that assessment-to-ready-to-install elapsed time remain the primary
BG-011 cycle-time endpoint, with accepted handover reported separately. This
clarifies the measure but does not set its event definitions or close OD-18.
The owner confirmed the BG-011
values as proposed, but the owner-delegated Executive Reviewer recorded
`CHANGES_REQUESTED` on 4 October 2026: the repository provides no directly
comparable target for these measures, no forecast establishes the proposed
magnitudes as achievable, and the proposal still depends on an unratified
measurement protocol. The decision is limited to draft-target ratification;
it is not Zava North Homes approval, a historical company decision, a waiver,
or permission to capture data or operate the programme.

Before BG-011 can be ratified for draft planning, OD-18 must record the
accepted-home population and denominator; start and stop events and elapsed-
time statistic; comparable baseline and cohort; measurement window and rules
for pauses, incomplete cases, withdrawals and exclusions; coordination-hour
roles and tasks, including effort shifted to residents, suppliers and housing
officers and the cost of recording, review and assurance; and the Phase 0
variance-based minimum detectable effect (MDE), including whether the pilot
can distinguish either target. Sector delivery scenarios and SHDF Wave 1
delivery results are not direct evidence for cycle-time or coordination-effort
reductions. If the approved MDE exceeds either BG-011 target, report an interval
estimate and caveat rather than a pass or fail. OD-18, the OD-36 DPIA and lawful
measurement basis, and all actual company approvals remain open.

Accepted handover requires current professional approvals, resident decision
or separately authorised lawful process, accepted physical and documentary
quality, no unresolved safety-critical or material defect, and accessible
handover evidence. Report homes achieving the intended energy outcome
separately: a completed measure does not necessarily move a home to EPC C.

## Provisional Sector Benchmark Pack

The benchmark pack supports scenario planning while company data is gathered.
It does not convert national or sector values into facts about Zava North
Homes.

| Domain | Provisional benchmark for 60,000 homes | Evidence class |
| --- | --- | --- |
| EPC C or above | 44,400 homes, or 74% | England social-rented estimate |
| Below EPC C | 15,600 homes, or 26% | Derived planning benchmark |
| Four-year trajectory | 3,900 accepted completions per year | Derived scenario |
| Rolling stock surveys | 12,000 homes per year for a five-year cycle | Stronger-practice comparator |
| Surveyor-assessed damp | 3,600 HA benchmark; 4,200 social-rent sensitivity | Stock-prevalence estimate |
| Resident-reported damp, mould or condensation | 23,400 HA benchmark; 27,600 LA sensitivity | Lived-experience estimate |
| Stage-one complaints | Approximately 3,270 per year | Landlord median translated to stock |
| Stage-two complaints | Approximately 504 per year | Landlord median translated to stock |
| Emergency repairs within landlord target | 95.1% median | Comparator, not the Awaab's Law standard |
| Non-emergency repairs within landlord target | 82.6% median | Targets differ by landlord |
| Ordinary WH:SHF grant ceiling | GBP 7,500 per eligible home | Scheme cap, not an award |
| Fully loaded retrofit scenario | GBP 20,000 per treated home | Planning assumption |
| First-appointment no-access | 10% central; 5% to 15% sensitivity | Planning assumption |
| Resident refusal or withdrawal | 5% to 10% | Planning assumption |
| Production mobilisation | 6 to 9 months | Planning assumption |
| Survey-ready reserve | 10% to 20% above completion target | Planning assumption |

Detailed sources, caveats, calculations and unsupported-average gaps are in
[UK Social Housing Baseline Research](../reference/research/sector/uk-social-housing-baseline-research.md).

## Stakeholders and Roles

| Stakeholder | Interest and responsibility | Required authority or involvement |
| --- | --- | --- |
| Board | Strategy, risk appetite and long-term financial stewardship | Approves acceleration, investment envelope and downside tolerances |
| Chief Executive | Corporate accountability and executive sponsorship | Escalation for material portfolio, resident or regulatory risk |
| Executive Director of Assets | Asset strategy and portfolio outcomes | Approves investment within delegated authority |
| Building Safety and Compliance Lead | Safety systems, hazard assurance and compliance evidence | Controls safety holds and specialist escalation |
| Retrofit Programme Manager | Programme scope, sequencing and delivery controls | Owns programme progression and exception governance |
| Retrofit Coordinator and competent specialists | PAS 2035 assessment, design and technical coordination | Approve controlled technical outputs within competence |
| Retrofit Assessor | PAS 2035 site survey and assessment | Signs off the survey separately from the Retrofit Coordinator's review under FR-010 |
| Finance and Grants Lead | Affordability, funding, claims and financial control | Validates and submits funding and claim decisions; approves eligibility rule versions under FR-026 |
| Procurement and Contracts Lead | Procurement route, supplier due diligence and performance | Accepts committed capacity and manages contractual escalation; named contract managers alone issue instructions under RULE-008 |
| Resident Engagement Lead | Accessibility, resident insight and complaint themes | Owns consent-process quality and engagement standards |
| Neighbourhood and repairs teams | Tenancy context, issue intake and local resident relationships | Accept resident exceptions and operational repair handoffs; repairs owns hazard categorisation and clocks under RULE-003 |
| Residents and authorised representatives | Home, choices, access needs and lived outcomes | Decide on proposed works unless a separate lawful process applies |
| Shared owners and leaseholders | Own an interest in the home; may fund or permit improvements | Decide and, where the lease requires, contribute through a tenure-specific route under FR-015 |
| Home ownership and leasehold team | Lease records, service charges and owner communication | Confirms tenure and lease-interest status before measures are offered |
| Legal adviser | Legal interpretation and applicability | Interprets leases, consultation duties, procurement modification, payment notice and contractor-awareness questions; no automated capability substitutes |
| Data and Performance Lead | Lifecycle measurement, data quality and evaluation design | Designs baselines, validity tolerances and shadow-test statistics; does not own operational decisions |
| Contractors and subcontractors | Installation, resident service and evidence production | Deliver work and evidence without self-approving acceptance |
| Data Protection Officer | Personal-data and special-category-data governance | Reviews lawful use, access, retention and resident rights |
| Digital service owner and data owners | Integrations, data stewardship, workflow, AI operation and continuity | Accept interfaces, recovery, model and rule changes, access controls and service support within delegated authority |
| Benefit owners | Attributable operational, financial and resident outcomes | Finance validates value; Programme validates effort and delivery; Resident Engagement validates lived-outcome evidence |
| Independent assurance | Quality, audit or specialist review | Verifies evidence where risk or funding conditions require it |

## Scope

### In Scope

* Property candidate identification and explainable prioritisation
* Property, safety, condition, energy and programme-data reconciliation
* Controlled assessment and design workflows
* Resident information, preferences, consent, challenge and accessibility
* Tenure and lease-interest decision routes for shared owners and leaseholders
* Supplier capacity validation and routine scheduling
* All of the association's current contracts and frameworks are included in
  the pilot supplier scope, as owner-directed; the complete inventory, named
  contract managers and authority limits remain to be verified under OD-30
  before live use
* Grant opportunity, award, claim and receipt controls
* Versioned eligibility and funding-route rules
* Capture and referral of hazard awareness from retrofit channels to the
  existing hazard service
* Installation hold points, evidence collection and quality review
* Closed-loop exception handoffs across safety, repairs, housing and programme
  teams
* Defect remediation, reopening and re-verification
* Portfolio, financial, resident, quality and regulatory reporting
* Auditable human approvals and segregation of duties
* Constraint discovery and comparison with non-agentic delivery options
* Building-level dependencies and alignment with planned maintenance
* Integration with existing systems, service continuity and portable evidence
* Shadow-mode evaluation, bounded live pilots and tranche-based scale decisions

### Out of Scope

* Autonomous diagnosis of hazards or resident needs
* Automated legal interpretation or tenancy enforcement
* Automated acceptance of residual safety risk
* Automated professional sign-off or competent-person substitution
* Automated resident consent or inference of consent from silence
* Autonomous investment, procurement award, payment or grant submission
* Contractor self-approval of technical quality or grant eligibility
* Replacement of emergency, damp-and-mould, repairs, safeguarding or complaint
  processes
* Direct control of building safety systems
* AI determination that statutory obligations are satisfied or closure of
  hazards, complaints or defects
* Mandatory sensors or a new platform as a prerequisite for current services
* An upfront commitment to five agents or portfolio-wide capital acceleration

### Digital Foundation and Authority

CON-007/AC-086 impose the real-platform exercise boundary without requiring
the full production ADR estate. Case access and manual draft completion
must not depend on AI availability; mandatory deployed AI is not mandatory
model use in every workflow or approval. Rejecting a narrow Decision task
does not permit a wholly disabled-AI application to pass exercise acceptance.
Source-linked rules/manual handling remains the baseline comparator.

The digital foundation connects authoritative asset, repairs, housing, finance,
procurement and contractor systems. It does not recreate their services or
transfer their statutory or financial accountability. Property records link to
building records where shared systems or building-level safety controls apply.

Deterministic workflow enforces evidence validity, safety and resident holds,
statutory timers, delegated approvals, funding and capacity gates, scoring
weights, eligibility and route rules, lifecycle states, queues, audit and
reconciliation. Only authorised people make the underlying controlled
decisions. A workflow may execute a validated transition after those decisions;
an AI recommendation cannot satisfy an approval gate.

Decisions that must follow clear rules and be transparent, repeatable and
explainable to residents, regulators, funders or the Board use the
deterministic approach. Agents are placed only where the
[Agent Request Challenge](../reference/research/company/agent-request-challenge.md)
found a plausible gain: turning free text, documents and messages into
concrete, sourced values for the rules and benefits measures; proposing
missing values with source-based confidence categories for owner confirmation,
never inventing an observation; reconciling records; drafting from approved
records; and raising signals for human triage. Confidence means one of four
source categories: verified from an authoritative source, owner-confirmed,
agent-proposed and unconfirmed, or unknown. Numeric model confidence may be
shown only where Comparison 2 has tested calibration for that capability;
self-reported language-model confidence is not used as a confidence measure.
Agent-proposed values stay visibly marked at field level until a named owner
confirms them. Programme supervision and portfolio reporting stay deterministic
in the initial pilot.

Because Zava North Homes is a regulated not-for-profit accountable to
residents, the Regulator of Social Housing, funders and its Board,
explanations are designed for all four audiences. Resident explanations use
plain language and non-digital routes; staff explanations support timely human
review; funder, regulator, Board and audit explanations preserve reconstruction
and assurance evidence without implying that the association currently works
wrongly.

| Capability | Deterministic core | Initial agent responsibility and boundary | Human authority |
| --- | --- | --- | --- |
| Property data and prioritisation | Versioned scoring weights, pass, fail or unknown eligibility rules (FR-026), published prioritisation policy and reason-code controls (FR-042) and data validity rules | Reconcile records, extract condition facts from free text, flag missing or stale fields and explain scores; no ranking weights, eligibility decisions or silent exclusion | Asset and safety owners approve rules, cohorts and exceptions; named data owners confirm proposed values and resolve critical conflicts |
| PAS 2035 assessment preparation | Stage gates, separate assessor and coordinator sign-off (FR-010), material-change rules and safety-hold check | Pre-populate sourced factual inputs, structure survey notes and track omissions; no generated site findings | Competent assessors, designers, coordinators and evaluators own professional outputs |
| Grant and funding evidence | Four-state grant ledger (FR-023), eligibility and route rules, reconciliation and claim holds | Match evidence to the per-measure schedule and assemble draft packs for Finance review, only once the ledger exists and an award or open route is evidenced | Finance approves funding, validates and submits bids and claims, and confirms receipts |
| Resident service | Measure-specific decision record, adjustments, pauses and failed-access rules (RULE-006) | Draft accessible content, route free-text messages to fixed categories and suggest options; no autonomous consequential contact or consent determination | Residents decide on discretionary measures; staff own support, communication, exceptions and redress |
| Supplier coordination | Committed-capacity register, standard work orders, appointment outcome codes and contract-manager instructions | Suggest appointments within approved design, resident decisions and committed capacity, and convert contractor messages to outcome codes; no autonomous works release or instruction | Contract manager accepts capacity; Programme releases work and confirms appointments |
| Quality evidence assurance | Per-measure evidence checklist, defect severity rules and independent acceptance | Check evidence and raise anomalies; a missing flag is not assurance (RULE-014); no acceptance or automated defect closure | Competent quality authority accepts work and verifies remediation |
| Hazard signals | Statutory clocks and awareness timestamp in the existing hazard and repairs service (FR-003, RULE-003) | Raise-only scan of retrofit notes and messages feeding human triage; no hazard categorisation or clock control | Hazard and repairs service owns categorisation, clocks and closure |
| Programme supervision and reporting | Lifecycle states, queues, clocks, audit and reports from controlled records | None in the initial pilot; later summarisation support requires its own RULE-019 test | Programme owns the workflow; executives and Board approve investment, risk and further tranches |

Shadow mode permits no live consequential actions. The initial live pilot
retains these draft-and-recommend boundaries. Any later routine automation
requires a separately tested authority change under RULE-020; prohibited
decisions remain prohibited.

### Delivery Phases and Approval Gates

| Phase | Proposed scope and timing | Evidence and authority to proceed |
| --- | --- | --- |
| 0. Readiness | Indicative 6 to 8 weeks; validate pilot-area stock and building data, twelve-month throughput, delay causes, resident journeys, competence, suppliers, funding, headroom and platform options; after the frozen protocol and the OD-36 DPIA and lawful measurement basis are approved, switch on identical event capture for the proposed pilot locality and matched locality before resident contact | Sponsor and Finance authorise a capped discovery envelope; relevant control owners accept the baseline, options appraisal, Comparison 1 and Comparison 2 evaluation protocol, guardrails and data-protection gates before any Phase 0 pilot or comparison event capture. Shadow testing additionally requires the shadow-mode entry evidence listed for Phase 1 |
| 0D. End-to-end demonstrator | Build and self-test the complete target workflow in a non-production environment using constructed exercise records or approved de-identified cases; include representative successful, safety-hold, consent, eligibility, missing-evidence and integration-failure paths | Sponsor accepts demonstrator scope and cost; architecture, security, data and control owners accept that no live authority or production dependency is implied. Progression to shadow mode requires documented component contracts, threat controls, evaluation results, observability, known gaps and tested fallback |
| 1. Shadow mode | Recommendations, drafts and exception tests without live commitments or resident contact; duration agreed after readiness; run paired agent outputs against the same cases handled by workflow-only teams where lawful | Sponsor authorises live pilot only after safety, technical, resident, finance, procurement, data and digital owners accept controls, comparison results, DPIA, continuity tests, guardrail stop triggers and pilot budget |
| 2. Controlled live pilot | Indicative 6 to 9 months; existing teams and suppliers in one locality, a few understood archetypes, named accountable owners, agents operating within recommend, draft, reconcile and flag boundaries, 80 to 100 candidate homes and at least 50 accepted handovers proposed; assurance capacity needed for safety remains a control | Control owners and independent assurance review the frozen benefits scorecard, operating dashboard exceptions and guardrail breaches; Board authorises any acceleration beyond the existing annual plan under RULE-011 |
| 3. Repeatable schemes | Approved archetype patterns, geographic packages, planned-maintenance alignment, supplier scorecards and risk-based inspection | Next tranche requires accepted quality, resident, capacity, funding and financial evidence within the approved envelope |
| 4. Selective scale | Add only automation with proven incremental value and extend by archetype or geography | Board approves the next envelope after independent assurance and downside testing; relevant owners approve each authority change |

Before any Phase 0 pilot or comparison event capture, Phase 0 must ratify
cohort size, archetypes, schedule, cost ceiling and thresholds through the
frozen protocol and the approved OD-36 DPIA and lawful measurement basis. These
are planning proposals, not a delivery promise or a statistically sufficient
demonstration of safety.
Time elapsed or handover count alone cannot pass a gate. Include varied
resident communication and adjustment needs; technically excluded homes remain
visible with named owners and appropriate service routes.

Each phase authorises only its stated scope. All applicable Must controls,
including service continuity, are required before live use; phasing cannot
waive safety, resident or financial gates. Portfolio optimisation may be
deferred, but pilot properties must already have the necessary building and
planned-maintenance checks. Failure to demonstrate AI value can lead to
conventional workflow delivery rather than a forced AI rollout.

### User Value, Adoption and End-to-End Demonstration Strategy

The programme should not be pitched as a technology demonstration alone. The
value proposition is an agent-led modernisation of the current retrofit model
that reduces administrative drag, eliminates avoidable rework and improves
decision quality without diluting resident choice, safety controls, professional
authority or financial discipline. The solution therefore has two parallel goals:

1. prove the complete workflow and architecture across representative
   non-production property journeys; and
2. prove the people who run the process find it easier to use than the current
   spreadsheet-based coordination model.

The main design tension is that the evaluation rubric requires a complete,
end-to-end architecture demonstration, while the staged-implementation logic
requires controlled evidence before live use. The solution separates technical
completeness from operational authority. The demonstrator implements the
complete architecture in a non-production environment with constructed
exercise records or
approved de-identified cases. Shadow and live validation then test whether the
same capabilities create attributable value in the operating context. A
complete demo therefore does not imply a portfolio-wide autonomous
implementation.

The architecture should therefore be demonstrated across one complete retrofit
journey from property readiness through assessment, eligibility, resident
engagement, contractor coordination, evidence assurance and portfolio
reporting. Within that slice, the deterministic workflow establishes the
source of truth and the agent functions are limited to recommend, draft,
reconcile and raise-only behaviours. The value to users is visible in every stage:

* property, risk and grant data are reconciled before survey and no longer
  re-entered manually across spreadsheets;
* the team sees a single queue of homes by stage, age, owner and block reason;
* draft PAS 2035 inputs and grant evidence packs are assembled from approved
  records, reducing rework and missed evidence;
* resident decision records and communication drafts are generated and routed to
  named staff for approval, not silently assumed;
* capacity, work-order and appointment planning is suggested against committed
  supplier capacity instead of through manual chasing;
* quality evidence is checked for omissions and anomalies before handover, with
  flagged exceptions routed to a person;
* reports show where the programme is blocked, who owns the next action and
  which homes remain off-plan because of data, resident access, capacity or
  professional review.

This provides immediate value to the end users because it removes the work they
currently do in Excel, not because it creates an additional process layer.
Legal, regulatory and resident-safeguard controls remain visible and
non-negotiable. Human users keep authority for safety holds, resident consent,
professional sign-off, supplier instruction, grant approval, payment and quality
acceptance.

The adoption plan lowers resistance to change by showing user value before
asking the organisation to change live work. The demonstrator should contain a representative constructed exercise case
pack covering straightforward journeys, resident-contact-heavy journeys,
supplier dependencies, missing or conflicting data and controlled failures.
Staff can test those journeys and influence the
design without affecting a resident or live decision. The later operational
cohort should cover one locality, a limited number of archetypes and a bounded
set of completion routes, with a matched comparison group.

| Demonstration objective | Proposed design | Value to users | Approval gate |
| --- | --- | --- | --- |
| End-to-end architecture proof | Non-production implementation of the full lifecycle from intake to handover, with deterministic workflow, bounded agent functions and constructed exercise records or approved de-identified cases | Team sees one path through an otherwise fragmented system without the spreadsheet shuffle | Sponsor accepts the scope; architecture, security and control owners accept the evidence and known gaps |
| User-value proof | Staff test current pain points: duplicate data entry, missing evidence, queue ambiguity, resident communication and manual rework | Users experience fewer manual steps, clearer ownership and faster escalation in a safe proving environment | Process owners validate the scenarios and usability findings |
| Adoption and trust | Human approval gates, evidence lineage, explanations, overrides and failure recovery are visible during the demo | Staff can see where the workflow helps and where human judgement still matters | Data, DPO, resident engagement and technical owners accept progression to shadow mode |
| Operational value | One locality and a matched comparison group validate the demonstrated capabilities against current delivery | Teams learn from real cases without unbounded operational risk | Sponsor approves the cohort, lawful measurement basis, measures and stop criteria |

The demonstrator should therefore be designed as a complete but bounded
proving environment, not a collection of disconnected feature prototypes. It
must exercise at least one complete property journey in every major pathway,
supported by the shared record, lifecycle state, queue management, named
ownership, approval gates, agent handoffs, observability and failure recovery.
The later operational validation provides the comparison arm and evidence of
real-world value.

The proposed staged sequence is:

1. Baseline and design: define the property lifecycle, map the current
   resident and contractor journey and identify the manual work now done in
   spreadsheets.
2. End-to-end build: implement the common property record, state model, queue,
   handoff ownership, consent status, quality checklist, grant ledger,
   deterministic controls and bounded agent assistance in non-production.
3. Architect self-test: execute representative happy, exception and failure
   paths; capture logs, metrics, traces, latency, quality and cost; disclose
   simulated boundaries and known gaps.
4. Staff validation: ask representative users to complete the same scenarios,
   test whether the workflow is faster and clearer than the spreadsheet
   process, and correct barriers before shadow use.
5. Shadow and operational comparison: instrument the current process in the
   pilot and matched localities, freeze the event dictionary, and use task-level
   and process-level evidence to show whether the demonstrated capabilities
   improve accepted outcomes.
6. Scale decision: proceed to the next tranche only after value is
   demonstrated and controls prove stable, with reporting and governance
   revalidated for the broader rollout.

This gives the sponsor a more ambitious plan than a few disconnected pilots
while preserving an evidence-led, low-risk progression. The architecture is
built and exercised end to end first. Operational authority is added only
after self-test, staff validation and control-owner review. The project does
not seek to prove a fully autonomous agent portfolio; it proves that a bounded,
accountable workflow can work as a complete service and then tests whether it
outperforms the spreadsheet model.

The user-value measures should be visible to the programme team in the first
month of demonstration, not only at the end of the pilot. Lead indicators should
include:

* time to reconcile missing records and evidence;
* manual hours avoided per home;
* number of homes left unowned or stalled in the queue;
* repeat resident contacts and failed access events;
* number of grant evidence packs drafted without manual correction;
* percentage of homes with clear next action, owner and promised update;
* number of critical exceptions caught before a survey or handover.

Lagging indicators should include accepted handovers, defect rates, quality
rework, grant conversion efficiency, resident satisfaction and maintenance of
safety and consent controls. These metrics support the BRD's requirement that
value be assessed against current delivery, not against the activity count or
the number of AI features shown in a demo.

The governing principle is therefore straightforward: prove a complete,
value-bearing operating slice end-to-end, keep the decision authority with
people, and only then expand. This satisfies the rubric requirement for a
credible architecture demonstration while aligning with the staged, regulated,
resident-safe delivery model expected by the BRD.

### Pilot Evaluation

| Dimension | Required evidence at the live-pilot exit |
| --- | --- |
| Safety and professional authority | Zero works released with unresolved relevant safety holds; all technical outputs attributable to competent roles; every urgent hazard handed to its existing response service without timer suppression |
| Resident rights and experience | Zero unauthorised starts or automatically inferred refusal; adjustment fulfilment, kept appointments, disruption, repeat contacts, complaints and resident feedback, including non-digital journeys |
| Quality and energy outcome | Physical and evidence right-first-time acceptance measured separately by severity; no unresolved safety-critical or material defects at handover; energy outcomes reported separately from installations |
| Throughput, cycle time and effort | BG-002 and BG-011 measured against comparable homes, with exclusions, pauses, incomplete cases and reopened work visible |
| Capacity and finance | Forecast versus accepted output by role, supplier, subcontractor and work package; cost per accepted home, grant reconciliation, peak cash and covenant headroom within approved tolerances |
| AI usefulness and control | Accuracy and error severity, draft acceptance, overrides, review time, unsupported-claim rate, explanation fidelity, automation-bias indicators and missed critical exceptions versus rules-based or conventional workflow; no autonomous controlled approvals |
| In-use evaluation | Lawful, proportionate follow-up plan for energy, comfort, affordability, moisture and ventilation; seasonal evidence reported as pending where not yet available |

RULE-019 requires baselines, denominators, comparison design and owners before
testing. The proposed counterfactual is the instrumented Phase 0 and shadow-mode
pre-period plus a concurrent matched comparison cohort, pending OD-18
ratification. Short pilots must not claim seasonal bill savings or safety
assurance from a small number of successful handovers.

The pilot protocol must use two named comparisons:

* Comparison 1, locality with agents versus matched locality without agents,
  tests whether adding agents to existing teams improves accepted outcomes. It
  freezes the cohort before any resident contact; analyses all homes that
  entered on an intention-to-treat basis; uses a concurrent matched comparison
  locality using existing teams without agents; switches on identical event
  capture in both localities during Phase 0; compares each locality with its
  instrumented pre-period using difference-in-differences; reports output per
  unit of committed competent capacity as well as total output; and logs shared
  staff or supplier time because shared resources can contaminate the
  comparison.
* Comparison 2, per-capability task-level evidence, tests which agent
  capabilities scale. It uses paired shadow-mode comparison on the same cases,
  and task-level allocation between agent-assisted and workflow-only handling
  where safe and lawful. Measures include review minutes, drafts accepted
  without material edit, error severity, overrides, missed critical exceptions,
  unsupported-claim rate, explanation fidelity sampled by reviewers and
  automation-bias indicators such as review time below an owner-set floor or
  near-total acceptance.

Before any Phase 0 pilot or comparison event capture, RULE-019, OD-18 and
OD-36 must freeze and version the event dictionary, accepted-handover
definition, clock and pause rules, eligibility, entry cut-off, denominators,
matching variables, primary measures, minimum detectable effect, thresholds,
unfinished-case handling, exclusions and analysis code version, and approve the
DPIA and lawful measurement basis. Later changes record a new version and reason.

Analysis uses medians and 80th or 90th percentiles for cycle time. Open cases
are reported as censored time-to-event observations, with withdrawal and
technical exclusion as competing outcomes. If the minimum detectable effect is
larger than the BG-011 targets, the pilot reports an interval estimate rather
than a pass or fail. Safety, resident rights and quality are must-not-worsen
tests, not benefits to trade against throughput. Zero incidents in about 50
handovers is not evidence of safety.

Effort measurement is part of the RULE-019 protocol governed by AC-077. The
design uses work sampling, short time studies or short diary weeks in both arms,
net of review and assurance, and shows effort shifted to residents, suppliers
and housing officers, including the time spent recording. Measurement, parallel
running and assurance are technology costs under FR-025.

Proposed guardrails and stop triggers are:

| Guardrail | Governing requirement IDs | Accountable owner | Required measurement | Proposed stop trigger | Restart authority |
| --- | --- | --- | --- | --- | --- |
| Unresolved safety hold | FR-001, RULE-001, RULE-024 | Accountable safety role | Gate passes with a missing, stale or unresolved hold | Any one pauses the affected work package for review | OD-35 named authority under RULE-020 |
| Hazard response | FR-002, FR-003, RULE-003, RULE-024 | Repairs and Building Safety owners | Pilot-locality cases meeting each Awaab's Law step, split by source, including the awareness-to-referral gap | Any retrofit-linked breach or unaccepted referral pauses affected work | OD-35 named authority under RULE-020; hazard response remains with the repairs and hazard service |
| Defects at handover | FR-029, FR-030, AC-043, RULE-013, RULE-024 | Competent quality authority | Safety-critical, material and minor defects by severity, plus reopened cases | A safety-critical defect holds the home; repeated or systemic defects trigger competent review and hold affected further work | OD-35 named authority under RULE-020, with competent quality disposition |
| Post-retrofit damp, mould and ventilation | FR-032, RULE-014, RULE-024 | Assets, Building Safety and DPO-approved evaluation owners | New or recurrent cases over fixed follow-up windows against comparable homes | A confirmed significant hazard triggers competent review; a cluster pauses the archetype | OD-35 named authority under RULE-020, after evaluation-owner review |
| Fire-relevant measures | FR-035, AC-055, RULE-024 | Assets, Building Safety and competent technical roles | Measures affecting fire-relevant elements reviewed before instruction and inspected at handover | Missing review, missing inspection or fire-stopping defect holds that work | OD-35 named authority under RULE-020, with competent technical approval |
| Resident authority | FR-011, FR-013, FR-014, FR-015, RULE-024 | Resident Engagement, Home Ownership and Legal where tenure or lease interests apply | Works started without a current resident decision or authorised exception | Any one pauses the work package | OD-35 named authority under RULE-020 after the current decision or authorised exception is recorded |
| AI explanation and claim integrity | FR-034, FR-044, RULE-019, RULE-024 | Data and Performance Lead, DPO and relevant control owner | Unsupported eligibility, consent, safety or evidence claims; explanation-fidelity failures; automation-bias indicators against owner thresholds | Any unsupported eligibility, consent, safety or evidence claim accepted undetected, or any owner-threshold breach, pauses the affected capability | OD-35 named authority under RULE-020 after reviewer sampling, remediation and control-owner acceptance |

RULE-024 records the pause-and-restart rule for guardrail breaches. Override
authority, if any, is open under OD-35. Awaab's Law clocks stay outside any acceleration or
cycle-time measure (FR-002, RULE-003). The local [Awaab's Law Phase 1 guidance](../reference/regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md)
is official non-statutory guidance for requirements in force from 27 October
2025, retrieved 2026-09-19; section 1.4 records fixed timeframes including 24
hours for emergency hazards and 10 working days to investigate potential
significant hazards. The local [Awaab's Law Phase 2 guidance](../reference/regulatory/social-housing-regulation/awaabs-law-phase-2-guidance-2026.md),
also official non-statutory guidance, states that Phase 2 requirements apply
from 30 November 2026. Legal must confirm current scope and applicability before
the protocol is frozen.

## Current and Future Business Processes

### Current-State Summary

The source describes spreadsheet-led coordination across assessment, funding,
procurement, resident consent and quality assurance. The authoritative systems,
handoff rules, approval thresholds, data quality and performance baselines are
unknown.

For RULE-016, the readiness evidence includes a twelve-month accepted-throughput
reconstruction by archetype, measure and supplier, plus stage timings, delay
causes, repeat work, manual effort, access outcomes and defects. The
reconstruction provides context with coverage flags. It does not establish the
counterfactual on its own. The proposed counterfactual for the options appraisal
and pilot is the instrumented Phase 0 and shadow-mode pre-period plus the
concurrent matched comparison cohort, pending OD-18 ratification.

### Future-State Lifecycle

Each property will follow a controlled lifecycle with separate technical,
resident, financial, safety and quality gates:

1. Candidate identified and matched to property and building records
2. Prioritisation recommended with planned-maintenance, funding and capacity screens
3. Safety and data readiness checked; resident information, adjustments and survey access arranged
4. Assessment completed and accepted by the competent roles
5. Options, whole-dwelling pathway and disruption discussed with the resident
6. Property-specific design approved
7. Resident decision recorded
8. Investment, funding and supplier capacity confirmed
9. Work released and scheduled
10. Installation hold points completed
11. Completion and quality evidence accepted
12. Accessible resident handover completed
13. Payment and grant evidence reconciled
14. In-use outcomes monitored
15. Property closed or reopened for remediation

Safety, damp-and-mould and emergency processes operate independently of this
sequence and take precedence where required. Linked identifiers and handoff
status connect them without making retrofit or AI availability a dependency.
Early funding and capacity screens are provisional; final confirmation remains
mandatory before works release. Resident engagement continues throughout, and
material design or circumstance changes trigger affected decisions to be
reviewed again.

### Operating Model for a Home-Centred Workbench

The next product should coordinate work around one versioned home case,
connected to its building, scheme, work package, provider and resident-service
cases. It should present role-specific queues over the same governed records,
not create separate versions of the truth for each profile. The local
prototype's four task perspectives show the value of changing emphasis by
task; they are not identity or authorisation controls. A production service
must enforce permissions server-side.

This is a proposed operating model, not a description of current company
practice. Named service owners, source systems, response targets, approval
limits, contract terms, payment milestones and resident channels remain to be
validated. The resident intake described here covers complaints, service
requests and repair or defect reports. It does not define resident
compensation or reimbursement claims.

#### Two linked levels of property context

The building or block record is the parent for shared context and decisions:

* Stable building identity and links to every included home
* Shared fabric and systems, building archetype, access and common-area
  constraints, and applicable building-safety or other shared holds
* Planned-maintenance dependencies, shared surveys or designs, consultation
  status where applicable, and building-level sequencing decisions
* Shared work packages, contract and capacity commitments, common costs and
  decisions that apply to more than one home

Each apartment or house has its own home case and retains its own evidence and
decisions:

* Property identity, tenure or lease status, condition, EPC and source dates
* In-home systems, assessment, design version, measure-level funding and cost
* Resident communication preferences, adjustments, representative authority,
  access arrangements and a separate decision for each proposed measure
* Home-specific holds, appointments, accepted evidence, defects, invoice
  allocation, handover and aftercare

A shared intervention may have one building work package but still needs
property-specific readiness, technical review, resident decision, cost
allocation, quality evidence and closure. A building-level dependency blocks
only the affected scope and homes; the relationship and reason must be
recorded. It must not silently transfer one apartment's consent, condition or
approval to another.

#### Prioritisation and readiness

Use three distinct decisions rather than one opaque ranking:

1. Route known hazards, emergencies and statutory response clocks through the
   existing safety or repairs service. They do not wait in a retrofit queue or
   compete with discretionary investment scoring.
2. Apply versioned, deterministic eligibility and readiness checks. Missing or
   conflicting identity, tenure, condition, building dependency, safety,
   technical, resident, funding or supplier evidence is `unknown` or a named
   hold, not an assumed pass or a silent exclusion.
3. Apply only the published, approved capital-prioritisation policy to the
   remaining discretionary choices. Show the score, source freshness, reason
   codes, dependencies and what could change the order. Group homes for shared
   works only after preserving home-specific gates. A resident's support need
   or a missing adjustment must prompt support and review, not a lower
   priority.

The minimum prioritisation record therefore needs authoritative property and
building identifiers; condition and energy evidence with dates and provenance;
planned-maintenance and shared-system dependencies; hazard and hold references;
tenure and funding-route evidence; measure scope and cost; resident decision
and adjustment status with minimum necessary detail; committed competent and
provider capacity; rule versions; and an inclusion, deferral or exclusion
reason. Asset and safety owners approve the policy and exceptions. Data owners
resolve conflicts; agents may surface discrepancies but cannot set the
priority.

#### Team coordination and resident/provider contact

The shared case should expose role-oriented work queues, not require every
function to review every home at every step:

* Programme coordination owns the case timeline, next-action owner, due date,
  cross-team dependencies and confirmation that a handoff was accepted.
* Asset and competent retrofit roles review cohort, building dependencies,
  assessment, design and technical changes within their authority.
* Housing or Resident Engagement owns the resident relationship and supported
  contact; Building Safety and Repairs own hazard categorisation and response;
  Procurement and the named contract manager own supplier authority;
  Quality owns independent evidence acceptance; Finance and Grants own budget,
  invoice and grant decisions.
* Digital operators see import, integration, access and recovery exceptions;
  assurance reviewers see decisions, sources, versions, overrides and audit
  history.

A handoff is not complete when a message is sent. The receiving team must
accept it, acknowledge urgency, own the next action, state when the resident
will next be updated and record the outcome. Routine case coordination can be
async through these queues; linked-building decisions, overdue holds, material
changes and disputed handoffs trigger a named cross-functional review. The
review cadence and escalation targets require company validation.

Residents need an accessible, non-digital route as well as any approved digital
channel. Staff record the resident's words, desired outcome, property,
accessibility needs, relevant evidence, safe callback method and permission to
use a representative. A first human triage checks for an urgent hazard and
routes it immediately to the existing service without waiting for the retrofit
workflow. Other complaints, service requests and defect reports receive a
reference, named owner, next-update date and a traceable investigation,
remedy, complaint or appeal route. A service report is not consent to a
measure; a complaint is not closed merely because a retrofit stage advances.

The provider-facing path is separate. The contract manager sends a controlled
work order only after technical, resident, safety, funding, budget and capacity
gates pass. It identifies the home or shared work package, approved scope and
version, schedule, evidence checklist, approved contact route and change
process. Provider appointment outcomes, hazards, variations, completion packs
and invoices enter through contract-approved channels; an API or provider
portal is not assumed. Provider-caused failures are coded separately from
resident access outcomes. Only the authorised contract manager can issue an
instruction or approve a variation, suspension or reallocation.

#### Work, budget, invoice and grant controls

Keep four approvals visible and distinct:

1. The competent roles approve the property-specific technical scope and
   design.
2. The resident makes and may change the decision for each discretionary
   measure, with accessible information and a recorded pause or withdrawal.
3. Asset and Finance approve the investment and funding against delegated
   authority, an identified budget line, whole-life cost, match and cash
   exposure. Procurement confirms the contract or call-off route and the
   contract manager confirms committed capacity.
4. The Retrofit Coordinator releases the approved work package after the
   deterministic gates pass. The released instruction, approved design,
   budget ceiling and funding references are version-linked. A scope, cost,
   building condition, resident circumstance or funding change returns the
   affected decisions for review before more work proceeds.

Provider invoice intake is an accounts-payable workflow, not a grant claim.
Capture the supplier, contract/call-off and work-order references, home or
building allocation, invoice and line-item amounts, applicable milestone or
valuation, tax details required by the finance process, supporting completion
evidence and any change authority. Match the submission to the authorised
scope, approved budget, recorded work, accepted milestone evidence, prior
payments and open defects or holds. Route unmatched, duplicate, over-budget,
unsupported or disputed lines to a named human queue. The provider cannot
approve its own work or payment. Finance verifies the match, applies the
contract's payment and notice terms, obtains the required independent approval,
records the due date and any lawful/contractual hold, executes payment and
reconciles the ledger and remittance. No fixed payment interval, retention
percentage or milestone is set by this BRD; Legal and Finance must validate
the governing contract and applicable payment rules before operational use.
A defect or hold is not authority to withhold an unrelated amount unless the
contract and legal review permit it.

Grant claims are a separate Finance-controlled path. The programme can assemble
property- and measure-linked evidence only after the funding route and award
are evidenced, eligibility passes, work and quality evidence are accepted,
and the claim schedule is satisfied. Finance reviews, certifies and submits;
award, claimable value, submitted claim, accepted claim and cash receipt remain
separate ledger states. A provider invoice or its payment status is not proof
that a grant claim is eligible or reimbursed.

#### Agent assistance and next-step interaction

The main screen should explain the current gate, its evidence and blocker, then
offer a short, role-relevant next-step suggestion. Each suggestion shows its
source records, rule or model version, why it is relevant, proposed owner,
prerequisites, due-date basis and what remains unknown. The user can accept,
edit or reject it with a reason; acceptance creates or updates a task, not an
approval.

Agents may reconcile records, extract cited fields from documents, summarise a
resident or provider report, draft an accessible response for review, identify
possible duplicate intake, flag missing invoice evidence, prepare a claim pack
and suggest a handoff. A deterministic workflow owns mandatory ordering,
timers, eligibility, authority, budget checks and state changes. An agent
cannot diagnose a hazard, infer consent, choose who deserves investment,
contact a resident or provider without authorised review, issue a work order,
approve an invoice or claim, release payment or close a complaint, defect or
safety case. Failure or stale evidence leaves the work visibly blocked and
owned.

### Workflow Portfolio and Business Value

The workbench is the shared coordination surface, not the whole solution and
not one giant agent workflow. The underlying business is a set of connected
workflows, each with a different control owner, outcome and value test. The
problems below are the case-study challenge and role-agent analysis: they are
research-backed problem hypotheses, not verified findings about Zava North
Homes' current operations. Phase 0 must show which are material constraints.

| Workflow and problem to solve | End-to-end outcome and accountable roles | Where agents may help; what remains deterministic or human-owned | Business value evidence |
| --- | --- | --- | --- |
| Stock data, safety triage and fair prioritisation. The requested ranking assumes reconciled condition, energy, building, tenure and hazard data and an approved cohort policy; neither data quality nor policy is established. | Reconcile home and building records; route hazards to the existing service; determine eligibility as pass, fail or unknown; apply the approved investment policy; review the cohort, exceptions and resident questions. Asset owns investment policy with Safety, Finance and data owners for their domains. | Reconcile conflicting records, extract sourced facts and draft explanations. Identity resolution, eligibility, weights, hazard routing, exceptions and final cohort decisions are controlled rules and named human decisions. | Homes remaining viable after survey; critical conflicts found before survey; time and rework to form a cohort; reasons for deferral; outcome and override patterns by relevant resident groups. Supports BG-001, BG-002, BG-005, BG-007 and BG-012. |
| Technical assessment and design readiness. The challenge is not to have AI perform a PAS 2035 assessment; it is to get complete, reliable evidence to competent roles and avoid preventable returns while respecting assessor and coordinator responsibilities. | Gather property/building evidence; complete the site survey; record the Retrofit Assessor's sign-off; coordinate technical review and risk path; resolve dependencies; approve a versioned design; re-review affected decisions after material change. Competent assessors, designers and Retrofit Coordinator own professional outputs; Programme coordinates. | Pre-fill only sourced facts, flag conflicts and missing checklist items, and prepare review packs. Site observations, technical judgement, professional approval and design release stay with competent people. | Assessment-to-ready-to-install elapsed time; first-pass completeness; returned/re-approved assessments and designs; pre-fill error rate; review effort net of checking. Supports BG-002, BG-003, BG-006 and BG-011. |
| Resident service, access, choice and redress. The research identifies fragmented contacts, unclear disruption information and a risk of treating failed access as refusal; actual channels, rates and resident experience need validation. | Receive and triage service requests, complaints and repair/defect reports; route urgent hazards; provide accessible information and support; record a separate decision per measure; arrange/recover appointments; honour pauses and withdrawals; investigate, remedy and keep the resident updated. Housing and Resident Engagement own the relationship and redress; Repairs/Safety own their service cases; the resident owns discretionary measure choices. | Classify inbound messages to staffed queues and draft accessible responses from approved facts for human review. No automated persuasion, inferred consent/refusal, unsupported vulnerability inference or unreviewed consequential contact. | First-time appointments kept; adjustments met; repeat contacts; time to a resident decision; complaint and service resolution; resident-reported disruption, comfort and affordability, disaggregated where lawful and appropriate. Supports BG-005 and BG-009. |
| Procurement, committed provider capacity and work release. Scheduling cannot solve missing installers, incomplete work orders or contract ambiguity; actual available capacity and contract permissions are unknown. | Verify the contract/call-off and authority; confirm competent capacity, subcontractors and contingency; prepare a complete work order; match work to capacity and resident availability; approve and issue the instruction; track delivery, exceptions and recovery. Procurement and the authorised contract manager own contractual acts; Programme owns release gates and coordination. | Reconcile provider schedules and emails to controlled capacity records, detect likely clashes, and suggest slots within confirmed capacity. A person confirms commitments, instructions, variations and supplier reallocation. | Committed versus delivered capacity; provider-caused cancellations/no-shows and abortive visits; first-time appointment performance; time to resolve capacity gaps; accepted homes by supplier, quality and cost. Supports BG-002, BG-006, BG-009 and BG-011. |
| Hazard awareness and damp-and-mould response. The case and analysis identify a risk that reports from residents, visits and providers do not become one timestamped, owned response; the actual company pathway remains open for validation. | Capture the source and awareness time; send the referral to the existing hazard/repairs service; obtain human acceptance; investigate and act under that service's rules; link any retrofit hold and only release it on accountable evidence. Repairs and Building Safety own categorisation, clocks, action and closure. | A raise-only scan may surface possible missed signals in text for human triage, subject to capacity and legal/privacy gates. The existing service owns clock calculation, classification, resident updates, statutory decisions and closure; the retrofit workbench cannot pause or reset them. | Awareness-to-referral time; unaccepted referral ageing; cases meeting applicable investigation, action and update requirements; missed critical reports in agreed tests. Supports BG-003, BG-004 and BG-010. |
| Quality acceptance, defects and resident handover. The underlying risk is paying, claiming or handing over incomplete work, late discovery of defects, or loss of the link from scope to evidence; independent capacity and current evidence quality are unknown. | Collect per-measure completion evidence; run the positive checklist; perform independent inspection or sampling; accept or return evidence; track defects, remediation and reinspection; provide accessible handover and aftercare; reopen the affected case when required. Competent Quality authority accepts work and controls defect closure; providers submit evidence but do not self-approve. | Compare photos and documents with a fixed checklist, identify missing/mismatched evidence and raise possible systemic patterns. A competent person determines compliance, accepts or rejects work, grades defects and closes them. | Right-first-time physical and evidence acceptance; defect rate and severity; false/missed flags against human review; evidence review effort; rework and remediation cost; recurrence and resident aftercare outcomes. Supports BG-003, BG-006, BG-007 and BG-009. |
| Budget, provider invoice, grant claim and cash reconciliation. A work invoice, a grant claim and cash received are different events. The real issue is linking approved scope and completed evidence to valid payment and funding records, not generating claim prose. | Approve the investment and budget; record commitments; intake and match provider invoices/valuations to contract, work order, approved scope, milestone evidence, prior payments and defects; Finance reviews and pays under applicable terms; separately assemble, certify and submit eligible grant claims; reconcile receipts and clawbacks. Finance and Grants own financial decisions; Procurement/Legal own contract interpretation and the contract manager owns instructions. | Reconcile documents and ledgers, identify missing evidence or duplicate lines, and draft packs from controlled values. Rules calculate eligibility and amounts; Finance validates, approves, submits and records cash; the authorised payment process executes payment. | Invoice match exceptions and first-pass acceptance; time and effort per invoice and claim net of review; claim acceptance/rejection and clawback; time from accepted evidence to submission/receipt; grant by opportunity, award, claimable, submitted and cash states; cost per accepted home and peak cash exposure. Supports BG-007, BG-008, BG-011 and BG-012. |
| Programme handoffs and case orchestration. The role analysis finds no single view of each home's state, blocker, owner and next step; actual queue and delay data must establish the scale and cause. | Maintain linked home/building/scheme cases, lifecycle states, clocks, named queues and dependencies; ensure handoffs are accepted; escalate overdue or unowned work; keep residents informed; recover from failures; reopen work when evidence or circumstances change. Programme owns the operating workflow; each receiving team owns its decision and action. | Summarise case evidence, surface stale or missing records, draft next-step suggestions and detect unowned handoffs. Deterministic workflow enforces state transitions, timers, authority and escalation; a human accepts, edits or rejects suggestions and owns exceptions. | Assessment-to-ready-to-install elapsed time; accepted handoff and overdue/unowned queue rates; coordination hours per accepted home net of review, assurance and shifted effort; repeat work and elapsed wait by cause. Supports BG-010, BG-011 and BG-012. |
| Portfolio investment, performance and scale decisions. The executive question is whether retrofit produces safe, resident-accepted outcomes within real capital, cash, covenant, quality and capacity limits; estimates in the case study are not a validated investment case. | Reconcile stock trajectory, approved cohorts, accepted outcomes, grant states, programme and technology costs, cash exposure, risks and resident outcomes; compare against an agreed baseline; decide whether to pause, change or release the next investment tranche. Asset and Finance prepare the decision; the Board or delegated authority approves the envelope and scale. | Generate traceable summaries and scenario packs from controlled data after the underlying records are validated. Forecast assumptions, risk appetite, investment choice, tolerances and scale decisions remain human-owned. | Homes reaching intended outcomes and accepted handover; quality-adjusted cost per home; grant and cash reconciled by state; peak cash/liquidity/covenant headroom; resident outcomes and guardrails; attributable value versus the non-agent alternative. Supports BG-001 through BG-009 and BG-012. |

This portfolio makes the business-value chain explicit: reliable evidence and
fair selection feed competent, resident-ready designs; committed capacity and
authorised funding enable work; independently accepted quality supports
handover and eligible claims; and the shared workflow reduces avoidable delay
without relaxing safety, resident choice or financial control. These links are
testable hypotheses, not guaranteed causal benefits.

Measure value at two levels. Comparison 1 tests the end-to-end operating model
with existing teams and agents against a matched locality without agents.
Comparison 2 tests each proposed agent task against the same workflow without
that agent, counting review, assurance, recording and shifted effort. Report
resident and safety guardrails alongside accepted outcomes; starts, agent
activity and unreviewed hours-saved estimates are not benefits. The owner-
directed 20% cycle-time and 25% coordination-effort figures remain proposed
targets, not ratified forecasts, while OD-18 remains open. Scale a capability
only when the relevant workflow has a valid baseline, a named human owner,
measured incremental value and no agreed critical-control failure.

## Business Requirements

### Requirement Identifier Scheme

Every requirement row carries one canonical identifier, its legacy alias, the
business goals it supports and one or more acceptance criteria. Numbering is
sequential in creation order within each family. Identifiers added in later
amendments (FR-045 to FR-048) sit beside their related requirements and are not
renumbered after insertion, deletion or reordering.

| Prefix | Family | Use in this BRD | Count |
| --- | --- | --- | --- |
| BG | Business goal | Outcome in Business Objectives and Success Metrics; legacy alias OBJ-## | 12 |
| FR | Functional requirement | Business capability or control the programme must provide | 48 |
| AC | Acceptance criterion | Testable condition in the Acceptance criteria column of each requirement row | 90 |
| NFR | Non-functional requirement | Quality attribute classified by ISO/IEC 25010 category | 9 |
| CON | Constraint | Imposed boundary from legislation, regulation, funding, case study or owner-directed exercise delivery | 7 |
| RULE | Business rule | Standing policy or authority rule that outlives the solution; replaces the canonical BR prefix to avoid a clash with legacy BR-### aliases | 24 |
| OD | Open decision | Unresolved company decision; not a requirement | 43 |

Requirement rows remain grouped by business domain below, so a domain table
can hold FR, RULE and NFR rows together. The prefix states the type.
Requirements Traceability lists goal alignment, FR-to-AC and FR-to-BG
coverage, business-rule enforcement and the legacy map.

### Imposed Constraints

Constraints bound the programme. They are not requirements the programme
chooses, and no programme role can waive them. Each constraint was checked
against the local snapshot named in its source on 26 September 2026, not
against the official source online.

CON-007 is the later owner-directed exercise boundary, not legislation or
company policy. It requires the owner's new decision to change; it does not
authorize spending or supersede legal, resident or professional controls.

| ID | Constraint | Imposing source and date | Category | Affected boundary | Non-negotiable condition | Exception authority | Affected requirements |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CON-001 | Awaab's Law Phase 1 duties for emergency hazards and significant damp and mould hazards apply to social homes regardless of retrofit status. | Hazards in Social Housing (Prescribed Requirements) (England) Regulations 2025, SI 2025/1042, regulation 1(2), in force 27 October 2025; duties in regulations 5 to 14 ([local snapshot](../reference/regulatory/social-housing-regulation/awaabs-law-hazards-in-social-housing-regulations-2025.md), converted 2026-09-19). The original case study treats Awaab's Law timescales as hard constraints. | Legislation | Hazard response, clocks and resident updates for every home in the programme | No retrofit hold, platform outage, AI output or contractor arrangement may delay, pause, reset or close a hazard duty. | None within the programme; Legal interprets applicability. Phase 2 (guidance date 30 November 2026) must be verified before activation. | FR-002, FR-003, RULE-003, FR-004, NFR-004 |
| CON-002 | The association must hold accurate, evidenced, property-level stock condition data and consider tenant safety in designing and delivering landlord services. | Regulator of Social Housing, Safety and Quality Standard, effective 1 April 2024, required outcomes 1.1.1, 2.1.1, 2.2.1 and 2.2.3 ([local snapshot](../reference/regulatory/social-housing-regulation/social-housing-safety-and-quality-standard-2024.md), converted 2026-09-19) | Regulatory standard | Property records, safety evidence and service design used by the programme | Programme data and automation may not reduce the accuracy or evidence base of stock records or bypass consideration of tenant safety. | None; the Regulator of Social Housing sets the standard. | FR-001, FR-005, FR-006, RULE-001, RULE-015 |
| CON-003 | Personal-data processing by the programme and any agent needs a lawful basis, a special-category condition where relevant, transparent information and data-subject-rights handling, a data protection impact assessment where processing is likely to result in high risk, and safeguards if any significant decision would otherwise be based solely on automated processing. | UK GDPR Articles 5, 6, 9, 12 to 18, 20, 21, 22A to 22C, 25, 28, 30, 32 to 35 and 44 to 46 ([local snapshot](../reference/regulatory/data-protection/uk-gdpr-current-text.md), converted 2026-09-19) and the Data Protection Act 2018 ([local snapshot](../reference/regulatory/data-protection/data-protection-act-2018.md)). Article 12(1) requires concise, transparent, intelligible and easily accessible information in clear and plain language; Articles 13(2)(f), 14(2)(g) and 15(1)(h) require meaningful information about the logic involved where Article 22C safeguards apply; Article 22A defines solely automated significant decisions by the absence of meaningful human involvement; Article 22C(2) lists information, representations, human intervention and contest safeguards. The regulatory register rates automated-decision rules as High change likelihood in [Regulatory Context Reference Documents](../reference/regulatory/README.md), retrieved 2026-09-19. | Legislation | Resident, vulnerability, health and safeguarding data used in prioritisation, coordination and evaluation | No live use of personal data by an agent before the gates in RULE-022 pass, and no design may rely on token human review to avoid the solely automated threshold. | None; the Data Protection Officer advises and the association remains accountable as controller. The DPO checks the official source for amendments and commencement before each release. | RULE-022, NFR-001, NFR-003, FR-037, FR-034, FR-042, FR-043, FR-044 |
| CON-004 | Recovery of retrofit costs from leaseholders is limited by the lease and by statutory consultation and charge limits. | Service Charges (Consultation Requirements) (England) Regulations 2003, SI 2003/1987, regulations 4 and 6 (consultation above GBP 250 per leaseholder for qualifying works, or GBP 100 a year under a qualifying long-term agreement); Housing Act 1985, Schedule 6, paragraphs 16B and 16C (right to buy charge limits for five years). Cited through the [Housing Association Primer](../reference/research/sector/housing-association-primer.md#right-to-buy-and-preserved-right-to-buy-leasehold); not held in the local regulatory corpus. | Legislation | Communal works, framework and call-off contracts, and homes held by shared owners and leaseholders | No communal works or long-term agreement proceeds before Legal records the consultation status. | None; Legal determines applicability and must validate the legislative source before live use. | FR-015, FR-022, FR-047, RULE-023 |
| CON-005 | Any WH:SHF Wave 3 award is subject to the scheme's eligibility, route and spend conditions. | WH:SHF technical annex, January 2025: in scope (EPC D or below) does not by itself mean eligible (Page 3, footnote 1); formula allocations to the Greater Manchester (5.7%) and West Midlands (7.8%) combined authorities (Page 5, Table 3) ([local snapshot](../reference/regulatory/retrofit-standards-and-funding/warm-homes-social-housing-fund-technical-annex-2025.md), converted 2026-09-19). Spend by 31 March 2028 is recorded by the addendum and supporting research, not verified against a grant agreement. | Funding condition | Funding route, eligibility, match funding and claim evidence for grant-funded homes | Applies once an award is evidenced; no allocation to Zava North Homes is evidenced. | The grant authority only. | FR-023, FR-024, FR-026, FR-027, RULE-009, RULE-010 |
| CON-006 | Residents control consent, the asset director approves investment and Finance submits grant applications. | [Original Case Study 48](../case_study_48_original.md), Transformation Objective and Agentic Architecture Brief | Organisational (case-study fact) | Resident decisions, investment approval and grant submission | No agent or programme role may take these decisions for their owners. | Changes only through the association's scheme of delegation. | FR-011, FR-013, FR-014, FR-045, FR-046, RULE-010, RULE-011 |
| CON-007 | Every subsequent accepted application exercise build uses real AI, real SQL state and an actual Azure deployment on the continuing generated stock/programme lineage. | Owner direction 2026-10-11, [addendum](../case_study_48_addendum.md#subsequent-application-exercise-builds-2026-10-11) | Exercise delivery (owner decision) | Delivered AMA prototypes/PoCs/MVPs and updates; not documentation/unit/CI checks | At least one permitted real model task, actual SQL durability and Azure workflow evidence under AC-086; local/mock-only delivery cannot pass. No premium topology or production approval inferred. | New explicit exercise-owner decision only; no waiver by an implementer or model | FR-036, FR-044, NFR-002, NFR-004, RULE-018, RULE-019, RULE-020; AC-086 |

### Non-Functional Requirement Categories

| ISO/IEC 25010 category | Requirements | Coverage note |
| --- | --- | --- |
| Functional suitability | FR rows | Expressed through functional requirements and their acceptance criteria |
| Performance efficiency | None yet | Volumes, response times and capacity need company data from readiness (OD-03, OD-09, OD-25) |
| Compatibility | NFR-005 | Interfaces to authoritative systems |
| Interaction capability (usability) | NFR-008, NFR-009 | Accessibility, fair access, non-digital alternatives and plain-language explanation comprehension |
| Reliability | NFR-004 | Safe operation during model, integration or platform failure |
| Security | NFR-001, NFR-002, NFR-003 | Minimum necessary access, immutable versions and role-based access |
| Maintainability | NFR-007 | Versioned, evaluated and reversible change |
| Portability (flexibility) | NFR-006 | Exportable evidence independent of an AI supplier |

### Safety and Regulatory Control

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | BR-001 | The programme shall block controlled property progression when mandatory safety evidence is missing, stale, contradictory or identifies an unresolved hazard. | BG-003, BG-004 | Residents, safety, repairs, retrofit | AC-001: 100% of test cases with an evidence exception are blocked from design approval, works instruction, installation, handover and closure. | Must |
| RULE-001 | BR-002 | A safety hold shall be released only through a recorded decision by the named accountable safety role, informed by competent specialists and coordinated with the Retrofit Coordinator. | BG-003 | Safety, competent specialists, retrofit | AC-002: The release identifies evidence, decision-maker, rationale, controls, date and review date. No agent or contractor can release the hold. | Must |
| FR-002 | BR-003 | Emergency action, resident protection and statutory hazard response shall continue when normal retrofit progression is held. | BG-003, BG-004 | Residents, repairs, safety | AC-003: A safety hold cannot suppress or reset an emergency or hazard-response workflow or its timer. | Must |
| RULE-002 | BR-004 | Applicable duties, guidance versions and programme control rules shall be dated and reviewable. | BG-004 | Compliance, legal, programme | AC-004: Each controlled rule identifies its source, effective date, owner and review date. | Must |
| FR-003 | BR-062 | Every retrofit channel, including surveys, assessor, coordinator, contractor and liaison visits, resident contact and free-text notes, shall capture any possible hazard with its source, reporter, channel and awareness timestamp and refer it to the existing hazard and repairs service. | BG-003, BG-004, BG-010 | Residents, repairs, safety, retrofit, contractors, housing, legal | AC-005: Survey, visit and contact forms cannot be submitted without answering a hazard question. Each referral stores the awareness and referral timestamps, which cannot be edited, and the gap between them is reported. Unaccepted referrals escalate within limits set by the repairs and safety owners. Contractor and liaison scripts include a proposed same-visit reporting duty, reflecting the advice to review contractor agreements (Awaab's Law Phase 1 guidance, sections 3 and 7.5, converted 2026-09-19). FR-001 holds apply to the linked retrofit record. | Must |
| RULE-003 | BR-062 | The existing hazard and repairs service shall own hazard categorisation, clocks, investigation, resident summaries and closure; retrofit tooling may only create or link a hazard case. | BG-003, BG-004, BG-010 | Residents, repairs, safety, retrofit, contractors, housing, legal | AC-006: Retrofit tooling can create or link a hazard case but cannot categorise, pause, reset or close it. The handoff completes only under FR-018. | Must |
| FR-004 | BR-063 | Any automated hazard-signal scan of retrofit, repairs, complaint or contractor free text shall only raise possible hazards for human triage. | BG-003, BG-004, BG-012 | Repairs triage, safety, legal, DPO, digital | AC-007: Each flag cites its source text. A human triager records every referral or non-referral decision with a reason, and threshold changes cannot remove human review of a hit. A hit suggesting earlier landlord awareness than recorded goes to Legal and Safety without changing any live clock. The scan is disabled if any output delays, suppresses or closes a clock, or if hits exceed the triage capacity Repairs has approved. RULE-022 gates apply before live use. | Must |

### Property Lifecycle and Technical Approval

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| FR-005 | BR-005 | The programme shall maintain a property-level lifecycle record with distinct assessment, design, resident, funding, works, quality, handover, monitoring, hold and reopened-defect states, linked to applicable building-level controls. | BG-002, BG-006 | Retrofit, residents, finance, safety | AC-008: A state transition cannot imply completion of an unrelated approval gate or bypass a relevant building-level hold. | Must |
| FR-006 | BR-006 | Every controlled state transition shall record the property, prior and new state, timestamp, initiator, authority, reason, evidence version and open exceptions. | BG-006, BG-010 | All control owners | AC-009: The full transition history is retrievable and cannot be overwritten. | Must |
| FR-007 | BR-007 | No property shall be released to install until a version-controlled property-specific design is approved by the appropriate competent professional and formally released by the Retrofit Coordinator. | BG-003, BG-006 | Retrofit Coordinator, designers, installers | AC-010: Scheduling remains blocked until all required approvals reference the current design version. | Must |
| FR-008 | BR-008 | A material change to property condition, scope, design, resident circumstances, cost, contractor or funding conditions shall invalidate affected downstream approvals. | BG-003, BG-005, BG-006 | All control owners | AC-011: Reused evidence, such as an assessment, EPC or survey reference, never transfers an approval, consent or review to a changed scope; each affected approval is re-reviewed or explicitly confirmed unaffected by its owner. Unless its owner records that confirmation, the property returns to the earliest affected approval gate and cannot progress until reapproved. | Must |
| FR-009 | BR-009 | Outputs shall be labelled as recommendations, drafts, flags or approved decisions and shall not misrepresent automated output as human approval. | BG-003, BG-006 | All users | AC-012: Audit tests find no recommendation, draft or flag displayed as an approval. Field-level tests show agent-proposed values as agent-proposed and unconfirmed until a named owner confirms or rejects them, with the source and confidence category visible. | Must |
| RULE-004 | BR-010 | Contractors may submit completion evidence but shall not approve technical compliance, final quality, payment, grant eligibility or closure. | BG-006, BG-007 | Contractors, quality, finance | AC-013: Segregation-of-duties tests prevent contractor self-approval. | Must |
| FR-010 | BR-068 | The Retrofit Assessor's survey sign-off and the Retrofit Coordinator's review and risk-path decision shall be recorded as two separate professional approvals. | BG-003, BG-006, BG-011 | Retrofit Assessor, Retrofit Coordinator, programme | AC-014: One approval cannot satisfy both gates, and the coordinator cannot pass a survey the assessor has not signed. Any case where one person holds both roles is visible and needs an authorised exception. Pre-filled content contains only facts with a named source. A competent Retrofit Coordinator confirms the applicable PAS 2035 edition and role duties before release. | Must |

### Resident Consent, Accessibility and Challenge

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| FR-011 | BR-011 | Resident records shall distinguish information provision, survey access, appointment agreement, agreement to each proposed measure and any separate personal-data consent. | BG-005 | Residents, engagement, retrofit, data protection | AC-015: Consultation, silence, appointment access or survey access cannot be recorded as consent to installation. | Must |
| FR-012 | BR-012 | Residents shall receive property-specific information on proposed measures, benefits, uncertainty, disruption, access, material risks, data use, alternatives, aftercare and complaint routes in an accessible format. | BG-005, BG-009 | Residents, engagement | AC-016: The record identifies the content version, language, format, channel and date supplied. | Must |
| FR-013 | BR-013 | Residents shall be able to agree, decline, defer, request more information or withdraw agreement for each proposed measure through digital and non-digital channels. | BG-005 | Residents, engagement, retrofit | AC-017: Each decision and change is timestamped, confirmed to the resident and propagated to downstream scheduling. | Must |
| FR-014 | BR-014 | Disputed or withdrawn consent, unresolved adjustments, safeguarding concerns or a resident-requested pause shall place affected non-urgent activity on hold. | BG-005 | Residents, engagement, housing, contractors | AC-018: Work cannot start or restart until an authorised human records the decision and the resident is notified. | Must |
| RULE-005 | BR-015 | Residents shall have access to an independent human review and the association's formal complaints route without detriment to unrelated repairs, tenancy services or future engagement. | BG-005, BG-009 | Residents, complaints, housing | AC-019: The reviewer can correct data, vary conditions, pause or reschedule work, overturn recommendations and explain escalation routes. Complaints, challenges and review requests are tagged where an AI output, draft, route, score or explanation was involved, and the tag is reportable without reducing access to the ordinary complaints route. | Must |
| NFR-001 | BR-016 | Sensitive resident information shall be restricted to the minimum operational adjustment needed by each recipient. | BG-005 | Residents, data protection, contractors | AC-020: Contractors cannot access unrestricted health, safeguarding or vulnerability histories. | Must |
| FR-015 | BR-061 | Each home and each affected household shall have a recorded tenure and lease-interest status that sets its decision route before any measure is offered. | BG-005, BG-009 | Tenants, shared owners, leaseholders, legal, home ownership, engagement, finance | AC-021: Status is tenant, shared owner, right to buy or preserved right to buy leaseholder, mixed block or unverified. Unverified homes cannot be offered measures until the owning team confirms the status. Owner information states who decides, who pays and whether landlord permission is needed. Communal works are held until Legal confirms whether leaseholder consultation applies (RULE-023). Agreement from one household is never applied to another. No automated capability interprets a lease. | Must |
| FR-045 | None | Where an advocate, carer, family member, interpreter or other representative acts for a resident, the programme shall record the task-limited authority, its source, scope and review date, and the resident's own wishes. | BG-005, BG-009, BG-010 | Residents, representatives, engagement, housing, DPO | AC-087: Each record states who may receive information, communicate, attend or act for which tasks, the evidence and date of the authority and an expiry or review date. Expired, unclear or disputed authority stops disclosure and consent actions until a human confirms it with the resident through an accessible route. A representative's agreement is not the resident's consent to works unless the recorded authority covers that decision (FR-013). Personal data about representatives follows the minimisation, retention and access rules in RULE-022, CON-003 and NFR-003. Tests cover expired authority, interpreter-only authority, several representatives and a changed safe contact. | Should |
| FR-046 | None | Appointments, access visits and disruption arrangements shall be confirmed commitments within confirmed capacity, with recorded household constraints, options offered, deferral or pause and a named owner for each update. | BG-005, BG-006, BG-009 | Residents, engagement, contractors, programme, housing | AC-088: An offered slot, proposed visit bundle or contractor availability is an offer, not a commitment, until the resident or authorised representative (FR-045) and an authorised staff member confirm it and the contractor confirms capacity (FR-019). Household constraints such as care, noise, work patterns and outages are visible to scheduling and consistent with FR-012. Bundling visits needs resident agreement and competence checks and never delays urgent safety response (FR-002). Provider no-shows and contractor changes are recorded separately and not attributed to the resident (RULE-006). A non-digital confirmation route exists. Preference breaches and abortive visits are counted by cause and owner and reviewed at each programme control meeting, with the reporting threshold ratified by the programme owner. | Should |

### Frontline Exception Handoffs

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| FR-016 | BR-017 | Automated progression shall stop for safety, damp and mould, safeguarding, disputed consent, vulnerability, failed access, complaint, quality, data-conflict or privacy exceptions, including unclassifiable or insufficient-evidence cases. | BG-003, BG-004, BG-005, BG-010 | Residents, housing, repairs, safety, retrofit | AC-022: Each exception creates a traceable human handoff and prevents inappropriate progression; missing classification cannot permit progression or suppress urgent response. | Must |
| FR-017 | BR-018 | Each handoff shall contain the resident's description, desired outcome, risk, urgency, applicable deadline, consent status, necessary adjustments, prior activity, evidence, receiving team and required decision. | BG-010 | Receiving teams, residents | AC-023: The receiving team can act without asking the resident to repeat information already held, subject to access controls. Shared information is limited to the stated purpose and receiving role, and a changed safe-contact or consent status stops reuse until a human confirms it. | Must |
| FR-018 | BR-019 | A handoff shall count as complete only when a named human accepts ownership, acknowledges urgency, confirms the next resident update and records the resulting action, escalation or justified closure. | BG-010 | All receiving teams | AC-024: Referral creation or message delivery alone cannot close the handoff. Unowned and overdue cases are reported. | Must |
| FR-047 | None | A complaint response, work package completion, handover or financial closure shall not close an outstanding remedy, defect, household-level dispute or charge query. | BG-005, BG-006, BG-009 | Residents, complaints, home ownership, Legal, Finance, programme | AC-089: The record keeps complaint response and remedy completion as separate statuses with named owners and dates. Building or package progress cannot erase an open household-level complaint, defect, lease-responsibility question or leaseholder charge query, and an affected approval is re-reviewed when scope changes. Leasehold answers come only from Legal-reviewed positions and approved evidence; missing lease evidence is recorded as unknown and holds the affected decision (FR-015, CON-004). Open remedies are reported by age band and owner, with age bands and escalation points set by Housing and Complaints owners. The complaints route remains available without detriment (RULE-005). | Must |
| RULE-006 | BR-020 | Failed access shall not be treated automatically as resident refusal or non-cooperation. A configurable threshold shall have a provisional default of five. Only a confirmed appointment with a verified resident no-access outcome counts; provider or contractor no-shows, cancellations and reschedules shall be recorded separately and shall not count. Count eligible events while the same case is active and reset the counter only when a human closes the case; retain the event history and threshold/configuration version for audit. When the count is greater than the configured threshold, the case shall be escalated for human investigation and corrective action. | BG-005, BG-009, BG-011 | Residents, housing, contractors, repairs | AC-025: With the provisional default of five, the sixth eligible event on an active case triggers review by a named human owner. The owner checks appointment confirmation, notice, attendance, accessibility and adjustment arrangements, contact history and relevant resident circumstances before classifying the cause; records the investigation, corrective action and next resident update; and records any case closure that resets the active counter without deleting the event history or configuration version. The counter alone does not establish refusal or non-cooperation, impose a consequence, or delay an urgent hazard response. | Must |

### Supplier Capacity and Contract Control

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| RULE-007 | BR-021 | Work shall not be scheduled or communicated as confirmed until supplier capacity is contractually committed for the work package, location, volume and period. | BG-002, BG-006 | Procurement, retrofit, contractors, residents | AC-026: Forecast capacity or supplier self-declaration alone cannot unlock scheduling. | Must |
| FR-019 | BR-022 | Capacity evidence shall cover competent resources, subcontractors, mobilisation, plant, materials, supervision, quality assurance, competing commitments and contingency arrangements by role, work package, geography and period. | BG-002, BG-006 | Procurement, contractors, programme | AC-027: The contract manager validates supplier allocations; Programme validates assessor, designer, coordinator, liaison, inspection and client-side capacity against the same trajectory. | Must |
| FR-020 | BR-023 | Material loss of committed capacity shall trigger revalidation, resident communication, contractual escalation and contingency assessment before rescheduling. | BG-002, BG-009 | Procurement, retrofit, residents | AC-028: A reduced commitment cannot remain available for new scheduling. | Must |
| FR-021 | BR-024 | Supplier performance and further tranche allocation shall reflect quality-adjusted accepted outcomes, physical and evidence acceptance, defects, missed appointments, complaints, capacity and recovery actions. | BG-002, BG-006, BG-009 | Procurement, contractors, programme | AC-029: Scorecards reconcile forecast and delivered output by supplier, subcontractor and work package; allocation decisions record the quality and resident evidence rather than starts alone. | Must |
| RULE-008 | BR-065 | Only a named, authorised contract manager shall issue a contractor instruction, variation, scope change, capacity commitment, suspension or reallocation between suppliers. System drafts are not instructions. | BG-006, BG-008, BG-010 | Procurement, contract managers, contractors, legal, finance, audit | AC-030: Tests stop any tool from sending contractor-facing messages that change scope, cost, time or allocation without contract-manager approval, across email, phone scripts and portals. Drafts carry a "not an instruction" marker. Each approved action records the approver, delegated authority, contract reference, version and time. A reallocation cannot be released until the contract manager records a modification check and Legal has reviewed it where required. | Must |
| FR-022 | BR-066 | Before a retrofit contract, framework or call-off is let or renewed, it shall include a channel-neutral data schedule. | BG-002, BG-006, BG-008, BG-011 | Procurement, contractors, quality, finance | AC-031: The schedule covers a standard work order, appointment outcome codes, contractor-owned scheduling with service levels, same-day hazard and safeguarding reporting under FR-003, RULE-003, and a per-measure evidence schedule linked to FR-028. It is deliverable by email or spreadsheet as well as an interface; no scheduling API is assumed. The award gate cannot pass without the schedule. Contractor data feeds FR-021 scorecards and does not replace RULE-004 approvals. | Must |
| RULE-023 | BR-066 | Before a retrofit contract, framework or call-off is let or renewed, Legal shall record whether leaseholder consultation, including for qualifying long-term agreements, applies and is complete. | BG-002, BG-006, BG-008, BG-011 | Legal, procurement, home ownership, leaseholders | AC-073: The award gate cannot pass without a recorded consultation status, including "not required", made by a named Legal adviser. | Must |

### Grant and Financial Control

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| FR-023 | BR-025 | Grant reporting shall maintain mutually exclusive states for opportunity, awarded grant, claimable grant and cash received. | BG-007 | Finance, board, programme | AC-032: Reports cannot aggregate the four states as a single grant-captured value. | Must |
| RULE-009 | BR-026 | The case-study GBP 40 million shall remain labelled as an unverified grant opportunity until formal evidence supports a state change. | BG-007 | Finance, board | AC-033: No dashboard presents the amount as secured funding, income, approved budget, claimable value or cash. | Must |
| FR-024 | BR-027 | Every grant state transition shall record dated source evidence, scheme, amount, property or work package, named approver and immutable history. | BG-007 | Finance, audit, programme | AC-034: Finance can reconcile opening award, claims, approvals, receipts, adjustments and closing balance. | Must |
| RULE-010 | BR-028 | Automated capabilities shall not submit a bid, approve match funding, certify a claim or record cash receipt without designated human financial authority. | BG-007, BG-008 | Finance, board | AC-035: Role and authority tests block unauthorised actions. | Must |
| FR-025 | BR-029 | The business case shall separately model the retrofit investment and incremental technology option, eligible delivery, grant conversion, whole-life costs, match funding, monthly cash exposure and downside scenarios. | BG-007, BG-008, BG-012 | Finance, board, assets, digital | AC-036: Finance reconciles existing, rephased, displaced and incremental spend; current-plan, incremental, accelerated and at-risk grant; technology measurement, parallel-running and assurance costs; cost inclusions; peak cash, liquidity, covenant and security headroom. Neither grant nor cost items are double counted. | Must |
| RULE-011 | BR-030 | Delivery acceleration shall require a board-approved investment envelope integrated with the long-term asset plan, liquidity forecast and covenant model. | BG-001, BG-002, BG-008 | Board, executive, finance | AC-037: Acceleration cannot exceed the approved annual plan until the gate is satisfied. | Must |
| RULE-012 | BR-031 | Board-defined downside tolerances shall pause further acceleration when safety, resident, quality, capital, grant or capacity exposure exceeds approved limits. | BG-003, BG-005, BG-006, BG-008 | Board, executive, programme | AC-038: A tolerance breach creates an escalation and blocks new acceleration; affected live activity is contained under the relevant hold. Restart records remediation and approval by the control owners and Board where its envelope is affected. | Must |
| FR-026 | BR-059 | Eligibility for each home, scheme and funding route shall be a deterministic pass, fail or unknown result from a versioned rule set approved by Finance and traced to a named section of the scheme guidance. | BG-007, BG-012 | Finance, assets, data owners, audit, legal | AC-039: Each result records rule version, guidance section, inputs and their sources, tenure and a reason code; the same inputs and version always give the same result. Rule changes create a new version with approver and effective date, and earlier results are kept. Missing tenure, EPC or lease data returns unknown and opens an investigation under NFR-008. Only passed homes feed opportunity, award or claimable value; injected unknown and failed test homes show zero. Non-social conditions return unknown until the rule is verified against the national scheme guidance. | Must |
| FR-027 | BR-060 | Each scheme shall record an evidenced funding route, and each eligible home shall record a named co-funding source. | BG-007, BG-008, BG-012 | Finance, board, assets, leaseholders, shared owners | AC-040: Routes distinguish national competition from combined-authority integrated settlement. An unknown route blocks bid preparation and benefit claims. Each home shows grant, provider match from an approved budget line and any owner contribution. Owner contributions count only with a signed agreement. The business case shows the provider's additional spend next to any additional grant, and grant never offsets technology cost unless it is incremental and net of match (FR-025). | Must |

### Quality, Handover and Remediation

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| FR-028 | BR-032 | The programme shall link requirements, approved design, installation activity, inspection, test, result, approver, defect and final acceptance. | BG-006 | Retrofit, quality, contractors | AC-041: Each accepted measure has a complete, traceable evidence chain. | Must |
| FR-029 | BR-033 | A failed inspection, missing evidence, complaint, safety concern, sensor exception or confirmed defect shall reopen the property at the control point where failure occurred. | BG-003, BG-006, BG-009 | Residents, retrofit, safety, contractors | AC-042: The original history is preserved and a linked defect record is created. | Must |
| FR-030 | BR-034 | Reopened defects shall record severity, resident impact, containment, owner, target date, remediation, reinspection and potential effect on related homes or claims. | BG-003, BG-006, BG-007 | Quality, contractors, finance, residents | AC-043: Material defects block final closure and applicable payment or claim recommendations. Repeated or potentially systemic defects trigger competent review of the related building, archetype, product or installer cohort and holds on affected further work until disposition. | Must |
| RULE-013 | BR-035 | Defect closure shall require remediation evidence and competent re-verification independent of the original installation decision where risk warrants it. | BG-006 | Quality, competent specialists, contractors | AC-044: Contractor self-certification alone cannot close a controlled defect. | Must |
| FR-031 | BR-036 | Resident handover shall provide accessible operating guidance, warranties, aftercare contacts and confirmation of receipt. | BG-005, BG-009 | Residents, retrofit, contractors | AC-045: Closure is blocked until required handover evidence is accepted. | Must |
| FR-032 | BR-037 | The pilot and each subsequent tranche shall have a lawful, proportionate in-use evaluation plan covering energy, comfort, affordability, damp, mould, ventilation, complaints and unintended outcomes. | BG-003, BG-009 | Residents, assets, safety, data protection | AC-046: Before release, owners approve follow-up methods and timing; reports disclose pending seasonal evidence and adverse outcomes. Material concerns trigger human review and remediation; sensors are not mandatory and a normal reading cannot override a resident report. | Must |
| FR-048 | None | Where a home has consented, lawfully recorded in-use monitoring (for example humidity and temperature sensors), the programme shall capture each observation with its source, device-to-property mapping, calibration status and time as a retained record, separate from any derived analysis or decision. | BG-003, BG-009 | Assets, safety, residents, DPO, data owners | AC-090: Raw observations are retained unaltered with provenance and cannot be overwritten; rejected, duplicate, out-of-order or unmapped data raises an owned data-quality exception and never silently changes a property record. Derived signals are versioned, reproducible and labelled by data sufficiency, and a signal can only create a human condition-review task. A signal never diagnoses a hazard, starts or back-dates a statutory clock, releases a hold, overrides a resident report or changes investment ranking directly. Missing, stale or invalid data shows as insufficient and never lowers a home's priority or service. Resident choice to decline is recorded, honoured and never penalised (RULE-014, FR-032). | Should |
| RULE-014 | BR-067 | Neither the absence of an AI flag nor the absence of a sensor alert shall count as evidence toward acceptance, closure, payment or claim, and sensor data shall inform a decision only after it passes validity rules. | BG-003, BG-006, BG-007, BG-009 | Quality authority, finance, safety, residents, DPO, data owners | AC-047: A pack with no flags still needs human acceptance against a positive per-measure evidence checklist. Validity rules cover device-to-UPRN mapping, in-date calibration, gaps and clock drift, heating-season coverage and pre-retrofit baseline status; invalid or missing data shows as "insufficient", never "normal". Reports disclose homes with no baseline. Sensor use needs an approved lawful basis and DPIA, and residents can decline. Data owners set the tolerances. | Must |

### Data, Audit and Reporting

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| RULE-015 | BR-038 | The association shall define an authoritative source and accountable owner for each property, safety, resident, contract, finance and quality data domain. | BG-003, BG-006, BG-007 | Data owners, all users | AC-048: Conflicting records prevent controlled progression until reconciled by an authorised owner. | Must |
| NFR-002 | BR-039 | Controlled assessments, designs, consents, instructions, evidence packs, handovers and decisions shall have immutable version identifiers and retained prior versions. | BG-005, BG-006 | All control owners | AC-049: Approved records are superseded rather than overwritten. | Must |
| NFR-003 | BR-040 | Access to personal, vulnerability, safety, commercial and financial information shall follow role, purpose and minimum-necessary principles. | BG-003, BG-005, BG-008 | Data protection, security, all users | AC-050: Access tests demonstrate separation by role and record all disclosures. | Must |
| FR-033 | BR-041 | Programme reporting shall distinguish starts, accepted handovers and intended energy outcomes, and show holds, resident pauses, handoffs, capacity, defects, grant states, financial tolerances and attributable technology benefit. | All | Board, executive, programme, residents | AC-051: Reports expose overdue, unowned, blocked and reopened work, with cycle time, effort and quality-adjusted cost denominators; no incomplete work is presented as accepted. | Must |
| FR-034 | BR-042 | Decision explanations shall show the data, rules, source-based confidence category, exceptions and human authority relevant to each prioritisation, eligibility, hold or agent-assisted output. | BG-005, BG-010 | Residents, staff, audit | AC-052: 100% of prioritisation, eligibility, hold and agent-assisted outputs carry an explanation record before they are used. Each record states whether the output is a recommendation, draft, flag or approved decision and gives a correction or challenge route.<br>AC-080: Explanation records have audience-specific fields: resident records include a plain-language reason, main factors, data used, what is unknown, who decided and how to correct data or challenge; staff records include sources, rule and model version, source-based confidence category and open exceptions; audit records link to the full reconstruction required by FR-040.<br>AC-081: Before live resident contact, Resident Engagement tests resident explanations with a representative resident group, including accessible and non-digital formats linked to NFR-008. The Resident Engagement lead sets and records comprehension and accessibility thresholds before live use, and deficiencies block the affected explanation pattern. | Must |
| FR-042 | None | The programme shall use a Board-approved or delegated Asset Director-approved plain-language prioritisation policy with versioned scoring weights, published resident-facing rationale and per-home reason codes for inclusion, deferral or exclusion. | BG-001, BG-005, BG-007, BG-009, BG-012 | Residents, Board, assets, finance, data owners | AC-082: Before cohort use, the approved policy shows the authority, effective date, scoring weights, rule versions, source data and review date. Each home receives reason codes equivalent to FR-026 for inclusion, deferral or exclusion. Residents can request a "why not yet" explanation through digital and non-digital channels, with an indicative timescale where one exists. The control supports Safety and Quality Standard 2.3.2 on setting and clearly communicating timescales for planned improvements ([local snapshot](../reference/regulatory/social-housing-regulation/social-housing-safety-and-quality-standard-2024.md), effective 1 April 2024, converted 2026-09-19). | Must |
| FR-043 | None | The programme shall maintain an AI capability register and provide a periodic AI assurance report to the Board covering each agent capability used or proposed for use. | BG-003, BG-005, BG-006, BG-008, BG-009, BG-012 | Board, DPO, residents, digital, assurance, control owners | AC-083: The register records purpose, data used, lawful-basis reference, owner, authority level, current model and configuration version, evaluation results, gate status and known limitations for each capability. Board assurance reports include incidents, overrides, unsupported-claim rate, outcome breakdowns across resident groups and gate status. Cadence is recorded as an owner decision before live pilot. A resident-facing summary may be published as proposed good practice only after Board and DPO approval. | Must |
| FR-044 | None | Every agent output record shall preserve output provenance, human review and decision disposition for reconstruction, export and supplier-independent evidence retention. | BG-003, BG-005, BG-006, BG-010, BG-012 | Residents, staff, audit, digital, suppliers, control owners | AC-084: Each agent output stores model and configuration version, prompt or template version, source record references, source-based confidence category or "unknown", timestamp, reviewing human, and accept, edit or reject decision with reason. Records are immutable under NFR-002, exportable under NFR-006 and reconstructable through FR-040. | Must |

### Proportionate Solution and Professional Authority

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| RULE-016 | BR-043 | Readiness shall establish binding delivery constraints and compare process redesign, existing platform configuration, conventional workflow integration and bounded AI before selecting a solution. | BG-002, BG-008, BG-011, BG-012 | Assets, programme, finance, digital, frontline teams | AC-053: Sponsor and Finance accept an appraisal with measured delay causes, comparable scope, whole-life cost, risks, retained staffing and reasons for the preferred option. No five-agent commitment is assumed. | Must |
| RULE-017 | BR-044 | The programme shall name competent assessors, designers, coordinators and evaluators and retain professional ownership of assessments and technical decisions. | BG-003, BG-006 | Competent specialists, programme, residents | AC-054: Each output records its professional owner, competence scope and evidence version. Generated factual inputs link to sources; missing observations require assessment, not AI completion. Capacity and current PAS and scheme rules are validated before release. | Must |
| FR-035 | BR-045 | Cohort selection and design release shall consider building-level dependencies, whole-dwelling needs, planned maintenance, condition, whole-life value and provisional funding and capacity. | BG-001, BG-002, BG-003, BG-008 | Assets, safety, technical roles, finance | AC-055: Each scheme records the bundling or sequencing decision and rationale; shared-system and higher-risk-building controls are identified and satisfied before affected works. Archetype reuse cannot bypass property-specific review or final funding and capacity confirmation. | Must |

### Automation Authority, Integration and Continuity

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| FR-036 | BR-046 | Deterministic workflow shall enforce mandatory gates and an explicit allow/deny authority matrix. | BG-003, BG-004, BG-005, BG-006, BG-007, BG-012 | All control owners, digital, audit | AC-056: Tests block AI diagnosis, statutory-duty determination, safety-hold release, professional approval, consent inference, investment or procurement commitment, contractor instruction, payment, bid or claim submission, and hazard, complaint or defect closure. Approval cannot be supplied by generated text.<br>AC-086: Each accepted application exercise build records its authorized Azure endpoint and source/image/revision/config versions, verified least-privilege workload identity, actual Azure SQL write/read and independent before/after restart state/audit evidence, plus at least one permitted real generative or Decision task with source/model/provider/usage/outcome, citations and Not reviewed authority. Failure/manual handling preserves case access and controls. Missing effective budget, authorization or service evidence is Blocked or Not run; templates, mocks or unrelated historical calls cannot pass. Retained generated-stock/programme lineage and separate quality/value gates remain explicit. | Must |
| RULE-018 | BR-046 | In the initial pilot, AI shall be restricted to sourced recommendations, drafts, reconciliation, routing to fixed categories and raise-only flags. Accepted application exercise builds require deployed real AI under CON-007, but invoking assistance per record is optional and manual case access never depends on model availability. | BG-003, BG-004, BG-005, BG-006, BG-007, BG-012 | All control owners, digital, audit | AC-057: A flag can only add work to a human queue and can never clear, accept or close an item. Routing sends messages only to staffed queues. Consequential resident contact requires human authorisation. | Must |
| NFR-004 | BR-047 | Service operation shall remain safe during model, integration or platform failure through monitored queues, a disable mechanism, tested manual fallback and controlled recovery. | BG-003, BG-004, BG-010, BG-012 | Digital, repairs, safety, housing, programme | AC-058: Owners approve response and recovery limits before live use. Outage tests preserve hazard response and statutory clocks, expose unowned work, block unverified controlled transitions and reconcile missed or duplicate actions before restart. | Must |
| NFR-005 | BR-048 | The solution shall connect authoritative systems through documented interfaces. | BG-005, BG-006, BG-008, BG-010, BG-012 | Digital, data owners, procurement, audit | AC-059: Owners accept identifier mapping, conflict handling and reconciliation for each interface. | Must |
| NFR-006 | BR-048 | The solution shall preserve exportable, versioned evidence independently of an AI supplier. | BG-005, BG-006, BG-008, BG-010, BG-012 | Digital, data owners, procurement, audit | AC-060: Export tests retain source, approval and supersession history. Contracts specify data access, retention, support and exit responsibilities. AI supplier terms require model documentation, advance notice of model or material behaviour changes, access to relevant evaluation results and output logs, and support for NFR-007 version evaluation. | Must |
| NFR-007 | BR-048 | Model, rule and configuration changes shall be versioned, evaluated before release and reversible. | BG-005, BG-006, BG-008, BG-010, BG-012 | Digital, data owners, procurement, audit | AC-061: Each model, rule and configuration change records its version and evaluation result and can be reversed. | Must |

### Evaluation, Release and Equitable Outcomes

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| RULE-019 | BR-049 | Before any Phase 0 pilot or comparison event capture and before shadow testing, the programme shall approve a frozen pilot protocol, the OD-36 DPIA and lawful measurement basis, and a benefits register with Comparison 1 for existing teams with agents versus a matched locality without agents, plus Comparison 2 for per-capability task-level evidence. Shadow testing also requires the shadow-mode entry evidence. | BG-002, BG-006, BG-009, BG-011, BG-012 | Programme, finance, residents, digital, assurance | AC-062: The protocol freezes and versions the event dictionary, accepted-handover definition, clock and pause rules, cohort eligibility, entry cut-off, denominators, matching variables, primary measures, minimum detectable effect, thresholds, unfinished-case handling, exclusions and analysis code version. Later changes create a new approved version. The approval record includes the OD-36 DPIA and lawful measurement-basis decision. Finance validates attribution and cashability separately from released staff capacity.<br>AC-074: Comparison 1 design uses a cohort frozen before resident contact, intention-to-treat analysis, concurrent matched comparison in another locality without agents, identical Phase 0 event capture in both localities, difference-in-differences against the instrumented pre-period, output per unit of committed competent capacity and shared-resource logs for staff or suppliers working across localities.<br>AC-075: Comparison 2 design uses paired shadow-mode comparison on the same cases and task-level allocation between agent-assisted and workflow-only handling where safe and lawful, with measures of review minutes, draft acceptance, error severity, overrides, missed critical exceptions, unsupported-claim rate, explanation fidelity and automation-bias indicators.<br>AC-076: Statistical reporting uses medians, 80th or 90th percentiles, censored time-to-event analysis, interval estimates where the minimum detectable effect exceeds BG-011 targets, and must-not-worsen safety, resident and quality tests.<br>AC-077: Effort measurement uses work-sampling, short time studies or short diary weeks in both arms, net of review and assurance, and includes effort shifted to residents, suppliers and housing officers plus the time spent recording.<br>AC-085: The protocol defines reviewer-sampled unsupported-claim rate, explanation fidelity checks and automation-bias indicators, including review time below an owner-set floor and near-total acceptance against owner thresholds. Any unsupported eligibility, consent, safety or evidence claim accepted by a reviewer undetected, or automation-bias indicators breaching owner thresholds, pauses the affected capability under RULE-024. | Must |
| RULE-020 | BR-050 | Each delivery phase, tranche and later authority expansion shall require an evidence-based release decision within an approved cost and risk envelope. | BG-002, BG-003, BG-005, BG-006, BG-008, BG-012 | Sponsor, Board, control owners, assurance | AC-063: Release records identify applicable requirements, acceptance evidence, unresolved issues and named approvers. Shadow mode cannot cause live actions. Safety or resident-rights breaches stop affected activity; failed value or quality gates prevent expansion. Restart and rollback are tested; prohibited AI decisions remain prohibited at scale. | Must |
| RULE-024 | None | A guardrail breach shall pause the affected home, work package, archetype or workstream regardless of throughput until restart is authorised under the OD-35 authority and RULE-020 release decision. | BG-003, BG-004, BG-005, BG-006 | Sponsor, control owners, assurance, residents, contractors | AC-078: The breach record identifies scope, owner, evidence, containment, resident impact, remediation and restart authority. Affected work cannot restart until the OD-35 authority and the relevant RULE-020 release decision accept remediation evidence; emergency and statutory hazard response continues outside the pause. | Must |
| NFR-008 | BR-051 | Prioritisation, resident journeys and outcome evaluation shall be tested for accessibility and unfair exclusion, with human review of missing data, support needs and incomplete appointments. | BG-001, BG-005, BG-009 | Residents, engagement, assets, housing, data protection | AC-064: Before live contact, representative digital and non-digital journeys are tested and deficiencies resolved. Reports show lawful, proportionate outcome breakdowns; neither missing sensors nor support needs silently deprioritise a home. Consent rates are not an optimisation target. | Must |
| FR-037 | BR-064 | Prioritisation shall not depend only on recorded vulnerability flags and shall include staffed officer-nomination and resident self-referral routes. | BG-003, BG-005, BG-009 | Residents, housing officers, engagement, assets, DPO | AC-065: Missing flags are recorded as "unknown", never "none". The original account of a nomination or self-referral is preserved with correctable identity, and each has a named human owner for review. A challenge or correction keeps competing evidence visible, never changes priority automatically and triggers re-review of dependent decisions. Each cohort run is reported with and without flags, and differences go to human review. Flag coverage is compared with prevalence benchmarks by tenure and scheme type. Self-referral works by phone, letter, in person, through trusted intermediaries and digitally; every referral and nomination is acknowledged, decided by a human and explained, with a challenge route (RULE-005, FR-034). No automated capability infers health status. Special category data is used only after DPO approval of the DPIA (RULE-022). Damp and mould hazards stay on the statutory route (FR-002). | Must |

### Regulatory Knowledge and User Service

| ID | Legacy ID | Requirement | Business goals | Impacted stakeholders | Acceptance criteria | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| FR-038 | BR-052 | The solution shall maintain a regulatory source register separate from the searchable document index. | BG-003, BG-004, BG-006, BG-007, BG-010, BG-012 | Legal, compliance, data protection, funding, digital, audit | AC-066: Each source records stable identifier, official URL, jurisdiction, authority type, publication, retrieval, effective, review and supersession dates, hash, completeness, applicability, change likelihood, cadence and accountable owner. Historical and current-use sources are distinguishable. | Must |
| FR-039 | BR-053 | Scheduled monitoring shall prefer official legislation data, publication metadata, feeds and alerts, using scraping only as a controlled fallback for discovery. | BG-003, BG-004, BG-007, BG-010, BG-012 | Digital, legal, compliance, funding | AC-067: Tests detect new, changed, withdrawn, incomplete and unreachable sources. Retrieval preserves the prior snapshot, provenance and error state. A detected or scraped change cannot overwrite an approved interpretation or live rule. | Must |
| RULE-021 | BR-054 | Every detected regulatory, guidance, funding or standards change shall enter a human-owned assessment and approval workflow before operational activation. | BG-003, BG-004, BG-006, BG-007, BG-010, BG-012 | Legal, compliance, DPO, competent roles, finance, digital | AC-068: The review identifies affected requirements, rules, decisions, communications, evidence templates, reports and user journeys. Approval records interpretation, owner, tests, effective date, notification, rollback and any temporary hold. | Must |
| FR-040 | BR-055 | Consequential decisions and external submissions shall be traceable to the approved source, interpretation and rule versions effective when the decision was made. | BG-003, BG-004, BG-005, BG-006, BG-007, BG-010 | Residents, employees, contractors, officials, audit | AC-069: An export reconstructs source provisions, evidence, model and configuration version, prompt or template version where applicable, recommendation, human decision, override, communication and correction history. Missing or conflicting authority blocks compliance claims and external certification. | Must |
| FR-041 | BR-056 | The service shall provide role-appropriate evidence views that reduce repeated entry and evidence chasing without exposing unnecessary personal or commercially sensitive information. | BG-005, BG-007, BG-009, BG-010, BG-011 | Employees, residents, contractors, officials, data protection | AC-070: Employees have named queues and one controlled evidence pack; residents have accessible explanations and correction or challenge routes; contractors receive authorised scope and minimum necessary adjustments; officials receive qualified, reusable assurance packs. Management views show complaints and challenges where AI was involved, linked to RULE-005, without exposing unnecessary personal data. | Must |
| NFR-009 | BR-057 | Each material user journey shall have accountable ownership, service-time measures, escalation and tested manual or non-digital alternatives. | BG-003, BG-004, BG-005, BG-009, BG-010, BG-011 | Residents, employees, contractors, officials | AC-071: Measures cover intake-to-owner, hazard action, professional review, resident contact and adjustment, appointment recovery, evidence review, defect resolution and external-query response. Results expose overdue, paused and reopened work and lawful accessibility differences. Thresholds for each measure are set by the journey owners under OD-09 and OD-25 before live use. | Must |
| RULE-022 | BR-058 | Personal-data use by agents shall pass purpose, lawful-basis, special-category, transparency, automated-decision, DPIA, security, supplier and incident gates before live processing. | BG-003, BG-005, BG-009, BG-012 | Residents, employees, DPO, digital, suppliers | AC-072: Processing records separate each purpose. Pilot design keeps agent outputs below the solely automated threshold by requiring meaningful, not token, human involvement before any significant outcome. Where Article 22C safeguards would apply, records show the four safeguards: information about the decision, ability to make representations, ability to obtain human intervention and ability to contest. Reviewers can depart from an output and record reasons. Resident works decisions are not treated as blanket data-processing consent. Vulnerability data is minimised, and contractor access is limited to functional adjustments.<br>AC-079: Before live processing, the DPO approves privacy notice updates covering each agent purpose under UK GDPR Articles 13 and 14 and a published plain-language statement of where AI is used in the programme, what it does and does not decide, and how to reach a person. Resident-facing AI-drafted content is approved by a named human before sending. Residents can ask for a human explanation or review at any time through digital and non-digital channels. The gate supports Safety and Quality Standard 2.3.3 on clear and timely communication about planned improvements ([local snapshot](../reference/regulatory/social-housing-regulation/social-housing-safety-and-quality-standard-2024.md), effective 1 April 2024, converted 2026-09-19). The Transparency, Influence and Accountability Standard is noted only as a secondary reference through Awaab's Law Phase 2 guidance section 3 ([local snapshot](../reference/regulatory/social-housing-regulation/awaabs-law-phase-2-guidance-2026.md), converted 2026-09-19) pending OD-39 local snapshot. | Must |

## Data and Reporting Requirements

### Minimum Data Domains

* Authoritative property and building identifiers
* EPC, condition, component and planned-maintenance data
* Safety, hazard, inspection, action and completion records
* PAS 2035 assessment, pathway, design and competent-person records
* Resident communication, adjustment, consent and challenge records
* Supplier, subcontractor, competence and committed-capacity records
* Work orders, appointments, installation and quality evidence
* Grant opportunity, award, claim, receipt and clawback records
* Tenure, lease-interest, owner-contribution and consultation-status records
* Versioned eligibility rules, funding routes and per-home eligibility results
* Hazard awareness records with source, channel, awareness and referral
  timestamps
* Standard work orders, appointment outcome codes and contract data schedules
* Sensor device register with property mapping, calibration and validity
  status
* Budget, commitment, cash-flow and approval records
* Handover, complaint, defect, remediation and in-use outcome records
* Building-to-property dependencies, planned-maintenance sequencing and
  scheme-level investment decisions
* Model, rule, configuration and interface versions with source provenance,
  authority decisions, reconciliation and recovery records
* Agent output provenance records, including prompt or template versions,
  source references, confidence category, reviewing human and accept, edit or
  reject decision with reason
* AI capability register records covering purpose, data used, lawful basis,
  owner, authority level, model and configuration version, evaluation results,
  gate status and known limitations
* AI-involved complaint, challenge and review tags linked to the ordinary
  complaints and resident review routes
* Regulatory source, snapshot, difference, interpretation, approval,
  activation, notification, test and retirement records
* Baselines, comparison cohorts, event dictionaries, analysis code versions,
  effort measurements, evaluation results, benefits owners and tranche approvals
* Shared-resource allocation logs, work-sampling records and short time-study
  records, including recording burden

### Required Management Views

The pilot needs two separate instruments. The operational dashboard steers the
pilot week to week, can change definitions as the team learns, reports at team
level rather than individual-officer level and is not gate evidence. The
benefits scorecard uses frozen, versioned definitions under RULE-019, is
independently assured and is the gate evidence. Suppliers see contractual KPIs.
Evaluation measures may be shared with suppliers after a delay, with a right to
review and challenge data before publication but no veto over the scorecard.

* Portfolio trajectory and validated EPC baseline
* Safety holds, emergency handoffs and response performance
* Properties by lifecycle state, gate and ageing
* Resident decisions, withdrawals, pauses, accessibility and challenges
* Supplier committed capacity, utilisation and recovery plans
* Right-first-time quality, defects, recurrence and remediation
* Grant value by controlled state and funding scheme
* Gross and net programme cost, match funding and peak cash exposure
* Liquidity, covenant and board-tolerance position
* Resident energy-cost, comfort, satisfaction and complaint outcomes
* Accepted handovers versus homes reaching the intended energy outcome
* Stage delay causes, manual effort net of review, cycle time and cost per
  accepted home
* Committed versus delivered capacity by competent role and subcontractor
* Draft accuracy, override rates, unsupported-claim rate, explanation
  fidelity, automation-bias indicators, critical exceptions and attributable
  value versus the agreed counterfactual
* AI capability register status, gate status and a proposed resident-facing
  summary where approved as good practice
* AI assurance report to the Board, including incidents, overrides,
  unsupported-claim rate, outcome breakdowns across resident groups and gate
  status, at a cadence set by the responsible owners
* Complaints, challenges and human-review requests where AI was involved,
  linked to RULE-005 and FR-041
* Phase and tranche readiness, stop decisions, pending seasonal evidence and
  resident outcomes across relevant groups
* Regulatory source freshness, failed retrievals, detected changes, pending
  reviews, approved effective dates and rules awaiting regression tests

Measures that must not be used as benefit evidence are starts, installations or
works released as throughput; completed-only averages; agent activity counts;
"hours saved" calculated as task counts multiplied by assumed minutes or
converted into cash; consent rate as a target; combined grant captured;
supplier-declared utilisation; zero incidents or days since last incident; and
the absence of an AI flag or sensor alert.

## Benefits and High-Level Economics

### CXO Value Proposition

The proposed value is the ability to convert approved investment into safe,
resident-complete, evidence-accepted and fundable outcomes with fewer avoidable
delays and failures. Agent count and automated activity are not benefits.

| Value domain | Proposed value | Owner and measurement |
| --- | --- | --- |
| Resident and social | Safer, warmer homes, informed choices, reliable appointments and less disruption | Resident Engagement and Assets: comfort, affordability, adjustments, complaints and adverse outcomes; do not promise universal bill reductions |
| Operational | Less duplicate entry, evidence chasing, repeat work and unowned handoffs | Programme: cycle time, manual hours net of review, repeat visits and accepted throughput against the comparison cohort |
| Asset and programme | Better sequencing with maintenance and fewer abortive interventions or systemic defects | Assets and Quality: whole-life cost, accepted energy outcomes and physical defects by archetype and supplier |
| Financial | More compliant conversion of eligible awards, less avoidable expenditure and clearer cash exposure | Finance: incremental grant cash, verified budget reductions, cost per accepted home, peak cash and covenant headroom |
| Risk and governance | Traceable approvals, earlier containment and stronger Board, funder and audit evidence | Safety and assurance: unresolved holds, breaches, critical exceptions, recovery and evidence completeness; use a risk scorecard rather than unsupported cash values |
| Strategic | Reusable property and evidence capability without supplier dependence | Assets and Digital: data quality, portability, ownership, supportability and whole-life affordability before further use cases |

### Separate Investment Cases and Attribution

FR-025 and RULE-016 require separate appraisals for the physical retrofit programme
and the incremental technology option. Each must distinguish existing planned
expenditure, rephased or displaced expenditure, incremental acceleration and
financing. Technology costs include discovery, data remediation, integration,
licensing or consumption, retained staff, training, measurement design and
capture, parallel operation, human review, assurance, support, model and rule
maintenance, and exit.

Only differences attributable to the selected option against the agreed
counterfactual count as technology benefits. Staff time released is capacity,
not cash savings unless a budget owner confirms expenditure will reduce.
Existing-plan grant is not incremental grant; an earlier receipt is a timing
benefit rather than a second grant award. Resident savings and strategic risk
reduction remain separate from landlord cash returns.

Grant capture cannot fund the technology case on its own. Grant is capped and
needs co-funding, so winning more grant also increases the provider's spend,
as the GBP 66.7 million provider balance against the GBP 40 million
opportunity illustrates. The technology value case must therefore rest on
more accepted handovers, less rework, avoided clawback, faster cash and
committed budget reductions (FR-027).

Finance must reconcile monthly spend and receipts, match funding, peak cash,
liquidity, covenant and security headroom. Downside cases cover grant delay or
loss, inflation, low volume, supplier failure, defects, financing and competing
safety spend. Gross programme value is not the solution's return on investment.

### Unvalidated Value Claims

The case study proposes:

* Doubling retrofit delivery
* Capturing GBP 40 million of grant
* Protecting borrowing capacity potentially measured in hundreds of millions
* Reducing resident energy bills

These remain hypotheses until the association validates:

* Current annual throughput and accepted-completion baseline
* Actual homes below EPC C and data confidence
* Unit costs by archetype and measure
* Eligible homes, funding rates, award status and match funding
* Programme technology, integration, staffing and support costs
* Grant timing, rejected-cost and clawback assumptions
* Liquidity, debt, security and covenant headroom
* Resident access, consent, quality and delivery attrition
* A method for measuring actual resident energy-cost outcomes

### Illustrative Economics and Review Qualifications

| Scenario | Calculation | Interpretation |
| --- | --- | --- |
| Provisional below-C cohort | 60,000 x 26% = 15,600 homes | Sector-derived planning cohort, not a verified requirement |
| Four full delivery years | 15,600 / 4 = 3,900 per year | Simple trajectory; mobilisation and the actual start and end dates require rephasing |
| Gross cost | 15,600 x GBP 20,000 = GBP 312 million | Illustrative cost, not a budget |
| Ordinary full-cap scenario | 15,600 x GBP 7,500 = GBP 117 million | Ceiling illustration before eligibility, allocation and claim conditions |
| Provider balance at that ceiling | GBP 312 million - GBP 117 million = GBP 195 million | Funding balance on the same assumed cost basis, not demonstrated affordability |
| GBP 40 million full-cap equivalent | GBP 40 million / GBP 7,500 = about 5,333 homes | Rounded full-cap equivalent; not a universal maximum number of homes supported |
| Cost and balance for that equivalent cohort | About 5,333 x GBP 20,000 = GBP 106.7 million; less GBP 40 million = GBP 66.7 million | Approximate provider funding illustration, not an award or commitment |
| Only GBP 40 million received for the full cohort | GBP 312 million - GBP 40 million = GBP 272 million | Conditional full-programme funding balance; the opportunity is not secured |
| Gross cost rises 10% | GBP 312 million x 10% = GBP 31.2 million additional cost | Sensitivity before any change to funding or scope |

The addendum's "at most" wording is interpreted here as a full-cap illustration:
lower average awards could spread the same amount across more eligible homes.
Finance must use the actual scheme averaging rules and approved property
schedule, not this rounded equivalent, for commitments.

The GBP 20,000 input is labelled "fully loaded" in the sources, but its cost
inclusions are not established. The balances above use that same basis. Finance
must map financing, technology, overhead, enabling work, defects and contingency
to included or excluded costs before adding them; treating all as additional
would risk double counting.

### Benefits Validation Register

| Hypothesis | Evidence before scale | Accountable owner | Requirement |
| --- | --- | --- | --- |
| Coordination is a material delivery constraint | Stage delays, failure demand, capacity and root causes | Programme | RULE-016 |
| Accepted outcomes increase rather than activity | Frozen cohort, intention-to-treat analysis, concurrent matched comparison, instrumented pre-period and accepted handovers with separately measured energy outcomes | Programme and Assets | FR-033, RULE-019 |
| Grant conversion improves | Eligible award, evidence acceptance, claims and receipts net of the current plan | Finance | FR-023, FR-024, FR-025, RULE-009, RULE-010 |
| Administrative benefits exceed review costs | Work sampling or short time studies in both arms, net effort including shifted burden and recording time, staffing consequences and verified cashability | Programme and Finance | RULE-019, FR-025 |
| Quality is maintained at higher volume | Independent physical inspection, rejection, defect severity, recurrence and remediation cost | Quality | FR-028, FR-029, FR-030, FR-031, FR-032, RULE-013 |
| Residents receive equitable value | Accessible journey tests and lawful outcome breakdowns, including adverse outcomes | Resident Engagement | FR-032, NFR-008 |
| Acceleration remains affordable | Monthly cash and severe-but-plausible treasury scenarios | Finance and Board | FR-025, RULE-011, RULE-012 |
| Agent capabilities add value over conventional workflow | Comparison 2 paired shadow-mode evidence, lawful task-level allocation where used, error severity, review effort, missed critical exceptions and incremental whole-life economics | Digital and Finance | RULE-016, FR-036, RULE-018, RULE-019, RULE-020 |
| Safe acceleration does not worsen guardrails | Approved stop triggers, breach logs, affected-work pauses and restart evidence | Building Safety, Programme and Sponsor | FR-001, FR-002, FR-003, FR-030, FR-032, RULE-003, RULE-020 |

### Executive Trade-Offs as Approval Criteria

The [pinned #58 learning](../ideas/typesafe-system-one-agent-fit.md#observed-feasibility-and-parallel-value-experiment-2026-10-11)
records real source-bound Decision 1 selection, cited generative inference
and Azure SQL deployment, inspected 2026-10-11. Narrow integration is feasible;
calibrated task quality, three-class support and net benefit remain unproved.
The owner reports a parallel four-arm experiment: rules/manual, Decision/
templates, generative agent and hybrid agent with Decision tools. This can
inform Comparison 2, not establish locality-level or resident outcomes.

Data and Performance reviews versioned protocol/source/split/task/model/
schema/threshold records, independent human labels, denominators/exclusions,
quality and uncertainty; Finance reviews complete human preparation/review/
correction effort and whole-life cost; task/control owners and the exercise
owner review adoption. Proposed protocol is not executed benefit evidence.
Binary support cannot satisfy three-class screening; insufficient labels,
participants or precision remain Inconclusive/Not evaluated. Negative
results may reject narrow tasks while independent platform/control work
continues. No result automatically activates a live control.

| Trade-off | Required decision discipline | Requirement |
| --- | --- | --- |
| Speed versus safety and quality | Accepted outcomes and independent evidence outweigh starts or calendar pressure | FR-001, FR-028, RULE-020 |
| Grant eligibility versus whole-asset value | Record why the intervention fits condition and planned maintenance, not merely a grant | FR-025, FR-035 |
| Automation versus accountability | Enforce the authority matrix and preserve human professional and resident decisions | RULE-017, FR-036, RULE-018 |
| Breadth versus deliverability | Test agent capabilities in a bounded locality with existing named owners before expanding capabilities or capital | RULE-016, RULE-020 |
| Standardisation versus property context | Reuse archetype details only after property and building checks | FR-007, FR-035 |
| Portfolio optimisation versus resident agency | Investigate missing data and support needs rather than exclude silently | RULE-005, NFR-008 |
| Supplier scale versus resilience | Validate capacity and contingency; use quality-adjusted scorecards for new allocations | FR-019, FR-020, FR-021 |
| Innovation versus lock-in | Require continuity, portable evidence and tested exit arrangements | NFR-004, NFR-005, NFR-006, NFR-007 |

## Risks and Controls

| Risk | Consequence | Required control |
| --- | --- | --- |
| Unsafe sequencing | Resident harm or regulatory failure | Mandatory safety hold and competent-human release |
| Poor or conflicting data | Incorrect prioritisation or approval | Authoritative data owners and stop-on-conflict rules |
| Inferred resident consent | Unauthorised work and loss of trust | Measure-specific decisions, accessible challenge and pause rights |
| Supplier capacity shortfall | Missed appointments and undeliverable plans | Contractually committed capacity and contingency routes |
| Quality failure at scale | Defects, harm, rework and clawback | Design release gate, installation hold points and independent verification |
| Grant overstatement | Unaffordable commitments or misleading reporting | Separate opportunity, award, claimable and cash states |
| Financial pressure | Reduced liquidity or displaced safety investment | Board-approved envelope, scenarios and downside tolerances |
| Handoff failure | Residents repeat information or urgent issues wait | Named ownership, acceptance and next-update evidence |
| Automation overreach | Decisions outside delegated authority | Role-based approvals, segregation of duties and audit history |
| Regulatory change | Outdated controls | Dated rules, accountable review and current official validation |
| Wrong constraint automated | Technology cost without additional accepted outcomes | Measured bottlenecks, non-agentic options and incremental-value gates |
| Pilot optimism or selection bias | Small or easy cohorts misrepresented as proof of safe scale | Prespecified comparisons, representative resident journeys and visible exclusions and pending outcomes |
| Platform outage or model change | Lost handoffs, invalid transitions or service interruption | Tested fallback, disable mechanism, version control and recovery reconciliation |
| Double-counted benefits or costs | Misleading investment return or funding requirement | Separate capital and technology cases, cost-inclusion map and Finance-owned attribution |
| Shared-building or repeat defect missed | Harm extends beyond the initially affected dwelling | Building-linked holds, related-stock review and competent containment before further release |
| Hazard awareness lost in a retrofit channel | Statutory clock starts without the hazard service knowing, or earlier awareness is discovered late | Mandatory hazard question, timestamped referral and raise-only scan with Legal handoff (FR-003, RULE-003, FR-004) |
| Clean evidence pack or normal sensor reading read as assurance | Defective work accepted, paid or claimed | Positive evidence checklist, absence-of-flag rule and sensor validity rules (RULE-014) |
| Tenure or lease interest misrouted | Works offered without the owner's decision, permission or lawful cost recovery | Recorded tenure status, owner route and Legal consultation check (FR-015, RULE-023) |
| Incomplete vulnerability records drive priority | Known residents favoured and unrecorded residents penalised | Unknown-not-none rule, with-and-without-flag runs, nomination and self-referral routes (FR-037) |
| Drafted message treated as a contract instruction | Unauthorised variation, cost or procurement modification | Contract-manager-only instructions and "not an instruction" drafts (RULE-008) |
| In-scope homes counted as eligible | Overstated opportunity and unaffordable match funding | Deterministic pass, fail or unknown eligibility and evidenced route and co-funding (FR-026, FR-027) |
| Opaque or unsupported AI explanation accepted | Resident detriment, poor challenge handling or unreliable assurance | Explanation records, output provenance, unsupported-claim sampling, human review and guardrail pause (FR-034, FR-044, RULE-019, RULE-024) |

## Assumptions and Open Decisions

| ID | Unknown company detail | Required owner | Approval impact |
| --- | --- | --- | --- |
| OD-01 | Replace the 74% EPC C+ sector benchmark with a validated address-level baseline | Asset Director | Portfolio target |
| OD-02 | Replace the 3,900-home required trajectory with current accepted throughput and an approved delivery path | Retrofit Programme Manager | Delivery target |
| OD-03 | Authoritative system and owner for each data domain | Executive/data governance | Data design |
| OD-04 | Higher-risk building register and safety evidence baseline | Building Safety Lead | Safety controls |
| OD-05 | Mandatory evidence sets, validity periods and hazard thresholds | Building Safety Lead | Progression gates |
| OD-06 | Named PAS 2035 roles, competence and annual capacity | Retrofit Programme Manager | Technical approvals |
| OD-07 | Resident demographics, channels, accessibility and advocacy needs | Resident Engagement Lead | Consent service |
| OD-08 | Replace the no-access, refusal and TSM planning benchmarks with company consent, challenge and complaint funnels | Resident Engagement Lead | Outcome targets |
| OD-09 | Exception teams, response targets and out-of-hours routes | Housing and repairs leads | Handoff design |
| OD-10 | Validate the 6 to 9 month mobilisation and 10% to 20% reserve assumptions against committed suppliers | Procurement Lead | Scheduling controls |
| OD-11 | Replace the GBP 40 million opportunity and grant-cap scenario with award, eligibility and match-funding evidence | Finance and Grants Lead | Benefit case |
| OD-12 | Replace sector warning comparators with the provider's capital envelope, liquidity, covenants and approval thresholds | Finance and Board | Acceleration gate |
| OD-13 | Material-change rules, defect severity and payment or claim holds | Quality and Finance | Remediation |
| OD-14 | Lawful basis, DPIA, retention and data-sharing rules. The [addendum baseline](../case_study_48_addendum.md) proposes default retention periods, deletion rules and evidence for DPO, Legal and record-owner approval; no numeric period exists in the regulatory corpus. | Data Protection Officer | Data controls |
| OD-15 | Board risk appetite and downside tolerances | Board | Programme approval |
| OD-16 | Measured binding constraints and selection among process, existing-platform, workflow and AI options; owner directs Azure-led hybrid only as a provisional non-production demonstrator baseline, with customer/production architecture open pending Phase 0 appraisal | Programme, Digital and Finance | Phase 0 exit |
| OD-17 | Pilot locality, archetypes, representative residents, exclusions, budget, schedule and existing named accountable owners; owner directs every current contract/framework to participate in live pilot delivery, subject to contract-level Procurement/Legal clearance before any supplier activity | Sponsor and Programme with control owners | Shadow and live-pilot scope |
| OD-18 | Comparable baseline, primary endpoint event definitions, metric definitions, benefits owners, critical-exception tests and ratified 20% cycle-time and 25% effort targets; assessment-to-ready-to-install is the owner-directed primary cycle-time measure, with accepted handover reported separately | Programme, Finance and independent assurance | Evaluation protocol before Phase 0 capture and shadow testing |
| OD-19 | Allow/deny matrix, initial human-review workload and later authority-change procedure | Digital and all control owners | Live-pilot and automation release |
| OD-20 | Interfaces, reconciliation, recovery limits, manual fallback, model and rule change control, support and exit terms | Digital service owner, data owners and Procurement | Live service readiness |
| OD-21 | Cost inclusions within GBP 20,000, actual grant averaging rules, and separate incremental technology economics | Finance | Investment and tranche affordability |
| OD-22 | Building dependencies, planned-maintenance bundling, archetype reuse and related-stock defect review | Assets, Safety and competent technical roles | Cohort and design release |
| OD-23 | Accessible resident journey evidence and proportionate seasonal follow-up and outcome breakdowns | Resident Engagement, Assets and DPO | Live contact and in-use evaluation |
| OD-24 | Regulatory source owners, official retrieval methods, interpretation authority, emergency holds and activation process | Legal, Compliance, DPO, Finance and Digital | Regulatory knowledge service and live-rule change control |
| OD-25 | Employee, resident, contractor and official service journeys, baseline times, escalation owners and non-digital fallbacks | Programme, Resident Engagement and service owners | Phase 0 and shadow-mode exit |
| OD-26 | Stock by local authority area, and whether any falls within the Greater Manchester or West Midlands integrated settlements; national DESNZ check of the 30% non-social rule | Finance and Grants Lead with Asset Director | Funding route and eligibility rules (FR-026, FR-027) |
| OD-27 | Verified tenure and lease type per home; lease sample review of improvement, cost-recovery and consultation terms; whether measures are offered or funded for owners | Legal, home ownership team, Asset Director and Finance | Owner decision routes and cohort scope (FR-015, RULE-023) |
| OD-28 | Recorded vulnerability flag coverage against prevalence benchmarks; lawful basis and Article 9 condition; weight given to health risk in the cohort policy | Resident Engagement, DPO, Asset Director and Board | Prioritisation (FR-037) |
| OD-29 | Current route and system for hazards spotted by assessors, installers and liaison staff; when contractor knowledge counts as landlord awareness; referral and escalation limits; timestamp correction rules | Repairs, Building Safety and Legal | Hazard referral (FR-003, RULE-003, FR-004) |
| OD-30 | Live contracts and frameworks for the pilot, contract form, named contract managers and authority limits; applicability of Procurement Act 2023 modification rules, Construction Act payment notices and section 20 | Procurement Lead, Finance and Legal | Contractor control and award gate (RULE-008, FR-022) |
| OD-31 | Quality flag autonomy: L4 raise-only flags or recommend-level evidence reading. Proposed settlement: a blinded three-arm shadow test (checklist only, L4 flags, recommend level) on past packs and seeded defects. L4 is rejected if a safety-critical seeded defect is missed, detection on unflagged packs falls below the checklist arm, false flags exceed approved reviewer capacity, or recall does not improve | Retrofit Programme Manager, Building Safety and Data and Performance Lead; Sponsor approves any authority change under RULE-020 | Quality module authority (FR-036, RULE-018, RULE-014) |
| OD-32 | Whether booking of confirmed slots for residents who have opted into digital contact could later move to L3; revisit only after Phase 1 evidence | Resident Engagement, Neighbourhood Housing and Programme | Later authority change under RULE-020 |
| OD-33 | Who carries out the Retrofit Assessor survey and who acts as Retrofit Coordinator for pilot homes, employed or contracted, and each role's monthly capacity | Retrofit Programme Manager | Separate sign-offs and pilot capacity (RULE-017, FR-010) |
| OD-34 | Proposed owner resolution on 2026-09-26: the pilot gate decides which agent capabilities scale, using Comparison 1 and Comparison 2; the existing retrofit model is modernised with agents rather than replaced | Sponsor, Executive Director of Assets and Finance | Proposed resolution pending Sponsor, Executive Director of Assets and Finance confirmation in the RULE-019 protocol |
| OD-35 | Guardrail stop override authority, if any, and evidence needed to restart affected work | Building Safety and Sponsor | Live-pilot approval, breach response and restart under RULE-020 |
| OD-36 | DPIA and lawful basis for new resident and staff measurement data, including staff-level monitoring | Data Protection Officer | Blocks Phase 0 capture |
| OD-37 | Supplier data duties in existing pilot contracts and whether adding pilot measurement duties requires contract variations | Procurement and Legal | Blocks pilot protocol and supplier data capture |
| OD-38 | Who funds recording time for frontline and matched-locality staff, including housing officers | Programme and Housing | Blocks Phase 0 capture budget and effort measurement |
| OD-39 | Obtain dated local snapshots of the Transparency, Influence and Accountability Standard, the Housing Ombudsman Complaint Handling Code, the Governance and Financial Viability Standard and ICO guidance on explaining decisions made with AI before they are relied on | Legal, Compliance and DPO | Blocks reliance on those sources for operational rules, external assurance or release gates |
| OD-40 | Ratify the configurable no-access threshold and event codes, counting only while a case is active and resetting only on human case closure; name the policy/configuration owner and approve change, audit and resident-review controls | Housing and Repairs leads, with Resident Engagement review and Programme/Digital input | Blocks operational use of RULE-006 |
| OD-41 | Validate the journey atlas stages, pains, gains and handoffs through voluntary, accessible research with real residents, staff, contractors and representatives, including declined or deferred work, failed visits, reopened defects and non-digital households | Resident Engagement and Programme, with Data and Performance input | Blocks use of journey claims as company facts or targets; does not block the exercise demonstrator |
| OD-42 | Approve how representative authority is evidenced, reviewed, revoked and retained, and which channels may record it | DPO, Legal and Resident Engagement | Blocks operational use of FR-045 with real residents |
| OD-43 | Confirm the actual in-use monitoring inventory and ownership: device types, count, protocol, sampling cadence, device-to-property mapping and calibration owner, lawful basis and DPIA, resident choice, retention, freshness and gap rules, analysis windows and thresholds, and the operational review owner | Assets, Building Safety, DPO and data owners, with Digital input | Blocks operational use of FR-048 with real data; does not block the simulator exercise |

### Owner Direction and Company Role-Profile Challenge (2026-10-04)

The owner made two project-level design directions after reviewing the
company-role perspectives:

* **Demonstrator architecture:** Use an Azure-led hybrid only as the
  provisional, non-production demonstrator baseline. Keep the customer and
  production architecture open until the Phase 0 options appraisal compares
  process redesign, existing-platform configuration, conventional workflow
  integration and bounded AI on measured constraints, whole-life cost,
  adoption/support capability, integrations and control needs. This is not a
  customer architecture, procurement or investment approval; OD-16 and OD-20
  remain open.
* **BG-011 endpoint:** Keep assessment-to-ready-to-install elapsed time as the
  primary cycle-time measure and report accepted handover separately. This
  resolves the owner-level choice of primary measure only. It does not define
  event clocks, denominator, cohort, case handling or MDE and does not change
  the Executive Reviewer's `CHANGES_REQUESTED` target-ratification decision.
  OD-18 remains open.

The owner clarified that every current contract/framework is required to
participate in live pilot delivery. This is an owner-directed scope condition,
not evidence that any agreement permits the work or that suppliers have
capacity. No supplier may be included in live activity until Procurement and
Legal verify each agreement, applicable authority and required data/measurement
terms, and the relevant readiness gates pass. If any contract fails those
gates, live pilot approval is blocked until the gap is resolved; the owner
direction does not waive a contract, safety, privacy or legal control. OD-17
and OD-30 remain open for the required pilot details and evidence.

The owner also clarified the missed-appointment escalation direction:

* Set the threshold as configurable, with five as a provisional default and
  escalation only when the eligible count is greater than the configured
  value. At the default, the sixth eligible event triggers human review.
* Count only a confirmed appointment with a verified resident no-access
  outcome. Record provider/contractor no-shows, cancellations and reschedules
  as distinct outcomes that do not count toward the threshold.
* Count eligible outcomes while the same case remains active; reset the
  counter only when a human closes that case. Keep the event history for audit.

These are owner-directed draft rules, not a sector benchmark or company policy
approval. Public evidence reviewed for this control does not establish five
as a standard. The Executive Reviewer returned `CHANGES_REQUESTED` on the
earlier wording because it omitted the event categories and case-count
semantics; the requirement above incorporates the owner's clarifications.
Housing and Repairs must still ratify the rule against company appointment
records, with Resident Engagement review. OD-08, OD-09 and OD-40 remain open;
the rule does not authorize operational use or delay urgent hazard response.

The following perspectives were gathered from company role profiles. They
are consultation hypotheses and recommendations, not statements from actual
employees, company approvals or verified company evidence:

| Profile | Challenge recorded | Accountable follow-up |
| --- | --- | --- |
| Executive Reviewer | Retained `CHANGES_REQUESTED` for BG-011. The endpoint choice clarifies the measure but leaves direct comparability, forecast plausibility, frozen cohort, case handling, effort scope and MDE unresolved. Recommended prioritizing pilot scope, asset baseline/capital plan, competent capacity, grant and affordability evidence, safety/resident controls and lawful measurement approvals. | Programme and Finance with independent assurance; relevant control owners for their decisions |
| Asset Executive | Establish address-level EPC/condition and building data, plan-linked trajectory and capital envelope, affordability downside, and resident/tenure impact. Do not substitute sector figures or grant eligibility for asset priorities. | Asset, Finance and Board within their actual delegations |
| Retrofit Programme Manager | Reconcile locality/archetype boundaries with all-current-contract direction; evidence named PAS 2035 competence and capacity; distinguish pilot volume, primary cycle time and accepted handover. | Programme, Sponsor, Procurement and competent technical roles |
| Finance and Grants | Verify the reported award and eligibility, match, deadlines, cash and clawback; separate retrofit capital from technology economics; do not treat released capacity as cash savings. | Finance and Grants, with Asset and Board approvals as applicable |
| Resident Engagement | Validate measure-specific choice, accessibility, challenge and non-digital journeys with residents; evidence fair appointment recovery and avoid measurement burden. | Resident Engagement and Housing, with DPO where processing applies |
| Building Safety | Evidence building/hazard baselines, hazard service handoffs and named stop, hold and restart authorities; keep safety and quality gates independent of throughput. | Building Safety, Repairs, competent professionals and Sponsor for the distinct decisions |
| Procurement | Inventory the contract/framework universe, terms, named authorities, capacity, data duties and potential variation needs before supplier participation. | Procurement and Legal; do not infer permission from owner scope direction |
| Data and Performance | Freeze cohort, comparison, estimand, event/pause rules and MDE; record effort symmetrically, including shifted, recording, review and assurance effort; separate operational dashboard from assured scorecard. | Programme, Data and Performance, Finance, DPO and independent assurance |
| Neighbourhood Housing Officer | Test real handoffs, appointment recovery, resident updates, non-digital fallback and frontline recording burden with staff and residents. | Housing and Resident Engagement with service owners |
| Executive Reviewer (missed-appointment review) | Returned `CHANGES_REQUESTED` on the prior RULE-006 wording because it did not define the configurable default, strict-greater-than comparator or eligible event categories. Follow-up review found those semantics resolved in v0.12.0 and requested that event history remain auditable after counter reset; this is now explicit. Public evidence does not validate five. | Housing and Repairs leads, with Resident Engagement review; Programme/Digital for configuration and audit controls |
| Asset Executive (missed-appointment review) | Supported recording five only as a provisional human-review trigger; required reliable company event history, named service ownership and no adverse resident treatment from the count alone. | Housing and Repairs, with Asset oversight as applicable |
| Resident Engagement (missed-appointment review) | Supported human review only, with verified event records, accessible notice/adjustment checks, correction and complaint routes, privacy minimisation and a separate urgent-hazard path. No resident evidence was supplied to validate the trigger. | Resident Engagement and Housing/Repairs; DPO for data controls |
| Retrofit Programme Manager (missed-appointment review) | Confirmed the sixth qualifying event can be expressed operationally, subject to distinct outcome codes, evidence provenance, active-case counting, human closure/reset and a staffed handoff. No technical choice for the owner remains; operational owners must ratify the configuration. | Housing and Repairs, Resident Engagement, Programme and Digital |

Minimum follow-up evidence from the panel is recorded as open work, not as
approval: validated asset/building and hazard baselines; actual systems and
data ownership; pilot cohort and contract register/terms; competent PAS and
assurance capacity; grant and affordability records; resident journey
validation; frozen OD-18 protocol and OD-36 DPIA/lawful measurement basis;
named stop/restart authority; and technical options appraisal. The
owner-delegated reviewer can decide only whether to ratify BG-011 for draft
planning or request changes. It cannot close company decisions or exercise
actual executive authority.

### TypeSafe Batch Review of Open Decisions

On 20 September 2026, the 25 decisions then open (OD-01 to OD-25) were
reviewed in one TypeSafe System One request using `jev-1.13.0`. The full BRD
and its evidence-classification rule were supplied as shared state. OD-26 to
OD-43 were added later and have not been through this review. Each decision
received:

* A Choice judgment on whether it was resolved by company evidence, supported
  only as a provisional direction, still required company evidence, or had
  been superseded
* A Noul judgment estimating whether the BRD contains a concrete provisional
  direction that can guide readiness work without being treated as company
  evidence or approval

The batch used 28,304 input tokens and 2,475 output tokens. TypeSafe judgments
are semantic review signals, not evidence, professional advice or approval.
Choice confidence describes how concentrated the model's answer distribution
was. The provisional-direction value is the probability of yes, not a
confidence score.

| ID | TypeSafe answer | Choice confidence | Provisional direction probability | Current answer |
| --- | --- | ---: | ---: | --- |
| OD-01 | Company evidence required | 0.74 | 0.76 | Keep the 74% benchmark only for scenario planning; Asset must provide the address-level baseline. |
| OD-02 | Company evidence required | 0.80 | 0.84 | Keep 3,900 homes per year as a trajectory scenario; Programme must establish accepted throughput and an approved path. |
| OD-03 | Company evidence required | 0.75 | 0.67 | Use RULE-015 to structure the decision; executives and data governance must name each authoritative system and owner. |
| OD-04 | Company evidence required | 0.93 | 0.62 | No building-safety baseline is evidenced; Building Safety must provide the register, status and accountable owners. |
| OD-05 | Company evidence required | 0.83 | 0.47 | No operational evidence set, validity period or hazard threshold can be inferred; Building Safety must define and approve them. |
| OD-06 | Company evidence required | 0.91 | 0.80 | Preserve the named-role model in RULE-017; Programme must evidence competent people, scope and committed capacity. |
| OD-07 | Company evidence required | 0.88 | 0.69 | Retain accessible digital and non-digital journeys as the design direction; Resident Engagement must provide resident evidence. |
| OD-08 | Company evidence required | 0.66 | 0.73 | Keep sector rates as sensitivities only; Resident Engagement must replace them with the association's complete funnel. |
| OD-09 | Company evidence required | 0.82 | 0.57 | FR-016, FR-017, FR-018, RULE-006 define the control pattern; Housing and Repairs must name teams, targets and out-of-hours routes. |
| OD-10 | Company evidence required | 0.69 | 0.82 | Retain the 6-to-9-month mobilisation and 10% to 20% reserve only as test assumptions pending committed-supplier evidence. |
| OD-11 | Company evidence required | 0.87 | 0.86 | Continue to report GBP 40 million as opportunity only; Finance must supply award, eligibility, match-funding and claim evidence. |
| OD-12 | Company evidence required | 0.92 | 0.54 | No acceleration envelope is established; Finance and Board must provide liquidity, covenant, security and approval tolerances. |
| OD-13 | Company evidence required | 0.41 | 0.81 | FR-008 and FR-029, FR-030, RULE-013 provide a provisional control pattern; Quality and Finance must ratify classifications and holds. |
| OD-14 | Company evidence required | 0.72 | 0.74 | RULE-022 defines the required gates; the DPO must determine lawful basis, DPIA, retention and sharing controls. The addendum Data Handling and Retention Baseline (proposed, 2026-10-08) supplies defaults to approve or replace; funder, PAS 2035 and limitation-period retention terms are not in the corpus and remain unknown. |
| OD-15 | Company evidence required | 0.89 | 0.61 | No Board risk appetite is evidenced; the Board must approve downside tolerances and pause conditions. |
| OD-16 | Company evidence required | 0.50 | 0.91 | Phase 0 should compare process, platform, workflow and bounded AI; measured constraints and Finance-approved economics must select the option. |
| OD-17 | Company evidence required | 0.34 | 0.90 | Use one locality, limited archetypes and existing named accountable owners as the planning proposition only; control owners must ratify scope and budget. |
| OD-18 | Company evidence required | 0.49 | 0.88 | Use RULE-019 and the proposed 20% cycle-time and 25% effort improvements to design the protocol; owners must ratify baselines and thresholds. |
| OD-19 | Provisional direction only | 0.57 | 0.88 | Start with AI limited to recommendations, drafts, reconciliation and flags under FR-036, RULE-018; all control owners must approve the detailed authority matrix and workload. |
| OD-20 | Company evidence required | 0.54 | 0.86 | NFR-004 and NFR-005, NFR-006, NFR-007 define continuity and portability outcomes; Digital, data owners and Procurement must select interfaces, limits and terms. |
| OD-21 | Company evidence required | 0.86 | 0.81 | Keep GBP 20,000 and grant-cap calculations illustrative; Finance must define cost inclusions, actual scheme rules and incremental technology economics. |
| OD-22 | Company evidence required | 0.46 | 0.86 | FR-035 supplies the provisional sequencing rule; Assets, Safety and competent roles must define building dependencies and reuse limits. |
| OD-23 | Company evidence required | 0.51 | 0.86 | FR-032 and NFR-008 provide the provisional evaluation pattern; Resident Engagement, Assets and the DPO must approve evidence and follow-up. |
| OD-24 | Company evidence required | 0.47 | 0.86 | FR-038, FR-039, FR-040, RULE-021 define the candidate workflow; accountable functions must assign sources, interpretation authority, holds and activation. |
| OD-25 | Company evidence required | 0.68 | 0.84 | FR-041 and NFR-009 define the service standard; service owners must map journeys, baseline times, escalation and non-digital fallback. |

The batch therefore closes none of the open decisions. It provides provisional
readiness directions for owner validation and confirms that no quantified
company baseline, authority, capacity, funding or approval assumption should
be promoted to an approved requirement without the requested evidence.

## Requirements Traceability

Coverage figures are computed from the requirement rows above. Every
acceptance criterion is a testable statement written in the row it verifies.
Acceptance criteria are not yet written in Given/When/Then form.

### Business Goal Alignment

| Business goal | Functional requirements | Business rules | Non-functional requirements |
| --- | --- | --- | --- |
| BG-001 | FR-033, FR-035, FR-042 | RULE-011 | NFR-008 |
| BG-002 | FR-005, FR-019, FR-020, FR-021, FR-022, FR-033, FR-035 | RULE-007, RULE-011, RULE-016, RULE-019, RULE-020 | None |
| BG-003 | FR-001, FR-002, FR-003, FR-004, FR-007, FR-008, FR-009, FR-010, FR-016, FR-029, FR-030, FR-032, FR-033, FR-035, FR-036, FR-037, FR-038, FR-039, FR-040, FR-043, FR-044, FR-048 | RULE-001, RULE-003, RULE-012, RULE-014, RULE-015, RULE-017, RULE-018, RULE-020, RULE-021, RULE-022, RULE-024 | NFR-003, NFR-004, NFR-009 |
| BG-004 | FR-001, FR-002, FR-003, FR-004, FR-016, FR-033, FR-036, FR-038, FR-039, FR-040 | RULE-002, RULE-003, RULE-018, RULE-021, RULE-024 | NFR-004, NFR-009 |
| BG-005 | FR-008, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-031, FR-033, FR-034, FR-036, FR-037, FR-040, FR-041, FR-042, FR-043, FR-044, FR-045, FR-046, FR-047 | RULE-005, RULE-006, RULE-012, RULE-018, RULE-020, RULE-022, RULE-024 | NFR-001, NFR-002, NFR-003, NFR-005, NFR-006, NFR-007, NFR-008, NFR-009 |
| BG-006 | FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-019, FR-021, FR-022, FR-028, FR-029, FR-030, FR-033, FR-036, FR-038, FR-040, FR-043, FR-044, FR-046, FR-047 | RULE-004, RULE-007, RULE-008, RULE-012, RULE-013, RULE-014, RULE-015, RULE-017, RULE-018, RULE-019, RULE-020, RULE-021, RULE-024 | NFR-002, NFR-005, NFR-006, NFR-007 |
| BG-007 | FR-023, FR-024, FR-025, FR-026, FR-027, FR-030, FR-033, FR-036, FR-038, FR-039, FR-040, FR-041, FR-042 | RULE-004, RULE-009, RULE-010, RULE-014, RULE-015, RULE-018, RULE-021 | None |
| BG-008 | FR-022, FR-025, FR-027, FR-033, FR-035, FR-043 | RULE-008, RULE-010, RULE-011, RULE-012, RULE-016, RULE-020 | NFR-003, NFR-005, NFR-006, NFR-007 |
| BG-009 | FR-012, FR-015, FR-020, FR-021, FR-029, FR-031, FR-032, FR-033, FR-037, FR-041, FR-042, FR-043, FR-045, FR-046, FR-047, FR-048 | RULE-005, RULE-006, RULE-014, RULE-019, RULE-022 | NFR-008, NFR-009 |
| BG-010 | FR-003, FR-006, FR-016, FR-017, FR-018, FR-033, FR-034, FR-038, FR-039, FR-040, FR-041, FR-044, FR-045 | RULE-003, RULE-008, RULE-021 | NFR-004, NFR-005, NFR-006, NFR-007, NFR-009 |
| BG-011 | FR-010, FR-022, FR-033, FR-041 | RULE-016, RULE-019 | NFR-009 |
| BG-012 | FR-004, FR-025, FR-026, FR-027, FR-033, FR-036, FR-038, FR-039, FR-042, FR-043, FR-044 | RULE-016, RULE-018, RULE-019, RULE-020, RULE-021, RULE-022 | NFR-004, NFR-005, NFR-006, NFR-007 |

### FR-to-AC and FR-to-BG Coverage

48 of 48 functional requirements have at least one acceptance criterion
(100.0%, against the 80.0% threshold). 48 of 48 link to at least one business
goal (100.0%, against the 100.0% target). Coverage shows that a link exists,
not that the linked goal or criterion has been validated.

| Functional requirement | Legacy ID | Acceptance criteria | Business goals |
| --- | --- | --- | --- |
| FR-001 | BR-001 | AC-001 | BG-003, BG-004 |
| FR-002 | BR-003 | AC-003 | BG-003, BG-004 |
| FR-003 | BR-062 | AC-005 | BG-003, BG-004, BG-010 |
| FR-004 | BR-063 | AC-007 | BG-003, BG-004, BG-012 |
| FR-005 | BR-005 | AC-008 | BG-002, BG-006 |
| FR-006 | BR-006 | AC-009 | BG-006, BG-010 |
| FR-007 | BR-007 | AC-010 | BG-003, BG-006 |
| FR-008 | BR-008 | AC-011 | BG-003, BG-005, BG-006 |
| FR-009 | BR-009 | AC-012 | BG-003, BG-006 |
| FR-010 | BR-068 | AC-014 | BG-003, BG-006, BG-011 |
| FR-011 | BR-011 | AC-015 | BG-005 |
| FR-012 | BR-012 | AC-016 | BG-005, BG-009 |
| FR-013 | BR-013 | AC-017 | BG-005 |
| FR-014 | BR-014 | AC-018 | BG-005 |
| FR-015 | BR-061 | AC-021 | BG-005, BG-009 |
| FR-016 | BR-017 | AC-022 | BG-003, BG-004, BG-005, BG-010 |
| FR-017 | BR-018 | AC-023 | BG-010 |
| FR-018 | BR-019 | AC-024 | BG-010 |
| FR-019 | BR-022 | AC-027 | BG-002, BG-006 |
| FR-020 | BR-023 | AC-028 | BG-002, BG-009 |
| FR-021 | BR-024 | AC-029 | BG-002, BG-006, BG-009 |
| FR-022 | BR-066 | AC-031 | BG-002, BG-006, BG-008, BG-011 |
| FR-023 | BR-025 | AC-032 | BG-007 |
| FR-024 | BR-027 | AC-034 | BG-007 |
| FR-025 | BR-029 | AC-036 | BG-007, BG-008, BG-012 |
| FR-026 | BR-059 | AC-039 | BG-007, BG-012 |
| FR-027 | BR-060 | AC-040 | BG-007, BG-008, BG-012 |
| FR-028 | BR-032 | AC-041 | BG-006 |
| FR-029 | BR-033 | AC-042 | BG-003, BG-006, BG-009 |
| FR-030 | BR-034 | AC-043 | BG-003, BG-006, BG-007 |
| FR-031 | BR-036 | AC-045 | BG-005, BG-009 |
| FR-032 | BR-037 | AC-046 | BG-003, BG-009 |
| FR-048 | None | AC-090 | BG-003, BG-009 |
| FR-033 | BR-041 | AC-051 | All (BG-001, BG-002, BG-003, BG-004, BG-005, BG-006, BG-007, BG-008, BG-009, BG-010, BG-011, BG-012) |
| FR-034 | BR-042 | AC-052, AC-080, AC-081 | BG-005, BG-010 |
| FR-035 | BR-045 | AC-055 | BG-001, BG-002, BG-003, BG-008 |
| FR-036 | BR-046 | AC-056, AC-086 | BG-003, BG-004, BG-005, BG-006, BG-007, BG-012 |
| FR-037 | BR-064 | AC-065 | BG-003, BG-005, BG-009 |
| FR-038 | BR-052 | AC-066 | BG-003, BG-004, BG-006, BG-007, BG-010, BG-012 |
| FR-039 | BR-053 | AC-067 | BG-003, BG-004, BG-007, BG-010, BG-012 |
| FR-040 | BR-055 | AC-069 | BG-003, BG-004, BG-005, BG-006, BG-007, BG-010 |
| FR-041 | BR-056 | AC-070 | BG-005, BG-007, BG-009, BG-010, BG-011 |
| FR-042 | None | AC-082 | BG-001, BG-005, BG-007, BG-009, BG-012 |
| FR-043 | None | AC-083 | BG-003, BG-005, BG-006, BG-008, BG-009, BG-012 |
| FR-044 | None | AC-084 | BG-003, BG-005, BG-006, BG-010, BG-012 |
| FR-045 | None | AC-087 | BG-005, BG-009, BG-010 |
| FR-046 | None | AC-088 | BG-005, BG-006, BG-009 |
| FR-047 | None | AC-089 | BG-005, BG-006, BG-009 |

### Business Rule Enforcement

Rules without an enforcing functional requirement are governance controls,
verified by the record named in the Verification column.

| Business rule | Legacy ID | Enforcing requirements | Verification |
| --- | --- | --- | --- |
| RULE-001 | BR-002 | FR-001, FR-006, FR-036 | AC-002 |
| RULE-002 | BR-004 | FR-038, FR-040 | AC-004 |
| RULE-003 | BR-062 | FR-003, FR-018 | AC-006 |
| RULE-004 | BR-010 | FR-028, FR-036 | AC-013 |
| RULE-005 | BR-015 | FR-013, FR-014, FR-047 | AC-019, AC-089 |
| RULE-006 | BR-020 | FR-016, FR-017, FR-046 | AC-025, AC-088 |
| RULE-007 | BR-021 | FR-019, FR-020 | AC-026 |
| RULE-008 | BR-065 | FR-022, FR-036 | AC-030 |
| RULE-009 | BR-026 | FR-023, FR-024 | AC-033 |
| RULE-010 | BR-028 | FR-024, FR-036 | AC-035 |
| RULE-011 | BR-030 | FR-025 | AC-037 |
| RULE-012 | BR-031 | FR-025, FR-033 | AC-038 |
| RULE-013 | BR-035 | FR-029, FR-030 | AC-044 |
| RULE-014 | BR-067 | FR-028, FR-029, FR-048 | AC-047, AC-090 |
| RULE-015 | BR-038 | None | AC-048; Data-owner register approved by the executive team and data governance (OD-03) |
| RULE-016 | BR-043 | None | AC-053; Readiness decision record approved by the executive sponsor |
| RULE-017 | BR-044 | FR-007, FR-010 | AC-054 |
| RULE-018 | BR-046 | FR-009, FR-036 | AC-057 |
| RULE-019 | BR-049 | None | AC-062, AC-074, AC-075, AC-076, AC-077, AC-085; Frozen Comparison 1 and Comparison 2 pilot protocol, benefits scorecard and benefits register approved by the programme board, with the Data and Performance Lead as evidence owner |
| RULE-020 | BR-050 | None | AC-063; Release decision for each phase and tranche recorded by the executive sponsor |
| RULE-021 | BR-054 | FR-038, FR-039, FR-040 | AC-068 |
| RULE-022 | BR-058 | NFR-003 | AC-072, AC-079; DPO-approved DPIA, transparency and gate record |
| RULE-023 | BR-066 | FR-022 | AC-073 |
| RULE-024 | None | None | AC-078; Guardrail breach and restart record approved by the OD-35 authority under RULE-020 |

### Legacy Identifier Map

OBJ-01 to OBJ-12 map one to one to BG-001 to BG-012. The legacy BR identifiers
map as follows.

| Legacy ID | Canonical identifiers | Acceptance criteria | Note |
| --- | --- | --- | --- |
| BR-001 | FR-001 | AC-001 | Relabelled |
| BR-002 | RULE-001 | AC-002 | Relabelled |
| BR-003 | FR-002 | AC-003 | Relabelled |
| BR-004 | RULE-002 | AC-004 | Relabelled |
| BR-005 | FR-005 | AC-008 | Relabelled |
| BR-006 | FR-006 | AC-009 | Relabelled |
| BR-007 | FR-007 | AC-010 | Relabelled |
| BR-008 | FR-008 | AC-011 | Relabelled |
| BR-009 | FR-009 | AC-012 | Relabelled |
| BR-010 | RULE-004 | AC-013 | Relabelled |
| BR-011 | FR-011 | AC-015 | Relabelled |
| BR-012 | FR-012 | AC-016 | Relabelled |
| BR-013 | FR-013 | AC-017 | Relabelled |
| BR-014 | FR-014 | AC-018 | Relabelled |
| BR-015 | RULE-005 | AC-019 | Relabelled |
| BR-016 | NFR-001 | AC-020 | Relabelled |
| BR-017 | FR-016 | AC-022 | Relabelled |
| BR-018 | FR-017 | AC-023 | Relabelled |
| BR-019 | FR-018 | AC-024 | Relabelled |
| BR-020 | RULE-006 | AC-025 | Relabelled |
| BR-021 | RULE-007 | AC-026 | Relabelled |
| BR-022 | FR-019 | AC-027 | Relabelled |
| BR-023 | FR-020 | AC-028 | Relabelled |
| BR-024 | FR-021 | AC-029 | Relabelled |
| BR-025 | FR-023 | AC-032 | Relabelled |
| BR-026 | RULE-009 | AC-033 | Relabelled |
| BR-027 | FR-024 | AC-034 | Relabelled |
| BR-028 | RULE-010 | AC-035 | Relabelled |
| BR-029 | FR-025 | AC-036 | Relabelled |
| BR-030 | RULE-011 | AC-037 | Relabelled |
| BR-031 | RULE-012 | AC-038 | Relabelled |
| BR-032 | FR-028 | AC-041 | Relabelled |
| BR-033 | FR-029 | AC-042 | Relabelled |
| BR-034 | FR-030 | AC-043 | Relabelled |
| BR-035 | RULE-013 | AC-044 | Relabelled |
| BR-036 | FR-031 | AC-045 | Relabelled |
| BR-037 | FR-032 | AC-046 | Relabelled |
| BR-038 | RULE-015 | AC-048 | Relabelled |
| BR-039 | NFR-002 | AC-049 | Relabelled |
| BR-040 | NFR-003 | AC-050 | Relabelled |
| BR-041 | FR-033 | AC-051 | Relabelled |
| BR-042 | FR-034 | AC-052 | Relabelled |
| BR-043 | RULE-016 | AC-053 | Relabelled |
| BR-044 | RULE-017 | AC-054 | Relabelled |
| BR-045 | FR-035 | AC-055 | Relabelled |
| BR-046 | FR-036, RULE-018 | AC-056, AC-057 | Split into single-obligation requirements |
| BR-047 | NFR-004 | AC-058 | Relabelled |
| BR-048 | NFR-005, NFR-006, NFR-007 | AC-059, AC-060, AC-061 | Split into single-obligation requirements |
| BR-049 | RULE-019 | AC-062 | Relabelled |
| BR-050 | RULE-020 | AC-063 | Relabelled |
| BR-051 | NFR-008 | AC-064 | Relabelled |
| BR-052 | FR-038 | AC-066 | Relabelled |
| BR-053 | FR-039 | AC-067 | Relabelled |
| BR-054 | RULE-021 | AC-068 | Relabelled |
| BR-055 | FR-040 | AC-069 | Relabelled |
| BR-056 | FR-041 | AC-070 | Relabelled |
| BR-057 | NFR-009 | AC-071 | Relabelled |
| BR-058 | RULE-022 | AC-072 | Relabelled |
| BR-059 | FR-026 | AC-039 | Relabelled |
| BR-060 | FR-027 | AC-040 | Relabelled |
| BR-061 | FR-015 | AC-021 | Relabelled |
| BR-062 | FR-003, RULE-003 | AC-005, AC-006 | Split into single-obligation requirements |
| BR-063 | FR-004 | AC-007 | Relabelled |
| BR-064 | FR-037 | AC-065 | Relabelled |
| BR-065 | RULE-008 | AC-030 | Relabelled |
| BR-066 | FR-022, RULE-023 | AC-031, AC-073 | Split into single-obligation requirements |
| BR-067 | RULE-014 | AC-047 | Relabelled |
| BR-068 | FR-010 | AC-014 | Relabelled |

## Validation and Approval Criteria

Approval is stage-specific under RULE-020. Approval to gather evidence is not
approval to deploy AI, instruct works, commit portfolio capital or claim grant.
Every phase decision records its budget, delegated authority, requirements,
evidence, unresolved decisions and accountable owners.

### Readiness and Shadow Approval

Exercise build acceptance under CON-007 is distinct from shadow/live
authority. AC-086/PRD AC-057 require the changed build's actual Azure
workflow, SQL durability and enabled AI proof; unchanged resources may be
reused, not merely assumed connected. Record current source/image/revision
and separate recorded #58 observations from newer undeployed source tests.
Full workflow, permissions, performance/recovery and direct human acceptance
are not established by one successful inference or restart.

Record effective build budget, scope and approval/override, including
accrued/unbilled liabilities. EXA-012 USD 450/360/405 limits are historical;
#58's owner cap removal applies to that rebuild, not all future spending.
Source/task/input bounds, upper-liability reservations and usage/cost
telemetry remain. Missing budget/authorization blocks acceptance, never
licenses mock substitution or silently waives spend controls.

* The sponsor and Finance approve a capped readiness envelope and named owners
  for open decisions.
* Before any Phase 0 pilot or comparison event capture, the frozen RULE-019
  protocol, OD-18 comparison decision and OD-36 DPIA and lawful measurement
  basis are approved. Shadow testing additionally requires the binding constraint
  and options appraisal, pilot scope, baselines, proposed targets, guardrails,
  explanation-quality measures, automation-bias thresholds, cost inclusions and
  no-live-action controls to be accepted.
* Shadow activity has no live consequential permissions or resident contact;
  any use of real data has approved access and data-protection controls.

### Live-Pilot Approval

* All applicable Must requirements have named owners and accepted test evidence.
* The approved RULE-019 protocol defines Comparison 1 and Comparison 2, frozen
  metrics, identical event capture, the OD-36 DPIA and lawful measurement
  basis, the benefits scorecard, operational dashboard limits, assurance, cost
  treatment and guardrail stop triggers.
* Current regulatory rules, professional competence and authority boundaries
  are confirmed.
* Property and building controls, planned-maintenance alignment, approved
  designs, resident decisions and supplier capacity are verified before the
  respective controlled transitions.
* Representative resident journeys, adjustments, complaints and human handoffs
  have been tested before live contact.
* Pilot homes have verified tenure and lease-interest status, deterministic
  eligibility and funding-route results, and a tested hazard referral route
  from every retrofit channel (FR-003, FR-015, FR-026, FR-027, RULE-003).
* DPIA, privacy notice updates, published plain-language AI statement, access,
  explanation records, AI output provenance, evidence provenance, integration
  reconciliation, supplier model-change terms, disable mechanisms, manual
  continuity and recovery are accepted by the responsible owners.
* Finance accepts the pilot budget, verified funding position and monthly
  cash and downside model; unawarded grant is not committed funding.
* In-use follow-up, AI capability register ownership, Board AI assurance
  cadence and all unresolved issues have owners and dates. No issue blocking a
  relevant safety, resident, technical, financial, data-protection or
  transparency gate is deferred.
* A guardrail breach pauses affected work regardless of throughput under
  RULE-024. Any restart uses the authority and evidence agreed under OD-35 and
  RULE-020.

### Tranche and Scale Approval

* Independent assurance and control owners review the complete pilot
  scorecard, including errors, complaints, AI-involved challenges, unsupported
  claims, explanation fidelity, automation-bias indicators, pauses, excluded and
  reopened cases.
* The chosen option demonstrates attributable value after technology,
  integration, operating, human-review and assurance costs. Failure of the AI
  value case can result in a non-agentic option or a stopped expansion.
* Physical quality, resident outcomes, competent and supplier capacity,
  funding and financial headroom support the next tranche.
* Pending seasonal evidence is disclosed with follow-up and decision limits;
  unobserved bill savings or absence of harm are not claimed as proven.
* The Board approves acceleration beyond the annual plan, the next investment
  envelope and downside tolerances. Later authority changes require separate
  evaluation; no approval removes the prohibited-decision boundaries.
* Breaches trigger containment and pause under RULE-012 and RULE-020. Restart
  requires remediation evidence and the relevant control owners' approval,
  plus Board approval where its risk or investment envelope is affected.

## Source and Review Record

The 2026-10-14 candidate amendment (v0.17.0) follows the
[customer journey atlas](../reference/research/ux/customer-journeys/customer-journey-atlas.md),
the updated addendum and the retained v0.16.0 owner direction. It adds FR-045
to FR-048, AC-087 to AC-090, OD-41 to OD-43, and refines AC-011, AC-023 and
AC-065. FR-048 and OD-43 capture in-use monitoring (IoT) data from the owner request and the
[sensor data-flow design in ADR 0002](../adrs/0002-pilot-readiness-architecture.md); the BRD names no device or platform. The atlas is role-instrument desk research; no resident, staff or
contractor was observed, and no company fact, target or approval follows. The
Zava naming, five-assistant operator evidence and draft-experiment closure in
the addendum are recorded there and in the PRD and ADRs, because they change
no business requirement. Fresh quality review and owner acceptance remain
separate from this amendment.

The 2026-10-11 candidate amendment follows the owner's mandatory real
AI/SQL/Azure direction, pinned #58 source/results and the independent
decision-model experiment boundary. See the addendum's Subsequent Application
Exercise Builds and the dated model/simplicity syntheses. These are
exercise-owner decisions and reported technical observations, not company
facts, new regulatory claims, approved BRD targets or measured business benefit.
Counts are 48 FRs, 90 ACs, 9 NFRs, 7 constraints, 24 rules and 43 open decisions; existing
functional IDs and human authority boundaries are retained. Fresh full-BRD
quality/business review remains required; RPI outcome review does not ratify
BG-011 or close the formal approval gate.

This draft integrates:

* [Original Case Study 48](../case_study_48_original.md)
* [Case Study 48 Addendum](../case_study_48_addendum.md)
* [Capstone Rubric Review of the Agentic Retrofit Programme BRD](../reference/research/company/capstone-brd-rubric-review.md)
* [Case Study 48 Addendum - Executive Solution Proposal](../case_study_48_addendum.md)
* [Company Profile Research](../reference/research/company/company-profile-research.md),
  including the Modelled Customer Profile added on 25 September 2026
* [Housing Association Primer](../reference/research/sector/housing-association-primer.md)
* [Agent Request Challenge](../reference/research/company/agent-request-challenge.md)
* [Pilot Measurement Challenge](../reference/research/company/pilot-measurement-challenge.md),
  a 26 September 2026 role-agent panel whose findings are sector-informed
  hypotheses and proposals, not company facts
* [System One Decision Models for Retrofit Agents](../ideas/typesafe-system-one-agent-fit.md)
* [UK Social Housing Baseline Research](../reference/research/sector/uk-social-housing-baseline-research.md)
* [Retrofit Flow and Constraint Discovery Brief](./retrofit-flow-discovery-brief.md)
* [UK Social Housing Baseline Source Register](../reference/research/sector/uk-social-housing-baseline-source-register.md)
* [Regulatory Context Reference Documents](../reference/regulatory/README.md)
* Reviews from the Housing Asset Executive, Building Safety Lead, Finance and
  Grants Lead, Neighbourhood Housing Officer, Procurement and Contracts Lead,
  Resident Engagement Lead, Retrofit Programme Manager and Data and
  Performance Lead

The Housing role reviews provide sector-informed recommendations. They do not
replace resident research, competent professional judgement, formal governance
or legal advice.

The 30 September 2026 capstone review assessed this BRD against all 20 FY27 AMA
criteria. It found a strong design and governance foundation but no working
evidence for implementation completeness, observability, demo delivery or
dissemination. Version 0.6.0 therefore separates a complete non-production
demonstrator from shadow and live operational authority and adds a Board
decision narrative. This change does not validate any business outcome or
authorise live use.

The 11 September 2026 addendum review informs the revised digital foundation,
pilot gates, value attribution and new requirements. Pilot sizes, durations
and improvement targets remain proposals. The financial qualifications above
clarify the full-cap home equivalent and unspecified cost inclusions without
changing either source document. The 20 September 2026 legal-corpus and
user-journey reviews inform FR-038, FR-039, FR-040, FR-041, RULE-021, RULE-022, NFR-009.

The 26 September 2026 owner decision reframed the BRD as agent-led
modernisation of the existing retrofit model, with Comparison 1 and Comparison
2 measuring agent value and OD-34 marked as a proposed resolution pending
Sponsor, Executive Director of Assets and Finance confirmation.

The 26 September 2026 BRD review integrated the modelled customer profile,
the housing association primer, the agent request challenge and the pilot
measurement challenge. Gaps in the BRD were put as focused questions to the
Building Safety, Resident Engagement, Procurement, Finance, Retrofit Programme
and Data and Performance role agents, and their proposed wording informs
FR-003, FR-004, FR-010, FR-015, FR-022, FR-025, FR-026, FR-027, FR-037,
RULE-003, RULE-008, RULE-014, RULE-019, RULE-024, AC-062, AC-074 through
AC-078 and OD-26 through OD-38.
The role agents had no company data. Regulatory citations in those
requirements were checked against the local snapshots on 26 September 2026,
not against the official sources online. Specialist input is not
organisational approval; named human owners must validate this BRD before the
relevant release.

The 5 October 2026 operating-model review adds a proposed home-centred
workbench flow with linked building, home, work-package and service-case
records; distinct resident service/defect intake, provider invoice and Finance
grant-claim paths; role-oriented queues; and source-linked agent next-step
suggestions. It draws on the constructed retrofit operating-data exercise
dictionary and
the `feat/zava-forward-prototype` review at commit `5e52ceb`. These are design
proposals, not company-validated process or authority. Payment milestones,
contract terms, resident channels, service ownership, response targets and
approval limits remain open; no payment timing or compensation process is
assumed.

The 26 September 2026 explainability and transparency review updated CON-003,
RULE-022, FR-034, FR-040, NFR-006, FR-041, RULE-019 and RULE-024, and added
FR-042, FR-043, FR-044, AC-079 through AC-085 and OD-39. The review cited the
UK GDPR current-text snapshot, the Safety and Quality Standard 2024 snapshot,
the regulatory source register and the Awaab's Law Phase 2 guidance only as a
secondary reference for the Transparency, Influence and Accountability Standard
pending OD-39.

On 26 September 2026 a BRD quality review graded this draft against the
canonical requirements rubric. It found the requirements substantive but
blocked the Define gate because the legacy BR and OBJ identifiers gave 0.0%
canonical FR-to-AC and FR-to-BG coverage. The requirement set was then
relabelled to the canonical taxonomy with legacy aliases, four compound rows
were split and six constraints were extracted. The quality report is kept in
the BRD session evidence, and the review is repeated after each material
revision.
