<!-- markdownlint-disable-file -->
# RPI Plan Critique: Proper Warm PRD Prototype

## Metadata

* Task ID: prd-prototype-2026-10-06
* Critique date: 2026-10-06
* Plan: .copilot-tracking/plans/2026-10-06/prd-prototype-plan.md
* Phase details: .copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Use the latest-main baseline already fetched; prototype the current PRD; obtain UX/UI Designer review for every named profile; company-role agents may add user-perspective feedback. The prototype is one standalone local HTML deliverable, using constructed/non-identifying exercise records, with no production use, live action/contact/integration, or resident user journey. Role selection is not authentication.
* Research and evidence considered: .copilot-tracking/research/2026-10-06/prd-prototype-research.md; docs/prds/proper-warm-retrofit-programme-demonstrator.md; the supplied plan and phase details.
* Decisions, dependencies, and acceptance criteria considered: User direction and stated latest-main status; all 11 PRD profiles, nine workflow areas, and four increments; one shared workbench and PRD boundaries; P01 and P01-T01 through P01-T03 dependencies; named local, offline, keyboard, responsive, theme, accessibility, UX-review, and source/diff validation criteria.
* Assessment boundary: This is a single critique of the supplied final-candidate plan and matching phase details against the supplied research, current PRD, and caller direction. No implementation, source revision, external research, or inference about actual company users, roles, permissions, or operating evidence was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| User direction: latest main and current PRD | Covered | Plan records fetched/up-to-date baseline; PRD is identified as draft v0.6.2, matching its supplied frontmatter. |
| User direction; C3; P01-T02 | Covered | UX review is explicitly required for all 11 profiles, with per-profile review dimensions and missing UX coverage treated as a blocker. |
| User direction; C8; P01-T02 | Covered | Company-role input is bounded as perspective rather than privileged evidence; the plan does not treat it as validated research. |
| C2-C7, C10; P01-T01; acceptance criteria | Covered | One shared workbench, all nine workflow areas, constructed-data provenance, non-authoritative profile selection, human boundaries, non-production limits, and accessibility expectations are represented. |
| C5; P01-T01; four-increment scope | Partial | The plan calls for showing the four increments, but its acceptance criteria and final inventory do not explicitly verify coverage and demonstration-status labeling for each increment. See PC-001. |
| P01 and P01-T01 through P01-T03 | Covered | Build precedes UX review and feedback changes; validation follows both. Research and critique are dependencies, with review and change evidence assigned to tracking artifacts. |
| Validation and change locks | Covered | The single HTML deliverable, no-network/source inspection, interaction/accessibility checks, final diff review, and documentation write boundary are stated. |

## Verdict

* Verdict: Revise
* Rationale: The plan is otherwise credible and faithfully preserves the current PRD's prototype boundary, all-profile UX review, and nine-workflow coverage. One stated scope requirement, representing all four PRD increments, lacks an explicit completion check; implementation readiness should wait for that small planner-owned alignment.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Make all four increments an explicit acceptance check

* Related IDs: Caller requirement (four increments); C5; P01-T01; plan scope and acceptance criteria; P01-T03.
* Evidence: .copilot-tracking/plans/2026-10-06/prd-prototype-plan.md says to show the four PRD increments as scope context and distinguish later-increment concepts where useful, while its acceptance criteria require the 11 profiles and nine workflows but do not check increment coverage. .copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md does not require an increment-by-increment coverage inventory. The PRD's “Release increments within this PRD” section defines four increments and says they remain one non-production product.
* Concern: The required increment context could be omitted or presented without clearly distinguishing demonstrative/later-increment concepts, yet the current completion checks could still pass.
* Impact: The prototype could satisfy the role and workflow counts while leaving an explicit scope expectation unverified or implying later-increment concepts are delivered or approved.
* Smallest useful change: Add one acceptance criterion and corresponding final validation inventory requiring each of the four named increments to be represented as scope context, with later-increment concepts visibly framed as demonstrative rather than delivered or approved functionality.
* Action owner: Planning parent.
* Exact resolving evidence: Updated plan acceptance criteria and P01-T03 validation expectations explicitly name all four increments; the eventual changes record includes a four-row increment inventory with the relevant prototype surface and its demonstrative/later status.
* Decision route: Direct planner correction; current user direction resolves the scope, so no divergent user decision is needed.

## Strengths and Residual Risk

* All 11 provisional PRD profiles are named and reachable; UX review criteria require coverage per profile, not a generic persona pass.
* The user/research distinction is preserved: company-role feedback is perspective only, constructed records are not company evidence, and residents are affected stakeholders rather than MVP users.
* Role selection, proposals, resident/safety/finance decisions, and workflow actions are consistently bounded away from authentication, approval, persistence, and live operations.
* All nine workflows, four-increment context, single-file/offline delivery, and broad accessibility checks are in scope. Actual user validation, operational authorities, and production decisions remain appropriately out of scope.

## Questions or Blocking Evidence Gaps

* No decision-critical evidence gap blocks the exercise prototype. PC-001 is a planner-owned acceptance/traceability correction, not a request for new research or user input.

## Limitations

* The critique relies only on the supplied plan, phase details, research, current PRD, caller requirements, and skill template. It does not establish usability, company role authority, resident outcomes, or production readiness.

| [.copilot-tracking/plans/2026-10-06/prd-prototype-plan.md](.copilot-tracking/plans/2026-10-06/prd-prototype-plan.md) | Final-candidate plan assessed |
| [.copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md](.copilot-tracking/details/2026-10-06/prd-prototype-phase-details.md) | Matching phase and task details assessed |
| [.copilot-tracking/research/2026-10-06/prd-prototype-research.md](.copilot-tracking/research/2026-10-06/prd-prototype-research.md) | Supplied research evidence considered |
| [docs/prds/proper-warm-retrofit-programme-demonstrator.md](docs/prds/proper-warm-retrofit-programme-demonstrator.md) | Current PRD requirements checked |

## Next Steps

* Critique execution status: Complete. Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Highest-impact finding: PC-001. Action owner: planning parent. Smallest next action: add an explicit four-increment acceptance check and final inventory.
* User response required: No.
* In this standalone invocation, use `/rpi-plan` to apply the planner-owned correction and finalize; this critique does not invoke a peer stage or revise plan sources.
