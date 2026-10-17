---
title: "RPI Plan Critique: Resident update and remedy controls"
description: One final-candidate assessment for task 88 against the supplied requirements and committed source
ms.date: 2026-10-17
ms.topic: reference
---

## Metadata

* Task ID: 88
* Slug: resident-update-remedy-controls-88
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/resident-update-remedy-controls-88-phase-details.md
* Research: .copilot-tracking/research/2026-10-17/resident-update-remedy-controls-88-research.md
* Source base verified: 1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c
* Branch: fix/resident-update-remedy-controls-88
* Critique execution status: Complete
* Execution boundary: exactly one full final-candidate assessment; no subsequent critique requested or performed.

## Inputs and Criterion Boundary

* The caller requires purpose, current named owner, due date and basis for resident-update commitments; complaint-response or package closure must not close outstanding remedies, defects or charge queries; each status must retain its own owner and date.
* The caller also requires current registry name/email/code/OID and date/version/input checks at the writer transaction, independent existing quality/procurement/finance states, reopen/history, pre-COMMIT rollback, truthful post-COMMIT outcomes and no successful-audit replay. Unknown legacy provenance must remain unknown; role names must not stand in for fictional named people.
* The complete supplied plan, phase details and research were assessed. Research C1-C11 was checked selectively against current requirements and directly relevant resident actions, workflows, projection, writer/recovery code, API/UI call sites and existing tests. W1 was treated as supplied research, not a fresh UI-guideline review.
* Required project context was consulted in docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md and the housing-association primer. Component guides supplied existing installed-source and control boundaries.
* Dependencies are none at issue level; #81 is hierarchy only. The shared sqlstore.py boundary with #91/#102 and possible store.py/API overlap remain coordinator-owned integration concerns. No other worktree or unmerged source was read. quality.py, assistants.py, progress.py and parallel fixtures remain excluded from edits; #92 HOLD remains excluded.
* The assessment preserves the test ownership lock: test_resident_decisions.py, at most 18 new semantic methods with the planned SQL subclasses; test_resident_api.py, at most five new methods; only the already-authorized handoff-test amendments; no test removals, duplicate fixture system or generated-dataset changes.
* Sending, actual authority, model calls, private data, Azure, IAM and a portal remain outside scope. The broader PRD lease, approval-reassessment and age-band requirements are not silently added to this task.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Commitment purpose/current owner/due/basis; C1/C3; P01-T01/T02 | Covered for new records; partial for legacy | Full explicit commitments and handoff preservation are planned; PC-001 identifies the missing legacy-confirmation path. |
| Independent response/remedy/defect/charge-query closure; C2/C4/C8; P01-T01 | Covered in intended domain model | Separate subordinate remedy state and retained external domains are appropriate. PC-004 addresses the missing mixed-state acceptance oracle. |
| Every status has its own owner/date; P01-T01; P02-T01 | Partial | New remedy dates/history are specified; named ownership must also be actionable under actual role gates (PC-002), and cross-domain field provenance needs explicit verification (PC-004). |
| Current registry and writer-time date/version/input checks; C5/C6; P01-T01 | Covered in intent | Direct registry lookup rather than sequence-dependent staff caching is planned; actor/destination mutation and actual writer conflicts are explicitly required. |
| Legacy unknowns and captured versus current identity; P01-T01 | Partial | Non-fabrication and separate snapshots are explicit; bootstrap/confirmation behavior is not executable yet (PC-001). |
| Pre-COMMIT rollback, audit prefix and recovery failure; C5/C6; P01-T01; P02-T01 | Covered | Canonical discard, prior-prefix preservation, original exceptions and first/persistent recovery-read fault probes are explicitly planned. |
| Truthful post-COMMIT outcome/no audit replay; P01-T01/T02; P02-T01 | Partial | Core recovery is planned, but the real HTTP/UI outcome is unspecified (PC-003). |
| Reopen/return/history and restart; P01-T01/T02; P02-T01 | Partial | Explicit reopen/version/history and restart are present; the combined independence scenario still needs an owned assertion (PC-004). |
| Existing panel, restricted references, no prompt expansion; C7/C9; P01-T02 | Covered in intent | Scoped native forms and role-limited new fields avoid a redesign. No accessibility conformance is inferred from this critique. |
| Test limits, loopback SQL, installed source and honest skips; P02-T01 | Covered | Findings can be resolved within existing limits; no extra test file or enlarged allowance is necessary. |
| Docs/KB route/log, parallel exclusions, one original Review; P02-T02 | Covered | Append-only log and coordinator boundaries are explicit; no second critique is needed after disposition. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 2 Medium.
* The core approach is appropriately bounded and most adverse persistence probes are already explicit. Four substantive planning gaps remain. They require one compatible revision batch, not a new research stage, wider implementation scope or a significant user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Legacy records require confirmation but have no defined path into the new lifecycle

* Related IDs: legacy-unknown requirement; C3/C4; P01-T01; P01-T02; P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md:52-61 specifies create/revise/reassign, a remedy for each new service request, and explicit confirmation before mutating legacy records. .copilot-tracking/details/2026-10-17/resident-update-remedy-controls-88-phase-details.md:29-42 preserves unknowns, but neither that task nor the web task identifies how confirmation happens. src/core/src/zava_forward/core/workflows.py:186-202 creates legacy owner/due-only updates. src/core/src/zava_forward/core/resident_decisions.py:309-372 has existing requests without any remedy object or expected remedy version.
* Concern: The candidate does not define how an incomplete existing commitment or remedy-absent request becomes eligible for the promised actions. The named remedy actions presuppose a remedy. Treating absence as an ordinary new record can fabricate original ownership/open dates, while refusing every mutation can permanently strand legacy requests. A commitment revise action could implement confirmation, but that behavior is not currently specified.
* Impact: The new lifecycle can either become unusable for existing records or acquire false historical provenance, violating the explicit unknown/confirmation boundary.
* Smallest useful change: Specify a bounded explicit confirmation/bootstrap operation, either within the proposed revise action or as a dedicated resident action. Define authorization, the expected-version rule for an absent/unversioned record, required supplied purpose/basis/current owner evidence, and its existing-panel entry point. Preserve the original incomplete snapshot and unknown original dates/owners; record confirmation time/current responsibility as a new event, not a reconstructed original event. For an existing response, confirmation must not change its response state or infer historical remedy completion.
* Action owner: Planning parent, updating P01-T01/T02 and the P02-T01 allocation.
* Exact resolving evidence: Synchronized plan/details identify the confirmation contract and allocate a grouped existing-file regression for owner/due-only commitment and remedy-absent Closed-response records. That regression must specify refusal without confirmation, successful explicit confirmation, unchanged historical unknowns and response state, stale-version refusal, and restart persistence without audit on refusal.
* Decision route: Direct planner correction. The caller already requires explicit legacy confirmation and prohibits fabrication; no new user policy decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Remedy-owner eligibility is not reconciled with the actual resident-action role gate

* Related IDs: named actionable ownership; C4/C9; P01-T01; P01-T02; P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md:58-63 grants remedy transitions to the current named owner or a "resident manager" and restricts new fields to existing resident-view roles. src/core/src/zava_forward/core/resident_decisions.py:185-192 gates service writers through RESIDENT_VIEW_ROLES, but :309-318 allows any registered non-contractor service/redress owner. src/core/src/zava_forward/core/controls.py:12-13 excludes Quality Inspector, Building Safety Liaison and Grants and Evidence Officer from resident-view roles. src/api/src/zava_forward/api/web/panels.js:123-124 similarly offers every non-contractor.
* Concern: Simply reusing these owner selectors can assign the new remedy to a valid registered person who cannot view the new references or pass the action gate. The plan does not say whether remedy ownership is separately supplied, derived from redress ownership, or restricted to eligible roles. "Resident manager" is not an existing literal registry role.
* Impact: A nominally valid named owner can be unable to progress their remedy, leaving manager intervention as the only functioning path and making core/UI authorization disagree.
* Smallest useful change: Define a small action/owner matrix using existing exact registry roles. Specify the remedy-owner source and eligible assignee roles, the manager exception, and commitment create/revise/reassign rights. Keep response service/redress ownership separate and retain existing independent-review restrictions. Filter new selectors and repeat the same eligibility checks at the writer transaction; do not introduce a new role or loosen projection to make an ineligible selection work.
* Action owner: Planning parent for the contract; P01-T01/T02 implement the same contract.
* Exact resolving evidence: Plan/details name the existing eligible roles and allocate a grouped JSON/SQL/API assertion: an eligible distinct fictional named owner succeeds, an ineligible non-contractor assignment refuses without mutation/audit, a non-owner cannot transition, and the named existing manager exception succeeds. Include role change without case-sequence change in the already-planned writer probe.
* Decision route: Direct planner correction within existing resident permissions. No invented resident-manager role, actual delegation or user decision is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Truthful post-COMMIT outcomes stop at the core exception boundary

* Related IDs: truthful post-COMMIT outcome/no replay; C5/C6/C7; P01-T01; P01-T02; P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md:69-70 requires reporting a committed outcome. The phase details at :39-42 and :74-76 plan core recovery and post-COMMIT fault injection, but specify no HTTP outcome contract. src/core/src/zava_forward/core/hazard.py:60-90, the selected recovery example, annotates and rethrows the original exception. src/api/src/zava_forward/api/server.py:878-885 calls the domain operation and then performs additional detail/check work; :905-912 rethrows ordinary exceptions for the resident route. src/api/src/zava_forward/api/web/app.js:26-35 and :433-436 expose ordinary request errors without a committed-outcome distinction.
* Concern: Reusing the core pattern alone can correctly quarantine audit and annotate an exception while the actual resident caller receives a transport/generic error after the transaction committed. Python exception notes do not reach the JSON/browser client. A failure in response projection after a successful domain operation is another distinct committed case.
* Impact: The user can be told only that an action failed, then retry a committed commitment/reassignment/remedy transition. This does not establish the required truthful outcome even if the original SQL event is not automatically replayed.
* Smallest useful change: Define a resident-route-specific committed-versus-refused error contract and the trusted signal crossing the domain/API boundary. Preserve the original diagnostic while giving the client an explicit committed outcome and reload/reconcile instruction; do not claim rollback or offer an ordinary retry as though nothing was written. Cover the subsequent detail/check failure boundary as well. Keep the change scoped to resident handling rather than globally changing all workflow errors.
* Action owner: Planning parent, assigning the bounded API contract to P01-T02 and its fault assertions to P02-T01.
* Exact resolving evidence: Plan/details explicitly include server.py resident outcome handling and scoped client behavior. Allocate within the existing five-method HTTP/browser allowance a fault-injected post-COMMIT synchronization/projection scenario that asserts the actual response/message, persisted new version/state, exactly one successful event, preserved prior audit and no replay on recovery or retry. Contrast it with pre-COMMIT refusal and unchanged state/audit.
* Decision route: Direct planner correction; the caller already requires truthful persistence outcomes. No new user decision or general API redesign is necessary.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Existing domain regressions are not a mixed-state closure acceptance test

* Related IDs: exact independent-closure and per-status owner/date criteria; C2/C8/C10; P01-T01; P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md:78-81 requires the mixed state through order completion, quality handover, financial note, case return/reopen and restart, including defects/charge queries. The details at :72-78 enumerate persistence probes and running existing closure suites but do not allocate this combined scenario. src/core/tests/test_resident_decisions.py:660-701 proves response-review behavior and closed-case access, not the proposed remedy. src/core/src/zava_forward/core/quality.py:128-175 retains defect owner/raised date, transition history and separate handover actor/date; src/core/src/zava_forward/core/procurement.py:398-409 records work-order completion separately. Those distinct representations cannot be verified by assuming one generic owner/date field or running their old suites alone.
* Concern: Independent old suites do not contain the new remedy/charge-query objects. The plan lacks an explicit mixed-state assertion and a field-level oracle distinguishing accountable owner, transition actor, original open date and current status date. In particular, an event's recorder must not silently be promoted to the status owner when owner provenance is unknown.
* Impact: Green existing regressions can coexist with a new projection that hides an open item, borrows another domain's owner/date or resets age/original provenance on reopen.
* Smallest useful change: Allocate a grouped semantic scenario in test_resident_decisions.py that carries a Closed response, Open remedy and independently open defect/charge query through the required unrelated transitions and a reopened store. State which canonical field/history supplies each status, owner and date; missing historical evidence remains Unknown. Use existing public domain helpers/fixtures and existing states; do not edit quality.py, procurement/finance semantics or parallel test fixtures. Where mutually exclusive quality states prevent one fixture from representing all transitions, use subcases rather than forcing an impossible lifecycle.
* Action owner: Planning parent for P02-T01 scenario ownership and P01-T01 projection expectations.
* Exact resolving evidence: Synchronized plan/details allocate the scenario within the maximum 18 new semantic methods, with explicit unchanged state/owner/original-date/history assertions for each open item after each unrelated action and restart. Include response-only reopen, remedy-only reopen and independent charge-query progression; assert projections do not substitute the current actor or hide the open records. Existing domain suites remain additional regression evidence, not the sole acceptance proof.
* Decision route: Direct planner correction. This implements the caller's existing criterion without adding full PRD age bands, lease decisions or new quality work.

## Strengths and Residual Risk

* Reusing resident_action, service_requests and resident_update avoids a duplicate closure registry and respects the existing domain boundaries.
* The intentional handoff compatibility change is correctly acknowledged, including amending existing tests instead of deleting them.
* Direct writer-time registry checks, rowversion retention, canonical discard, prior-audit preservation and persistent recovery-read fault injection are already substantive strengths. They should not be replaced by a sequence-only cache check or a second recovery system.
* The plan correctly distinguishes constructed engineering evidence from actual resident/legal authority and operational acceptance.
* Shared-file integration remains a declared coordination risk. The findings do not authorize touching #91/#102 implementation, adopting #92 or inventing issue dependencies.
* Actual SQL/browser/image availability is not established by planning. The candidate's requirement to record unavailable/skipped checks honestly remains appropriate; an unavailable check must not be described as passed.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is required for this finding set.
* No decision-critical external research gap prevents this assessment. The gaps concern converting already-confirmed requirements into executable task/acceptance contracts.
* Do not request broader role policy, source migration or operational authority simply to resolve these bounded planner corrections.

## Limitations

* This is a plan credibility assessment, not implementation review, security audit, accessibility conformance, legal-currentness determination or acceptance of the full PRD.
* No tests, containers, browser sessions, model calls, cloud operations or GitHub mutations were executed for this critique. The research's reported 59-test baseline/one opt-in skip is attributed to research, not rerun or promoted to implementation evidence.
* Only the specified worktree was used. Initial inspection showed the supplied planning/research/state artifacts as untracked and no tracked source modifications; this assessment did not move, stage or alter them.
* No source, plan, phase details, research, state or earlier review record was edited. This critique artifact is the only authored file.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define the legacy confirmation/bootstrap contract, then resolve PC-002 through PC-004 in the same compatible plan/details revision batch, retaining the locked test ownership, maxima and no-removal rule.
* User response required: No.
* Critique is complete. Return this single complete finding set to the parent; do not launch research, implementation, review or a second critique from this task.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md](.copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md) | Assessed final candidate; unchanged |
| [.copilot-tracking/details/2026-10-17/resident-update-remedy-controls-88-phase-details.md](.copilot-tracking/details/2026-10-17/resident-update-remedy-controls-88-phase-details.md) | Assessed task contracts; unchanged |
| [.copilot-tracking/research/2026-10-17/resident-update-remedy-controls-88-research.md](.copilot-tracking/research/2026-10-17/resident-update-remedy-controls-88-research.md) | Supplied evidence and decisions; unchanged |
| [.copilot-tracking/reviews/plans/2026-10-17/resident-update-remedy-controls-88-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/resident-update-remedy-controls-88-plan-critique.md) | Complete single-pass critique and four actionable findings |

## Next Steps

The planning parent can directly revise and disposition PC-001 through PC-004 in one batch without another critique. No user action is required. This critique task stops here and initiates no peer stage.
