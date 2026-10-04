---
title: Case Study 48 Addendum - Executive Solution Proposal
description: Critical assessment, solution trade-offs and business value for the retrofit programme
ms.date: 2026-10-04
ms.topic: reference
---

## Purpose and Status

Read this addendum alongside the unchanged
[original Case Study 48](./case_study_48_original.md) and its
[Business Requirements Document](./brds/agentic-retrofit-programme-brd.md).
The original case study records the request exactly as first committed. This
addendum contains every later addition to that request and provides the
critical assessment, proposed solution, trade-offs, business value and
conditional executive investment recommendation.

The recommendations are proposals for validation, not approved requirements
or observed outcomes. Sector benchmarks and illustrative economics are not
company facts. Where this addendum challenges the original claims or autonomy
levels, the distinction is intentional; the original remains unchanged.

### Capstone Review Gate

The final presentation, architecture and pitch must each be checked and
challenged against the complete
[Capstone Assessment Guide](./reference/method/ama-capstone-assessment-guide.md)
before they are treated as ready. The review must use the published criteria
and descriptors, cite the evidence for each judgement, expose gaps and
assumptions, and apply the section and individual-criterion floors rather than
relying on an overall score.

### Additions Since the Original

The following information was introduced after the original case study and is
preserved in this addendum:

* The association name, Proper North Homes, and programme name, Proper Warm
* The owner-confirmed fact that Proper North Homes is a not-for-profit
  organisation, while its exact legal form and charitable status remain
  unknown
* The working presentation line, "Ready, steady, retrofit," with legal,
  trademark and resident-communication restrictions
* The clarified objective of moving homes toward EPC C while the 2030 standard
  remains a proposal
* The provisional sector baseline and its evidence classifications
* The derived delivery, programme-cost and grant-ceiling scenarios
* The supporting baseline-research reference and its limitations
* The reference to the modelled customer profile in company research, whose
  values are modelled estimates, not company facts
* The research-backed caveat and owner-directed provisional missed-appointment
  escalation rule, pending company evidence and Housing/Repairs ratification
* The executive challenge, modernised retrofit delivery objective, digital
  foundation for agents, delivery gates, success measures, trade-offs and
  conditional recommendation
* The pilot measurement challenge, including Comparison 1, Comparison 2,
  benefits scorecard, guardrails and counterfactual caveat

## Proper Warm at Proper North Homes

| Field | Details | Field | Details |
| --- | --- | --- | --- |
| Industry | Real Estate (Affordable Housing) / Decarbonisation | Headquarters | United Kingdom |
| Operating Region | United Kingdom (North of England) | Regulatory Context | UK Net Zero; final SRS MEES policy not yet evidenced as commenced law; Social Housing Regulation Act; Awaab's Law; UK GDPR; PAS 2035 retrofit standard |
| Association | Proper North Homes | Programme | Proper Warm |
| Operating purpose | Not-for-profit, confirmed by the project owner on 26 September 2026 | Legal form | Unknown; do not infer charitable status, registration or group structure |

The working presentation line is "Ready, steady, retrofit." The name is not
cleared for legal, trademark, domain or resident-facing use. It must not be used
for hazard, complaint, safeguarding or consent communications.

## Business Challenge

Proper North Homes is a housing association with 60,000 homes. It is planning
for the final government SRS MEES policy position while the downloaded evidence
does not yet establish a commenced 2030 landlord duty. It must also respond to
damp and mould within statutory timescales under Awaab's Law.
A small team holds a complex programme together through spreadsheet-based
coordination across retrofit assessments, grant applications, contractor
procurement, resident consent and quality assurance, and progress is far
behind plan.

The spreadsheet dependency shows how much coordination currently rests on a
small team. It is not yet proven to be the main constraint on delivery.
Capital, competent people, supplier capacity, property data, resident access,
technical complexity, quality failure and grant conditions may be equally or
more important. Automating current administration before identifying the
binding constraint could make unreliable decisions faster without increasing
safe, accepted completions.

## Provisional Sector Baseline

Research completed on 11 September 2026 provides an initial planning benchmark,
not company facts:

| Measure | Provisional benchmark | Evidence status |
| --- | --- | --- |
| Homes at EPC C or above | 74%, or 44,400 homes | England social-rented estimate |
| Homes below EPC C | 26%, or 15,600 homes | Derived planning benchmark |
| Four-year accepted-completion trajectory | 3,900 homes per year | Derived scenario |
| Surveyor-assessed damp | 6% HA benchmark, or 3,600 homes | Stock-prevalence estimate |
| Resident-reported damp, mould or condensation | 39% HA benchmark, or 23,400 households | Lived-experience estimate |
| Repairs satisfaction | 73.6% | RSH landlord median |
| Complaint-handling satisfaction | 35.5% | RSH landlord median |
| Stage-one complaints | 54.5 per 1,000 homes, or about 3,270 per year | RSH landlord median translated to stock |
| Ordinary WH:SHF Wave 3 grant cap | GBP 7,500 per home with normally at least 50% co-funding | Scheme limit, not an award |
| First-appointment no-access | 10% central; 5% to 15% sensitivity | Planning assumption only |
| Discretionary retrofit refusal or withdrawal | 5% to 10% | Planning assumption only |

The initial below-C scenario implies 3,900 accepted completions per year. A
GBP 20,000 fully loaded planning assumption gives a GBP 312 million gross
programme, with a maximum GBP 117 million ordinary grant ceiling before
eligibility and award constraints. The stated GBP 40 million remains an
unsecured opportunity and would support at most about 5,333 homes at the
GBP 7,500 cap.

Full sources, limitations and alternative sensitivities are recorded in
[UK Social Housing Baseline Research](./reference/research/sector/uk-social-housing-baseline-research.md).

### Missed-Appointment Escalation Evidence (2026-10-04)

The public evidence reviewed does not validate five missed appointments as a
UK housing-sector threshold. The [Inside Housing/Localz survey](https://www.insidehousing.co.uk/sponsored/counting-the-cost-of-missed-repairs-appointments)
reports organisation-level missed-appointment bands, while [Aspire Housing's
published no-access figures](https://www.aspirehousing.co.uk/you-and-your-home/myhome/myhome-summer-26/no-access/)
are provider-specific and do not establish repeated-event criteria. [Stevenage
Borough Council's no-access policy](https://www.stevenage.gov.uk/documents/housing/policies-and-strategies/no-access-policy.pdf)
uses a three-contact sequence for statutory compliance checks, not a general
missed-repair threshold. The [government resident-panel report](https://www.gov.uk/government/publications/social-housing-resident-panel-reports-2022-to-2023/repairs-maintenance-and-awaabs-law-resident-panel-report-accessible-version)
is explicitly not statistically representative; the [RSH Tenant Satisfaction
Measures technical requirements](https://www.gov.uk/government/publications/tenant-satisfaction-measures-technical-requirements)
and [Housing Ombudsman repairs guidance](https://www.housing-ombudsman.org.uk/centre-for-learning/learning-hub/knowledge-and-information-management/)
do not establish a comparable repeat no-access measure or numeric threshold.
These sources differ in definitions, populations and denominators and must
not be pooled as a benchmark.

The owner directs a configurable default of five, with a strict greater-than
comparator: the sixth eligible event triggers human review. Count only a
confirmed appointment with a verified resident no-access outcome. Record
provider/contractor no-shows, cancellations and reschedules separately; they
do not count. Count events while the same case remains active and reset the
counter only when a human closes the case, retaining the event history for
audit. The rule triggers investigation and corrective action, not a finding
of refusal or non-cooperation, and must not delay an urgent hazard response.

This is a provisional owner-directed draft rule, not a validated sector norm
or Proper North Homes policy approval. Housing and Repairs must ratify the
event definition, case lifecycle, configuration/change authority and handoff
arrangements against the association's own appointment records, with
Resident Engagement review. No company baseline or operational approval has
been supplied.

A modelled profile of Proper North Homes, covering its likely archetype,
tenure mix, leaseholders and resident indicators, is recorded in the
[Modelled Customer Profile](./reference/research/company/company-profile-research.md#modelled-customer-profile)
of the company profile research. Its values are modelled estimates from
sector medians and national rates, and company details are not yet
confirmed. It is not copied here and must not be read as company fact.

## Executive Assessment

The case for improving retrofit delivery is credible. The case for immediately
building five end-to-end agents is not yet proven.

The 42 controls in the supporting
[Business Requirements Document](./brds/agentic-retrofit-programme-brd.md)
describe a portfolio workflow, evidence, integration and assurance capability,
not a quick agent deployment. The association should therefore approve a
gated discovery and pilot, not a portfolio-wide autonomous implementation or
capital acceleration.

> [!IMPORTANT]
> The strategic proposition is an agent-led modernisation of the association's
> existing retrofit model. Existing teams, suppliers, professional roles and
> systems remain; agents take on manual coordination, chasing, re-keying,
> reconciliation and evidence assembly. The agents earn the right to scale only
> by increasing safe, resident-accepted and evidence-complete handovers at an
> affordable risk-adjusted cost.

### Regulatory Evidence and Service Design

The legal and regulatory corpus in
[Regulatory Context Reference Documents](./reference/regulatory/README.md) is a dated
evidence set for research and for the proposed solution. It is not a
self-updating legal authority. The service needs a managed source register,
versioned snapshots, official-source monitoring and human approval before a
detected change alters an operational rule.

The regulatory operating model should:

* Prefer consolidated legislation, regulator publications and applicable grant
  or contract terms over guidance, impact assessments and consultations
* Record source authority, jurisdiction, retrieval and effective dates,
  applicability, supersession, change likelihood and accountable owner
* Detect official-source changes automatically, but route differences through
  legal, compliance, data-protection, funding or competent-professional review
* Link each approved interpretation to requirements, deterministic rules,
  communications, evidence templates, tests and decisions
* Preserve the last approved version and provide rollback, audit and effective
  date control
* Increase monitoring around announced commencement dates, new funding rounds,
  consultations and standards revisions

Service design must make lawful work easier and faster for four user groups.
Employees need one evidence pack, named queues, clear authority and fewer
repeated entries. Residents need accessible choices, human and non-digital
routes, reliable appointments, explanations, correction, complaint and
aftercare. Contractors need complete work orders, minimum necessary resident
information and precise evidence checks. Officials, funders and regulators
need traceable, versioned and reusable assurance packs with unresolved
exceptions visible.

Automation must not trade speed for rights or safety. A source update, sensor
reading, missed contact or generated interpretation cannot diagnose a hazard,
infer consent, remove a resident's priority, satisfy a statutory duty, approve
professional work or certify an external submission.

### What We Are Challenging

| Initial proposition | Executive challenge | Required evidence |
| --- | --- | --- |
| Double retrofit delivery | Current accepted throughput and causes of delay are unknown | Twelve-month baseline by archetype, measure, stage, delay cause and reopened defect |
| Capture GBP 40 million of grant | This is an opportunity, not an award, claimable value or cash receipt | Award evidence, eligible-property schedule, match requirement, claim profile and receipt timing |
| Protect hundreds of millions of borrowing capacity | No causal treasury or lender model supports the amount | Covenant, liquidity, security, valuation and refinancing sensitivity approved by Finance |
| Lower resident energy bills | Bills may fall, remain stable or rise as previously under-heated homes become warmer | Property-specific assumptions and measured energy, affordability, comfort and ventilation outcomes |
| Use agents to run PAS 2035 assessments | Competent professionals must own assessment, design, coordination and evaluation | Named roles, competence, capacity, current standards and controlled professional approvals |
| Automate resident and contractor coordination | Automation can amplify pressure, exclusion, missed adjustments and supplier failure | Tested resident journeys, committed capacity, human exception ownership and manual fallback |
| Use sensors to identify health risk and verify quality | Sensors provide partial evidence and cannot overrule a resident report or competent inspection | Lawful purpose, data quality, maintenance model and evidence of predictive value |
| Measure acceleration with a dashboard | A dashboard can steer work but cannot prove benefits if definitions change, cohorts are selected for success or safety holds are pressured | Frozen protocol, concurrent comparison, benefits scorecard, assurance and guardrails that pause affected work |

### Challenge of the Requested Agents

On 2026-09-26 the eight Proper North Homes role agents challenged each
requested agent's "owns end-to-end" line. No role supported building any of
the five as an end-to-end agent. Each request combines three things:
deterministic control work, accountable human decisions, and a smaller set
of tasks where bounded AI helps. Those tasks are reconciliation, reading
evidence, drafting, message routing and raise-only signal scanning. Every
request also depends on the same shared records, which is further evidence
for the digital foundation below. These are sector-informed role hypotheses, not
company findings. The per-agent problems, alternatives, stop criteria and
open questions are recorded in the
[Agent Request Challenge](./reference/research/company/agent-request-challenge.md).
The BRD review of the same date turned these findings, and the modelled
customer profile, into proposed requirements BR-059 through BR-068 and open
decisions OD-26 through OD-33. They cover eligibility and funding route,
tenure, hazard awareness from retrofit channels, vulnerability data,
contractor instructions, quality assurance when nothing is flagged, and
separate PAS 2035 sign-offs. They remain proposals for owner validation.
The BRD has since relabelled its requirements to canonical FR, AC, NFR, CON,
RULE and BG identifiers. BR-### and OBJ-## references in this addendum remain
valid legacy aliases, resolved by the BRD's Legacy Identifier Map.

On 2026-09-27 a follow-up what-if session tested whether richer inputs would
move any of the five verdicts. It ran 20 scenarios, two or three per requested
agent, from phone photos with EXIF GPS, structured digital invoices and
app-based consent to funder-portal integrations, ambient sensors and call
transcription. It scored each scenario on value against complexity. The role
agents' clarification answers, revised verdicts and grid are recorded in the
[Agent What-If Study](./reference/research/company/agent-what-if-study.md).
The headline verdict is unchanged: the augmentations enrich the digital
foundation and expand bounded AI's useful checks, but they do not create an
end-to-end agent. They expand UK GDPR Article 9 and Articles 22A to 22C,
Awaab's Law, Construction Act and Procurement Act 2023 duties before they
expand autonomy. A post-merge review the same day confirmed the verdict
against the agent-led modernisation reframe. It corrected the automated-decision
citations and re-ran answers first attributed to roles without an agent. It
also positioned the grid as a candidate order for Phase 0 and Comparison 2
testing, not a scaling decision. All role-agent answers were then re-run
against the current proposal, and the verdict still holds. Six answers
tightened the study's controls to match the BRD:

* photo and transcript scans only raise flags for human triage and never
  set or back-date a clock
* AI-proposed PAS 2035 risk paths stay in blind shadow mode until released
* suppliers offer capacity through any channel
* a named person approves every AI-drafted resident message
* programme supervision has no AI summarisation in the initial pilot

## Modernised Retrofit Delivery Objective

Modernise the association's existing retrofit delivery model with agents,
supported by the digital foundation they need:

* Establish a shared stock, condition, safety and energy record
* Align retrofit with planned maintenance, building safety and the long-term
  asset plan
* Move each home through explicit technical, resident, supplier, funding,
  quality and handover stages
* Name handoff owners so agents can chase, reconcile and assemble evidence
  without taking decisions from people
* Use deterministic workflow for mandatory controls and bounded AI for
  recommendations, drafting, reconciliation and exception detection
* Preserve accountable human authority for safety, professional judgement,
  resident decisions, investment, procurement, payment, grant submission and
  quality acceptance
* Measure accepted resident and asset outcomes rather than starts, automated
  actions or nominal installations

## Solution Proposal

### Executive Proposition

Invest in bounded retrofit agents and the digital foundation they need to turn
verified property need, resident readiness, competent capacity and committed
funding into safe, quality-adjusted outcomes. Begin with one locality using
existing teams and suppliers, then scale only the agent capabilities that
demonstrate measurable value over matched existing delivery without weakening
controls.

This positions the programme as an agent-led modernisation of the existing
retrofit model that builds on the teams, suppliers and systems already in
place. It avoids asking the Board to approve an artificial intelligence
platform before the physical programme, financial envelope and delivery
constraints are understood.

### Digital Foundation for Agentic Delivery

The digital foundation should connect existing asset, repairs, housing,
finance, procurement and contractor systems rather than replace every service.
It should maintain a property-level lifecycle, a building-level parent record
where work affects shared systems or higher-risk buildings, and a portfolio
view for investment decisions.

Deterministic rules should control:

* Safety holds, statutory response clocks and emergency handoffs
* Mandatory evidence, validity periods and material-change rules
* Resident decisions, withdrawals, pauses and accessibility adjustments
* Delegated authority, segregation of duties and approval limits
* Funding, budget, supplier-capacity, payment, claim and closure gates
* Property scoring weights, grant eligibility and funding-route rules
* Lifecycle states, queues, handoff ownership and programme reporting
* Version history, audit, reconciliation and fail-closed behaviour

### Where Agents Fit and Where They Do Not

Where a decision must follow clear rules and be transparent, repeatable and
explainable to residents, regulators, funders or the Board, the programme uses
a deterministic approach. Examples are eligibility, scoring, statutory clocks,
gates, consent status and approvals. An agent adds risk there, because its
output can vary and is harder to audit.

Agents add value where the work is unstructured, incomplete or text-heavy:

* Turning free text, survey notes, emails, documents and photos into concrete,
  sourced values for the rules and the benefits measures
* Filling gaps by proposing a missing value with its source and confidence,
  for the data owner to confirm, and never inventing an observation
* Reconciling conflicting records and flagging missing, stale or contradictory
  evidence
* Drafting packs, letters and explanations from approved records for a person
  to review
* Routing messages into fixed categories and raising possible hazard or quality
  signals for human triage

AI must not diagnose hazards, decide that a statutory duty is satisfied,
release a safety hold, approve professional work, infer consent, commit capital,
award work, submit claims, accept quality, close complaints or defects, or use
the absence of a sensor alert to contradict a resident.

### Agentic Architecture Brief

The pilot places agents only where the
[Agent Request Challenge](./reference/research/company/agent-request-challenge.md)
found a plausible gain. Programme supervision and portfolio reporting stay
deterministic in the initial pilot; later summarisation support would need its
own test.

| Capability | Deterministic core | Where an agent helps | Proposed business value measure | Accountable human authority |
| --- | --- | --- | --- | --- |
| Property data and prioritisation | Versioned, published scoring weights; pass, fail or unknown eligibility rules; data validity rules | Reconcile conflicting legacy records; extract condition facts from free-text survey notes; flag missing or stale fields; explain each score in plain language | Data reconciliation time; critical conflicts found before survey; homes still viable after survey | Asset and safety owners approve cohort rules and exceptions; named data owners confirm proposed values |
| PAS 2035 assessment preparation | Stage gates; separate assessor and coordinator sign-off; material-change rules; safety-hold check | Pre-populate sourced facts; turn survey notes into structured assessment inputs; check completeness before sign-off | Assessment-to-ready-to-install time; returns and re-approvals per home | Competent assessors, designers, coordinators and evaluators own professional outputs |
| Grant and funding evidence | Four-state grant ledger; eligibility and route rules; monthly reconciliation; claim holds | Match installation evidence to the per-measure schedule; assemble draft claim packs from approved records, only once the ledger exists and an award or open route is evidenced | First-time grant evidence acceptance; rejected or clawed-back value; time to claim | Finance validates, approves and submits |
| Resident service | Measure-specific decision record; adjustments; pauses; failed access never recorded as refusal | Draft accessible content; route free-text messages into fixed categories; suggest options | Repeat resident contacts; adjustments met; first appointments kept | Residents decide on discretionary measures; staff own support, exceptions and redress |
| Supplier coordination | Committed-capacity register; standard work orders; appointment outcome codes; instructions only from contract managers | Suggest appointment slots within committed capacity; convert contractor emails and notes into outcome codes | Coordination hours per accepted home; supplier-caused appointment failures | Contract manager accepts capacity; programme releases work |
| Quality evidence assurance | Per-measure evidence checklist; defect severity rules; independent acceptance | Read documents and photos; raise gaps and anomalies; never clear or accept | Evidence rework; right-first-time evidence acceptance; defects found before handover | Competent quality authority accepts work and closes defects |
| Hazard signals | Statutory clocks and awareness timestamp in the existing repairs and hazard service | Raise-only scan of retrofit notes and messages for possible damp, mould or safety signals, routed to human triage | Awareness-to-referral time for retrofit-channel hazards | Hazard and repairs service owns categorisation, clocks and closure |
| Programme supervision and reporting | Lifecycle states, queues, clocks, audit and reports built from controlled records | No agent in the initial pilot | Queue ageing and unowned handoffs, reported as operational measures | Programme owns the workflow; executives and the Board make investment and risk decisions |

The value measures are proposals for the benefits scorecard, not forecast
results. Each agent capability scales only if Comparison 2 shows it beats the
same deterministic workflow without the agent once review effort is counted.
Draft acceptance, review minutes and missed critical exceptions apply to every
agent capability.

Typed decision models that return closed-set answers and probabilities, rather
than generated text, are an implementation option under research for some of
these capabilities. The strongest candidate fits are resident and contractor
message routing and quality evidence flags. This remains an unvalidated
proposal for Phase 1 shadow-mode comparison, recorded in
[System One Decision Models for Retrofit Agents](./ideas/typesafe-system-one-agent-fit.md)
and the [Idea Register](./ideas/idea-register.md).

### Implementation Options and Provisional Platform Recommendation

This assessment records the owner's 3 October 2026 request to compare Azure
development with Microsoft 365 and business-platform solutions before
justifying a platform choice. The owner prefers Azure for the Azure Master
Architect (AMA) project and their Solution Architect practice. This is a
capstone preference, not evidence that Azure is the best customer investment.
The recommendation below is a proposal, not an approved architecture,
procurement decision or validated company requirement.

On 4 October 2026 the owner directed that Azure-led hybrid be used only as the
provisional baseline for a non-production demonstrator. The customer and
production architecture remain open for the Phase 0 options appraisal under
BRD OD-16 and OD-20. This direction is not customer architecture, procurement
or investment approval.

On 3 October 2026 the owner confirmed that Proper North Homes currently uses
Excel files for this coordination and does not have Dataverse or Dynamics 365.
This is owner-confirmed company context. The existing Microsoft 365 tenant,
SharePoint availability, licences, governance, retention configuration and
support capability remain unverified. The business-apps alternative would
therefore be a greenfield platform adoption in this comparison, not reuse of
an existing Dataverse or Dynamics 365 estate.

The key choice is where programme state, business controls and evidence
authority live, not whether a conversational Copilot is present. The
[BRD](./brds/agentic-retrofit-programme-brd.md), Digital Foundation and Authority,
requires a controlled property lifecycle with bounded AI. RULE-016 and AC-053
require comparison of process redesign, existing platform configuration,
conventional workflow integration and bounded AI before solution selection.
Improving or configuring existing systems without AI therefore remains the
baseline against which these implementation options must earn their cost.

#### Comparable Implementation Options

| Option | Proposed implementation | Principal advantage | Principal trade-off |
| --- | --- | --- | --- |
| Azure custom application | Programme workbench, domain APIs, transactional programme store, durable workflow, integration adapters and Foundry-based AI capabilities | Direct control over contracts, evaluation, telemetry, resilience and user experience | Highest bespoke engineering and ongoing operational responsibility |
| Business-platform-led | Greenfield Power Apps and Dataverse, Power Automate, Copilot Studio and SharePoint documents; no current Dataverse or Dynamics 365 estate is available for reuse | Could offer a managed low-code platform if the organisation adopts, licenses and supports it | Requires new platform adoption and operating capability; licensing, capacity, migration, integration and governance need full costing and validation |
| Azure-led hybrid | Azure owns the programme control layer and bounded AI services; M365 supplies documents, collaboration and optional staff-facing agent channels | Customise distinctive controls while reusing commodity capabilities | Cross-platform identity, permissions, evidence ownership and support boundaries must be explicit |

SharePoint, OneDrive and M365 Copilot alone are not the strongest comparator
for the full BRD. A fair business-platform option includes Dataverse or an
existing operational system for structured records and controlled transitions.
Proper North Homes has no Dataverse or Dynamics 365 estate to reuse, so
Dataverse would require a greenfield adoption.
SharePoint can hold managed documents; OneDrive can support personal working
material. Personal drives are not proposed as the authoritative programme
approval or evidence store.

M365 Copilot is a productivity experience; Copilot Studio builds agents and
tools. Neither becomes an approval authority because it can invoke an action.
Low-code does not imply weak governance, and Azure does not confer compliance
automatically. Existing asset, repairs, housing, finance and contractor systems
retain their authoritative records and accountable services under all options.

#### Fit to the BRD Controls

| BRD concern | Azure-led approach | Business-platform approach |
| --- | --- | --- |
| Mandatory gates and authority, FR-036 | Explicit state transitions and server-side authorisation in a domain API | Dataverse records and server-side rules or custom APIs, with flows coordinating work |
| Immutable evidence version identifiers and retained prior versions, NFR-002 | Versioned evidence records and storage with appropriate retention controls | Controlled document libraries and Dataverse references, with explicit retention and supersession controls |
| Failure, disablement and recovery, NFR-004 | Durable execution, monitored queues, retries, idempotency and reconciliation | Governed flows, exception queues and reconciliation, with actual timeout and recovery behaviour tested |
| Authoritative-system integration, NFR-005 | API or event adapters with documented source ownership and conflict handling | Connectors and custom APIs, using Azure integration services where justified |
| Portable evidence and exit, NFR-006 | Exportable records, evidence and approval history independent of the model provider | Exportable Dataverse and document evidence, including approval and supersession history |
| Evaluated and reversible changes, NFR-007 | Code-managed evaluation harness and versioned model, prompt, rule and tool configurations | Platform lifecycle management and evaluations, supplemented by custom controls where required |
| Staff experience | Custom workbench, optionally surfaced through Teams | Power Apps and Teams with familiar document collaboration |

These are candidate implementation approaches, not acceptance evidence.
Neither database audit logs nor ordinary document version history alone proves
the required immutability, retained approvals, access separation or exit path.
Both options must pass the same BRD acceptance tests, including permissions,
prohibited actions, evidence export and failure recovery.

#### Proposed Azure-Led Implementation Boundary

Build a focused programme control layer, not a replacement housing-management
system. The candidate components are:

* Container Apps for the programme workbench, domain APIs and services.
* A relational programme store for lifecycle state, approvals and
  reconciliation, with Blob Storage or SharePoint for evidence. Define one
  authority for each artefact and avoid competing approval records.
* Durable Functions or another justified durable execution approach for
  long waits, handoffs and recovery. Add Service Bus where asynchronous
  integration warrants its complexity.
* Foundry-hosted models for sourced extraction, reconciliation, drafting and
  raise-only anomaly flags. Tool APIs enforce access and allowable actions
  independently of agent instructions.
* Entra ID, managed identities, appropriate secret management, telemetry and
  deployment automation, with measured quality, latency and operating cost.

Azure AI Search, Document Intelligence and Copilot Studio are optional
components, justified by retrieval, document-processing or channel needs rather
than service count. Region, feature availability, support status, licensing,
data boundaries and deployment constraints require verification before design
approval.

Copilot Studio data policies can govern connectors, knowledge sources, HTTP
access and authentication [S1]. They complement business authorisation rather
than replace it. Azure durable workflow patterns support persisted execution,
recovery and human approval waits [S2]; safe external actions still require
application-level authority checks, idempotency and reconciliation.

#### Customer Value and AMA Evidence

Keep two arguments separate:

* Customer selection: choose the lowest whole-life-cost option that satisfies
  all mandatory controls and can be supported by the organisation. The owner
  confirmed there is no current Dataverse or Dynamics 365 estate to reuse.
  A greenfield Power Platform adoption could still be preferable if it meets
  the controls at lower whole-life cost and the organisation funds its
  governance and support capability.
* Capstone selection: Azure provides a direct way to demonstrate contracts,
  failure recovery, model comparisons, instrumentation and cost per business
  outcome. This is a legitimate project preference, not proof of customer
  superiority.

The [Capstone Assessment Guide](./reference/method/ama-capstone-assessment-guide.md)
rewards justified alternatives (A2), implementation completeness (A4),
measured operations and cost (A5), model evaluation (A6), and meaningful bounded
autonomy (A7). It does not reward Azure service count. The assessment should not
present a scripted approval flow as agentic autonomy or expand AI authority to
meet the rubric.

A candidate bounded task is for an agent to identify missing evidence, select
permitted sources, reconcile discrepancies and assemble a sourced review-ready
draft within tool, iteration, time and cost limits. Deterministic workflow
still controls property progression; people retain consequential decisions.
This task remains subject to the BRD's comparison, safety and release gates.

#### Evidence Needed Before a Platform Decision

The owner reports that current coordination uses Excel files and that
Dataverse and Dynamics 365 are not present. The Microsoft 365 tenant,
SharePoint availability and licences, Excel workbook formats and quality,
available APIs, operating-team skills, transaction volumes, document
sensitivity and support ownership are still unknown. No comparative
implementation, licensing quotation, whole-life cost model or direct
stakeholder validation establishes a winning platform yet.

Given the confirmed absence of Dataverse and Dynamics 365, the hybrid approach
is the provisional demonstrator baseline for the PRD: Azure owns the new
structured programme state, deterministic gates, integrations and bounded AI;
M365 services may support managed documents and staff collaboration once
tenant capability, licensing and governance are verified. Excel is treated as
the current source material to assess for controlled import, not as the target
live workflow or an authoritative approval record. The greenfield business-apps
option remains a priced comparator, not the selected build target. This
direction remains subject to sponsor, architecture, security, Finance and
control-owner review.

Agree appraisal criteria before assigning weights or scores. Compare equivalent
scope and operating assumptions across options, including implementation,
integration, migration, licences, infrastructure, model use, support, assurance
and exit costs. Include staff review effort rather than treating generated
outputs as completed work.

Use the same representative property journey to test the options, including
successful progression, a safety hold, withdrawn consent, missing evidence and
integration failure. Measure errors, review effort, latency, recovery and cost
per reviewed task; assess cost per accepted handover only when operational
evidence supports it. Synthetic demonstrations can establish technical
feasibility, not attributable live delivery benefits. The BRD's Comparison 1
and Comparison 2 remain the operational and task-level value tests.

The provisional decision statement is:

> Prefer an Azure-led programme control layer, subject to options appraisal,
> because the proposed lifecycle requires explicit cross-system controls,
> recoverable execution and measurable AI behaviour. Reuse M365 for
> collaboration and documents only after tenant and governance verification.
> Compare a greenfield Dataverse/Copilot Studio-led alternative if it meets
> the same requirements with lower whole-life cost, including platform
> adoption and operating capability.

#### Platform Evidence

| Reference | Source and relevant section | Classification | Checked | Limitation |
| --- | --- | --- | --- | --- |
| S1 | [Configure data policies for agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention), Copilot Studio connectors and common data policy use cases | Official product documentation | 2026-10-03 | Describes platform data governance, not proof of business-control compliance |
| S2 | [Workflow in Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/workflows-overview), workflow frameworks and durable execution for AI agents | Official product documentation | 2026-10-03 | Describes execution patterns, not end-to-end action authorisation or a verified deployment choice |

## Phased Delivery and Decision Gates

| Phase | Scope | Evidence to proceed |
| --- | --- | --- |
| 0. Readiness, 6 to 8 weeks | Validate pilot-area stock data, current throughput, delay causes, resident journeys, PAS 2035 capacity, supplier routes, grant status, financial headroom and system options | Asset, safety, resident, finance, procurement, data and technical owners accept the baseline and pilot controls |
| 1. Shadow mode | Run recommendations, drafts and exception tests without live consequential actions; compare conventional workflow, rules-based automation and bounded AI | Accuracy, override rate, missed critical exceptions, review time, data quality, accessibility and whole-life cost support a live test |
| 2. Controlled live pilot, 6 to 9 months | Use existing teams and suppliers in one locality, a small number of understood archetypes, named accountable owners and agents operating within recommend, draft, reconcile and flag boundaries; retain assurance needed for safety as a control | At least 50 accepted handovers from an indicative 80 to 100 candidate homes, subject to validated company data and no uncontrolled safety or resident-rights breach |
| 3. Repeatable scheme delivery | Add approved archetype patterns, geographic work packages, planned-maintenance integration, supplier scorecards and risk-based quality sampling | Quality, resident, capacity, grant, cash and operating measures remain within approved tolerances |
| 4. Selective scale | Add separately governed automation only where the pilot proves incremental value; release capital in tranches | Board approves the next envelope after independent assurance and downside testing |

The pilot size and durations are planning proposals, not commitments. They must
be adjusted after Phase 0 establishes complexity, procurement lead times,
resident needs and competent capacity.

### Pilot Success Measures

| Dimension | Proposed measure |
| --- | --- |
| Safety | Zero works released with an unresolved relevant safety hold; 100% of urgent hazards routed without suppressing the separate statutory response |
| Resident authority | Zero installations without a current measure-specific decision; zero incomplete appointments automatically classed as refusal |
| Professional control | 100% of controlled technical outputs attributable to named competent roles |
| Quality | Right-first-time physical and evidence acceptance by severity; zero unresolved safety-critical defects at handover |
| Throughput | Accepted handovers and homes reaching the intended energy outcome, not starts or agent actions |
| Cycle time | At least 20% reduction in assessment-to-ready-to-install time against a comparable measured baseline |
| Administration | At least 25% reduction in manual coordination time per accepted home, net of review and assurance effort |
| Resident experience | Adjustments met, appointments kept, disruption promises honoured, complaints resolved and comfort or affordability outcomes measured |
| Supplier capacity | Forecast versus delivered quality-adjusted capacity by role, work package, subcontractor and period |
| Funding | Installed scope, accepted evidence, claim recommendation, Finance decision and cash receipt reconciled separately |
| Financial control | Cost per accepted home, peak cash, match funding, contingency and covenant headroom within approved tolerances |
| AI safety and value | Zero autonomous controlled approvals; no missed critical exception in agreed tests; draft acceptance and review effort demonstrate incremental value |

On 4 October 2026 the owner confirmed assessment-to-ready-to-install elapsed
time as the primary BG-011 cycle-time measure; accepted handover is reported
separately as an outcome. The event definitions, denominator, cohort, case
handling, baseline and MDE remain open under OD-18. The 20% and 25% values
remain proposed targets after the owner-delegated Executive Reviewer requested
changes; this direction does not ratify them.

Measurement-design note: the pilot should use the updated comparison proposal
from the
[Pilot Measurement Challenge](./reference/research/company/pilot-measurement-challenge.md).
Comparison 1 tests existing teams with agents in the pilot locality against
matched existing teams without agents in another locality, using a frozen
cohort before resident contact, identical Phase 0 event capture,
intention-to-treat analysis and difference-in-differences against the
instrumented pre-period. Comparison 2 tests each agent capability through
paired shadow-mode comparison and, where safe and lawful, task-level allocation
between agent-assisted and workflow-only handling. The twelve-month
reconstruction is context with coverage flags; the proposed counterfactual is
the instrumented pre-period plus the concurrent matched comparison cohort. The
operational dashboard steers the pilot and is not gate evidence. The benefits
scorecard has frozen, versioned definitions, assurance and supplier
data-challenge rights without veto. Shared staff or suppliers across localities
are logged because they can contaminate the comparison. Guardrail breaches
pause affected work regardless of throughput, and seasonal comfort, damp, mould
and ventilation outcomes remain pending where the pilot window cannot observe
them. If Phase 0 shows supplier or competent-assessor capacity is the binding
constraint, agents cannot create that capacity; their value case must focus on
forecasting, scheduling within confirmed capacity and evidence flow. These are
role-agent hypotheses and proposals, not company facts.

## Executive Trade-Offs

| Trade-off | Recommended executive position |
| --- | --- |
| Speed versus safety and quality | Optimise accepted, defect-free and resident-handed-over outcomes, not starts |
| Grant eligibility versus whole-asset value | Do not install poor lifecycle choices because they attract grant; align work with condition and planned maintenance |
| Automation versus accountability | Automate evidence handling and routine drafting; retain human authority wherever harm, consent, professional judgement or financial commitment is involved |
| Breadth versus deliverability | Prove one coherent lifecycle segment before commissioning all capabilities |
| Standardisation versus property context | Reuse archetype patterns only with property-specific checks and controlled exceptions |
| Central optimisation versus resident agency | Missing data, support needs or incomplete appointments trigger investigation, not silent deprioritisation |
| Supplier scale versus resilience | Commit capacity in tranches, retain contingency and link allocation to quality-adjusted outcomes |
| Innovation versus lock-in | Require open interfaces, exportable evidence, manual fallback, model and rule versioning, and a tested exit route |

## Business Case and Value

### Expected Outcomes

The programme is expected to improve safe accepted throughput, resident
experience, evidence quality, grant conversion and decision confidence. These
are value hypotheses rather than guaranteed benefits. Phase 0 must establish
the baseline, and the pilot must demonstrate attributable improvement before
the outcomes are included in an approved investment case.

The target outcome is not "more automation." It is more homes reaching a safe,
resident-accepted, defect-controlled and evidence-complete handover while the
association remains within its capital, cash, covenant, competence and supplier
capacity.

### Value Narrative for the Board and CXO Team

The primary value is not the number of agents deployed. It is the association's
ability to make better capital decisions and convert approved investment into
safe, resident-complete, evidence-accepted and fundable outcomes with fewer
avoidable delays and failures.

As a not-for-profit, Proper North Homes should appraise the programme as
mission investment under financial discipline. Resident and social value,
stewardship of homes and compliance outcomes are primary, while operating
surplus, liquidity, covenant headroom and value for money preserve the
organisation's capacity to pursue those outcomes. The business case must not
use distributable profit or shareholder return as an objective, and it must
not treat not-for-profit status as evidence of unlimited affordability.

| Value domain | Potential business value | Evidence and treatment |
| --- | --- | --- |
| Resident and social value | Safer, warmer and more comfortable homes; clearer choices; fewer repeated contacts; more reliable appointments; earlier identification and resolution of adverse outcomes | Measure comfort, affordability, damp, mould, ventilation, disruption, complaints and distribution of outcomes; do not promise universal bill savings |
| Operational value | Less duplicate entry, evidence chasing, rework and queue ambiguity; faster exception ownership; more specialist time focused on judgement rather than administration | Compare cycle time, manual hours, handoff ageing, repeat visits, overrides and assurance effort against a credible counterfactual |
| Asset and programme value | Better sequencing with planned maintenance; fewer abortive interventions; visible constraints; quality-adjusted throughput; earlier detection of systemic defects | Measure cost and accepted outcome by archetype, lifecycle stage, supplier and defect severity |
| Financial value | Higher conversion of eligible awards into compliant claims and cash; lower avoidable rework; clearer peak-cash and match-funding exposure; better capital allocation | Count only incremental grant received and cashable budget reductions; include technology, integration, staffing, assurance, financing, contingency and exit costs |
| Risk and governance value | Stronger evidence for Board, regulator, funder and audit scrutiny; fewer uncontrolled approvals; earlier pause when tolerances are breached | Use a risk scorecard; do not convert the same risk reduction into multiple cash benefits |
| Strategic value | A reusable property and evidence capability that supports future asset, safety and decarbonisation decisions | Scale only if portability, data quality, named ownership and whole-life affordability are proven |

### Illustrative Economics

The provisional 15,600-home scenario at GBP 20,000 per home implies GBP 312
million of gross cost. Even if every home received the GBP 7,500 ordinary grant
cap, the provider-funded balance would be GBP 195 million before financing,
technology, programme overhead, ineligible work, defects and contingency.

The stated GBP 40 million opportunity would support at most about 5,333 homes
at the cap. At the same unit-cost assumption, those homes would cost about
GBP 106.7 million and require about GBP 66.7 million from the provider. This is
an illustration, not a budget: property eligibility, award evidence, measure
mix, unit cost, match funding, delivery timing and grant receipt remain
unvalidated.

The investment appraisal must separate:

1. The cost and benefits of the underlying retrofit programme
2. Existing expenditure already included in the long-term plan
3. Rephased or displaced capital expenditure
4. Incremental acceleration expenditure and financing
5. The whole-life cost of data, workflow, integration and AI capabilities
6. Benefits attributable to the selected technology compared with a credible
   non-agentic alternative

### Value Hypotheses

| Hypothesis | Evidence required before scale |
| --- | --- |
| Coordination and evidence failures materially constrain throughput | Cause-of-delay, queue, rework and handoff analysis |
| The solution increases accepted outcomes rather than activity | Controlled comparison using accepted handover and intended energy outcome |
| Grant conversion improves | Award, eligible cohort, evidence acceptance, claim and receipt records |
| Administrative savings exceed review and assurance costs | Time study, staffing impact and confirmed budget-owner action |
| Quality holds as volume increases | Physical inspection, evidence rejection, defect severity, remediation cost and recurrence |
| Residents receive equitable value | Disaggregated access, decision, disruption, complaint, comfort and affordability outcomes |
| Acceleration remains affordable | Monthly cash, liquidity, covenant, security and severe-but-plausible downside model |
| Bounded AI adds value over workflow automation | Options appraisal, pilot attribution, total cost of ownership and error severity |

## Why Now (2026-2028)

Awaab's Law Phase 1 came into force on 27 October 2025 for emergency hazards and
significant damp and mould hazards. Phase 2 guidance states an intended
30 November 2026 commencement, but the implementing instrument is not in the
local corpus and must be verified before rules are activated. Phase 3 remains
future and requires an implementing instrument. The government published its
final SRS MEES policy on 1 April 2026, including one qualifying metric by
1 April 2030 and a second by 1 April 2039, but the corpus does not yet evidence
the directions, revised regulatory standard and commencement needed to treat
that policy as an in-force landlord duty.

WH:SHF Wave 3 delivery runs to September 2028, with grant spend required by
31 March 2028. The case study does not establish that Proper North Homes has an
allocation. The immediate pressure is therefore to confirm any existing award,
protect eligible delivery and establish a credible asset and funding trajectory.
A new digital platform must not become a precondition for meeting current
hazard duties or protecting an existing grant.

## Recommended Executive Decision

Approve a capped readiness and pilot stage within delegated authority. Do not
approve a five-agent portfolio rollout, recognise GBP 40 million as secured
funding, or accelerate the capital programme until the relevant gates are met.

The Executive Director of Assets should sponsor the proposition with the Chief
Executive. Finance, Building Safety, Resident Engagement, Procurement, the
Retrofit Programme Manager, the Data Protection Officer and competent PAS 2035
roles should hold independent approval and stop authorities within their
mandates.

The Board should receive a balanced scorecard covering:

* Safe and accepted handovers
* Homes reaching the intended energy outcome
* Resident decisions, adjustments, complaints and lived outcomes
* Serious and recurring defects
* Supplier and competent-person capacity
* Grant opportunity, award, claimable value and cash received
* Gross and net cost, peak cash, match funding and covenant headroom
* Administrative effort, cycle time and attributable technology benefit
* Paused, overdue, unowned and reopened work

The proposition should proceed only if the pilot shows that benefits exceed the
technology, integration, operating and assurance burden without weakening
safety, resident rights, professional accountability, quality or financial
resilience.
