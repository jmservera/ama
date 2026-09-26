---
title: Agent Request Challenge
description: Role-by-role challenge of the five requested Proper Warm agents, the problems behind them, non-agent alternatives and what to build instead
ms.date: 2026-09-26
ms.topic: reference
---

## Purpose and Method

The [original Case Study 48](../../../case_study_48_original.md) asks for five
agents. Each has an "Owns end-to-end" line and an autonomy level. That line is
the business's own statement of why it wants an agent. This page tests each
request by asking four questions. What problem is it really trying to solve?
What cheaper alternatives exist? Where would an agent fit, and where would it
not? What has to be built behind it for the result to be worth anything?

On 2026-09-26 the eight `company-*` role agents answered these questions in
parallel. Each agent covered the requests within its own decision rights:

| Role agent | Primary scope | Secondary scope |
| --- | --- | --- |
| Executive Director of Assets | Stock Prioritisation | Programme supervisor; five agents versus control plane |
| Data and Performance Lead | Stock Prioritisation data; Quality Verification data | Grant reporting |
| Retrofit Programme Manager | Assessment; Quality Verification | Programme supervisor; scheduling |
| Head of Finance, Capital and Grants | Grant & Funding | Grant eligibility in prioritisation; overall financial case |
| Head of Procurement and Contract Management | Coordination, contractor side | Quality Verification, contractor accountability |
| Head of Resident Engagement and Insight | Coordination, resident side; resident channel | Sensor versus resident report; health-risk prioritisation |
| Head of Building Safety and Compliance | Damp-and-mould loop; Quality Verification | Health-risk prioritisation; safety content of Assessment |
| Neighbourhood Housing Officer | Coordination, frontline and access; damp intake | Health-risk prioritisation |

The role agents are research instruments. They are not employees with
company knowledge. Their answers are sector-informed hypotheses unless they
restate the case study, the addendum or the
[Agentic Retrofit Programme BRD](../../../brds/agentic-retrofit-programme-brd.md).
Nothing on this page is a company fact. The BRD requirement IDs and the
regulatory provisions cited below were spot-checked against the local files on
2026-09-26. They were not checked against the official sources online.

## Summary

Across all eight roles, the answer was the same: none of the five requests
should be built as an end-to-end agent. Every "owns end-to-end" line bundles
three kinds of work:

* Deterministic control work, such as gates, clocks, holds, eligibility rules,
  consent records and evidence checklists
* Accountable human decisions, such as cohort policy, professional sign-off,
  consent, hazard categorisation, grant submission and quality acceptance
* A small amount of work where bounded AI genuinely helps: reconciling data,
  reading unstructured evidence, drafting from approved records and spotting
  signals in free text

The problem underneath is missing shared records and undefined lifecycle
states. A lack of intelligence is not the problem. Each agent, if built,
would need the same foundation. That supports the addendum's control plane
proposal, with AI capabilities added as modules only where Phase 1 shadow
testing proves they add value.

| Requested agent | Owns end-to-end (as requested) | Real problem behind the request | Role verdict | What to build behind it |
| --- | --- | --- | --- | --- |
| Stock Prioritisation | Ranks homes by energy, health risk and grant eligibility (L2) | Defensible capital allocation from fragmented stock, EPC, condition and hazard data with no approved cohort policy | Do not build as agent. Transparent, versioned scoring model and deterministic eligibility rules, with bounded AI for reconciliation and explanation | Property master with building parent, field-level source register, data-confidence score, versioned eligibility rules, exception register, approved cohort policy |
| Assessment | Drafts PAS 2035 assessments from surveys and data (L3) | Too few homes reach ready-to-design because of assessor capacity, fragmented data and rework | Bounded AI inside workflow, limited to pre-filling sourced facts and checking completeness | Property evidence record with source and date per field, archetype templates, separate assessor and coordinator sign-off, material-change rules, safety-hold check |
| Grant & Funding | Prepares funding applications and reporting (L3) | Turning delivered homes into grant cash without clawback; no evidenced award | Bounded AI inside workflow, only after the ledger exists. Reporting is a data problem, not an agent problem | Four-state grant ledger, versioned eligibility rules, per-home evidence pack, monthly reconciliation, claim holds, named preparer, validator and submitter |
| Contractor & Resident Coordination | Schedules works, secures consent, communicates (L3) | Committed capacity and resident readiness do not meet; no-access is logged as refusal; frontline context is lost | Split in two. Resident side: no agent, deterministic decision record plus bounded drafting and routing. Contractor side: bounded AI suggesting slots within committed capacity | Measure-specific decision record, preference and adjustment record, single contact log, committed-capacity register, standard work order, appointment outcome codes, named liaison owner |
| Quality Verification | Checks evidence and post-retrofit sensor data (L4 flags) | Paying, claiming or handing over incomplete or defective work; late detection of systemic defects | Bounded AI inside workflow. Flags can only raise concerns; they never clear, accept or close anything | Per-measure evidence schedule in contracts, defect register graded by severity, sampling rules, named independent acceptance, sensor device register with validity status, seeded defect test set |
| Programme supervisor | Orchestration across schemes | No single view of each home, owner or blocked step; handoffs have no owner | Do not build as agent. Deterministic workflow engine with lifecycle states, queues and clocks | Lifecycle state machine, gate definitions, delegated-authority matrix, audit trail, frontline progress view |
| Damp-and-mould loop | Alerts routed to a dedicated response loop | Awareness of hazards leaks across channels; the awareness date is not captured; triage and inspection capacity is short | Do not build as agent. Statutory clocks in the repairs case system, with a bounded AI signal scan feeding human triage | Hazard case record with awareness timestamp, versioned clock rules, retrofit safety hold, one damp intake route, contractor reporting clauses |

The verdicts differ in wording, not in substance, on two items. They are
listed under [Divergences](#divergences-and-open-contradictions).

## Stock Prioritisation Agent

### Real Problem

The job is capital allocation. The association has to decide which homes to
treat, in what order and in what bundles, in a way that survives board and
regulator scrutiny. The likely root cause is data and governance. The
spreadsheet dependency is a case-study fact. Merged or stock-transfer records
spread across several systems are a sector hypothesis. There is no approved
cohort policy or data-confidence model.

### Challenge

* Once the weights are agreed, ranking is arithmetic. The weights,
  exclusions and treatment of health risk are investment and safety policy.
  The Executive Director of Assets recommends them and the Board approves
  them.
* Eligibility is a rules question. It should be a deterministic pass, fail or
  unknown result, not a model ranking. The WH:SHF Wave 3 technical annex says
  that "in scope" (EPC D or below) does not necessarily mean eligible for the
  scheme
  ([local snapshot](../../regulatory/retrofit-standards-and-funding/warm-homes-social-housing-fund-technical-annex-2025.md),
  Page 3, footnote 1).
* Health and vulnerability inputs are UK GDPR special category data. They need
  a lawful basis and a DPIA, and there is a restriction on solely automated
  significant decisions. Recorded vulnerability flags are probably far less
  complete than the modelled prevalence. A ranking that relies on them would
  therefore favour residents who are already known and penalise those who
  are not recorded.
* Open damp and mould hazards follow the statutory route and never wait in a
  retrofit queue (BRD BR-003).
* Missing data must trigger an investigation, never silent deprioritisation
  (BRD BR-051).

### Alternatives, Cheapest First

* An approved cohort policy plus a transparent scoring model in the existing
  asset system or a BI layer, with published weights and sensitivity runs
* Targeted remediation of EPC and stock-condition data
* Nominations from housing officers and a resident self-referral route for
  health-risk households

### Where AI Fits

* Adds value: reconciling conflicting legacy records, pulling condition facts
  out of free-text survey notes, flagging missing or stale fields, and
  explaining each score in plain language
* Adds risk: setting weights, inferring health risk, producing rankings that
  cannot be reproduced, and chasing grant capture at the expense of
  whole-life value

### Value Test and Stop Criteria

* Phase 0 or 1: run a past cohort through three options: the spreadsheet
  selection, the rules model, and the rules model with bounded AI. Measure
  the share of top-ranked homes still viable after survey, critical conflicts
  detected, override rate, reproducibility and time to produce a cohort.
* Stop the AI element if any home is dropped without human review, if a
  statutory hazard is routed through the ranking, or if the AI does not beat
  the rules model on missed critical exceptions once review effort is
  counted.

## Assessment Agent

### Real Problem

Too few homes reach ready-to-design. The likely causes are assessor capacity,
fragmented property data and returned or repeated assessments. No one has
measured which of these is the binding constraint.

### Challenge

* The request leaves out the Retrofit Assessor. Under PAS 2035, the assessor
  carries out the site survey and owns it. The coordinator reviews it and
  sets the risk path. "Coordinator approves a draft" merges two professional
  sign-offs into one.
* An agent cannot make site observations. L3 is acceptable only for
  pre-filling facts from named sources. It is not acceptable for drafting the
  assessment itself.

### Alternatives, Cheapest First

* Accredited assessors contracted through a framework
* Configuring a PAS 2035 project platform that is already on the market
* Archetype pre-survey packs and a fixed completeness checklist

### Where AI Fits

* Adds value: pre-filling the survey pack from stock, EPC, repairs and
  planned-maintenance records with the source shown for every field; flagging
  conflicts such as an open damp case; checking for missing items before
  coordinator review; pre-populating known hazard, higher-risk building and
  fire-risk actions
* Does not fit: inferring construction, ventilation or condition that nobody
  observed

### Value Test and Stop Criteria

* Phase 1: pre-fill 30 to 50 homes in parallel with the manual process.
  Assessors score each field as correct, wrong or unsourced, and review time
  is measured against the addendum's target of at least a 20% cut in
  assessment-to-ready-to-install time.
* Stop if any site observation appears without a source, or if checking the
  drafts takes as long as doing the work manually.

## Grant and Funding Agent

### Real Problem

The job is turning delivered homes into grant cash without clawback, from
eligible home to award, claimable evidence and cash received. No award has
been evidenced. WH:SHF Wave 3 spend is due by 31 March 2028. Bid-writing
capacity is probably a secondary constraint.

### Challenge

* Deciding to bid, committing match funding, certifying claims, submitting
  and recording receipts stay with humans who hold financial authority (BRD
  BR-028).
* Figures produced by an agent cannot be audited. Reporting is a
  data-lineage problem that runs from accepted evidence through to claim
  lines (BRD BR-025).
* The funding route changes the value of drafting. In Greater Manchester and
  the West Midlands, WH:SHF Wave 3 funding is allocated by formula through
  integrated settlements, at 5.7% and 7.8% respectively. It is not allocated
  by competitive national bid
  ([local snapshot](../../regulatory/retrofit-standards-and-funding/warm-homes-social-housing-fund-technical-annex-2025.md),
  Page 3 and Page 5 Table 3). Whether Proper North Homes operates in either
  area is unknown.

### Alternatives, Cheapest First

* A claim evidence checklist for each scheme
* A four-state grant register in the finance system, with templated funder
  returns
* A bid consultant for peak rounds, consortium bidding or a combined-authority
  route

### Where AI Fits

* Adds value: reconciling installer evidence against claim conditions,
  flagging claimed scope that lacks accepted evidence, and drafting packs and
  narratives from controlled figures
* Does not fit: calculating figures, interpreting eligibility, filling gaps
  in evidence

### Value Test and Stop Criteria

* Phase 1: rebuild the last funder return and recent claims from the ledger,
  with and without AI drafting, and compare the results with Finance's own
  work.
* Stop if Finance's net review time does not fall by at least 25%, if any
  unsupported eligibility or evidence statement reaches a reviewer
  undetected, if the ledger alone meets the target, or if there is still no
  evidenced award or open route at the Phase 0 gate.

## Contractor and Resident Coordination Agent

### Real Problem

The job is turning committed supplier capacity and informed resident decisions
into kept appointments at homes that are ready for work. The sector-informed
root causes are:

* Overstated or uncommitted supplier capacity
* Incomplete work orders
* Distrust and unclear information about disruption
* Unreliable appointments
* Loss of frontline context, where a missed visit becomes "refused" and the
  housing officer finds out from a complaint

Scheduling software does not create installers. The 10% no-access and 5% to
10% refusal figures are planning assumptions. Proper North Homes' real rates
are unknown.

### Challenge

* An agent cannot "secure" consent. Agreement to each measure belongs to the
  resident and can be withdrawn. Silence or access for a survey is not
  consent (BRD BR-011, BR-013). A failed visit is not a refusal (BRD
  BR-020).
* Committing capacity, instructing contractors and changing scope are
  contract-manager acts. An agent's message could count as a client
  instruction or variation. Moving work between suppliers may raise
  Procurement Act 2023 modification questions that need Legal review.
* The role agents found no evidence that "contractor agents via scheduling
  APIs" exist in this market. Many small retrofit installers work by phone,
  email and spreadsheet.
* Putting supplier utilisation and resident choice in one agent creates a
  conflict of interest.

### Alternatives, Cheapest First

* A handoff rule: every failed or declined visit goes to a named officer
  before it is reclassified
* A single contact log shared by housing, repairs and the resident liaison
  officer
* A standard work-order template and contractor-owned scheduling with
  contractual service levels for appointment offers, kept appointments and
  abortive visits
* Resident liaison officers for each scheme, Easy Read packs, show homes,
  trusted intermediaries, and phone, text and letter booking
* KPI-linked payment and allocation of future work by quality-adjusted
  performance

### Where AI Fits

* Adds value: accessible and translated drafts checked by staff; routing
  inbound messages to staffed queues using fixed categories; pre-visit
  household summaries; flags for missed handoffs; checking contractor
  schedules against committed capacity, safety holds, open hazard jobs and
  unmet adjustments; suggesting slots only after resident preferences and
  capacity are confirmed (BRD BR-021)
* Harms or adds risk: chasing or persuading residents, becoming the default
  route for digitally excluded households, auto-sent messages to people in
  crisis, sharing more resident data than contractors need (BRD BR-016), and
  flags that nobody has capacity to work

### Value Test and Stop Criteria

* Phase 1: in one patch, working with one supplier, the AI drafts, routes and
  suggests alongside staff. Measure appointments kept first time, adjustments
  met, repeat contacts, time to decision, coordination hours per accepted home
  and complaints. Report the results separately by age, disability, language
  and channel.
* Stop if any safeguarding or hazard message is misrouted, a decision is
  recorded without a human, a slot is suggested against uncommitted capacity
  or an active hold, gaps between resident groups widen, or the net time
  saving after review stays below 25%.

## Quality Verification Agent

### Real Problem

The job is to avoid paying for, claiming on or handing over incomplete or
defective work, and to catch systemic defects early. Examples of such defects
include insulation fitted without adequate ventilation. The root causes are
variable contractor evidence, self-certification, a weak link between evidence
and payment or claims, and limited independent inspection and evaluator
capacity.

### Challenge

* Autonomous flags are acceptable only if a flag adds work to a human queue.
  Every role said the real risk is the reverse: a pack with no flags, or a
  normal sensor reading, gets read as proof of quality.
* The competent quality authority keeps acceptance and defect closure.
  Contractors do not accept their own evidence. An agent must not reject
  work, withhold payment or issue defect notices (BRD BR-034).
* A normal reading cannot override a resident report, and sensors are not
  mandatory (BRD BR-037). Awaab's Law Phase 1 guidance says a sensor risk
  notification does not by itself make the landlord aware of a hazard, and
  says tenant reports should generally be taken at face value
  ([local snapshot](../../regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md),
  section 3 and section 3.5, converted 2026-09-19). In-home sensors need a
  separate lawful basis, a DPIA and the resident's right to decline.
* Sensor data has its own validity problems: mapping devices to properties,
  calibration, missing data, clock drift, heating-season coverage, and many
  homes with no pre-retrofit baseline.

### Alternatives, Cheapest First

* A fixed per-measure evidence checklist enforced at the payment gate
* A contract term that holds payment until evidence is accepted, plus
  retention and a defects liability period
* Risk-based physical sampling by an independent clerk of works or a
  contracted Retrofit Evaluator
* A structured aftercare call at six weeks and after the first winter

### Where AI Fits

* Adds value: checking photos and documents against the checklist at volume;
  detecting mismatched serial numbers, dates or locations; spotting defect
  patterns by installer, product or archetype that should increase sampling.
  The addendum's typed decision-model idea is a candidate here.
* Does not fit: accepting work, closing defects, or giving an all-clear
  because nothing was flagged

### Value Test and Stop Criteria

* Phase 1: run the checks on past completed homes, on seeded defects, and in
  parallel with human reviewers and competent inspectors. Measure recall on
  confirmed rejections, precision, reviewer minutes per pack, right-first-time
  acceptance and reopened defects. Compare the results with the checklist
  alone.
* Stop if any safety-critical defect caught by humans is missed, if false
  flags overwhelm reviewers, if AI adds little recall over the checklist, or
  if there are too few valid sensor device-months to support conclusions.

## Programme Supervisor and Damp-and-Mould Loop

### Programme Supervisor

No one can see where each home is, who owns the next step or what is blocked.
The cause is undefined states, gates, authority limits and exception routes.
An AI orchestrator cannot enforce rules that have not been defined. Chaining
agents compounds errors and hides who is accountable. The alternative is a
conventional workflow engine with a lifecycle state machine, named queues,
clocks, escalation, audit and a frontline progress view. It is needed whether
or not agents are used. AI could later summarise exceptions and draft board
narratives from controlled records. Stop if any summary misstates a hold, a
clock or a consent status.

### Damp-and-Mould Loop

Retrofit tooling should not own the statutory response. It should link to the
existing repairs and hazard service and must never pause or reset the clock
(BRD BR-003). The Phase 1 clock starts from awareness through any channel,
including contractors and staff visits. The timescales are:

* Emergency hazards: investigate and make safe within 24 hours
* Significant hazards: investigate within 10 working days
* Written summary: within 3 working days of the investigation
* Safety work: within 5 working days
* Supplementary works: start within 12 weeks

([local snapshot](../../regulatory/social-housing-regulation/awaabs-law-phase-1-guidance-2025.md),
section 1.4 and section 3, in force from 27 October 2025).

The Phase 2 guidance adds excess cold and other hazards
([local snapshot](../../regulatory/social-housing-regulation/awaabs-law-phase-2-guidance-2026.md)).
It is planned from 30 November 2026, but the implementing instrument is not in
the local corpus and must be verified before any rule goes live.

* Cheapest alternatives: statutory clock fields and a working-day calendar in
  the repairs system; a mandatory hazard question on every contact, survey
  and contractor form; contractor same-day reporting clauses; scripted triage;
  an inspector rota and escalation matrix
* Where AI fits: a raise-only "hazard signal" scan of free text across repairs
  notes, complaints, retrofit surveys and contractor notes, which surfaces
  possible missed reports to a human triager. Hits may show that the landlord
  was aware earlier than recorded. That needs a Legal handoff.
* Does not fit: categorising hazards, deciding a report is out of scope,
  releasing safety holds or declaring a duty satisfied
* Stop if any AI output delays, suppresses or closes a clock, or if review
  load exceeds triage capacity

## Cross-Cutting Findings

### The Shared Foundation

Every request depends on the same records. If they are built first, they
deliver value without any AI:

* A property master keyed on UPRN, with a building parent record and a
  field-level source, date and authority register
* A lifecycle state machine with gates, queues, clocks and a
  delegated-authority matrix
* A hazard case record with the awareness timestamp and a linked retrofit
  safety hold
* A measure-specific resident decision record, a preference and adjustment
  record and a single contact log
* A committed-capacity register, a standard work order and appointment
  outcome codes
* A per-measure evidence schedule, a defect register and named acceptance
* A four-state grant ledger with versioned eligibility rules

### Recurring Bounded AI Candidates

These capabilities came up across several roles and are candidates for Phase
1 shadow testing:

1. Reconciling records and flagging missing data across legacy sources
2. Reading unstructured evidence, such as survey notes, photos and
   certificates, against fixed checklists
3. Drafting accessible resident, contractor, grant and board content from
   controlled records, reviewed by a human
4. Routing inbound messages to staffed queues using fixed categories
5. Raise-only signal scanning for missed hazard reports, missed handoffs and
   defect patterns

All five are recommend, draft or raise-only functions. None needs end-to-end
ownership. Items 2, 4 and 5 match the typed decision-model candidates in
[IDEA-001](../../../ideas/typesafe-system-one-agent-fit.md).

### Business Value

* Grant capture cannot pay for technology on its own. Grants are capped and
  need co-funding, so winning more grant increases the provider's spend. The
  addendum's illustration is GBP 66.7 million of provider funding against a
  GBP 40 million opportunity.
* The value case has to rest on more accepted handovers, less rework, avoided
  clawback, faster cash, and time released from coordination. Time released
  is capacity, not cash, unless a budget owner commits to a reduction.
* Every AI module needs a non-agent comparator and a stop criterion (BRD
  BR-029). The recurring comparators are the rules model, the evidence
  checklist, the ledger and the workflow engine.

## Divergences and Open Contradictions

* Coordination, resident side: the Resident Engagement Lead said "do not
  build as agent", while the Neighbourhood Housing Officer and Procurement
  Lead said "bounded AI inside workflow". The positions agree once the
  resident decision record is deterministic and AI only drafts and routes.
  The difference is about naming, not scope.
* Stock Prioritisation: the Data and Performance Lead and Finance said "do
  not build as agent", while the Asset Executive, Resident Engagement and
  Building Safety said "bounded AI inside workflow". All five agree that
  ranking and eligibility should be deterministic and AI should be limited to
  reconciliation and explanation.
* Quality Verification autonomy: most roles accept L4 for raise-only flags.
  The Data and Performance Lead recommends that AI reading of evidence should
  work at recommend level, not L4. This is unresolved.
* The Housing Officer suggested L3 might be acceptable for booking confirmed
  slots for residents who have opted into digital contact. The Retrofit
  Programme Manager recommends revisiting appointment suggestions only after
  Phase 1. This is unresolved.

## Questions for Proper North Homes

Each role named the question that would change its answer most:

| Role | Question |
| --- | --- |
| Executive Director of Assets | What share of homes has a physical stock-condition survey from the last five years, and in which system? |
| Data and Performance Lead | Which system, if any, is authoritative for property identity and EPC records? |
| Retrofit Programme Manager | Which PAS 2035 roles are employed, contracted or missing, and what is each role's monthly capacity? |
| Head of Finance, Capital and Grants | Does the association hold an executed grant award, and under which scheme and route? |
| Head of Procurement and Contract Management | Who delivers retrofit today, through which route and contract form, and do the contracts give rights to live schedule data? |
| Head of Resident Engagement and Insight | Can the association supply twelve months of no-access and withdrawal records, with reasons, by channel and adjustment need? |
| Head of Building Safety and Compliance | What are current damp and mould volumes, backlog and Phase 1 compliance, and which system records the awareness date? |
| Neighbourhood Housing Officer | How does a damp report from each channel become one timed case today, and who owns it? |

## Limitations

* The role agents answered from the case study, the addendum, the BRD, the
  company profile research and the local regulatory snapshots. They had no
  company data.
* Market claims, such as the absence of contractor scheduling APIs or the
  availability of PAS 2035 platforms, are sector-informed hypotheses. They
  have not been researched.
* Legal questions remain open: Procurement Act 2023 modification rules,
  Construction Act payment notices, when a contractor's knowledge counts as
  landlord awareness, and lease responsibility. They need named legal review.
