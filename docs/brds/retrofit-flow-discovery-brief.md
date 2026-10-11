---
title: Retrofit Flow and Constraint Discovery Brief
description: Proposed evidence, team and bounded assistant requirements for identifying retrofit delivery constraints
author: AMA Research Team
ms.date: 2026-09-19
ms.topic: concept
---

## Status and Purpose

This brief supports Phase 0 of the
[Agentic Retrofit Programme Business Requirements Document](./agentic-retrofit-programme-brd.md).
It proposes how Zava North Homes could establish where elapsed time and
avoidable effort are lost between candidate identification and accepted
handover.

The brief is a discovery proposal. It does not establish company facts,
approve an agent, appoint team members or authorise access to company or
resident data. Company owners, affected residents and competent professionals
must validate the operating model and evidence.

The immediate decision is whether to commission a linked twelve-month
property-flow analysis before selecting an intervention. Possible
interventions include process redesign, existing-platform configuration,
deterministic workflow, contract change, capacity investment and bounded AI.

## Discovery Proposition

The programme should not infer the cause of slow delivery from spreadsheet use
or from the five activities named in the original request. It should
reconstruct the complete population of properties identified during the
baseline period, including incomplete, paused, excluded, cancelled and reopened
cases.

The analysis should determine:

* Where each property spent calendar time
* Which periods involved active work and which involved waiting
* Which team, supplier or competent role owned each waiting period
* Which evidence, decision, capacity or resident condition prevented progress
* How often work was returned, repeated, rejected or reopened
* Which constraints recur across properties and which are isolated exceptions
* Whether the constraint changes by locality, archetype, measure, supplier,
  building type or resident journey
* Which intervention is proportionate to the evidenced constraint

Accepted handover is the endpoint. Candidate selection, work release,
appointment, installation, practical completion, invoice and documentary
completion must remain separate events.

## Discovery Outcomes

Phase 0 should produce:

1. A validated current-state lifecycle and event dictionary.
2. A linked property-level baseline with known coverage and quality limits.
3. A queue, wait-time and return-loop analysis.
4. A ranked constraint register with supporting and contradicting evidence.
5. A current-state property and resident journey.
6. An options appraisal comparing non-agent and bounded-agent responses.
7. A recommendation for the first controlled pilot or a decision not to
   automate.

No ranked constraint becomes a company finding until the relevant operational
owner validates the data and interpretation.

## Analysis Population and Method

### Population

Include every property first identified as a retrofit candidate during the
agreed twelve-month period. Preserve properties that did not progress so the
analysis does not favour successful cases.

Define and report:

* Baseline start and end dates
* Number of candidate properties
* Data coverage by system and field
* Properties excluded from analysis and the reason
* Events occurring before or after the baseline window
* Open cases whose eventual outcome is not yet known
* Duplicate, conflicting and unmatched property or building records

### Time Attribution

For each property, calculate:

1. Calendar time in each lifecycle state.
2. Active working time where reliable start and finish evidence exists.
3. Inactive queue or pause time.
4. Time awaiting each named team, supplier, subcontractor or professional role.
5. Return, rejection, repeat-visit and reopen counts.
6. Installation-to-physical-acceptance time.
7. Physical-acceptance-to-evidence-acceptance time.
8. Evidence-acceptance-to-resident-handover time.

Use mutually exclusive primary delay codes where evidence supports attribution.
Record contributing causes separately. Unknown or disputed causes must remain
visible rather than being assigned by inference.

### Constraint Test

A candidate constraint is supported when it:

* Accounts for a material share of the critical path
* Affects more than isolated properties
* Recurs across comparable cases
* Has a traceable owner or dependency
* Changes an operational or investment decision

It is weakened when complete timestamps show little queue time, when another
dependency explains the delay, or when the apparent improvement merely moves
work or risk to another team.

## Minimum Evidence Specification

| Evidence domain | Minimum fields | Proposed company owner |
| --- | --- | --- |
| Property and building identity | Property, address, parent building, locality, archetype, tenure and shared-system identifiers | Asset data owner |
| Candidate and cohort | Identification date, selection rule, source version, confidence, inclusion, exclusion and resequencing reasons | Asset Director and Retrofit Programme Manager |
| Lifecycle events | State, entry, exit, pause, restart, reopen, initiator, authority, reason and evidence version | Retrofit Programme Manager |
| Handoffs | Sending and receiving teams, named owner, referral, acceptance, first action, rejection, escalation and next resident-update dates | Respective operational owners |
| Resident journey | Contact requirement, attempts, successful contact, accessible format, appointment options, measure-specific decision, pause, withdrawal and authorised representative | Resident Engagement and Housing |
| Appointment and access | Notice, booking, change, attendance, outcome, human-reviewed failed-access reason, repeat attempt and remobilisation | Programme and contract manager |
| Safety and condition | Open repair or hazard, damp and mould, safety hold, building dependency, inspection, accountable owner, release evidence and release date | Building Safety, Repairs and Assets |
| PAS 2035 and technical | Assessment, design, review, approval, return and reapproval events; competent role and material change | Retrofit Programme Manager and competent role owners |
| Capacity and contracts | Supplier, subcontractor, work package, committed and delivered monthly capacity, mobilisation, contingency and competing commitments | Procurement and Contracts |
| Installation and quality | Design version, installation, inspection, evidence submission, rejection, defect, remediation, reinspection and physical acceptance | Programme and independent quality owner |
| Finance and grant | Approved budget, commitment, cost, payment hold, grant state, evidence rejection, claim and receipt | Finance and Grants |
| Handover and outcome | Accessible handover, resident acknowledgement, open defect, reopening, aftercare and intended energy outcome | Programme, Resident Engagement and Quality |

The final data specification requires a source-to-field map, lawful basis,
access rules, retention requirements, quality tests and named resolution owner
for each conflict. Sensitive resident information should be minimised to the
operational adjustment or analytical category needed for the approved purpose.

## Candidate Constraint Register

The executive and procurement role reviews proposed the following test order.
It is not a finding about Zava North Homes.

| Candidate constraint | Evidence that would strengthen it | Likely intervention class |
| --- | --- | --- |
| Supplier or professional capacity | Ready work waits for an evidenced capacity commitment; delivered capacity falls below commitment; one competent role governs the queue | Capacity investment, contract intervention and deterministic scheduling |
| Unaccepted handoffs and approval queues | Material inactive time occurs before ownership acceptance or after evidence is returned | Process redesign and closed-loop deterministic workflow |
| Resident access, adjustment and decision readiness | Repeated contact, unsuitable appointments, unfulfilled adjustments or recovery from failed access dominate elapsed time | Resident-service capacity, process change and contract standards |
| Property, building-safety or maintenance dependencies | Candidates are paused, redesigned or removed because existing dependencies were identified late | Readiness gates, prerequisite works and capital sequencing |
| Physical or documentary quality failure | Installation-to-accepted-handover time is material; defects, rejected evidence or repeat inspections recur | Contract intervention, assurance capacity and evidence controls |

## Human Team and Decision Rights

### Minimum Core Team

| Role | Discovery responsibility | Authority boundary |
| --- | --- | --- |
| Executive sponsor | Authorise the bounded discovery, require source participation and decide whether evidence supports a pilot | Does not determine technical, resident, safety or data-protection conclusions alone |
| Retrofit Flow and Data Analyst | Build the linked event baseline, calculate time attribution, document data quality and maintain the constraint register | Does not assign disputed causes or make programme approvals |
| Retrofit Programme Manager | Validate lifecycle states, operating events, queue ownership and accepted-handover definitions | Does not approve investment, grant claims or professional outputs outside delegated authority |
| Data or platform owner | Approve authoritative sources, identifiers, access, lineage and reconciliation rules | Does not reinterpret operational events without domain-owner validation |
| Benefits and evaluation owner | Define counterfactuals, denominators, attribution, review effort and whole-life cost | Does not count forecast activity as realised value |

The Retrofit Flow and Data Analyst is the missing coordinating capability. It
may be a named company analyst, a time-boxed cross-functional assignment or
specialist support. This is a human accountability even if software later
assists the work.

### Consulted Control Owners

Engage these roles only for the fields, causes and decisions they own:

* Asset data and planned maintenance
* Building safety, repairs and damp and mould response
* Competent PAS 2035 and technical assurance roles
* Resident engagement, neighbourhood housing and complaints
* Procurement, contracts and supplier performance
* Finance, capital and grants
* Quality inspection and defect remediation
* Data protection, information governance and security

No software output should resolve a disagreement between these owners. The
disputed attribution and its evidence should be presented for a recorded human
decision.

## Technical SME Routing

The cohort map can help route technical questions, but it does not establish
availability, project ownership or endorsement.

| Person | Suggested contribution | Evidence basis | Evidence confidence |
| --- | --- | --- | --- |
| Martin Pöckl | Data and AI platform options, including Microsoft Fabric for governed event data and reporting | Self-described Data and AI and Microsoft Fabric expertise in the cohort Loop | High |
| Graham Hosking | Copilot Studio, Microsoft 365 integration and multi-agent architecture boundaries | Profile and work evidence recorded in the cohort map | High |
| Niels Roos | Applied AI prototyping and comparison of bounded agent patterns | Customer and work evidence recorded in the cohort map | High |

Confidence describes the strength of the routing evidence, not proficiency or
performance. Ask each person to confirm or narrow the suggested contribution
before involving them.

The current cohort evidence does not identify a confirmed housing-retrofit,
PAS 2035, resident-research or housing-contract specialist. Zava North Homes
should nominate those experts from its own competent and accountable roles.

## Proposed Assistant Concept

The
[Housing Data and Performance Lead](../../.github/agents/company-data-performance-lead.agent.md)
is a fictional research profile for generating and interrogating clearly
labelled synthetic datasets against this brief. It is not the operational
assistant described below and has no implied access to company data.

### Working Name

Retrofit Flow Evidence Assistant

### Proposed Description

Reconstructs the evidence-backed property lifecycle from approved read-only
data extracts, calculates stage and queue time using deterministic rules,
identifies missing or conflicting records, and prepares candidate constraint
packs for validation by named operational owners. It does not determine root
cause without evidence, make controlled decisions, contact residents or change
source records.

### Intended Users

* Retrofit Flow and Data Analyst
* Retrofit Programme Manager
* Benefits and evaluation owner
* Authorised data and control owners reviewing their own domain

### Jobs to Support

1. Reconcile approved property and building identifiers across source extracts.
2. Map source events to the validated lifecycle dictionary.
3. Calculate deterministic stage, queue, handoff and return-loop durations.
4. Report missing timestamps, identifier conflicts and unsupported cause codes.
5. Segment results by approved operational dimensions.
6. Generate a traceable evidence pack for each candidate constraint.
7. Capture human validation, correction or dispute without overwriting source
   evidence.
8. Compare observed constraints with process, platform, workflow, capacity,
   contract and bounded-AI response options.

### Inputs

* Approved read-only extracts from authoritative company systems
* Validated property, building and work-package identifiers
* Lifecycle and event dictionary
* Delay and exception taxonomy
* Role and authority matrix
* Data-quality, access and retention rules
* Approved baseline and comparison definitions

### Outputs

* Data coverage and quality report
* Property lifecycle reconstruction with source traceability
* Stage-age, queue-time and return-loop analysis
* Unowned and disputed handoff report
* Candidate constraint evidence packs
* Contradicting evidence and unresolved-data register
* Intervention options matrix
* Human validation and decision log

### Authority and Safety Boundary

The assistant should begin at a low autonomy level with read-only access. It
may calculate, reconcile, draft and flag. It must not:

* Write to operational source systems
* Progress or close a property lifecycle state
* Infer consent, vulnerability, refusal or resident intent
* Diagnose hazards or release a safety hold
* Produce or approve a professional PAS 2035 output
* Commit supplier capacity, allocate work or confirm appointments
* Accept quality, close a defect or release payment
* Determine grant eligibility, submit a claim or record cash
* Rank properties for live investment without a separately approved policy
* Present an inferred cause as a validated company finding

Deterministic code should calculate identifiers, durations, counts and
reconciliations. A language model, if used, should be limited to source-linked
summaries, question generation and draft evidence narratives.

### Proposed Tools

The eventual agent design may require:

* Read-only data-query tools over an approved analytical store
* Deterministic lifecycle and duration calculation functions
* Data lineage and source-record retrieval
* Controlled document generation
* Human review, correction and sign-off capture
* Export of analysis and evidence independently of the AI supplier

Direct access to resident communication, scheduling, contract award, finance,
quality acceptance or operational workflow actions is not required for the
discovery agent and should be denied.

## Readiness Before Writing the Agent

Do not create an operational agent until the team has:

* Nominated the accountable discovery owner
* Agreed the baseline population and accepted-handover endpoint
* Validated the current-state lifecycle and event dictionary
* Produced the source-to-field and identifier map
* Approved lawful access, data minimisation, retention and security controls
* Defined delay, exception and disputed-attribution handling
* Established deterministic calculation and reconciliation tests
* Defined human reviewers and acceptance criteria
* Selected a non-agent comparator
* Confirmed manual analysis and export remain possible

An agent definition can be drafted earlier as a design hypothesis, but it
should not be connected to company data or described as an approved solution.

## Evaluation Criteria

Compare the assistant with manual analysis, conventional business intelligence
and deterministic workflow reporting.

| Measure | Proposed evaluation question |
| --- | --- |
| Population coverage | Does the analysis include incomplete, paused, excluded and reopened cases? |
| Identifier reconciliation | How many property and building records remain unmatched or disputed? |
| Event accuracy | Do source owners confirm the mapped state and timestamp? |
| Calculation repeatability | Does the same approved dataset produce the same durations and counts? |
| Attribution quality | How often do owners confirm, reject or dispute a proposed cause? |
| Traceability | Can every finding be traced to source events and calculation rules? |
| Review effort | Does assistance reduce analyst and domain-owner time after correction and assurance? |
| Decision usefulness | Does the analysis change a process, capacity, contract, capital or technology decision? |
| Error severity | Could an omission or incorrect attribution conceal safety, resident, financial or quality risk? |
| Whole-life value | Does incremental benefit exceed integration, review, assurance, support and exit costs? |

## Immediate Next Step

The sponsor should nominate one accountable discovery owner and confirm whether
the organisation can provide the complete twelve-month population with
property and building identifiers, lifecycle timestamps, pauses, reopens,
blocker reasons, queue owners, supplier and subcontractor references, and
accepted-handover status.

If the evidence cannot be assembled, the first investment is data ownership
and workflow instrumentation rather than an agent.
