---
title: Phase 1 Step 1.1 Engagement Contract Implementation Details
description: Execution details for drafting, confirming and accepting the engagement contract
ms.date: 2026-09-20
ms.topic: reference
---
<!-- markdownlint-disable-file -->

## Context Reference

Sources:

* `.copilot-tracking/research/2026-09-20/phase-1-step-1-1-engagement-contract-research.md`
* `.copilot-tracking/research/subagents/2026-09-20/phase-1-step-1-1-engagement-contract-research.md`
* `.copilot-tracking/research/2026-09-19/case-study-85-day-delivery-research.md`

## Implementation Phase 1: Create the Labelled Contract Draft

<!-- parallelizable: false -->

### Step 1.1: Reconcile the Delivery Sequence and Contract Defaults

Use the detailed eleven-session sequence as the baseline. Assign Session 3 to
operations and safety, Session 4 to resident, finance and option work, and
Session 5 to high-level architecture. Treat sponsor and evidence validation as
an asynchronous gate after the Step 1.1 and Step 1.2 artifacts unless the
sponsor explicitly reallocates a numbered session.

Preserve the ask, audience, investment envelope, pilot containment and review
commitments as `PROPOSAL` or `TBC` until accepted. Keep confirmed authority and
human-control boundaries labelled separately.

Files:

* `.copilot-tracking/changes/2026-09-19/case-study-85-day-delivery-changes.md` -
  Record the reconciled sequence and evidence-labelled defaults.

Discrepancy references:

* DD-01 resolves the Session 3-5 conflict.

Success criteria:

* One unambiguous eleven-session sequence governs the draft.
* Step 1.3 does not silently consume a delivery session.
* No unconfirmed default is presented as fact.

Dependencies:

* None

### Step 1.2: Create the Engagement-Contract Implementation Record

Create the missing target before requesting human confirmations. Populate:

1. Step status and confirmation log
2. One-page goal card
3. Decision ladder
4. Audience and influence map
5. Evidence classification legend and initial claim register
6. Eleven-session review calendar
7. Timed one-hour presentation shell
8. Acceptance record and unresolved items

Use explicit `PROPOSAL`, `TBC`, `CONFIRMED` and `BLOCKED` states. Calendar rows
without appointments, owners or deadlines remain `TBC`; they must not resemble
booked commitments. The presentation shell must total 60 minutes, including a
10-minute opening and 6-minute structured challenge.

Files:

* `.copilot-tracking/changes/2026-09-19/case-study-85-day-delivery-changes.md` -
  Create the self-contained draft implementation record.

Discrepancy references:

* DR-01 through DR-05
* DD-01 and DD-02

Success criteria:

* All eight required sections are present and internally consistent.
* Every claim has a source, classification, status and next check.
* Human authority and stop conditions are explicit.
* The record reports Step 1.1 as in progress.

Dependencies:

* Step 1.1 completion

## Implementation Phase 2: Obtain Human Confirmations and Calendar Evidence

<!-- parallelizable: false -->
<!-- blocked: awaiting human input -->

### Step 2.1: Obtain the Minimum Sponsor and Meeting-Owner Confirmations

Stop at this step if authorised people are unavailable. Report the open items
instead of fabricating responses. Collect one focused confirmation at a time:

1. Exact one-sentence decision request
2. Exactly four or five final executive audience roles
3. Existing deck treatment as editable baseline or reference-only
4. Evidence acceptance owner
5. Asynchronous Step 1.3 validation treatment

Record the respondent, authority, date, accepted wording and qualifications.
Fictional role-agent output, comparator practice and inferred availability do
not constitute confirmation.

Files:

* `.copilot-tracking/changes/2026-09-19/case-study-85-day-delivery-changes.md` -
  Update the confirmation log and item statuses.

Discrepancy references:

* DR-01 through DR-05

Success criteria:

* The ask and audience are accepted rather than merely drafted.
* Every confirmation identifies its authority and date.
* Rejected or qualified wording remains visible.

Dependencies:

* Implementation Phase 1
* Sponsor or authorised sponsor-level proxy
* Final meeting owner

### Step 2.2: Reserve All Eleven Work and Review Slots

For each session, record an exact start and end time, work owner, review owner,
feedback deadline, evidence input, gate and fallback. Convert provisional
windows into calendar invitations or equivalent reservations. Do not infer
availability from `support/cohort.md`.

Files:

* `.copilot-tracking/changes/2026-09-19/case-study-85-day-delivery-changes.md` -
  Add confirmed calendar commitments and reservation evidence.

Discrepancy references:

* DR-03

Success criteria:

* All eleven rows contain exact slots, owners and deadlines.
* Every feedback deadline precedes dependent work.
* Role assignments do not imply unconfirmed availability or endorsement.

Dependencies:

* Step 2.1 audience and authority confirmation
* Review-owner availability

## Implementation Phase 3: Finalize and Accept the Contract

<!-- parallelizable: false -->
<!-- blocked: awaiting human input -->

### Step 3.1: Verify Calendar Dependencies and the Finishing Margin

Walk the calendar in sequence. Confirm each input exists before its dependent
session, every review has a fallback route, and no substantive research,
architecture, feature or prototype recovery is scheduled from 2026-12-06
through 2026-12-13.

Files:

* `.copilot-tracking/changes/2026-09-19/case-study-85-day-delivery-changes.md` -
  Correct dependencies and document fallbacks.

Success criteria:

* No session depends on feedback due after the session starts.
* Every critical reviewer has an accepted fallback route.
* The finishing margin contains packaging, rehearsal, minor correction and
  final delivery only.

Dependencies:

* Implementation Phase 2

### Step 3.2: Run the Sponsor or Proxy Recall Check and Record Acceptance

Ask the sponsor or authorised proxy to repeat the problem, decision request,
evidence boundary, human-authority boundary, first-ten-minute promise and next
gate without additional explanation. Treat misunderstandings as corrections,
not acceptance.

Record the approver and date, accepted wording, rejected assumptions, open
items with owners and deadlines, deck-editing permission, and next gate.

Files:

* `.copilot-tracking/changes/2026-09-19/case-study-85-day-delivery-changes.md` -
  Update the acceptance record and final step status.

Success criteria:

* Recall covers all six required contract elements.
* Acceptance is distinguished from comments or positive feedback.
* Step 1.1 remains in progress if any blocking item is unresolved.

Dependencies:

* Step 3.1 completion
* Sponsor or authorised proxy availability

## Implementation Phase 4: Validate Step 1.1

<!-- parallelizable: false -->

### Step 4.1: Run Full Artifact Validation

Review the rendered Markdown for table structure, heading hierarchy, dates,
links and evidence labels. Verify the draft ask is one sentence and clearly
labelled, the audience contains no invented confirmations, and the calendar
contains exactly eleven rows with truthful statuses.

Run:

* `git diff --check`
* `git status --short`

If deck changes are separately authorised, edit maintained YAML sources rather
than the `.pptx`: `content/global/voice-guide.md`, `content/global/style.yaml`
and the opening, roadmap and decision-request slide YAML under
`.copilot-tracking/ppt/2026-09-18/proper-warm-cxo/`. Regenerate and visually
inspect the deck and rerun its existing property validation. Otherwise, confirm
all presentation artifacts remain unchanged.

Success criteria:

* Rendered Markdown is readable and internally consistent.
* Git reports no whitespace errors.
* Only approved targets changed.
* Step 1.1 status accurately reflects acceptance evidence.

Dependencies:

* Implementation Phase 1 for draft validation
* Implementation Phase 3 for acceptance validation

## Execution-Complete Criteria

* The draft implementation record exists with all eight sections.
* The 60-minute presentation shell and evidence labels are internally valid.
* Human-gated fields use explicit proposal, TBC or blocked states.
* Git diff validation passes for the draft.

## Human-Gated Acceptance Criteria

* DR-01 through DR-05 are resolved by authorised people.
* Eleven sessions have actual slots, owners and deadlines.
* Sponsor or proxy recall and acceptance are recorded.
* Step 1.1 is marked complete only after these conditions pass.
