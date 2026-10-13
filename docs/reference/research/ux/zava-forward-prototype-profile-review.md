---
title: Zava Forward Prototype Profile Review
description: Company-role critique, dated owner usability feedback and proposed next-prototype acceptance checks
ms.date: 2026-10-13
ms.topic: reference
---

## Outcome and Evidence Boundary

The source-inspected findings below describe the 2026-10-06 HTML artifact,
not every subsequent prototype. The separate
[2026-10-07 owner feedback](#owner-usability-feedback-2026-10-07) records
reported impressions of a later application without inspecting its code or
independently reproducing its behavior. Proposed checks are not passed tests.

All nine repository `company-*` profiles were launched in parallel to review
the current [constructed-data prototype](../../../../.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html).
Their own-role findings were collected, then the UX/UI Designer synthesized
all eleven [PRD profiles](../../../prds/zava-forward-retrofit-programme-demonstrator.md#users-and-personas).
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

## Owner Usability Feedback (2026-10-07)

### Source, Status and Scope

The project owner supplied the following feedback on 2026-10-07 while reviewing
the application served at `localhost:3410`. The related prototype
[PR #24](https://github.com/jmservera/ama/pull/24) is provenance only, not a
dependency or a merge prerequisite for these learnings. The URL identifies the
review context; it is not a durable evidence artifact.

This section captures owner-reported observations and requested direction,
not independently verified implementation facts, representative staff or
resident research, approved production requirements or user-tested success.
No runtime inspection, UI implementation, resident-data generation or prototype
code import accompanies this documentation capture. The original case,
addendum, PRD and owner memory remain unchanged.

The earlier source review found that workflow selection filtered the HTML
queue. The owner now reports that changing role or workflow does not visibly
change the UI or filters in the later application. These statements concern
different review contexts and evidence types. Do not silently replace either
with a universal implementation claim; verify the next artifact directly.

### Later Pinned-Source Reconciliation (2026-10-13)

The requested UX Designer review inspected final #24 source
`6029dc248911ddd3eebece5fb2067d881920494c` without running it.
Its [workflow handler](https://github.com/jmservera/ama/blob/6029dc248911ddd3eebece5fb2067d881920494c/apps/proper-warm/public/app.js#L135-L155)
sets the workflow filter and reloads cases; the
[scope/reset, failure and detail paths](https://github.com/jmservera/ama/blob/6029dc248911ddd3eebece5fb2067d881920494c/apps/proper-warm/public/app.js#L205-L345)
show scope/counts, clear failed list metrics and keep case detail independent
of register filters. These later source affordances neither disprove the
owner's earlier perception nor establish that the reviewed runtime used
this pin. UX-02/03 remain unexecuted; preserve both evidence types.

The [closure synthesis](./prototype-learnings-and-simplicity-review.md#draft-ux-closure-review-2026-10-13)
retains uncertain-write recovery and unique #58 journeys; it recommends
retirement or carry-forward, not a passed usability study or new requirement.

### Owner's Notes

> Take these notes: I like the style, logo, fonts and colors. Page seems clear,
> but the red or redish colors are appearing in multiple places and seem like
> they are errors when they are not. When we change the role or the workflow,
> the UI or the filters do not change, it must be clear when is it perpared to
> the next step, who takes the case, what will the agent do with the data or
> what decisions will us help with. Furthermore we should be able to open a
> case full screen, and having full address, phone of the resident, all the
> data needed at hand to fulfill the necessary data and steps. Review this,
> take the notes and store them in a new branch & PR where we could merge this
> information to influence the next prototype, but without storing the current
> code, just the learnings.

### Design Direction Derived from the Notes

| Owner feedback | Proposed next-prototype direction | Boundary |
| --- | --- | --- |
| Style, logo, fonts, colors and general page clarity are liked. | Preserve the brand identity, typography, general palette and clear page structure; correct semantic color use rather than redesign the brand. | A positive owner impression is not a general usability or accessibility finding. |
| Red/reddish elements look like errors where none are intended. | Reserve reddish operational status/action emphasis for genuine errors or blocking conditions. Use neutral informational/selection styling elsewhere; pair every state with explicit text and an appropriate icon, never color alone. | Retaining brand artwork does not justify error-like emphasis on routine metrics, selection or normal progress. Contrast still needs checking. |
| Role/workflow changes do not make the UI or filters visibly different. | Make active role/perspective, workflow, scope and result count visible. Contextualize queues, filters, evidence and available actions; explain unchanged/shared results, unavailable scenarios and pending, empty, loading or failed states. | A selectable prototype perspective is not authenticated authorization and changing context never changes case state. |
| Readiness and the person taking the case must be clear. | Show current stage, next step, missing/stale/conflicting evidence, readiness basis, current accountable owner, proposed destination and receiving owner. Distinguish sent, received and explicitly accepted handoffs, retaining an accountable chase owner while acceptance is pending. | Readiness for human review is not permission to release work. Unknown/unassigned ownership stays explicit; never infer acceptance from receipt. |
| Explain what the agent does with data and which decisions it supports. | Show agent purpose, permitted inputs with source/date/version, intended output, rationale, uncertainty and next human reviewer. Separate extraction, reconciliation, drafts, recommendations and raise-only flags from decisions and actions. | No agent approval of safety, professional work, consent, investment, procurement, payment, claims or quality; no external action merely because a suggestion is accepted. |
| Open a case full screen with address, phone and necessary working data at hand. | Provide a full-screen case workspace with case/home identity, full synthetic address, resident phone, contact preference, necessary accessibility adjustments or explicit unknowns, evidence, tasks, blockers, owners and next step. Provide a clear return to the originating queue. | Use only synthetic, clearly labelled records in the prototype. Production disclosure must follow role, case and field permissions and minimum-necessary purpose; do not expose sensitive histories by default or invent missing values. |

The contact request means sufficient information for the permitted task, not
unrestricted resident disclosure. Safe contact, preferences and adjustments
must be distinguishable from consent to a measure; no phone number, accessible
route or appointment record establishes consent. No real PII is recorded here.
Actual contact details, company access rules and adjustment needs remain
unknown pending authorized validation.

### Proposed Acceptance Checks for the Next Prototype

These checks translate the owner notes into candidate walkthroughs. All are
unexecuted; they supplement rather than approve or silently revise the
[PRD](../../../prds/zava-forward-retrofit-programme-demonstrator.md).
Publish the next artifact's scenario manifest and expected results before
running them. Static/mock states must be labelled as such.

| Check | Scenario and expected evidence | Related PRD anchor |
| --- | --- | --- |
| UX-01: Preserve identity, correct status color | Compare the next artifact with the reviewed brand reference: logo, type and general palette remain recognizable. Inspect normal, selected, informational, error and blocked examples: only genuine error/blocking states use reddish operational emphasis, and each state remains understandable without color through text/icons. Check text contrast and keyboard-visible focus, not appearance alone. | NFR-001; owner-requested semantic-color refinement |
| UX-02: Context has visible effect | Switch between two represented perspectives and two workflows using pointer and keyboard. Check visible context, expected case IDs/counts, applicable filters, evidence and actions against the manifest. Shared results are explained; unavailable actions state why. Announce updated scope/results without unexpected focus movement. An incompatible retained filter or selected case is cleared or explicitly explained. | FR-003/004/032/035; AC-005/006/034 |
| UX-03: Honest state and recovery | Exercise pending handoff, loading, no matches, no representative scenario and load failure through labelled mocks if needed. Each has distinct text; loading/failure never looks like success or zero actual work. Reset returns the declared perspective defaults with a usable focus position. | FR-032/035; AC-034; NFR-001/006 |
| UX-04: Readiness is evidence-based | Open ready-for-review and blocked/unknown examples. Identify current stage, next task, evidence/source/version, unmet prerequisite and responsible role without guessing. Missing evidence or approval keeps the step blocked/unknown; ready-for-review wording never claims authorized release or professional acceptance. | FR-008/025; AC-011/016/028 |
| UX-05: Ownership survives a handoff | Compare unassigned, sent, received, accepted and returned synthetic examples. Current owner, destination, proposed/confirmed receiver, chase owner and next-update owner are separately labelled. Receipt alone is not acceptance; an accepted state names its receiver and supporting event, and a pending/returned case still has an accountable follow-up. | FR-011/033; AC-014/035/036 |
| UX-06: Agent contribution is inspectable | Inspect a draft, a recommendation and a raise-only flag. Explain which permitted inputs/sources were used, what the agent produces, which decision it supports, what is unknown, who reviews it and what it cannot do. Unsupported inputs remain unknown; accepting a suggestion creates at most the permitted task/draft, not approval or external action. Include the explicit workflow-only/failure route. | FR-025-028; AC-028-030 |
| UX-07: Full-screen case is recoverable | From a filtered queue open a case full screen by keyboard; identity, evidence, tasks, readiness and owners remain accessible. Return restores role/workflow/search/filter/sort context, selection, queue position and focus to the originating control. Check logical headings, focus order/visibility, a labelled return/close control, narrow layout and 200% text zoom; no required task depends on hover or pointer alone. | FR-001/002/032; NFR-001; owner-requested full-screen refinement |
| UX-08: Necessary contact context, not invented data | Inspect a complete synthetic contact example and an incomplete one. Full address including postcode, resident phone, preferred/safe contact route and necessary adjustment references are available for the represented permitted task; missing fields say unknown/not supplied and name a follow-up, not fabricated values. Label all examples synthetic and provide no real contact actions. For production, require separate role/case/field access-denial checks across case detail, search, exports and AI inputs before release; hiding fields in a demo is not authorization evidence. | FR-003/014; AC-005/017/037; NFR-002/005 |

Use UX-01 to UX-03 for orientation first, UX-04 to UX-06 for an
exception-to-accountable-owner walkthrough, and UX-07 to UX-08 for the expanded
case workspace. Record artifact version, fixture IDs, expected versus actual
results and remaining gaps when these checks are eventually run. No timing,
completion-rate or satisfaction threshold is invented from this feedback.
Staff and accessible resident validation, production authority and privacy
review remain separate future gates.
