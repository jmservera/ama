<!-- markdownlint-disable-file -->
# RPI Phase Details: Proper Warm PRD Prototype

## Metadata

* Task ID: prd-prototype-2026-10-06
* Task slug: prd-prototype
* Related plan: .copilot-tracking/plans/2026-10-06/prd-prototype-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-06/prd-prototype-research.md; docs/prds/proper-warm-retrofit-programme-demonstrator.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Build and review the PRD prototype | complete | P01, P01-T01, P01-T02, P01-T03 |

<!-- rpi:phase id=P01 -->
## P01: Build and review the PRD prototype

### Context

The PRD defines one shared, home-centred workbench with 11 provisional role workspaces and nine connected workflow areas. It calls for constructed exercise records, clear evidence/authority boundaries and an accessible role-specific experience. It is draft v0.6.2; company baselines, actual roles and approvals remain unknown. The user's request expressly requires UX review for every profile and permits role-agent input.

### Intent

Deliver a locally inspectable prototype that makes the PRD concrete across profiles without implying production readiness or live authority, then use UX and role perspectives to improve and verify it.

### Boundaries

* Included: One HTML prototype, constructed examples, role/task context, shared case/portfolio views, workflow navigation, bounded proposal states, profile-by-profile critique, fixes and validation.
* Excluded: Production application, real data, network calls, persistence, authentication, actual role permissions, external contact/actions, PRD changes and operational approvals.

### Review continuation

The completed RPI Review identified RV-001: the selected case view showed current snapshot fields and a source trace but no inspectable case history. P01-T01 resumed and now adds a short constructed event history for each sample case. This does not imply live audit data or committed transitions; every event remains visibly illustrative, with source/context status and no operational action. The existing Review remains the task's one Review; the later fix was validated without repeating it.

### Likely Targets

* `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html`: deliverable prototype.
* `.copilot-tracking/changes/2026-10-06/prd-prototype-changes.md`: implementation evidence and review response.

### Dependencies

* Research artifact and PRD provide the settled boundaries and full profile/workflow inventory.
* UX and role-agent review follows a usable first candidate; no direct user research or external action is authorized.

### Validation Expectations

* Open locally with no network dependency; exercise role, workflow and case navigation.
* Check all 11 profiles, nine workflow labels and four increments against the PRD; verify role switching never presents itself as access control.
* Check keyboard focus, labels, contrast cues, narrow viewport, reduced motion and chart text/table equivalents.
* Inspect HTML/JavaScript for no live calls, persistence or action-shaped claims; review final Git diff.

### Completion Evidence

* Prototype file and explicit all-profile UX review coverage.
* Changes record listing accepted feedback, changes, validation and any residual concern.
* This phase's implementation evidence and reconciled checklist. The outer RPI Review phase records its separate review outcome after explicit advancement.

### Unresolved Items

* Direct employee/resident validation, approved company roles, operational values and production decisions remain outside this prototype and cannot be established by agent perspectives.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Build the shared workbench prototype

#### Context

The PRD user table lists 11 role workspaces; its workflow map covers prioritisation, technical readiness, resident service, procurement/capacity, hazard referral, quality/defects, finance/grants, handoffs and portfolio decisions. No single profile owns the whole lifecycle.

#### Intent

Create one interactive shared workbench with appropriate differences in role task context and common constructed home/building records.

#### Boundaries

* Included: Profile picker, profile-aware work queues, workflow navigation, representative case detail/history, evidence provenance, blockers, portfolio metrics/forecast caveats and unapproved bounded suggestions.
* Excluded: Authorization or simulated permissions, resident login, actual approval/write/save, AI generation, integrations, personal data and any persistent mutation.

#### Likely Targets

* `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html`: self-contained HTML/CSS/JS deliverable.

#### Dependencies

* Complete plan and details critique.

#### Validation Expectations

* Load locally, inspect all profiles/workflows, activate navigation and representative controls, verify no external/network dependency and read the UI as constructed exercise material.

#### Completion Evidence

* A single local HTML artifact with functioning profile/workflow context and explicit demonstrator status.
* For Review continuation RV-001: selected-case timeline with constructed events, preserved current-state boundary, and keyboard/narrow-screen validation. Complete: all eight constructed cases show three history entries with the explicit illustrative boundary.

#### Remaining considerations

* Specific profile copy is a product interpretation and should not assert unapproved company process.
* RV-001 was implemented and validated after the completed Review; P01-T02 and P01-T03 evidence remains complete from the prior implementation pass.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Review every profile and incorporate UX feedback

#### Context

The user explicitly asks the UX Designer to review every profile. The PRD names 11 profiles; eight company-role agents align to internal Asset, Safety, Programme, Finance, Procurement, Resident Engagement/Housing and Data/Performance perspectives. No company agent represents the external provider contact, Quality and Assurance or Digital Operator/Auditor; UX Designer coverage is required for those too.

#### Intent

Obtain an actionable UX review across the complete PRD profile set and use relevant company-role feedback as bounded user-perspective challenge.

#### Boundaries

* Included: A single UX/UI Designer review with explicit per-profile assessment; relevant role-agent responses from their proper scope; parent review and implementation of compatible corrections.
* Excluded: Claiming actual users participated, broadening profile count, making company or regulatory facts, or adopting any agent recommendation that conflicts with PRD/user direction.

#### Likely Targets

* `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html`: target for accepted corrections.
* `.copilot-tracking/changes/2026-10-06/prd-prototype-changes.md`: review ledger and dispositions.

#### Dependencies

* P01-T01 produces a reviewable candidate.

#### Validation Expectations

* UX reviewer explicitly addresses all 11 PRD profile labels with task entry, information priority, decision boundaries, key usability risk and concrete recommendation.
* Company-role feedback is clearly role-attributed and does not claim privileged knowledge.
* Every actionable finding is accepted, rejected with rationale, or recorded as unresolved; no silent omissions.

#### Completion Evidence

* Profile-by-profile UX coverage table and bounded role-agent feedback summary in the changes record.

#### Unresolved Items

* Direct employee/resident validation remains out of scope; role-agent perspectives are not validated user research.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Validate the prototype and close the implementation record

#### Context

PRD criteria require all nine workflow areas, usable role tasks, accessible controls and careful labels for exercise data, forecasts and permissions. The repo has no build/test/lint command; repository instructions call for rendered Markdown/diff review, while the HTML requires direct behavioral checks.

#### Intent

Verify the deliverable and produce traceable evidence that the user's request and plan acceptance criteria were met.

#### Boundaries

* Included: Browser/local execution, navigation and control checks, profile/workflow inventory, keyboard/responsive checks, and final diff review.
* Excluded: Production security certification, formal WCAG conformance claim, actual user validation, performance/SLO attainment and live integration tests.

#### Likely Targets

* `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html`: tested deliverable.
* `.copilot-tracking/changes/2026-10-06/prd-prototype-changes.md`: completed validation record.

#### Dependencies

* P01-T01 and P01-T02 complete.

#### Validation Expectations

* At least the browser console, profile and workflow navigation, a narrow responsive viewport, keyboard access and key demonstrator disclaimers are checked.
* The final inventory has one row for each of the four PRD increments, names its prototype surface, and labels later-increment concepts demonstrative rather than delivered or approved.
* Review diff for unexpected files and ensure source remains non-production.

#### Completion Evidence

* Changes record states concrete checks, outcomes and any unavailable checks; implementation and review readiness are reconciled. The separate RPI Review artifact is created only when that phase is explicitly advanced.

#### Unresolved Items

* Full keyboard/screen-reader user testing and production acceptance remain open PRD follow-ups.
