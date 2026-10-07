<!-- markdownlint-disable-file -->
# RPI Plan: Proper Warm PRD Prototype

## Task Metadata

* Task ID: prd-prototype-2026-10-06
* Task slug: prd-prototype
* Planning status: Implementation complete; prior Review finding RV-001 implemented; automatic post-Review checkpoint
* Plan date: 2026-10-06
* Phase details: .copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-06/prd-prototype-plan-critique.md

## Executive Summary

Build a self-contained, interactive prototype of the current Proper Warm workbench PRD. It presents one shared home-centred workbench through all 11 provisional role perspectives, nine workflow areas and four delivery increments, using constructed exercise records. Role switching demonstrates task context only; it does not imply authentication, permission, approval or an operational action. The UX/UI Designer reviewed every profile, and matching Proper North Homes role agents commented from their bounded perspectives. The artifact remains a draft demonstrator, not an approved product or a usability result.

### User Decisions and Requirements Highlights

* Use the latest version of `main` as the baseline; `origin/main` was fetched and this branch is already up to date.
* Build a prototype from the current PRD, not a production implementation.
* Ask the UX Designer to review the user experience for every named profile; company-role agents may also provide user-perspective feedback.

### What You May Not Know

* The current PRD v0.6.2 is a draft. Its role workspaces are provisional, and its constructed exercise records do not establish company performance, resident outcomes, actual authorities or operating decisions.
* Residents are affected stakeholders, not users of this non-production MVP. The prototype must not create a resident login or live-contact journey.
* A profile selector demonstrates a view only; permissions and controlled decisions remain outside this visual artifact.

### Unresolved Decisions or Blockers

* No blocker prevents an exercise prototype. Product ownership, actual role authority, company baselines, direct user validation and production architecture remain unresolved in the PRD and are outside this plan.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Pull the last version from `main` before starting the prototype.
* Build a new prototype from the new PRD.
* Ask the UX Designer to review the user experience for every profile.
* Company-role agents may also be asked for feedback as users.

## Goals

* Deliver a navigable, interactive, non-production representation of the current PRD's shared workbench.
* Make each of the 11 PRD profiles and nine workflow areas discoverable and meaningfully distinct without inventing actual company authority.
* Keep exercise-data provenance, proposal status, human decision boundaries and uncertainty visible.
* Apply relevant UX feedback and preserve a clear record of review coverage and validation.

## Scope and Non-Goals

### In Scope

* Create `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html` as a self-contained HTML artifact using the required Clawpilot theme and local-only constructed data.
* Provide all 11 provisional profiles from the PRD, profile-aware task context, a common case/portfolio view, all nine workflow areas, and representative interaction states.
* Show the four PRD increments as scope context and distinguish later-increment concepts where useful.
* Obtain a UX/UI Designer review that explicitly covers every profile and collect appropriate feedback from the eight matching company-role agents.
* Make compatible, evidence-grounded UX changes, then verify the artifact, profile/workflow coverage, interactions and accessible operation.

### Non-Goals

* Production software, authentication, authorization, source-system integration, persistence, real personal/operational data or deployment.
* Live resident/provider contact, appointment scheduling, safety/hazard determination, work release, professional approval, investment, procurement, invoice/payment approval, grant submission, quality acceptance or complaint/defect closure.
* Treating company-role-agent feedback as validated employee/resident research or as approval of company processes.
* Resolving open PRD decisions or changing the PRD/business requirements.

## Functional Requirements

* Users can switch among all 11 named PRD workspaces and understand that the selector changes the demonstrator perspective only.
  * Observable acceptance criteria: every listed profile is reachable and shows a role-relevant queue/task context; explanatory copy says it is not authentication or access control.
* Users can navigate all nine workflow areas on common constructed home/building records.
  * Observable acceptance criteria: each named PRD workflow has a discoverable destination or representative surface and visible constructed-data labeling.
* Users can inspect a representative case, source/evidence state, blockers, handoffs and history, and see a bounded next-step proposal.
  * Observable acceptance criteria: citations/provenance, unknowns, draft/unapproved state and a human review boundary are apparent; no control claims to commit a consequential transition.
* Users can inspect portfolio progress and forecast/quality context.
  * Observable acceptance criteria: any chart/table exposes measure meaning, denominator/as-of or exercise status, uncertainty and an equivalent accessible text/table view where relevant.
* Users can follow the key prototype interactions without network access or external dependencies.
  * Observable acceptance criteria: role/workflow navigation, filters and profile/task changes update the rendered interface; no user action contacts a person, submits a record, changes persisted operational data or invokes a service.

## Non-Functional Requirements

* The artifact is a single, self-contained HTML file.
  * Objective threshold or evaluation condition: all required markup, styling, data and scripts are embedded; it opens locally without network access.
  * Observable acceptance criteria: no external script, stylesheet, font, image, API request or dependency is required.
* The visual theme follows the web-artifacts-builder Clawpilot contract.
  * Objective threshold or evaluation condition: required theme initialization and exact CSS variables are present; component color values use only `var(--cp-*)`.
  * Observable acceptance criteria: theme selection works for light/dark, with required Segoe UI-family font stack.
* The interface remains usable across keyboard, screen size, zoom and reduced-motion settings.
  * Objective threshold or evaluation condition: keyboard-operable navigation/controls, visible focus, responsive layout, semantic headings/labels/status, non-color cues and reduced-motion handling.
  * Observable acceptance criteria: targeted interaction checks cover keyboard and narrow viewport; no critical content is clipped or only color-coded.
* The prototype is honest about status and failure.
  * Objective threshold or evaluation condition: every action is visibly demonstrative; no simulated save, approval or successful external outcome is represented as real.
  * Observable acceptance criteria: constructed examples, PRD draft status, unknowns and boundaries remain visible in the interface.

## Acceptance Criteria

* The HTML artifact loads as a standalone local document with no console/runtime errors in the tested browser.
* The UI presents exactly the 11 named PRD profiles: Asset and investment; Programme coordinator; Retrofit case team; Retrofit Assessor, designer and Coordinator; Housing and Resident Engagement; Repairs and Building Safety; Procurement and contract manager; Provider / contractor contact; Quality and assurance; Finance and Grants; Digital operator and auditor.
* All nine workflow areas are accessible and tied to representative constructed information.
* All four PRD increments are represented as scope context, with later-increment concepts visibly labeled as demonstrative rather than delivered or approved functionality.
* No resident access or live-action pathway appears; role switching is explicitly non-authoritative.
* Data is identified as constructed/non-identifying and all proposals, forecasts and metrics retain their draft/assumption/uncertainty labels.
* The UX/UI Designer's feedback explicitly addresses every profile; company-role perspectives and any relevant gaps are recorded; compatible fixes are applied without contradicting the PRD or user direction.
* Keyboard and responsive checks cover the main navigation and key profile/workflow interactions, and the final change review shows only the requested prototype and task artifacts.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-10-06/prd-prototype-plan.md |
| Phase details | .copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-10-06/prd-prototype-plan-critique.md; Complete, Revise; PC-001 resolved directly |
| Relevant research | .copilot-tracking/research/2026-10-06/prd-prototype-research.md |
| Changes-record role | .copilot-tracking/changes/2026-10-06/prd-prototype-changes.md is created or continued by implementation as its evidence record |
| Planning and implementation readiness | Planning critique PC-001 resolved; P01 implementation complete; ready for post-implementation Review |
| Continuation context | User explicitly requested building; parent RPI flow continues after planning gates |

## Sources

* `.copilot-tracking/research/2026-10-06/prd-prototype-research.md`: C1-C10 establish current PRD, profile/workflow scope, non-production limits, accessibility and unresolved company evidence.
* `docs/prds/proper-warm-retrofit-programme-demonstrator.md`: draft v0.6.2 and the complete role/workflow requirements.
* `docs/reference/research/company/company-profile-research.md`: bounded decision map for eight company-role perspectives.
* `docs/reference/research/ux/program-manager-document-workspace-journey.md`: generic accessibility hypotheses only; not direct evidence for this workbench.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Build and review the PRD prototype

* Intent: Produce and validate a role-complete interactive prototype while preserving the PRD's demonstrator and decision-authority boundaries.
* Dependencies: Completed research and final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Build the shared workbench prototype

* Requirement and evidence: All 11 profiles, nine workflows, constructed data and safe boundaries (research C1-C10).
* Expected result: Self-contained, interactive HTML prototype with a shared case/portfolio context and role-relevant views.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md
* Review continuation: RV-001 is implemented; the selected case view includes an inspectable constructed case history/timeline.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Review every profile and incorporate UX feedback

* Requirement and evidence: Explicit user direction; PRD user/workspace requirements; research C3, C8-C10.
* Expected result: UX Designer findings cover all 11 profiles; relevant company-role feedback is attributed as a perspective; accepted changes are applied and remaining disagreement is recorded.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Validate the prototype and close the implementation record

* Requirement and evidence: PRD NFR-001/NFR-003/NFR-005/NFR-012 and functional behavior, plus this plan's acceptance criteria.
* Expected result: Verified local behavior, all-profile/workflow inventory, keyboard/responsive review and a clean diff summary.
* Detail section: P01-T03 in .copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md

## Dependencies

* Completed RPI Research: Profile coverage, prototype constraints and open uncertainty must be resolved before plan approval (satisfied by current research artifact).
* UX/UI Designer review: Requires a runnable prototype and a profile inventory before the final validation task.
* Company-role agents: Their feedback must stay within their documented decision rights and must not be treated as verified company evidence.

## Validation and Change Locks

* Validation owner: primary implementation agent.
* Exact removals: none.
* Maximum new deliverable files: one HTML prototype; RPI tracking artifacts are maintained in their designated paths.
* Canonical target: `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html`.
* Generated targets: none.
* Semantic coverage: every named profile, all nine workflow labels, role-specific context, non-production authority boundaries, constructed-data cues and relevant proposal/forecast uncertainty.
* Regression coverage: local load without network, role/workflow/case navigation, keyboard operation, responsive viewport, light/dark theme and console errors.
* Validation evidence: direct rendered browser inspection, interaction and accessibility checks, source review for absence of external calls/persistence/consequential actions, profile/workflow inventory and final Git diff.
* Write boundary: prototype file plus the assigned RPI changes/review artifacts; no PRD/BRD/company research changes and no generated/dependency files.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|---|---|---|
| 2026-10-06, PC-001 [Medium] | resolved | Added explicit four-increment acceptance criterion and required a four-row increment inventory in final validation; later concepts must be labeled demonstrative, not delivered or approved. |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-06/prd-prototype-changes.md
* Ready phase or task: P01 implementation and its planned Review are complete. RV-001 was implemented in a later change and validated; no second Review is run.
* Remaining provisional question or blocker: Actual user validation, approved company roles/permissions and production decisions remain out of scope.
