---
title: Issue 215 regulatory alert and chat UX plan critique
description: Bounded final-candidate assessment with planner-owned corrections
ms.date: 2026-10-16
---

## Metadata

* Task ID: 215
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/regulatory-alert-chat-ux-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/regulatory-alert-chat-ux-phase-details.md
* Critique execution status: Complete
* Assessment: One bounded critique of the supplied final candidate; no implementation or delegation.

## Inputs and Criterion Boundary

* Caller requirements: seven audience alert/chat patterns; noticed, source,
  status, action, owner and clock; automated and keyboard WCAG 2.2 AA
  engineering checks; doubt and no-source states; a staff-trial protocol
  with the unavailable real trial explicitly unmet.
* Primary inputs: .copilot-tracking/plans/2026-10-16/regulatory-alert-chat-ux-plan.md,
  .copilot-tracking/details/2026-10-16/regulatory-alert-chat-ux-phase-details.md
  and .copilot-tracking/research/2026-10-16/regulatory-alert-chat-ux-research.md.
* Supplied evidence pointers consulted:
  docs/reference/research/ux/regulatory-literacy-for-journeys.md,
  docs/adrs/0005-regulatory-compliance-assistant.md and
  src/core/src/zava_forward/core/projection.py.
* Repository context consulted: docs/case_study_48_original.md, the opening
  exercise-baseline sections of docs/case_study_48_addendum.md,
  docs/reference/README.md and docs/reference/memory.md. Memory is context,
  not evidence.
* Decisions and dependencies: ADR 0005 accepted for synthetic development
  only on 2026-10-16; Juan Manuel Servera is exercise Legal, Compliance and
  DPO owner. Reuse the caller-confirmed merged #328, #331 and #348 backend
  without new rights, approvals, clocks or operational authority.
* Acceptance boundary: assess implementation-plan credibility and evidence
  honesty, not delivered software, legal currentness, full WCAG conformance
  or staff comprehension. The full remote issue body and merged PRs were
  not independently retrieved; caller requirements define this review.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Seven audience patterns; C1/C6; P01-T01/P02-T01 | Partial | Seven existing staff role mappings are not the seven journey audiences. The plan promises audience documentation but does not specify the crosswalk or its acceptance evidence. PC-002. |
| Noticed/source/status/action/owner/clock; C3; P01-T01 | Covered | Plan names all six fields and reuses scoped server alerts for the exact case; empty and failed reads are distinguished from safety/compliance. |
| Structured cited answers and plain mode; C4/C5; P01-T02 | Covered | Uses answer.sections and citations, expandable exact excerpts, presentation-only plain mode and preserved ordinary chat. |
| Doubt, missing source, disabled and outage states; P01-T01/P01-T02/P02-T01 | Covered | Explicit unknown/failure wording, visible disabled capability, existing persisted doubt API with receipt/error and browser checks for no-source/refusal and persisted doubt. |
| WCAG 2.2 AA engineering evidence; P02-T01 | Covered | Automated axe A/AA scope, native controls, Tab/Shift-Tab/Enter/Space, focus, polite status/error announcements and 320px reflow; no unsupported conformance claim. |
| Synthetic-only authority; C2/C6; P01-T01/P02-T01 | Covered | Current authenticated role, server projection, supplier access denial, constructed SQL fixtures and no outbound inference; no new approval controls. |
| Unavailable real staff trial; P02-T02 | Covered | Protocol specifies tasks, scoring, consent and stop rules; trial remains Not run and unmet. |
| Existing backend and test ownership; C3-C6; P02 | Covered | Reuse, API ownership, at most two new check/test files, existing regressions, ruff/mypy and actual loopback SQL-backed app. |
| Documentation, review and PR; P02-T02/P02-T03 | Partial | README, append-only KB log, index pointer and Refs #215 preserve acceptance limits. Unconditional routing of remaining review findings to later work lacks a blocking-defect gate. PC-001. |
| Operational source/delegate verification and chat-value ship test | Covered as deferred | Explicit follow-ups retain actual delegates, verified sources, comprehensive accessibility review and ADR chat-value evaluation; synthetic acceptance does not satisfy these gates. |

## Verdict

* Verdict: Revise
* Rationale: The engineering approach and accepted development boundary are
  credible. Two narrow planner corrections are needed: distinguish audience
  coverage from staff-account coverage, and prevent the one-review limit
  from becoming permission to defer blocking defects. Neither requires a
  new user decision, another research phase or another critique pass.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Review closeout permits deferring blocking findings

* Related IDs: P02-T02, P02-T03; source/authority and accessibility constraints.
* Evidence: .copilot-tracking/details/2026-10-16/regulatory-alert-chat-ux-phase-details.md,
  section P02-T02 and P02-T03: "Review once after implementation; remaining
  findings route to later work." The plan then schedules commit, push and
  PR without a severity or disposition qualification.
* Concern: One bounded review is compatible with fixing its findings, but
  this wording provides no distinction between accepted residuals and
  defects that violate the current implementation boundary.
* Impact: A known authorization, citation-integrity, safety-route or
  accessibility regression could be deferred while the engineering slice
  is represented as ready. This is a release-gate ambiguity, not evidence
  that any such defect currently exists.
* Smallest useful change: Keep the single review, but require correction
  and targeted verification of blocking findings before ready-for-review
  closeout. Allow later-work disposition only for explicitly justified
  nonblocking residuals. If a blocker cannot be corrected, record it and
  keep any PR draft/not ready; do not claim the slice passed.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T03 explicitly states this gate in the
  plan/details, and requires the eventual review artifact to record each
  finding's severity, owner, disposition and verification or remaining
  blocker. No additional critique pass is required.
* Decision route: Direct planner correction. Existing user direction
  authorizes implementation and a PR, not acceptance of blocking defects.
* Disposition: Open; correct before implementation handoff.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Staff-role count does not establish seven-audience coverage

* Related IDs: Seven audience requirement; C1, C6; P01-T01, P02-T01, P02-T02.
* Evidence: .copilot-tracking/details/2026-10-16/regulatory-alert-chat-ux-phase-details.md,
  P02-T01 requires "all seven existing staff role help mappings" and makes
  supplier design-only. P02-T02 promises a seven-audience README design.
  docs/reference/research/ux/regulatory-literacy-for-journeys.md, Needs by
  journey role, includes leasehold staff and residents/representatives as
  well as suppliers. Its everyone-handling-data row is cross-cutting.
  src/core/src/zava_forward/core/projection.py defines seven different
  staff account roles and denies chat/law access to contractors.
* Concern: The plan does not reconcile the two different sets. Testing
  seven staff mappings alone cannot demonstrate seven journey patterns,
  especially leasehold missing-source handling and resident plain-language,
  human-reviewed choice/contact guidance.
* Impact: An implementation could pass the stated account-mapping tests
  yet omit required audience patterns or imply that an unmapped audience
  needs new access. The latter would conflict with the explicit no-new-rights
  boundary.
* Smallest useful change: Add an explicit seven-audience crosswalk to
  P01-T01/P02 acceptance: repairs/contact/housing; Building Safety;
  survey/design/coordinator/QA; Programme/Assets/Finance/grants;
  leasehold-service staff; residents/representatives; and suppliers.
  Treat data-handling guidance as common to all. For each audience identify
  its recognition/action/owner pattern, mapped existing account role if any,
  and browser evidence or design-only evidence. Unmapped patterns remain
  documented proposals, not new permissions or delivered end-user journeys.
* Action owner: Planning parent.
* Exact resolving evidence: The plan/details require a seven-row README
  matrix with those delivery/evidence dispositions, plus separate browser
  assertions for the existing seven staff-account mappings and contractor
  denial. The criterion audit must not count a design-only row as a
  functioning resident, supplier or other unimplemented interface.
* Decision route: Direct planner correction within the caller's seven-pattern
  and no-new-rights requirements; no user authorization change is needed.
* Disposition: Open; correct before implementation handoff.

## Strengths and Residual Risk

* Deterministic alerts stay outside optional chat; server-owned clocks,
  scoped projection and unaltered cited excerpts prevent client-side legal
  interpretation or authority expansion.
* Empty scoped results are not presented as no risk. Unknown, source gaps,
  doubt receipts/errors and disabled capability are explicit design states.
* Actual loopback SQL-backed synthetic checks are more credible than
  template-only assertions; automated accessibility evidence remains
  distinct from manual assistive-technology and full conformance assessment.
* The caller accepts that real repairs/housing/grants trials cannot run.
  A protocol and explicit unmet criterion are the correct deliverable,
  not a reason to block synthetic development or invent participant results.
* Real delegates, current applicable sources, actual staff processing and
  measured chat value remain operational gates. The accepted exercise-owner
  decision does not resolve them and this critique does not reopen it.

## Questions or Blocking Evidence Gaps

* No decision-critical user question. Both findings are planner-owned.
* No need for additional legal retrieval: this plan introduces no new rule,
  commencement assertion or operational source-currentness claim.

## Limitations

* No app, scanner, keyboard check, test suite or staff trial was run during
  this read-only planning assessment; none is claimed as passed.
* Backend behavior is assessed from supplied research and selected pointers,
  not an independent full implementation or security audit.
* Only this critique artifact was written. Existing untracked plan, details
  and research inputs were left unchanged; no branch, commit or PR action
  was taken.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Qualify the single-review closeout gate, then add
  the audience-to-account/evidence crosswalk in the same planning revision.
* User response required: No.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/regulatory-alert-chat-ux-plan.md](.copilot-tracking/plans/2026-10-16/regulatory-alert-chat-ux-plan.md) | Reviewed final-candidate plan; unchanged. |
| [.copilot-tracking/details/2026-10-16/regulatory-alert-chat-ux-phase-details.md](.copilot-tracking/details/2026-10-16/regulatory-alert-chat-ux-phase-details.md) | Reviewed task details; unchanged. |
| [.copilot-tracking/research/2026-10-16/regulatory-alert-chat-ux-research.md](.copilot-tracking/research/2026-10-16/regulatory-alert-chat-ux-research.md) | Supplied bounded research; unchanged. |
| [.copilot-tracking/plans/2026-10-16/regulatory-alert-chat-ux-critique.md](.copilot-tracking/plans/2026-10-16/regulatory-alert-chat-ux-critique.md) | Complete critique; Revise, two actionable findings. |

## Next Steps

Planning parent: correct PC-001 and PC-002 directly, record their dispositions
and finalize without another critique. No user action is required. This
bounded critique stops here; implementation and source edits are not authorized
within this task.
