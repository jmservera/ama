---
title: Proper Warm Prototype Profile Review
description: Fresh company-role critique, UX discussion and proposed next iteration for all eleven prototype perspectives
ms.date: 2026-10-06
ms.topic: reference
---

## Outcome and Evidence Boundary

All nine repository `company-*` profiles were launched in parallel to review
the current [constructed-data prototype](../../../../.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html).
Their own-role findings were collected, then the UX/UI Designer synthesized
all eleven [PRD profiles](../../../prds/proper-warm-retrofit-programme-demonstrator.md#users-and-personas).
Four focused proposal discussions with Procurement, Resident Engagement,
Building Safety and Data/Performance were relayed through the coordinating
agent because the designer's own tool surface could not message peers.

This is source-based design research, not employee/resident interviews,
validated company practice, operational approval or an accessibility
conformance assessment. The role agents are research instruments grounded in
the [original case](../../../case_study_48_original.md),
[addendum](../../../case_study_48_addendum.md) and
[company-role evidence](../company/company-profile-research.md).
Recommendations, JTBD statements and user behavior/accessibility expectations
below are hypotheses pending direct, accessible user research.

The prototype remains unchanged by this review. No authentication, actual
permissions, live communication, integration, persistence, professional
sign-off, operational handoff, work instruction or payment is implemented.
The provider perspective is staff-facing, not a contractor portal. Residents
are affected stakeholders, not authorized users of this non-production MVP.

## What the Prototype Actually Covers

Source inspection and extraction of the data definitions establish eleven
profile perspectives, nine workflow cards, eight constructed cases and three
illustrative history entries per case. Workflow-card selection both displays
context and filters the queue; it does not progress a case through stages.
Profile selection is a view filter, not authorization.

The portfolio workflow has no matching case. Fixed headline values for a
128-home scenario, 42 active journeys, seven holds/reviews and nineteen homes
at handover are not derived from the eight inspectable case examples.
Narrative history has source context, but no event timestamps, actors or
versions. These limits do not invalidate a concept walkthrough; they prevent
claiming full PRD workflow, analytics or audit acceptance.

### All Eleven Profile Journeys

Each JTBD is an assumed job statement: when in the stated situation, the
user wants the stated action so they can reach the stated outcome. Observed
prototype behavior is distinguished from the proposed next slice.
Case numbers below abbreviate `EX-HOME-`.

| PRD perspective | Assumed job and current entry | Current route and safe endpoint | Proposed recovery/handoff and integrated accessibility |
| --- | --- | --- | --- |
| Asset and investment | When reviewing candidate homes, inspect data quality and dependencies to prepare an evidence-grounded investment discussion. Asset queue: 317, 646, 752. | Inspect source conflict, capacity dependency or invoice exception. Eligibility stays unknown; no investment decision follows from fixed metrics. | Expose conflict sources and a named resolution role; link building context and show investment inputs as unknown. Keyboard-operable links and textual source dates/unknowns; disclose metric population separately. |
| Programme coordinator | When coordinating teams, identify blocked work and accountable ownership to prepare the next handoff. All eight cases. | Select workflow and case, inspect snapshot/history. Unassigned receiver and missing return reason remain open; no accepted handoff is demonstrated. | Separate current owner, destination, receiver, chase owner and update owner. Announce filter/result changes; provide visible reset and labelled status fields. |
| Retrofit case team | When preparing a home's next step, inspect evidence and dependencies to avoid assuming another role's approval. Queue: 104, 208, 317, 422, 531, 863. | Inspect home/building context and held stage examples. Different homes do not constitute one home's lifecycle. | Start with a linked exception-to-owner slice, then a read-only lifecycle. Distinguish home/building headings and each home's independent consent, holds and acceptance. |
| Retrofit Assessor, designer and Coordinator | When reviewing a technical pack, inspect sources, design version and missing evidence to complete or return work within competent scope. Queue: 104. | Missing design reference blocks demonstrated readiness; opening the case is not sign-off. | Show missing reference, review/return reason and separate competent reviewers. Textual missing states and keyboard-navigable evidence; no color-only approval cue. |
| Housing and Resident Engagement | When handling a resident service issue, understand measure-specific choice and an accessible next-update commitment to preserve continuity. Queue: 208. | Decision scope and contact/access details unknown; no wider consent or communication inferred. | Separate choice, access, service, complaint, defect and hazard routes. Update purpose, owner, illustrative due date, safe-route/adjustment reference and sent evidence; labelled minimum-necessary fields, not sensitive history. |
| Repairs and Building Safety | When a potential hazard is reported, inspect awareness/referral evidence and affected retrofit scope to chase an authoritative-service response. Queue: 531. | Receipt/service unconfirmed; workbench cannot classify, close or run the hazard clock. | Distinct destination, chase owner, receipt and acceptance. Scoped hold/source and read-only authoritative human decision reference; text states and accessible announcements must not imply release. |
| Procurement and contract manager | When reviewing a package, distinguish offered capacity and draft scope from commitments to prepare accountable review. Queue: 317. | Period/package/capacity unconfirmed; no instruction or schedule issued. | Draft-package panel with period, scope/version, offered/committed state, call-off/work-order reference, unmet prerequisite and named next reviewer. Text labels and independent provider/quality/finance handoffs. |
| Provider / contractor contact | When responding to authorized package information, understand scope and evidence requirements to prepare a submission without self-approval. Queue: 317. | Staff-facing example only; no provider identity, approved intake or submission path. | Keep portal boundary visible. Future constructed submission/correction stays separate from independent review; keyboard-readable checklist/statuses. Procurement is an adjacent lens, not provider validation. |
| Quality and assurance | When inspecting delivered work, compare per-measure evidence and defects to independently accept or return it. Queue: 422. | Incomplete pack, no accepted handover or safety conclusion. | Navigable positive-evidence checklist, specific return reason, defect owner/reinspection and independent disposition. Textual incomplete states; submission never equals acceptance. Programme/Procurement provide adjacent, not dedicated inspector evidence. |
| Finance and Grants | When reviewing an invoice, compare authorized scope and accepted milestone evidence to disposition an exception without implying payment or grant approval. Queue: 752. | Quantity difference unresolved; payment unauthorized and grant/cash status not inferred. | Constructed line comparison and review owner first. Keep budget, commitment, invoice, payment, award, claim and cash separate; readable labelled rows, unknown monetary authority remains unknown. |
| Digital operator and auditor | When diagnosing conflict/return, trace sources and outcomes to prepare owned recovery without silent changes. Queue: 646, 863. | Conflicting values/run/event metadata not exposed; no replay or audit reconstruction. | Show both source values/provenance and unresolved eligibility; preserve original input. Active scope/reset, structured event fields and accessible status text. Data/Performance is an adjacent lens, not actual operator validation. |

## Ranked Recommendations and Acceptance Evidence

These are proposed checks for a later iteration, not assertions that the
prototype already meets them or that a company usability threshold is known.

| Priority | Recommendation and evidence | Proposed check |
| --- | --- | --- |
| P0: Correct ownership semantics | Table says "Next owner" but renders `item.owner`, which detail labels current owner. Especially misleading for 863 with unassigned receiver. HTML queue header/rendering and case detail, lines 680, 939-940, 964-966. | Queue and detail distinguish current owner and proposed/accepting receiver; unassigned remains unassigned. Changing view never assigns work. |
| P0: Correct explanations | Static suggestion rationale describes a missing link across capacity, quality and invoice cases. 863's source says "with return reason" while its context says reason absent. HTML lines 770-774, 851, 981-983. | All eight cases have rationale matching their own evidence/unknown; source and context agree. No proposal satisfies a gate or commits a transition. |
| P1: Make view scope recoverable | Search persists across profile changes; selected workflow overrides profile-focus filtering; portfolio has no sample. HTML `filteredCases`, `renderCases` and handlers, lines 908-955, 992-1020. | Active profile, workflow and search scope visible; one documented reset returns the expected view. Differentiate no supplied portfolio scenario from no search matches, without implying no actual work. |
| P1: Explain metric population | Fixed snapshot cannot reconcile to eight inspectable cases. HTML lines 626-641, 723-732. | State population, illustrative/as-of context and filter impact. Either reconcile a small cohort to records or clearly label snapshot independent of the case examples. Handover stage does not imply accepted handover. |
| P1: Deepen evidence, not dashboard volume | 646 hides compared values; 317 hides package scope/period; 752 hides match inputs. PRD FR-012/016/018/029, AC-015/019/021/031. | One static comparison shows sources and missing prerequisites with a named review role; unresolved evidence is a valid safe endpoint. Do not manufacture real company values. |
| P2: Add a connected synthetic slice | Current cases are stage snapshots, with 317/422 sharing a building but not a demonstrated dependency. PRD FR-001/002/011/022 and AC-012-014/025. | First demonstrate exception -> evidence -> accountable owner, then a read-only lifecycle with a second-home dependency. Preserve separate home gates and source/actor/time/version labels on any constructed events. |

### Sequencing and Scope Trade-Off

The Asset perspective favors a smaller exception-to-accountable-owner
walkthrough; the designer initially proposed a wider home lifecycle. Sequence
them rather than treat them as equivalent scope: correct misleading fields and
filters, deepen one exception/package comparison, then connect a synthetic
home journey. Show a second home only to explain shared-building impact,
never to transfer consent, hold release or quality acceptance.

Prioritize invoice-match depth over a new grant ledger, and draft package
readiness over work release. Add accessible service/choice and return/referral
scenarios as explicit synthetic states, not operational actions. No invented
company SLAs, approval limits, resident preferences or grant conditions are
needed to demonstrate unknowns and safe blocks.

## UX Discussion and Amendments

| Discussant | Designer proposal | Fresh response and disposition |
| --- | --- | --- |
| Procurement and Contracts | One package links scope/capacity/version and independent provider, quality and finance roles. | Agrees with amendment: anchor **draft** package readiness, not release. Show unknown/unmet prerequisites and named next reviewer; constructed readiness is not instruction, booking, contractual commitment, acceptance or payment. |
| Resident Engagement | Update owner, due date and proposed/sent status independent of operational acceptance. | Requires more: update purpose/linked issue; reference safe route and necessary adjustment or explicit unknown; sent timestamp/evidence, not proof of receipt/understanding. Outstanding responsibility remains until sent or explicitly reassigned in the proposed exercise; Housing/Programme must validate real continuity rules. |
| Building Safety | Destination, confirmed receiver, retained chase owner and scoped hold tied to authoritative human evidence. | Minimum synthetic evidence: sent time/reference, receipt state, confirmed receiving role/time only when evidenced, owned follow-up; hold scope/source/status and read-only release-decision/evidence reference. Receipt, acceptance, hazard resolution and work authorization are distinct. Workbench does not judge release sufficiency. |
| Data and Performance | Source/metric reconciliation and filter visibility before richer analytics. | Agrees with amendment: unresolved conflict with evidence and resolution owner is valid. Show denominator/as-of/filter impact; reconcile or label a separate cohort; both 646 values/provenance; portfolio "no representative supplied" not "no work." |

## Accessibility and Human Validation

For each journey, proposed keyboard navigation must retain logical focus and
visible focus indication; labels, heading structure, error/status
announcements and source links must work with screen readers. Verify WCAG AA
text contrast, non-color state meaning, minimum 24-by-24 CSS pixel targets,
200% text zoom and narrow layouts. Prior spot checks and native controls do
not establish conformance.

Real staff/provider research should test locating the right work, explaining
an unknown, identifying an accountable next step and recovering filters.
Direct accessible resident research must validate choice, support, contact
and redress semantics before product requirements are finalized. Device,
environment, accessibility needs, company ownership and acceptance thresholds
remain unknown; do not invent performance metrics or emotional observations.

## Provenance and Related Evidence

Detailed agent IDs, own-role findings, discussion questions and correction
history are in the
[review working record](../../../../.copilot-tracking/research/2026-10-06/proper-warm-profile-journey-critique-research.md#fresh-parallel-company-review---2026-10-06).
The earlier eight-role feedback predates the timeline and is kept separate in
the [prototype change record](../../../../.copilot-tracking/changes/2026-10-06/prd-prototype-changes.md).
Earlier claims that dispatch was unavailable and workflow cards only showed
text are superseded by the fresh review and verified source behavior.

All nine top-level company agents supplied own-role critiques, including the
Executive Reviewer. Any nested reviews or coordination attempted by individual
reviewers are excluded from this review's participation and agreement claims.
Four recommendation discussions were actually relayed and answered; this is
not nine-way consensus or real-user validation. No original case, PRD,
prototype, regulatory snapshot or owner memory was changed.
