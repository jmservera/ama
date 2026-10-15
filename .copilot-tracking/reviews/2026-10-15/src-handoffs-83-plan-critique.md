---
title: Issue 83 final-candidate plan critique
ms.date: 2026-10-15
---

## Metadata

* Task ID: #83 / src-handoffs-83.
* Critique date: 2026-10-15.
* Plan: .copilot-tracking/plans/2026-10-15/src-handoffs-83-plan.md.
* Phase details: .copilot-tracking/details/2026-10-15/src-handoffs-83-phase-details.md.
* Critique execution status: Complete.
* This is the one independent final-candidate critique, not an implementation review or a request for another critique.

## Inputs and Criterion Boundary

* Caller requirements: full RPI; additive provenance and receipt/escalation/completion in migrated core/API/UI; accepted ADR 0006; portable persistence without SQL schema or dependency changes; pip only; synthetic data; no edits to .env, .vscode or .copilot-tracking/github-issues. This critique writes only its designated output.
* Supplied evidence: .copilot-tracking/research/2026-10-15/src-handoffs-83-research.md, especially C1-C9 and the selected alternative; the plan and phase details above.
* Relevant source checks: docs/case_study_48_original.md; docs/case_study_48_addendum.md, EXA-005/008; docs/reference/README.md and docs/reference/memory.md for context; docs/reference/research/sector/housing-association-primer.md for customer framing; docs/adrs/0006-src-layout-and-cutover.md:145-177; docs/prds/zava-forward-retrofit-programme-demonstrator.md, FR-009/010/011 and AC-012/014/036; docs/brds/agentic-retrofit-programme-brd.md, BG-010; current workflow, projection, handover route, web panels and role-inventory tests under src/.
* Dependencies: P01 supplies the shared semantics used by P02 routes, projections and UI. P03 validates the integrated result before delivery. No new workload or SQL service is needed.
* Authoritative exclusions: approved operational escalation timing remains unmet and unticked at the user's direction. SQL Server, live Azure/model and unavailable image evidence cannot be substituted by local synthetic results. Broad FR-043 invalidation redesign is excluded, so this slice cannot claim full AC-008/013 acceptance.
* Assessment boundary: credibility of this bounded plan, including its acceptance and delivery gates. Existing source is evidence of integration risks, not proof of an implemented defect in a change that does not yet exist. No external research, private data, nested agents, implementation or source edits were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| ADR 0006; C1/C6; P01/P02 | Covered | Shared mixin and case-body persistence preserve the core/workload dependency boundary and avoid a new schema. |
| FR-009/010; AC-012; C3/C4; P01-T01 | Partial | Version, stages, source, actor, reason and next action are planned; selected receiving owner needs an explicit no-bypass contract, PC-001. |
| FR-011; C5; P01-T02 | Covered with coupled gap | Routing legacy hand_over through offer addresses the observed immediate transfer; return/reopen must not introduce another path, PC-001. |
| FR-011; C8; P01-T01 | Partial | Six canonical states and legacy labels are credible. Receipt/escalation actor and transition rules remain underspecified, PC-002. |
| FR-011; AC-014/036; EXA-008; P02-T01 | Partial | Queue roles, redaction and ownership labels are planned; urgency, handoff next action and resident-update commitments are not explicitly covered, PC-003. |
| C7; P02-T02 | Covered in intent | Need-role holding and contractor denial are explicit. Resolution tests for PC-002/003 should exercise real stateful routes and queue/detail/history responses, not rely solely on inventory route detection. |
| BG-010; C2/C9; OD-09 | Explicitly deferred | Manual escalation and optional human-entered due dates do not satisfy approved-time operational escalation. User direction already resolves this boundary; it is not a finding or a blocker for the bounded PR. |
| P03-T01 | Covered | Five suites, quality tools, JS syntax, migration checks, synthetic app run and Docker attempt are planned with unavailable live checks distinguished. |
| P03-T02; full RPI | Partial | One review is appropriate, but automatic deferral of any open finding lacks an in-scope defect gate, PC-004. |
| Scope and prohibited paths | Covered | src implementation/tests plus directly related documentation and RPI artifacts; no deployment, new model task, private data or excluded-file changes. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 2 High, 2 Medium, 0 Low.
* Rationale: the architecture and bounded acceptance posture are credible. Four direct planning corrections are needed to make ownership, permissions, cross-surface context and review disposition testable. None requires a significant or divergent owner decision. The parent should disposition this complete finding set directly and finalize without another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Selected return/reopen owner lacks a no-transfer invariant

* Related IDs: FR-010/011, AC-012/036, C4/C5, P01-T01/T02, P02-T01/T02.
* Evidence: phase details:12-15 introduces a selected staff owner; research:90-93 permits selection beyond the current case owner. Plan:39-40 prohibits ownership transfer before acceptance but does not say how that rule applies to return/reopen selection. Current src/core/src/zava_forward/core/workflows.py:38-78 preserves the existing owner on return/reopen, whereas src/core/src/zava_forward/core/store.py:341-350 demonstrates the immediate reassignment path this task intends to remove.
* Concern: the new receiving-owner input could be implemented as a direct update of owner_code/owner/owner_role or waiting_on, or could be displayed as confirmed ownership despite only naming a destination. The plan does not resolve that distinction. This is an ambiguity, not a claim that the future implementation already transfers ownership.
* Impact: closing hand_over alone would not establish the no-bypass acceptance criterion if another endpoint could directly assign or mislabel the selected colleague.
* Smallest useful change: state that receiving-owner selection records a proposed receiving responsibility only and cannot change accountable ownership before named acceptance. If selection initiates a handoff, use the same offer/accept guards and reject conflict with an active unfinished handoff; otherwise retain it as disposition metadata with an explicitly unconfirmed label. Preserve current-owner fallback without inventing receiving acceptance.
* Action owner: planning parent, with implementation/test work assigned to P01-T01/T02 and P02-T02.
* Exact resolving evidence: revised phase details explicitly distinguish disposition recipient from accountable case owner and specify active-handoff interaction. The planned JSON/SQLite and HTTP cases must select a different colleague during both return and reopen, assert unchanged accountable-owner fields and chase responsibility, assert an unconfirmed receiving label, and prove that any eventual transfer occurs only through recipient acceptance. Include the legacy handover endpoint in the same invariant coverage.
* Decision route: direct planner correction under the existing no-bypass requirement; no owner response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Receipt and escalation do not yet have an executable authority contract

* Related IDs: FR-011, C4/C7/C8, P01-T01, P02-T01/T02.
* Evidence: phase details:17-26 specifies the acceptor and completer, but not who may record receipt or initiate escalation, which states permit those actions, or what happens to rejection/withdrawal after receipt/escalation. Naming an escalation manager is not the same as authorizing the actor. Current src/core/src/zava_forward/core/projection.py:51-55 permits staff POSTs generically; authority therefore depends on domain guards. Current src/core/src/zava_forward/core/workflows.py:112-151 restricts accept/decline/withdraw to Offered. src/api/tests/test_role_endpoint_inventory.py:42-67 checks route coverage and broad role denial but does not prove each dynamic case action's stateful authority.
* Concern: generic promises of role checks, negative tests and replay rejection do not select a consistent receipt/escalation contract. Adding only the three new actions could also strand existing decline/withdraw behavior after leaving Offered.
* Impact: unrelated staff could acknowledge or escalate work, or sender/receiver controls could disappear at intermediate states; API and UI could enforce different rules.
* Smallest useful change: add one compact action/state/actor table covering offer, receive, accept, reject, withdraw, escalate and complete. Specify allowed actor relationships, valid source states, terminal/replay handling, manager-target validation and unchanged owner/chase semantics. Use recipient-only receipt and sender/chase-or-manager manual escalation as a conservative exercise contract consistent with existing authority boundaries; do not represent this as OD-09 operational approval.
* Action owner: planning parent; P01-T01 supplies the contract and P02-T01/T02 consumes and verifies it.
* Exact resolving evidence: revised details contain the table and the planned core/API cases exercise every allowed edge and forbidden actor/state combination, including received/escalated decline and withdrawal, duplicate receipt/escalation, accept-after-escalation, complete-before-accept, contractor/unknown-role denial and unchanged state/history/audit on rejection. UI controls must use the same permissions. Existing inventory must explicitly exercise the new dynamic actions with valid fixtures rather than merely match the /api/cases prefix.
* Decision route: direct planner correction for the bounded synthetic workflow. Operational authority remains an unticked follow-up, not a user question for this correction.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Handoff context omits urgency, next action and resident-update continuity

* Related IDs: FR-011, AC-014/036, EXA-008, C2/C3, P01-T01, P02-T01/T02.
* Evidence: docs/prds/zava-forward-retrofit-programme-demonstrator.md:846 requires urgency and next action separately from ownership and due date; :1460 requires the next resident update to be visible. docs/case_study_48_addendum.md:124 separates resident-update ownership and preserves pending commitments on rejection/reassignment. Plan:34-42 and phase details:31-35 omit urgency and resident-update context; the next step mentioned there follows return/reopen provenance and is not explicitly a handoff field. Current src/api/src/zava_forward/api/web/app.js:232-240 shows recipient-oriented offer wording, while :443-470 treats only Offered as actionable.
* Concern: six states and owner labels alone would leave required work context absent or generic; broadening the queue without updating its wording could still tell senders/managers to accept someone else's work. A due date is not a next resident-update commitment.
* Impact: queue and detail could disagree about who must act next, urgency or resident communication, and rejection/reassignment could lose pending commitments.
* Smallest useful change: explicitly add or project urgency, handoff next action, and resident-update owner/commitment independently of case/chase ownership and handoff due date. Render missing values as unknown/unassigned, without new timing policy. Specify queue labels/actions by viewer relationship and history/detail consistency, including preservation of existing pending update commitments on rejection, completion and subsequent offers.
* Action owner: planning parent; P01-T01 defines additive metadata and P02-T01/T02 handles projection, UI and tests.
* Exact resolving evidence: revised requirements/details list these distinct fields and their unknown-value behavior. Planned stateful tests compare sender, recipient and manager queue/detail/history for a populated fixture and a legacy fixture with missing fields, verify role-held text, and show a rejection followed by a new offer preserves pending resident-update responsibility. The synthetic app evidence must include sender and receiver views with Received/Escalated/Accepted/Completed controls and correct viewer-specific wording, not just a successful server startup.
* Decision route: direct planner correction to the supplied FR-011/AC-014 contract. No approved elapsed-hour target or resident communication is manufactured.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Review closeout automatically defers defects without a delivery gate

* Related IDs: P03-T02, full RPI, plan acceptance criteria.
* Evidence: phase details:50-53 says to route any open finding to follow-up, then commit, push and open the PR. Plan:74 requires a review but defines no disposition distinction between an in-scope ownership/permission defect and the explicitly accepted OD-09/live-evidence exclusions.
* Concern: the stated rule allows an acceptance-breaking defect discovered in the one implementation review to be treated identically to an approved residual risk.
* Impact: the loop could claim completed bounded delivery despite known failures of the very ownership and role invariants the PR is meant to establish.
* Smallest useful change: keep the one-review limit, but require direct correction and targeted verification of in-scope correctness/permission/acceptance failures before claiming implementation completion or PR readiness. Permit follow-up for the already excluded owner/live criteria and explicitly justified non-blocking residuals. A blocked result may be documented or published as draft, but not described as passing acceptance.
* Action owner: planning parent; implementation parent owns later review disposition and targeted validation.
* Exact resolving evidence: revised P03-T02 identifies blocking versus accepted/deferred categories and requires a finding-to-disposition/evidence ledger in the planned changes/review artifacts. The later ledger must link each fixed defect to its change and passing targeted validation, keep unavailable criteria unticked, and explicitly identify any remaining blocker. No second independent critique or repeated full review is required.
* Decision route: direct planner correction; the user has already accepted the operational-timing exclusion, so that exclusion is not reopened.

## Strengths and Residual Risk

* Reusing WorkflowMixin and case JSON persistence avoids a parallel service, nonportable SQL and workload import cycles.
* Keeping Offered/Declined storage compatibility with canonical labels avoids unnecessary data migration.
* Authenticated provenance, immutable transition history, role-held free text, contractor denial and sender chase ownership are explicit intentions worth retaining.
* Human-selected due dates and manual escalation are useful bounded functionality, not evidence of approved-time automation. The approved operational escalation criterion must remain unticked, as directed.
* Local JSON/SQLite evidence, synthetic app evidence and a Docker attempt cannot prove SQL Server, a successful image build, live Azure, real inference or operational readiness. Those limitations are already acknowledged.
* Retaining legacy direct-call compatibility with explicit unknown provenance is acceptable if new API confirmations still require the specified fields and projections never promote unknowns to verified evidence.

## Questions or Blocking Evidence Gaps

* No decision-critical user question is outstanding for this bounded plan.
* The four findings require direct planner revisions, not new research or owner approval.
* OD-09 and unavailable live evidence remain explicit follow-ups. Do not mark them satisfied to close this critique, and do not block this bounded PR solely because they remain unmet.

## Limitations

* This is a source-grounded planning assessment, not executed implementation acceptance. No tests, containers or live integrations were run.
* The issue's retrieved content is represented by supplied research W1; this critique makes no new remote issue/PR lifecycle or live regulatory claim.
* Uncommitted plan/research inputs and the existing environment were read in place on feat/src-handoffs-83. They were not moved, committed, discarded or edited.
* This report is the complete actionable finding set within the supplied boundary. It does not silently expand scope to FR-043, operational SLA approval, deployment or AI changes.

## Recommended Next Action

* Highest-impact finding: PC-001, prevent an alternate ownership bypass through return/reopen selection.
* Action owner: planning parent.
* Smallest next action: clarify the recipient/accountable-owner invariant in P01-T01 and attach its core/API test scenarios; disposition PC-002 through PC-004 in the same direct revision.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/src-handoffs-83-plan.md](.copilot-tracking/plans/2026-10-15/src-handoffs-83-plan.md) | Assessed implementation plan; unchanged by this critique |
| [.copilot-tracking/details/2026-10-15/src-handoffs-83-phase-details.md](.copilot-tracking/details/2026-10-15/src-handoffs-83-phase-details.md) | Assessed phase contracts; unchanged by this critique |
| [.copilot-tracking/research/2026-10-15/src-handoffs-83-research.md](.copilot-tracking/research/2026-10-15/src-handoffs-83-research.md) | Supplied evidence and authoritative exclusions |
| [.copilot-tracking/reviews/2026-10-15/src-handoffs-83-plan-critique.md](.copilot-tracking/reviews/2026-10-15/src-handoffs-83-plan-critique.md) | Complete one-pass critique and disposition requirements |

## Next Steps

The active planning parent should directly revise and disposition PC-001 through
PC-004, then finalize planning without another critique. Preserve the unticked
owner-decision/live-evidence criteria and continue the already requested RPI
workflow through its applicable gates. No user action is required. This critique
stops here; no implementation or peer-stage invocation is authorized by this
assessment.
