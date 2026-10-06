<!-- markdownlint-disable-file -->
# RPI Changes: Proper Warm PRD Prototype

## Metadata

* Task ID: prd-prototype-2026-10-06
* Related plan: .copilot-tracking/plans/2026-10-06/prd-prototype-plan.md
* Phase details: .copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md
* Implementation date: 2026-10-06

## Execution Status

* Status: Complete
* Declared invocation scope: full plan, P01
* Completed scope markers: P01, P01-T01, P01-T02, P01-T03
* All remaining active-plan markers: none
* Status basis: Original implementation and its one Review are complete. RV-001 was implemented in a later pass, adding constructed case history and targeted validation; no second Review is required or run.
* Active implementation boundary: Full plan P01 is complete. Automatic RPI continuation is at the post-Review follow-up selection checkpoint.

## Execution Summary

Implementation followed Research readiness and the final-candidate critique. Critique execution was Complete with a Revise verdict; PC-001 was directly resolved by adding an explicit four-increment acceptance criterion and final inventory. The single-file prototype covers all 11 profile options, nine workflow cards, four increment cards and eight constructed cases. At a 390px viewport the initial `documentElement.scrollWidth` was 509px against a 375px layout width, while body/app-shell width remained 375px and horizontal page scrolling was clamped. The narrow-screen fixed work-table layout now keeps root scroll width at the viewport width; internal case/portfolio table scrolling remains.

## Completed Work

* Created `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html` as a runnable candidate with profile-aware context, workflow navigation, constructed case/portfolio views and explicit demonstrator boundaries. Browser inspection confirmed 11 profiles, nine workflows, four increments and eight sample cases.
* Completed profile-aware queues, all-case scope control, honest unknown/forecast labels, keyboard focus restoration, case-specific accessible names and labelled table scroll regions after applying compatible reviewer feedback.
* Completed the required final local/browser validation and reconciled all P01 task markers; no production integration, persistence or consequential action was introduced.

## P01-T01 Responsive Correction

The 390px browser check traced an inflated root `scrollWidth` to the work-queue table's automatic layout: its intrinsic width extended beyond the layout viewport despite the table's own horizontal scroller. A narrow-screen-only fixed table layout now constrains the table. Verification reports document root width equal to the viewport at 320px, 390px, 768px and 1440px; table content remains internally scrollable. The 11-profile, nine-workflow and four-increment inventories remain intact.

## P01-T02 Bounded Perspective Feedback

Eight of eight requested company-role perspectives returned desk-review feedback. These are design perspectives, not employee or resident research, and do not establish company processes or authorities. Repeated observations and current dispositions:

| Perspective / finding | Disposition | Evidence or boundary |
|---|---|---|
| Asset, Housing/Resident Engagement, Repairs/Building Safety, Procurement, Finance and Digital perspectives noted that profile selection changes the copy but does not expose a role-relevant case queue. | Accept | Add a sample-only role-relevant default queue and a clear view-only control to show all cases; never imply authorization. |
| Data/Performance and Asset perspectives noted the “Forecast is not a commitment” badge conflicts with “No delivery forecast is inferred”; Data/Performance also noted the overview's “Accepted in scenario” label does not match the handover-stage count. | Accept | Use “No forecast shown” and “Homes at handover stage”; retain the scenario denominator and constructed-data notes. |
| Resident Engagement and Neighbourhood Housing perspectives noted the “Decision recorded” example lacks measure/scope and access context, risking over-reading the decision. | Accept narrowly | Mark the example as a constructed record whose measure-specific meaning and communication/access details are not supplied; do not invent preferences or resident facts. |
| Building Safety, Programme, Procurement, Finance and Resident perspectives requested deeper domain ledgers, event trails, evidence checklists, grant conditions, supplier capacity values, or delivery-sequence detail. | Defer beyond this low-scope correction batch | Those fields may imply unverified company facts, operational timing/authority, or more complete workflow behavior than this one-file prototype can substantiate. Preserve unknowns and the authoritative-system/human-review boundaries. |

The UX/UI Designer completed the explicit review of all 11 PRD profiles. This is design critique, not user research or a conformance assessment. Cross-profile findings and dispositions:

| PRD profile | Main review focus | Disposition |
|---|---|---|
| Asset and investment | Portfolio assumptions/denominator, investment view and reasoned priorities. | Narrow role tasks to visible stock conflict and scenario counts; do not invent company budgets or forecasts. |
| Programme coordinator | Queue clarity, handoff acceptance/returns and next owner. | Keep cross-workflow sample queue; defer a detailed timing/event ledger. |
| Retrofit case team | Case prerequisites, linked record context and stage history. | Add case-specific open-detail/unknown context; defer a full lifecycle/history view. |
| Retrofit Assessor, designer and Coordinator | Missing technical reference, design version and separate sign-offs. | State missing design reference and preserve competent human review; defer detailed sign-off checklist. |
| Housing and Resident Engagement | Decision meaning, adjustment/access context and update ownership. | Use a neutral unknown state and explicitly say measure meaning/access details are not supplied; do not fabricate resident preferences. |
| Repairs and Building Safety | Referral receipt and receiving-service ownership. | State that receipt/service are unconfirmed and retain the authoritative-service boundary. |
| Procurement and contract manager | Capacity state, package scope and instruction authority. | State offered capacity and scope are unconfirmed; defer a contract/capacity ledger. |
| Provider / contractor contact | Staff-facing boundary, package and evidence checklist. | Narrow role tasks to the available constructed supplier-capacity example; no portal or work instruction. |
| Quality and assurance | Incomplete per-measure evidence and remediation/acceptance boundary. | Explicitly label incomplete evidence and absence of acceptance; defer full quality trail. |
| Finance and Grants | Invoice exception versus grant/cash status. | Narrow tasks to the invoice case; state grant/cash details are not represented. |
| Digital operator and auditor | Import/recovery state and audit trace. | Narrow tasks to visible source conflict and returned handoff; state live integration/recovery is not represented. |

Cross-profile accessibility findings: workflow activation replaced the focused button; repeated “View case” labels lacked case identifiers; narrow tables needed a discoverable keyboard scroll surface. The source changes add workflow focus restoration, case-specific accessible names, and labelled focusable table regions with a mobile scroll hint. Larger domain ledgers, resident-access fields, technical/quality trails and delivery-sequence diagrams remain deferred because company values, preferences and operating rules are unknown and the approved artifact is a bounded prototype.

## Four-Increment Inventory

| PRD increment | Prototype surface | Status shown in prototype |
|---|---|---|
| 1. Shared workbench foundation | Shared profile selector, constructed role-relevant queue, case detail, evidence and handoff context. | Scope context only; the card is not release approval or a claim of delivered production capability. |
| 2. Workflow portfolio coverage | Nine workflow cards and representative constructed case examples across technical, resident, supplier, hazard, quality and finance areas. | Concept card; no workflow is operational or approved. |
| 3. Coordinator insight | Illustrative stage-count table and fixed scenario metrics; no inferred delivery forecast. | Concept card; constructed counts only, with the forecast explicitly not shown. |
| 4. Bounded-agent comparison | Demonstrative source-linked suggestion card and the PRD increment scope card; the prototype does not implement a measured paired comparison. | Concept card; no live action and no claim of agent value or approval. |

The card titles now match the PRD's four increment names. The whole section is labelled as draft-PRD scope context, not release approval.

## Implementation-Time Plan and Detail Updates

* P01-T01: Added a narrow-screen fixed table layout after browser evidence showed the work-table's intrinsic width inflating root `scrollWidth` at 390px; verified layout width is constrained while table content remains internally scrollable.
* P01-T02: Recorded eight bounded company-role perspectives and the UX review of all 11 profiles. Accepted low-scope fixes to profile queue relevance, unknown labels, forecast/handover/decision wording and accessibility; narrowed unsupported role copy and deferred larger operational detail pending evidence.
* P01-T03: Clarified that the implementation checklist and changes record establish Review readiness; the separate RPI Review artifact belongs to the next, explicitly advanced phase. This preserves the manual phase boundary while allowing P01 implementation evidence to be complete.

## RV-001 Case History Continuation

The post-implementation Review at `.copilot-tracking/reviews/logs/2026-10-06/prd-prototype-review.md` completed with outcome `Defects found` and routed RV-001 to `rpi-implement`. The selected case view has current snapshot attributes and a source trace, but no event list/timeline for following prior case state or handoffs. Reopened P01-T01 without changing requirements: add a small, clearly constructed, non-operational selected-case history; use no new user decisions, live event data, persistence, or transition controls. Automatic RPI mode was explicitly requested with `mode=auto`; this is a later implementation of a Review finding and does not trigger a second Review.

The prototype now shows a three-entry illustrative history for each of the eight constructed cases, with event descriptions and source-context labels. A native `details` disclosure keeps the panel compact and keyboard-operable. Every timeline states that it is constructed, is not a live audit trail, and does not represent committed transitions. No source-system calls, storage, or consequential actions were added.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|---|---|---|---|
| Local load, console and network | P01-T01/P01-T03 | Passed | The prototype loaded with zero browser-console errors. Browser inspection found no external requests; the temporary local server logged the HTML request and one harmless `/favicon.ico` 404. Source search found no external APIs, persistence or pop-up calls. |
| Profile, workflow and increment inventory | P01-T01/P01-T03 | Passed | All 11 PRD profiles, nine workflow areas, four exact increment titles and eight constructed cases are represented; each profile was exercised in the browser. |
| Profile queues and primary interactions | P01-T01 | Passed | Role-specific queues, all-case scope toggle, search/no-result state, case detail, theme toggle and all nine workflows were exercised using fresh controls after each render. |
| Responsive layout and table overflow | P01-T03 | Passed | Prior checks covered 320px, 390px, 768px and 1440px. For RV-001, all eight case timelines were exercised at 320px and 390px; document scroll width stayed within `window.innerWidth`, and case-detail content did not overflow its container. |
| Keyboard and accessibility spot checks | P01-T03 | Passed | Workflow activation with Enter restored visible focus; Tab advanced to the next workflow card. Case controls carry case-specific accessible names, table regions are labelled/focusable, and reduced-motion styling is present. This is targeted review, not a WCAG conformance assessment or user test. |
| Clawpilot theme and demonstrator boundaries | P01-T03 | Passed | Required theme initialization and light/dark tokens are present; the interface states constructed-data, no-authentication, no-contact and no-operational-action boundaries. |
| RV-001 case history behavior | P01-T01 | Passed | All eight sample cases render three matching history entries with the constructed-data/live-audit/transition disclaimer. Selecting a case updates the timeline; keyboard Enter opens its native disclosure. At 320px and 390px document scroll width stays within the window viewport and history content does not overflow its case-detail container. |
| Source and workspace change review | P01-T03 | Passed | Reviewed the prototype and task-specific RPI artifacts, including the completed Review record. The workspace contains only the requested prototype and task records; branch HEAD equals `origin/main`. The repository has no configured build/test/lint command. |

## Post-Review Implementation Reconciliation

* Plan markers and phase details: P01 and P01-T01/P01-T02/P01-T03 are complete; the phase-details index agrees.
* Completed-work evidence and handoff prose: Runnable prototype, all-profile UX coverage, bounded role reviews, accepted corrections, RV-001 implementation, and validation results are recorded.
* Validation, blockers, remaining work, and follow-up items: Targeted checks pass; no blocker or active implementation marker remains; the plan follow-up list is empty.
* Review status: One RPI Review completed with outcome `Defects found`; RV-001 is subsequently implemented and validated. The one-pass Review is not repeated.

## Blockers

* None.

## Remaining Work

* None.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-10-06/prd-prototype-plan.md, `## Follow-Up Items`
* None.

## Return-to-Caller State

* Implementation execution status: Complete for full-plan scope P01, including the later implementation of RV-001.
* Declared scope and markers: Full plan; P01 and P01-T01/P01-T02/P01-T03 are complete. UX coverage includes all 11 profiles and bounded feedback from eight company-role perspectives.
* Validation coverage: Local load, zero console errors, no external requests, all inventories, role queues, workflows, search/detail, theme, keyboard focus, reduced-motion source check, four prior viewport widths, and all eight three-entry case histories at 320px/390px passed; document width stayed within the window viewport and detail content did not overflow. The local server logged a harmless favicon 404.
* Blockers: None.
* Current plan and detail updates: P01 and all task markers are complete; changes and details agree; PC-001 remains resolved. RV-001 was implemented after the one completed Review.
* Planning and critique state: Implementation complete after RV-001; no second Review is run. The single critique Complete/Revise finding PC-001 was resolved.
* Follow-up items: None.
* Review readiness or no-handoff reason: The single Review is complete. RV-001 was later implemented and validated; do not repeat the Review.
* Continuation owner: Parent RPI Agent.
