<!-- markdownlint-disable-file -->

# Phase 1 Step 1.1 Research: Engagement Contract

## Research Status

Complete for planning. Step 1.1 itself is in progress, not complete. Its core
content is drafted in the primary research synthesis, but the sponsor has not
confirmed the proposed final ask or executive audience, the eleven sessions do
not have actual calendar appointments, review owners or feedback deadlines,
and treatment of the existing presentation artifacts is unresolved.

Research was performed against the repository state on 2026-09-20. This
document distinguishes repository facts from proposed implementation choices
and does not treat fictional-company details as confirmed.

## Focused Outcome

The implementation plan should convert the existing draft into one accepted
engagement contract for Session 1. The contract must let a sponsor or
sponsor-level proxy repeat:

* The problem and one-sentence decision request
* The evidence posture and major unknowns
* The deterministic and human-authority boundary
* The first-ten-minute promise and one-hour narrative
* The eleven-session delivery limit, review commitments and next gate

It must not expand into Phase 1 Step 1.2 traceability work, detailed
architecture, synthetic-data design or production deployment planning.

## Repository Context and Current State

| File | Authority and current state | Step 1.1 implication |
| --- | --- | --- |
| `docs/case_study_48_original.md` | Immutable source brief. It establishes the 60,000-home context, original five-agent request, Executive Director of Assets sponsorship, Chief Executive involvement and resident control of consent. | Read only. Preserve the original framing as source evidence and do not edit it. |
| `docs/case_study_48_addendum.md` | Canonical evolving specification, dated 2026-09-20. It challenges agent-first delivery and recommends a governed control plane, capped readiness and pilot, human approvals and conditional value claims. | Read only for Step 1.1 unless a new material confirmation changes the specification. Do not duplicate its full business case in the contract. |
| `docs/brds/agentic-retrofit-programme-brd.md` | Draft for business validation. It recommends capped readiness and a gated pilot, identifies 25 open company decisions, and defines stage-specific approval. | Use as a boundary and open-decision source, not as evidence of approval. |
| `docs/brds/retrofit-flow-discovery-brief.md` | Discovery proposal. It makes constraint discovery and accepted handover the immediate focus and prohibits operational authority for a discovery assistant. | Use to keep the requested decision focused on evidence and a bounded next step. |
| `.copilot-tracking/research/2026-09-19/case-study-85-day-delivery-research.md` | Controlling Step 1.1 draft. It already contains the goal card, decision ladder, audience map, evidence legend, 25-claim register, calendar skeleton and one-hour presentation shell. Chief Executive chair and decision authority are recorded as confirmed on 2026-09-20. | Reuse and reconcile rather than redraft from scratch. The explicit step status remains incomplete. |
| `.copilot-tracking/details/2026-09-19/case-study-85-day-delivery-details.md` | Implementation details require a one-page goal card, audience map, evidence controls, review calendar and presentation shell. Success requires a one-sentence ask, explicit rollout/benefit non-goals, and reserved slots plus owners for all sessions. | Supplies the acceptance criteria and operating method. |
| `.copilot-tracking/plans/2026-09-19/case-study-85-day-delivery-plan.instructions.md` | The active plan points Step 1.1 to the detailed instructions. Its frontmatter applies implementation to `.copilot-tracking/changes/2026-09-19/case-study-85-day-delivery-changes.md`, which does not yet exist. | This missing changes file is the primary implementation target. |
| `.copilot-tracking/research/subagents/2026-09-19/case-study-delivery-research.md` | Detailed research validates the decision-led narrative and eleven-session sequence and notes that the prior deck is not proof of narrative, factual or delivery readiness. | Use for cross-checking sequence, deliverables and presentation caveats. |
| `.copilot-tracking/ppt/2026-09-18/proper-warm-cxo/` | An 11-slide initial proposal, YAML sources, voice guide and rendered validation exist. Property validation reports no structural warnings, but only slides 3-8 are covered by that report and narrative/factual readiness is not established. | Treat as reference only until the user confirms whether it is the editable baseline. |
| `support/cohort.md` | A provisional help-routing map whose confidence concerns evidence strength, not proficiency or availability. | It may suggest technical reviewers, but cannot supply a review owner or calendar commitment without human confirmation. |
| `support/company-profile-research.md` | Evidence base for fictional role agents; it explicitly separates comparators, hypotheses and unknown company details. | Use its role boundaries, but do not present role-agent output as company confirmation. |

## Exact Implementation Targets

### Required target

Create:

`c:\source\ama\.copilot-tracking\changes\2026-09-19\case-study-85-day-delivery-changes.md`

This is the exact `applyTo` target declared by the active implementation plan
and is currently absent. It should contain the accepted Step 1.1 engagement
contract as a compact, self-contained implementation record:

1. Step status and confirmation log
2. One-page goal card
3. Decision ladder
4. Audience and influence map
5. Evidence classification legend and initial source/claim register
6. Eleven-session review calendar
7. One-hour presentation shell
8. Acceptance record and unresolved items

### Conditional targets

Only if the existing deck is confirmed as the baseline, update the relevant
files under:

`c:\source\ama\.copilot-tracking\ppt\2026-09-18\proper-warm-cxo\content\`

The minimum likely presentation targets are `global\voice-guide.md`,
`global\style.yaml`, and the slide YAML files that implement the opening,
roadmap and decision request. The exact slide files should be selected only
after comparing the accepted run of show with the existing deck. Do not edit
the `.pptx` directly when YAML is the maintained source.

No canonical document change is required merely to complete Step 1.1: the
addendum and BRD already contain the current proposition and controls. If a
new sponsor confirmation materially changes them, update
`docs/case_study_48_addendum.md` in a separately scoped change and advance its
`ms.date`; never change `docs/case_study_48_original.md`.

## Draft Contract Content Ready for Reuse

The primary research already supplies the following planning defaults:

* Final chair and decision authority: Chief Executive, confirmed
* Accountable sponsor: Executive Director of Assets, confirmed
* Proposed ask: approve a capped readiness and shadow-pilot exercise to test a
  controlled retrofit delivery service, not production or portfolio rollout
* Recommended option: Tier 2 readiness plus a narrow shadow pilot
* Proposed envelope: GBP 100,000 to GBP 250,000, with approval sought up to
  GBP 250,000 through gated tranches
* Pilot containment: one active locality or programme, no more than 12 weeks
  or 50 cases
* Human authority: consent, safety, PAS 2035 outputs, finance, procurement,
  claims, payments and quality acceptance stay with authorised people
* Delivery limit: eleven focused sessions through 2026-12-05, with
  2026-12-06 through 2026-12-13 protected as finishing margin
* First-ten-minute promise: decision, stakes, core insight, high-level
  architecture, labelled ROI scenario and stop conditions
* Non-goals: no production rollout, autonomous portfolio implementation,
  assumed five-agent approval or unvalidated company benefit claims

These items must retain their evidence labels. User confirmations recorded in
the synthesis may be treated as confirmed planning inputs; proposals and
unknowns must not silently become facts.

## Deliverables and Completion Evidence

| Deliverable | Required content | Completion evidence |
| --- | --- | --- |
| Goal card | Audience, one-sentence decision, first-ten-minute promise, non-goals, delivery limit, sponsorship and authority boundary | Sponsor or sponsor-level proxy accepts the wording; proposal and unknown labels remain visible |
| Decision ladder | Sequence from framing confirmation through readiness, shadow approval and any later live or scale decision | Each rung states its decision authority and proves that one approval does not imply the next |
| Audience map | Four or five executive roles, influence, assurance need and confirmation status | Named or role-based attendees are confirmed by the meeting owner |
| Evidence controls | Classification legend and an initial claim register with source, status and next check | Every claim used in the goal card has a source and label |
| Review calendar | Eleven exact work slots, review owner, feedback deadline, gate and fallback | Invitations or equivalent reservations exist; broad weekly windows alone do not qualify |
| Presentation shell | Eight timed modules totalling 60 minutes, including the first-ten-minute opening and six-minute structured challenge | Timing sums to 60 minutes and each module maps to an owner or later session output |
| Acceptance record | Date, approver, accepted wording, rejected assumptions, open items and next gate | A durable record distinguishes acceptance from comments, applause or positive feedback |

## Dependencies and Recommended Order

1. Reconcile the session calendar conflict described below before issuing
   invitations.
2. Confirm the final ask, the four or five audience roles and whether the prior
   deck is a baseline or reference.
3. Nominate a sponsor-level planning proxy and the smallest relevant set of
   reviewers. Do not infer availability from `support/cohort.md`.
4. Assign exact work slots, review owners and feedback deadlines for all eleven
   sessions. Deadlines must precede work that depends on that feedback.
5. Assemble the accepted content in the required changes file, reusing the
   primary synthesis and preserving evidence labels.
6. If authorised, initialise the living presentation shell in the YAML source;
   otherwise record the run of show in the contract and leave the old deck
   unchanged.
7. Run the sponsor/proxy recall check, record acceptance and carry unresolved
   evidence into Step 1.2 rather than broadening Step 1.1.

## Material Inconsistency to Resolve

The repository contains two incompatible mappings of work to the eleven
session numbers:

* The primary research review calendar uses Session 3 for ask/evidence
  validation, Session 4 for operations and safety, and Session 5 for resident,
  finance and options. It does not name the high-level architecture session.
* The detailed delivery sequence and detailed subagent research use Session 3
  for operations and safety, Session 4 for resident/finance/options and
  Session 5 for high-level architecture. Step 1.3 sponsor/evidence validation
  is a gate but not a separate numbered delivery session.

The detailed sequence preserves all eleven planned deliverables and should be
the planning default. Treat Step 1.3 validation as an asynchronous gate after
the Step 1.1 and Step 1.2 artifacts, unless the sponsor explicitly reallocates
one of the eleven sessions. The review calendar must be corrected before it is
presented as locked.

## Unresolved Gaps

### Blocking Step 1.1 acceptance

* The proposed one-sentence final ask has not been approved by the sponsor.
* The exact four or five executive attendees are not confirmed.
* None of the eleven sessions has an actual appointment, named review owner or
  feedback deadline; only date windows exist.
* The existing 11-slide presentation has not been designated as an editable
  baseline or reference-only prior work.
* The session-number inconsistency has not been resolved in the controlling
  calendar.

### Important but non-blocking for the contract draft

* The 12-month and cumulative three-year risk-of-inaction horizon remains a
  proposal.
* Named individuals are absent for the sponsor, assurance group, mentor and
  specialist reviewers.
* Final-meeting date, format and location are not recorded.
* The evidence standard is described through classifications, but an owner has
  not accepted the threshold for removing a contested claim from the core
  story.
* Reviewer availability, including year-end constraints, is unknown.
* The pilot locality, source systems, architecture standards, hosting
  constraints and internal approval route remain unknown. These belong to
  later readiness work and must not be invented to close Step 1.1.

## Validation Criteria for the Implementation Plan

### Content checks

* The decision ask is one sentence and clearly says what is and is not being
  approved.
* Non-goals explicitly exclude production rollout and portfolio benefit proof.
* The audience contains exactly four or five confirmed executive roles, with
  the Chief Executive identified as chair and decision authority.
* Every consequential activity retains the stated human approval and stop
  boundary.
* Every contract claim has a source and one of the accepted evidence labels.
* Sector scenarios, grant limits and value hypotheses are not presented as
  Proper North Homes facts.

### Calendar and presentation checks

* All eleven sessions have exact reserved dates/times, review owners and
  feedback deadlines, not just weekly ranges.
* The session numbering matches the accepted detailed delivery sequence.
* The 2026-12-06 through 2026-12-13 margin contains no planned research,
  architecture, feature or prototype recovery.
* Presentation segments total exactly 60 minutes, the opening totals 10
  minutes, and structured challenge retains 6 minutes.
* The opening allows a proxy to repeat the problem, ask, evidence boundary,
  architecture boundary and next gate without explanation.

### Repository checks

* Render the Markdown and verify tables, links, dates and heading hierarchy.
* Review `git diff --check` and `git status --short`.
* Confirm only approved target files changed.
* If presentation YAML changes are authorised, regenerate and visually inspect
  the deck and re-run its existing property validation.
* Do not claim Step 1.1 complete until sponsor/proxy acceptance and calendar
  evidence are recorded.

## Clarifying Questions

1. Do you approve the proposed one-sentence ask, or what exact wording should
   the Chief Executive be asked to decide?
2. Which four or five executive roles will attend the final hour?
3. Who owns review for each of the eleven sessions, and what exact slot and
   feedback deadline can each owner commit to?
4. Should the 2026-09-18 11-slide deck be revised as the living baseline, or
   retained only as prior reference?
5. Should Step 1.3 sponsor/evidence validation remain an asynchronous gate, as
   the detailed sequence implies, or consume one of the eleven sessions?
6. Who is authorised to accept the evidence threshold and remove contested
   claims from the core narrative?

## Sources Consulted

* `docs/case_study_48_original.md`
* `docs/case_study_48_addendum.md`
* `docs/brds/agentic-retrofit-programme-brd.md`
* `docs/brds/retrofit-flow-discovery-brief.md`
* `.copilot-tracking/research/2026-09-19/case-study-85-day-delivery-research.md`
* `.copilot-tracking/research/subagents/2026-09-19/case-study-delivery-research.md`
* `.copilot-tracking/details/2026-09-19/case-study-85-day-delivery-details.md`
* `.copilot-tracking/plans/2026-09-19/case-study-85-day-delivery-plan.instructions.md`
* `.copilot-tracking/plans/logs/2026-09-19/case-study-85-day-delivery-log.md`
* `.copilot-tracking/ppt/2026-09-18/proper-warm-cxo/content/global/voice-guide.md`
* `.copilot-tracking/ppt/2026-09-18/proper-warm-cxo/slide-deck/validation/deck-validation-report.md`
* `support/company-profile-research.md`
* `support/cohort.md`
