<!-- markdownlint-disable-file -->

# Planning Log: Case Study 48 85-Day Delivery

## Discrepancy Log

Revalidation found no remaining Critical or Major discrepancy.

### Resolved Findings

* PV-01, resolved: 2026-09-19 is explicitly planning day zero. The inclusive
  execution period from 2026-09-20 through 2026-12-13 is 85 days and is divided
  into exactly 12 session windows, with one protected workday in each
  (`case-study-85-day-delivery-details.md:12-16,39-399`).
* PV-02, resolved: Session 8 now requires mentor acceptance or rejection before
  code is retained. Session 9 owns complete discard and clean rebuild, switches
  automatically to the tested static fallback at its midpoint, and cannot use
  presentation-assurance capacity
  (`case-study-85-day-delivery-details.md:247-303`). Session 11 explicitly
  prohibits prototype rebuild (`case-study-85-day-delivery-details.md:348-352`).
* PV-03, resolved: The quantitative benefits/evaluation scorecard is drafted in
  Session 4, tested with an executive proxy in Session 10, and ratified or
  labelled provisional in Session 11. It includes definitions, baseline owner
  and status, proposed target, measurement window, attribution and stop
  threshold; the 20% and 25% figures remain unratified proposals
  (`case-study-85-day-delivery-details.md:132-160,308-379`).
* PV-04, resolved: Sessions 2 and 11 explicitly check PAS 2035 applicability,
  edition, contract and funding conditions and distinguish non-statutory
  guidance from legislation
  (`case-study-85-day-delivery-details.md:66-90,348-379`).

### Remaining Non-Major Open Input

* PV-05: The named C-suite chair, meeting authority and readiness budget ceiling
  remain unknown. This is not a plan defect or blocker because the documented
  default is a capped readiness and shadow-design mandate with no live
  deployment or portfolio capital release. Session 12 requires the final
  decision, amount or authority, owner, next gate and stop conditions to be
  explicit (`case-study-85-day-delivery-details.md:384-399`).

## Implementation Paths Considered

### Selected: Governed control-plane readiness and shadow pilot

* Approach: Present deterministic lifecycle and evidence controls with bounded
  AI assistance, tested through synthetic data and a narrow shadow scenario
* Rationale: It challenges the original agent-first framing while preserving
  ambition, resident value and a credible investment decision
* Evidence: `.copilot-tracking/research/subagents/2026-09-19/case-study-delivery-research.md`

### IP-01: Implement the original five-agent architecture

* Approach: Design and demonstrate all five named agents as the primary solution
* Trade-offs: Strong visual alignment with the brief, but weak evidence,
  excessive breadth, blurred authority and high demo risk
* Rejection rationale: Twelve sessions cannot validate five end-to-end agent
  responsibilities or prove that administration is the binding constraint

### IP-02: Deliver architecture and business case without a prototype

* Approach: Focus all capacity on evidence, diagrams, economics and presentation
* Trade-offs: Highest narrative reliability but less tangible proof of the
  lifecycle and evidence design
* Rejection rationale: A gated narrow demo can increase comprehension without
  making implementation success a dependency

### IP-03: Build a dashboard-first proof of concept

* Approach: Create portfolio reporting over synthetic data without workflow controls
* Trade-offs: Fast and demonstrable, but risks treating visibility as resolution
  and cannot show authority, evidence or safety gates
* Rejection rationale: The core proposition is controlled handover progression,
  not another reporting surface

## Suggested Follow-On Work

* WI-01: Validate the real operating baseline and binding constraint (High)
  * Effort: 6-8 weeks of readiness discovery
  * Source: Addendum, BRD and evidence gaps
  * Dependency: C-suite readiness approval
* WI-02: Complete legal, DPIA and information-governance assessments (High)
  * Effort: Specialist assessment during readiness and before real-data use
  * Source: UK GDPR and regulatory research
  * Dependency: Defined processing purpose, data scope, suppliers and hosting
* WI-03: Run a controlled shadow pilot in one bounded locality or flow (High)
  * Effort: 6-9 months subject to readiness findings
  * Source: Recommended executive proposition
  * Dependency: Validated baseline, architecture, funding and named owners
* WI-04: Create the production architecture and procurement package (Medium)
  * Effort: To be estimated after the shadow pilot
  * Source: Unknown company standards and supplier landscape
  * Dependency: Pilot evidence and technology-option decision

## Validation Status

Validated.

No Critical or Major issues remain. PV-01 through PV-04 are resolved, and PV-05
is a non-blocking input with a safe stated default. Revalidation confirms exact
85-day and 12-session capacity, accurate detailed-plan line ranges, explicit
evidence labels and regulatory caveats, decision and restart gates, high- and
medium-level architecture deliverables, synthetic-data controls, bounded
prototype rebuild and static fallback, quantitative evaluation measures, and a
60-minute presentation with a tested first 10 minutes and six-minute challenge
reserve. The artifacts satisfy the Task Planner requirements for referenced
research, actionable implementation detail, dependencies, validation criteria,
deferred follow-on work and linked discrepancy tracking.
