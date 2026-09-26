---
title: Phase 1 Step 1.1 Engagement Contract Planning Log
description: Discrepancies, implementation paths and follow-on work for the engagement contract
ms.date: 2026-09-20
ms.topic: reference
---
<!-- markdownlint-disable-file -->

## Discrepancy Log

Gaps and differences identified between research findings and the
implementation plan.

### Unaddressed Research Items

* DR-01: RESOLVED on 2026-09-20. The final meeting owner, acting with sponsor
  authority, approved the proposed one-sentence final ask as written.
  * Source: `.copilot-tracking/research/subagents/2026-09-20/phase-1-step-1-1-engagement-contract-research.md` (Line 167)
  * Resolution evidence: User confirmation in the implementation session.
  * Impact: resolved
* DR-02: RESOLVED on 2026-09-20. The final meeting owner, acting with sponsor
  authority, confirmed all five proposed executive audience roles.
  * Source: `.copilot-tracking/research/subagents/2026-09-20/phase-1-step-1-1-engagement-contract-research.md` (Line 168)
  * Resolution evidence: User confirmation in the implementation session.
  * Impact: resolved
* DR-03: Exact session slots, review owners and feedback deadlines are absent.
  * Source: `.copilot-tracking/research/subagents/2026-09-20/phase-1-step-1-1-engagement-contract-research.md` (Lines 169-170)
  * Reason: Calendar commitments require human availability.
  * Impact: high
* DR-04: RESOLVED on 2026-09-20. The existing deck is the editable baseline
  for later authorised work and remains unchanged in this contract-only run.
  * Source: `.copilot-tracking/research/subagents/2026-09-20/phase-1-step-1-1-engagement-contract-research.md` (Lines 171-172)
  * Resolution evidence: User confirmation in the implementation session.
  * Impact: resolved
* DR-05: RESOLVED on 2026-09-20. The Legal, Governance or Regulatory lead
  owns evidence-threshold acceptance and contested-claim removal.
  * Source: `.copilot-tracking/research/subagents/2026-09-20/phase-1-step-1-1-engagement-contract-research.md` (Lines 183-185)
  * Resolution evidence: User confirmation in the implementation session.
  * Impact: resolved

### Plan Deviations from Research

* DD-01: Use the detailed delivery sequence rather than the primary calendar's
  Session 3-5 mapping.
  * Research recommends: Session 3 operations and safety, Session 4 resident,
    finance and options, and Session 5 high-level architecture.
  * Plan implements: The recommended detailed sequence and asynchronous Step
    1.3 validation by default.
  * Rationale: This preserves all eleven outputs and avoids omitting the
    architecture session.
* DD-02: Do not update the existing deck during Step 1.1 by default.
  * Research recommends: Update presentation YAML only if the deck is confirmed
    as the baseline.
  * Plan implements: A complete run of show in the contract, with presentation
    edits gated by explicit permission.
  * Rationale: The existing deck is not proven narratively or factually ready.

### Validation Findings 2026-09-20

* VF-01: Every `Details` line-number reference in the plan is wrong.
  * Plan states Lines 9-39, 40-67, 68-94, 95-118, 119-151, 152-178, 179-210.
  * Actual detail sections start at 21, 56, 94, 121, 148, 181, 217 and the
    file ends at line 255.
  * Impact: critical (execution will read the wrong guidance).
* VF-02: The plan's Phase 3 ordering makes the only agent-executable
  deliverable unreachable.
  * Step 3.1 creates the missing implementation record but depends on
    Phases 1 and 2, which require sponsor, audience and calendar
    confirmations that planning may not invent.
  * Impact: critical (execution stalls at Step 1.2 with no artifact created).
* VF-03: Plan Success Criteria mix agent-completable and human-gated outcomes
  without distinguishing them, so Step 1.1 can never be reported complete by
  execution alone.
  * Affected: exact slots and owners, four or five confirmed roles, sponsor
    or proxy acceptance.
  * Impact: major.
* VF-04: Plan Steps 4.1 and 4.2 carry no `Details` reference, unlike every
  other step and the 2026-09-19 plan convention; details contain a single
  Step 4.1 covering all three plan steps.
  * Impact: major (plan and details step numbering diverge).
* VF-05: Planning-log source line references are offset from the subagent
  research.
  * Actual: ask line 167, attendees line 168, slots and owners lines 169-170,
    deck designation lines 171-172, evidence owner lines 183-185.
  * Impact: major (traceability cannot be verified as written).
* VF-06: Details Step 1.2 cites `DR-01 through DR-04`, but confirmation item 4
  in that step is the evidence acceptance owner, which is DR-05.
  * Impact: minor (discrepancy coverage gap).
* VF-07: The conditional presentation targets identified by research
  (`content/global/voice-guide.md`, `content/global/style.yaml` and the
  opening, roadmap and decision-request slide YAML) are not carried into the
  plan or details as exact file targets.
  * Impact: minor (only relevant if DR-04 resolves to baseline).

### Validation Resolution 2026-09-20

* VF-01 resolved: all plan-to-details references now use the actual section
  ranges in the revised details file.
* VF-02 resolved: the labelled draft record is created in Phase 1 before any
  human-gated work; blocked phases stop and report gaps without fabrication.
* VF-03 resolved: execution-complete and human-gated acceptance criteria are
  separate.
* VF-04 resolved: Phase 4 uses one plan step matching one details step.
* VF-05 resolved: DR-01 through DR-05 source lines match the research file.
* VF-06 resolved: confirmation work explicitly covers DR-01 through DR-05.
* VF-07 resolved: conditional YAML targets and the prohibition on direct
  `.pptx` editing are included in the implementation details.

Remaining, non-blocking:

* VF-08: DD-01 resolves the Session 3-5 conflict only inside the new Step 1.1
  record. The controlling `.copilot-tracking/plans/2026-09-19/` plan and
  details still carry the conflicting mapping, and no step or follow-on item
  corrects them.
  * Source: `.copilot-tracking/research/subagents/2026-09-20/phase-1-step-1-1-engagement-contract-research.md` (Lines 173-174)
  * Impact: minor (later phases may read the superseded sequence).
* VF-09: Phase 4 sits last in the checklist, but details allow draft
  validation after Phase 1 while Phases 2-3 remain blocked. The plan does not
  state this, so a blocked run may skip Git validation of the draft.
  * Impact: minor (ordering ambiguity only).

## Implementation Paths Considered

### Selected: Contract-First Consolidation

* Approach: Create one self-contained implementation record from existing
  research, then record sponsor acceptance and calendar evidence in it.
* Rationale: This directly satisfies the active plan target, preserves evidence
  labels and avoids premature presentation rework.
* Evidence: `.copilot-tracking/research/subagents/2026-09-20/phase-1-step-1-1-engagement-contract-research.md` (Lines 53-82)

### IP-01: Update the Existing Research In Place

* Approach: Treat the primary research synthesis as the engagement contract.
* Trade-offs: Fewer files, but it mixes research and accepted implementation
  state and leaves the active plan target absent.
* Rejection rationale: Research proposals must remain distinguishable from
  sponsor-accepted commitments.

### IP-02: Rebuild the Presentation Before Contract Acceptance

* Approach: Revise the existing YAML deck and use it as the contract.
* Trade-offs: Produces visible presentation progress, but risks rework and
  embeds unconfirmed ask, audience and evidence decisions.
* Rejection rationale: The deck baseline and core contract are not accepted.

## Suggested Follow-On Work

* WI-01: Complete Step 1.2 source-to-claim traceability after the contract is
  accepted (high priority, medium effort).
  * Source: The contract's evidence classification and initial claim register.
  * Dependency: Step 1.1 sponsor or proxy acceptance
* WI-02: Decide and initialise the living presentation baseline (medium
  priority, medium effort).
  * Source: Unresolved deck treatment.
  * Dependency: DR-04 resolution
* WI-03: Confirm pilot locality, source systems and approval route during
  readiness planning (medium priority, high effort).
  * Source: Known company-detail gaps excluded from Step 1.1.
  * Dependency: Approval of the capped readiness exercise

## Implementation Progress

### 2026-09-20 Draft Contract

* Implementation Phase 1 is complete.
* The engagement-contract record now contains all eight required sections.
* Sessions 3-5 follow the reconciled sequence in DD-01.
* The review calendar contains exactly eleven provisional sessions.
* The presentation shell totals 60 minutes, including the 10-minute opening
  and 6-minute structured challenge.
* The contract remains `IN PROGRESS`; DR-01 through DR-05 block acceptance.
* No canonical documentation, source code or presentation artifacts changed.
* Draft validation passed `git diff --check` and structural checks.
* Phase 4 acceptance validation remains open and must be repeated after
  Implementation Phases 2 and 3. exercise
* Partial Step 2.1 progress resolved DR-01 on 2026-09-20.
* Step 2.1 is complete. DR-02, DR-04 and DR-05 were resolved on 2026-09-20.
* DR-03 remains open, so Step 2.2 and Implementation Phase 2 are incomplete.

## User Decisions

* ID-01: Final decision request - Approved as written
  * Authority: Final meeting owner acting with sponsor authority
  * Date: 2026-09-20 exercise
* ID-02: Final executive audience - Confirmed all five proposed roles
  * Authority: Final meeting owner acting with sponsor authority
  * Date: 2026-09-20
* ID-03: Presentation treatment - Editable baseline for later authorised work
  * Authority: Final meeting owner acting with sponsor authority
  * Date: 2026-09-20
* ID-04: Evidence acceptance owner - Legal, Governance or Regulatory lead
  * Authority: Final meeting owner acting with sponsor authority
  * Date: 2026-09-20
* ID-05: Sponsor and evidence validation - Keep as an asynchronous gate
  * Authority: Final meeting owner acting with sponsor authority
  * Date: 2026-09-20 exercise
* ID-06: Eleven-session reservations - Leave all reservations TBC and stop at
  the human gate
  * Rationale: Exact times, work owners, review owners and feedback deadlines
    are unavailable and must not be inferred.
  * Date: 2026-09-20 exercise
* WI-04: Align the parent 2026-09-19 plan and details with the accepted
  Session 3-5 sequence (medium priority, low effort).
  * Source: DD-01 and validation finding VF-08
  * Dependency: Acceptance of the detailed eleven-session sequence
