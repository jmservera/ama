<!-- markdownlint-disable-file -->

# Implementation Details: Case Study 48 85-Day Delivery

## Context Reference

Sources: user requirements from 2026-09-19,
`.copilot-tracking/research/2026-09-19/case-study-85-day-delivery-research.md`
and
`.copilot-tracking/research/subagents/2026-09-19/case-study-delivery-research.md`.

## Working Method

Treat 2026-09-19 as planning day zero. The 85-day engagement runs from
2026-09-20 through 2026-12-13 inclusive. Complete substantive delivery in 11
protected weekly workdays ending 2026-12-05. Hold 2026-12-06 through
2026-12-13 as an unallocated finishing margin. Do not schedule research,
architecture, feature development or prototype rebuilding in that margin.

Start each session with a 30-minute capacity and evidence review. End with a
45-minute checkpoint that records the accepted artifact, rejected assumptions,
decisions, evidence gaps, feedback requests and remaining sessions. Limit work
in progress to the current session's primary deliverable.

Use three evidence labels in every artifact:

* Case-study fact
* Sector-informed hypothesis or comparator
* Unknown company detail requiring validation

Maintain a decision register for every material architecture, demo and narrative
choice. Record the decision, alternatives, evidence, trade-offs, owner,
reversal condition and date.

Maintain a living presentation shell from Session 1. Every accepted artifact
must update its slide-ready main-deck module or appendix module during the same
session. Run link, citation and readability checks on each new module before
the session closes. Session 10 integrates and tests these prepared modules; it
does not create the complete deck from scratch.

## Implementation Phase 1: Frame the Decision and Evidence

<!-- parallelizable: false -->

### Step 1.1: Session 1, 20-26 September, lock the engagement contract

Create a one-page goal card that names the audience, the requested final
decision, the first-10-minute promise, non-goals and the 11-session delivery
limit. Define success as an executive being able to repeat the problem, ask,
evidence, architecture boundary and next gate.

Files:
* `docs/case_study_48_original.md` - Immutable source problem
* `docs/case_study_48_addendum.md` - Evolving evidence and challenge record
* `.copilot-tracking/research/2026-09-19/case-study-85-day-delivery-research.md` - Planning synthesis

Outputs:
* Goal card and decision ladder
* Audience and influence map for four or five CxO roles
* Evidence classification legend
* Source and claim register skeleton
* Mentor review calendar with feedback deadlines
* Presentation shell with the one-hour run of show and slide placeholders

Success criteria:
* The final ask fits in one sentence
* The non-goals explicitly exclude production rollout and portfolio benefit proof
* Every one of the 11 delivery sessions has a reserved calendar slot and review owner

Dependencies:
* Access to the case-study source and available mentor calendar

### Step 1.2: Session 2, 27 September-3 October, establish traceability

Create a requirement and claim matrix covering the original case study,
addendum, BRD and current regulatory references. Separate facts, scenarios,
targets and unknowns. Record the MEES wording conflict and regulatory recheck
dates.

Outputs:
* Requirement and claim traceability matrix
* Dated rule-source register with in-force, future, guidance and
  confirmation-needed states
* Assumption and unknown-company-detail backlog
* Initial executive risk register
* Slide-ready evidence, regulation and unknowns module

Success criteria:
* Every claim intended for the first 10 minutes has a source and evidence label
* No grant, borrowing, throughput or resident outcome is presented as a company fact
* Awaab's Law Phase 2 and MEES status have dated review actions
* PAS 2035 is not presented as a general statutory duty; the applicable edition,
  contract and funding conditions are marked for competent confirmation
* Non-statutory guidance is labelled as guidance rather than legislation

Dependencies:
* Step 1.1 completion

### Step 1.3: Validate framing and evidence

Ask a sponsor proxy to review the goal card and a legal or sector reviewer to
challenge only the core regulatory statements. Do not ask reviewers to approve
the solution at this stage.

Validation:
* The sponsor proxy can identify the decision and non-goals without explanation
* The source register distinguishes binding requirements from policy direction
* Any contested claim is removed from the core story until resolved

## Implementation Phase 2: Challenge the Request and Select the Proposition

<!-- parallelizable: false -->

### Step 2.1: Session 3, 4-10 October, investigate operations and safety

Run one-question-at-a-time interviews with the fictional Asset Executive,
Building Safety Lead, Retrofit Programme Manager and Neighbourhood Housing
Officer. Treat every response as a research instrument output rather than
company knowledge.

Outputs:
* Current-state resident and property journey
* Fifteen-stage lifecycle and handoff map
* Human authority and stop-control matrix
* Ranked unknowns and candidate binding constraints
* Slide-ready resident journey, lifecycle and authority module

Gate A:
* Continue only if the problem and requested decision fit in one sentence
* If they do not, discard the solution framing and restart with an
  evidence-discovery proposition

Success criteria:
* Safety and damp-and-mould response are independent of retrofit progression
* Every irreversible decision has a named human role
* Interview statements retain fact, hypothesis or unknown labels

Dependencies:
* Phase 1 completion

### Step 2.2: Session 4, 11-17 October, investigate value and acceptance

Run equivalent interviews with Finance and Grants, Procurement and Contracts,
Resident Engagement, and Data and Performance profiles. Compare four paths:
process change, conventional workflow or BI, bounded AI control plane, and the
original five-agent concept.

Outputs:
* Resident choice, accessibility, withdrawal and redress journey
* Grant opportunity-to-cash evidence chain
* Supplier capacity and quality-control gate
* Synthetic-data specification
* Options appraisal with desirability, feasibility, viability and risk
* Draft benefits and evaluation scorecard covering accepted handovers,
  cycle time, manual review effort, resident outcomes, safety, quality,
  evidence completeness, complaints and cash
* Slide-ready options, value and scorecard module

Success criteria:
* At least one non-agent option remains viable
* Retrofit-programme value is separated from incremental technology value
* Resident consent cannot be inferred or optimised away
* Every scorecard metric has a definition, baseline owner, baseline status,
  proposed target, measurement window, attribution method and stop threshold
* The 20% cycle-time and 25% manual-effort improvements remain unratified
  proposals until a baseline owner accepts them

Dependencies:
* Step 2.1 completion

### Step 2.3: Session 5, 18-24 October, choose the proposition

Draft the high-level architecture and decide whether the core proposition is a
portfolio control plane with bounded AI assistance. Show actors, systems of
record, trust boundaries, deterministic controls, human decisions, analytics
and manual fallback on one slide.

Outputs:
* High-level architecture
* Target operating model
* Primary architecture decision records
* Executive options slide and recommendation
* Slide-ready high-level architecture and trade-off module

Gate B:
* Kill the five-agent-first design unless evidence shows unique value that a
  simpler process, workflow or BI option cannot deliver
* Restart from lifecycle, decision rights and evidence flow if human authority
  cannot be shown clearly

Success criteria:
* A non-technical reviewer explains the architecture in under 60 seconds
* AI verbs are limited to recommend, draft, reconcile and flag
* Systems of record remain authoritative

Dependencies:
* Steps 2.1 and 2.2 completion

## Implementation Phase 3: Review and Recover the Architecture

<!-- parallelizable: false -->

### Step 3.1: Session 6, 25-31 October, protected feedback and restart

Use this entire session for mentor, architecture, sector and privacy feedback.
Do not add features. Test whether the proposition solves an evidenced problem,
the ask is proportionate and the high-level boundaries are credible.

Decision paths:
* Accept: freeze the high-level concept and proceed
* Repair: correct a bounded evidence or diagram issue and repeat the check
* Restart: discard the value or boundary assumption and rebuild the
  high-level proposition during this session
* Stop: fall back to an evidence/readiness proposition if no solution is
  supportable

Outputs:
* Feedback synthesis grouped by evidence, value, control and communication
* Root-cause record for every rejected assumption
* Accepted high-level architecture or documented fallback proposition
* CxO objection and answer backlog seeded from reviewer feedback
* Updated slide modules reflecting accepted feedback
* Updated remaining-capacity forecast

Success criteria:
* No medium-level architecture begins from a rejected high-level design
* Every material review comment is accepted, rejected with rationale or deferred
* One restart can be absorbed without using Session 11

Dependencies:
* Phase 2 completion

## Implementation Phase 4: Detail the Design and Test Its Evidence

<!-- parallelizable: false -->

### Step 4.1: Session 7, 1-7 November, create medium-level architecture

Decompose the accepted concept into adapters, identity reconciliation,
append-only lifecycle events, dated policy rules, deterministic state machine,
work queues, evidence ledger, bounded assistants, approvals, exceptions,
analytics, audit, observability and rollback.

Outputs:
* Component and responsibility diagram
* Data and event flow diagram
* Trust-boundary and threat summary
* Failure, manual fallback, disable and replay paths
* Medium-level architecture decision records
* Slide-ready medium-level architecture and control module

Success criteria:
* Every high-level boundary maps to a component or human process
* Material changes invalidate stale approvals and evidence
* Source, version, authority, rationale and timestamp survive every transition
* No AI component can perform an irreversible action

Dependencies:
* Accepted Phase 3 output

### Step 4.2: Session 8, 8-14 November, create synthetic evidence and demo gate

Specify and generate approximately 500 synthetic properties over 12 months
with capacity, resident, supplier, building dependency, evidence, finance and
quality constraints. Keep ground truth separate and validate deterministic
relationships.

Outputs:
* Synthetic dataset, manifest and data dictionary
* Hidden ground truth and validation report
* Three executive demo scenarios, including a failure path
* Mentor-reviewed prototype specification with explicit rejection criteria
* Demo/no-demo decision record
* Slide-ready synthetic evidence and demonstration-method module

Gate C:
* Build only when the data validates, the slice can reset cleanly, the scenario
  fits six minutes and it adds decision evidence beyond two slides
* After two bounded failed build or validation attempts, reduce to one smaller
  deterministic slice or switch to a static walkthrough

Success criteria:
* All identifiers and records are explicitly synthetic
* No real names, addresses, credentials or free-text health data are present
* A reviewer can identify why a property is blocked and who owns the next action
* The mentor accepts or rejects the prototype specification before code is retained

Dependencies:
* Step 4.1 completion

### Step 4.3: Session 9, 15-21 November, prototype or rebuild the narrow slice

Begin from the Session 8 mentor decision. If the specification was rejected,
discard the prototype design and any exploratory code, then rebuild from a
clean slate around the corrected acceptance criterion. Build only the selected
flow: a property timeline, portfolio constraint queue, control preventing
unsafe progression and a source-linked bounded-AI summary. If the clean
rebuild does not pass by the midpoint checkpoint, stop coding and produce
tested screenshots or a short recorded walkthrough using the same scenario.

Outputs:
* Narrow prototype or static walkthrough
* Restart root cause and corrected acceptance criterion when a rebuild occurs
* Six-minute runbook and reset procedure
* Screenshot or recorded fallback
* Failure narration and known-limitations list
* Accepted demo/fallback record and slide-ready demonstration module

Success criteria:
* The demonstration starts from a clean state and is repeatable
* Network access, hidden credentials and live systems are unnecessary
* Failure does not produce an unsafe or success-shaped result
* The fallback communicates the same decision evidence
* A complete prototype discard consumes only Session 9 and cannot consume
  presentation assurance capacity

Dependencies:
* Gate C decision

## Implementation Phase 5: Build and Test the Executive Experience

<!-- parallelizable: false -->

### Step 5.1: Session 10, 22-28 November, integrate and test the executive story

Present the first 10 minutes to an executive proxy before polishing the full
deck. Test decision recall, evidence trust, architecture comprehension and the
value of the demo. Test whether the proxy can explain how the scorecard decides
if readiness should progress to a live pilot. Integrate the slide-ready modules
created in Sessions 1-9, apply at most one bounded rewrite of the opening
sequence, complete speaker notes and appendix assembly, and perform the full
claim, economics and scorecard reconciliation.

First-10-minute sequence:
* 0:00-1:30: Decision, urgency and explicit non-approval boundaries
* 1:30-3:30: Illustrative resident/property journey
* 3:30-5:30: Insight that spreadsheets may be a symptom, not the constraint
* 5:30-7:30: High-level architecture and human control
* 7:30-9:00: Labelled scenario value and largest unknowns
* 9:00-10:00: Staged ask, measures, kill gates and consequence of no

Full run of show:
* 10-18 minutes: evidence, regulation and unknowns
* 18-28 minutes: current journey, target operating model and high-level design
* 28-38 minutes: medium-level design, controls and trade-offs
* 38-44 minutes: demo or fallback
* 44-50 minutes: economics, value attribution and downside
* 50-54 minutes: roadmap, gates, owners and requested decision
* 54-60 minutes: structured challenge and decision confirmation

Outputs:
* Complete draft deck, notes and appendix
* Reconciled claim, economics and scorecard register
* Updated CxO objection and answer bank
* Executive-proxy findings and bounded opening revision record

Gate D:
* If the proxy cannot repeat the ask, supporting evidence and stop conditions,
  rewrite only the opening sequence using the already accepted evidence
* If the proxy still cannot repeat them after one bounded rewrite, remove the
  live demo and simplify the story rather than starting another narrative cycle

Success criteria:
* The ask is stated in the first and final 10 minutes
* Each core slide has one message and one executive purpose
* Architecture depth increases without repeating identical explanations
* Detailed legal, schema, economics and traceability content remains in appendix
* The scorecard separates unknown baseline, scenario, proposed pilot target,
  measurement owner, attribution and stop condition

Dependencies:
* Phase 4 completion

### Step 5.2: Session 11, 29 November-5 December, final assurance and readiness freeze

No narrative, architecture or prototype repair is permitted in this session.
Perform a delta-only legal review after Awaab's Law Phase 2 applies on
2026-11-30. Confirm the status of Phase 2 guidance, MEES implementation and the
applicable PAS 2035 edition, contract and funding conditions. Reconcile only
changes arising from that delta review. Run one timed rehearsal and one final
cold-start verification of the already accepted demo and static fallback, then
freeze the presentation package.

Outputs:
* Final regulatory and claim review
* Frozen deck, notes and appendix
* Delta reconciliation for any post-30-November change
* Ratified or explicitly provisional benefits and evaluation scorecard
* Timed rehearsal and demo-failure evidence
* Presentation-ready package

Gate E:
* Remove the live demo if it requires a network, credentials, manual data
  repair, more than six minutes or fails a cold-start rehearsal
* Freeze discretionary scope at the end of this session
* Do not enter the finishing margin with incomplete evidence, architecture or
  an untested opening narrative

Success criteria:
* One full rehearsal completes in 54 minutes or less before Q&A
* Opening pitch completes in 9-10 minutes
* The delta review resolves or labels every post-30-November regulatory change
* PAS 2035 and non-statutory guidance caveats are explicit
* Static fallback is immediately available
* High-level architecture is readable without narration
* Medium-level architecture is explainable in under 10 minutes
* Demo and fallback each fit the allocated six minutes
* The requested decision, authority, owner, next gate and stop conditions are explicit

Dependencies:
* Step 5.1 completion

## Reserved Finishing Margin and Presentation

The period from 2026-12-06 through 2026-12-13 is not a planned delivery
session. Keep up to one workday unallocated for last finishing details and the
presentation.

Permitted uses:
* Correct a citation, typo, broken link, layout defect or accessibility issue
* Apply minor wording improvements arising from the frozen rehearsal
* Package, export and back up the deck, appendix, diagrams and demo fallback
* Run one confidence rehearsal without changing the narrative structure
* Deliver the one-hour presentation and capture its decision

Prohibited uses:
* Add new research, claims, architecture, scope or features
* Rebuild the prototype or replace the selected technical direction
* Introduce a live dependency not tested and accepted in Session 11
* Conceal unresolved evidence or weaken safety, consent or approval boundaries

Presentation close:
* Ask each condition or objection to be attached to a named owner and date
* Record approval, conditional approval, request for more evidence or rejection
* Record the next gate, unanswered questions and evidence backlog

Success criteria:
* Main presentation completes in 50-54 minutes with at least six minutes for Q&A
* Outcome is recorded as a decision rather than inferred from positive feedback
* Conditions and follow-up owners are confirmed before the session ends

## Dependencies

* Weekly protected workday and mentor review windows
* Access to current repository evidence
* Human legal, housing, architecture, privacy and executive-proxy reviewers
* Presentation and diagram tooling
* Optional local development environment for a network-independent demo

## Success Criteria

* The substantive plan finishes in 11 weekly sessions by 2026-12-05
* The final 2026-12-06 through 2026-12-13 window remains unallocated margin
  until the presentation-ready package passes Session 11
* The first 10 minutes make a bounded, evidence-backed decision easy to repeat
* High- and medium-level architectures show human and deterministic controls
* Every material decision has evidence, alternatives and reversal conditions
* Synthetic data is non-identifying, validated and never presented as company data
* A failed prototype can be discarded without endangering presentation readiness
* The final hour ends with an explicit decision, conditions, owners and next gate
