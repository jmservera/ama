---
title: Independent Review of RAI release 218 bounded engineering slice
description: One independent post-implementation Review and acceptance boundary.
ms.date: 2026-10-27
---

## Opening Review State

* Goal: assess the complete supplied #218 engineering boundary independently of implementation and original plan critique.
* Scope: three core modules; release/assistant regressions; README, index and log; dated research, plan, phase details, original critique and changes evidence.
* Evidence readiness: supplied artifacts and dirty implementation diff are available; comparison and independent bounded validation are in progress.
* Acceptance basis: credible policy dependency invalidation, preservation of unrelated capabilities and actual approval boundaries, PC001 mapping/order regression coverage, and honest traceability.
* First comparison boundary: reconcile plan, details, critique and changes before tracing the source patch against existing lifecycle behavior.
* Read-only boundary: only this canonical review record may change; no subagents, heavy/full gate, SQLServer, browser, Azure, provider calls or private data.
* Initial blockers: no review blocker identified. Human/evaluator evidence is explicitly outside engineering acceptance and must not be inferred.

## Scope and Evidence

* Task: #218 bounded engineering slice, 2026-10-27, feat/rai-release-218.
* Assessed candidate: working-tree diff against HEAD 0ded682bab690d24eb59b78e704be82d337bf6cd, not a committed or published exact-head candidate.
* Complete tracked boundary: src/core/src/zava_forward/core/assistants.py, src/core/src/zava_forward/core/ai_registry.py, src/core/src/zava_forward/core/quality.py; src/api/tests/test_assistant_release.py, src/api/tests/test_assistants.py; src/core/README.md, docs/reference/README.md, docs/reference/log.md. Twelve added methods; no removals.
* Compared artifacts: .copilot-tracking/research/2026-10-27/rai-release-218-research.md; .copilot-tracking/plans/2026-10-27/rai-release-218-plan.md; .copilot-tracking/details/2026-10-27/rai-release-218-phase-details.md; original .copilot-tracking/plans/2026-10-27/rai-release-218-critique.md; .copilot-tracking/changes/2026-10-27/rai-release-218-changes.md.
* Lifecycle evidence: assistants.py capture/admission/enqueue/claim/dispatch/complete/view/export/review; assistant_release.py selection, recording and supersession; rai_release.py hashing/validation; ranking.py policy hash/description; quality.py checklist dispatch; ai_registry.py retained binding; ai.py dispatch/completion recheck; sqlstore.py release assessment; store.py retained priority generation/view/review.
* Acceptance cross-check: docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-051 to FR-054, AC-069 to AC-073 and OQ-017/018; docs/adrs/0002-pilot-readiness-architecture.md responsible AI control plane. Repository case-study, index, memory and customer context were consulted; memory is not acceptance evidence.
* GitHub approval/issue status is supplied dated evidence, not independently refreshed. No legal-currentness, deployment, semantic-evaluation or live-authority assessment is claimed.

## Execution Status

* Review execution: Complete. This is the one independent post-implementation Review, not a repeat critique or implementation pass.
* Implementation execution: P01/P02 complete within the supplied boundary; P03 remains partial until the parent reconciles this Review and handles publication.
* Review authority: only this canonical record changed; no fixes, issue checkbox edits or delegated work.

## Plan-to-Change Reconciliation

| Scope | Compared evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Nine DependentPolicyRelease methods; supplied failing-first three-method/five-failure record | Reconciled. Actual content, current capture, mapping-only and order-only mutation coverage is present, not merely stored-binding corruption. |
| P01-T02 | Three-module production patch | Reconciled. Canonical current ranking hash binds stock and retained priority; quality owns its checklist/ordered-dispatch fingerprint; stock capture explicitly selects CURRENT. |
| P02-T01 | Three HumanReviewMechanics methods | Reconciled as scripted mechanics only. Valid citations do not establish truth; deliberate false attestation accepts contradictory text without a controlled domain write. |
| P02-T02 | Changes validation table and independent bounded runs below | Reconciled with supplied broad-suite counts, environment skips and final supplemental-test timing disclosed. |
| P02-T03 | Core README, index, append-only log and criterion-level changes tables | Reconciled. All five named children receive evidence/gap dispositions; whole-feature PRD criteria remain Not run. |
| P03-T01/T02 | Unchecked Review/publication markers and handoff | Appropriate at intake. Parent must record this completed Review without treating publication or human acceptance as completed. |
| Follow-Up Items 1-4 | Research, plan, changes and docs | Consistently outside active engineering acceptance, with decisions/actions retained below. |

## Completed Work Assessment

* Dependency invalidation is credible: ranking.policy_hash recomputes content without trusting content_hash; rai_release.digest sorts object keys but preserves sequence order, so checklist items and first-match _KEYWORDS order remain semantic. Only dependent policy_version values change; unrelated assistant and retained-route bindings keep their prior shape/content.
* Existing lifecycle checks consume those bindings at admission, claim, pre-dispatch, completion and reliance. The new tests assert policy_version-specific denials, zero fresh/queued provider calls, in-flight quarantine, retained output history without reliance, and rejection of verify/accept/edit-accept after change. Retained priority also exercises dispatch, completion, historical accept and edit denial.
* Constructed renewal tests exercise the real record path, fresh proposal acceptance without case/control writes, invalidated historical proposals, and denial after rollback to the superseded release. No automatic release renewal is introduced.
* PC-001 is resolved. test_quality_mapping_and_first_match_order_require_release_without_source_change separately adds a mapping and reorders overlapping loft mappings, with fixed checklist definitions/version labels. The generic-case snapshot remains equal while admission specifically reports policy_version mismatch. Every other assistant and retained binding is compared for equality.
* Approval boundaries remain intact: no ranking/checklist rules, role grants, live approvers, controlled domain writers, resident consent paths or authority records change. Existing named-release approver, current-role/scope, quality independence and same-reviewer source-verification checks remain in their original code paths and passed bounded regressions.
* The defect scripts are not detectors or a reviewer study. They deliberately prescribe reject/correct actions. Rejection preserves actor/note/source provenance; correction preserves original/edited output across reopen. The negative control honestly demonstrates why syntactic verification cannot satisfy AC-070.
* No newly introduced source defect or material unaccepted scope divergence was identified in the complete supplied patch.

## Implementation-Time Plan and Detail Update Assessment

| Update | Evidence and rationale | Assessment |
| --- | --- | --- |
| PC-001 applied to P01-T01/details | Original critique requires independent mapping/order mutation and unchanged-source control | Compatible correction, explicitly dispositioned before implementation; original Revise verdict preserved. No new human decision or second critique needed. |
| Quality-owned helper | P01-T02 allows shared helper; quality.policy_fingerprint hashes definitions and dispatch | Within planned architecture; avoids duplicating private mapping knowledge in assistants. |
| Two supplemental methods | Changes records declared-hash and retained-priority review checks added after broad discovery began | Within twelve-method ceiling; independently reran all twelve final methods. Broad discovery alone is not claimed to cover these final additions. |
| No heavy/full gate | Plan, details and caller explicitly prohibit/decline it | Disclosed limitation, not a pass, waiver or fabricated receipt. Publication controls remain separate. |

## Critique and Material Revision Assessment

* Exactly one original critique: Revise, PC-001 Medium. Its disposition is supported by final code/tests and the independent twelve-test run.
* No material direction change, evaluator implementation, unapproved manifest adoption or human-authority substitution appears in the patch.
* The supplied chronology records correction before implementation. This Review did not reconstruct historical worktree states or independently replay failing-first tests.
* No second Review is requested after routed follow-up work.

## Plan Follow-Up Assessment

| Item | Why outside immediate scope | Owner/action and route |
| --- | --- | --- |
| 1: #421/#222 manifest | Corrected proposal is not an approved oracle; lawful fields, thresholds and sufficiency are unapproved | Owner approves/version-controls manifest and OQ-018 decisions before distinct #222 evaluator work; RV-001. |
| 2: OQ-017, #223, #221 | Real appointments, competent participants and witnessed acceptance cannot be supplied by code fixtures | Sponsor/competent task, Assurance, Safety and DPO/Legal functions establish authority and approved protocols; distinct human effectiveness/drill work; RV-002. |
| 3: wider #220 coverage | Existing retained-priority challenges do not establish assistant/form coverage | Product/control owner scopes distinct #220 delivery; RV-003. |
| 4: #224/#440 | Separate legal-screening and stabilization dependencies, not this patch | Respective issue owners retain distinct delivery/acceptance; RV-003. |

These are pre-existing planned follow-ups, not newly discovered implementation defects or additions to active P01/P02 scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Cohort/evaluator acceptance remains blocked by actual approval

* Evidence: plan Follow-Up Item 1; research W2; changes #222 matrix; PRD AC-073/OQ-018.
* Impact: no approved oracle, cohort/threshold decisions or evaluation results support #222 completion or fairness claims. This is a pre-existing acceptance dependency, not a source regression.
* Destination: distinct #222 follow-up, owner and competent Data/Resident Engagement/DPO/task functions.
* Next action: approve the corrected versioned #421 manifest and required decisions before evaluator implementation. Do not substitute scripts or invented thresholds.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Scripted oversight and restart mechanics are not human effectiveness or authority

* Evidence: test_assistants.py HumanReviewMechanics, especially the accepted false-attestation negative control; changes #223/#221 matrices; plan Follow-Up Item 2; PRD AC-070/AC-072/OQ-017.
* Impact: real reviewer competence, critical-defect detection, paired workflow-only effort, distinct restart authority and witnessed drill acceptance remain unproved. Existing role names and synthetic actors cannot authorize live use.
* Destination: distinct #223 and #221 human-acceptance follow-ups under named competent owners.
* Next action: establish appointments and approved participant/drill protocols, then collect actual evidence separately. This was planned residual work, not a new code defect.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Broader challenge coverage and epic dependencies remain open

* Evidence: plan Follow-Up Items 3-4; changes #220 matrix and epic closure section; core README limitations; PRD AC-071.
* Impact: retained-priority challenge regressions cannot demonstrate assistant/form coverage or close #220/#218; #224/#440 are not delivered here.
* Destination: distinct #220, #224 and #440 issue owners.
* Next action: deliver and accept their remaining scopes independently; use Refs only and leave acceptance checkboxes unchanged.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Publication readiness is not established by this dirty-tree assessment

* Evidence: P03-T02 remains unchecked; candidate is uncommitted; full local gate was expressly disallowed and no external receipt is supplied; hosted/owner approval is not evidenced.
* Impact: bounded test success and this Review cannot certify final exact-head publication, satisfy required gate policy or authorize merge/live activation. This is a known publication constraint, not a newly introduced source defect.
* Destination: distinct parent/owner publication-control action.
* Next action: retain the no-gate evidence limitation and resolve applicable publication prerequisites with the owner without running the prohibited gate, inventing a waiver/receipt, weakening controls or changing this Review's outcome. Any authorized PR must be evidence-qualified and Refs-only.

## Defects and Routed Findings

* Newly introduced implementation defects: none identified.
* Decision divergence requiring rpi-plan: none identified.
* Missing engineering research requiring rpi-research: none identified.
* RV-001 to RV-004 route only to the distinct follow-ups above; no later rpi-implement invocation is needed for this assessed patch.

## Validation Evidence

Independent commands used the supplied session venv, disabled bytecode writes and redirected unittest fixture scratch paths into the repository review directory through TMPDIR; fixtures cleaned up afterward. No private working data or real provider was used.

| Evidence | Status | Result and boundary |
| --- | --- | --- |
| From src/api: PYTHONPATH=tests:../core/tests:../agents/tests /home/azureuser/.copilot/session-state/2d83818b-bc33-4b41-8223-77363e84904f/files/venv/bin/python -m unittest test_assistant_release.DependentPolicyRelease test_assistants.HumanReviewMechanics -q | Independently passed | 12 tests, 4.134s, no skips. Final supplemental tests included. |
| Same Python/paths: python -m unittest test_assistant_release.Release test_assistant_release.Legacy test_assistants.ReviewTests test_assistants.ContractTests.test_every_capability_reactive_verified_edit_reject_domain_unchanged test_assistants.ContractTests.test_exact_source_role_matrix_and_no_cross_audience_leaks -q | Independently passed | 25 existing tests, 8.073s, no skips; release permissions, actual/constructed distinction, lifecycle and review independence. |
| git diff --check | Independently passed | No tracked-patch whitespace errors. |
| Initial new-test attempt from repository root | Failed invocation, corrected | Two module-import errors, no behavior tests executed. Repeated once from documented src/api directory with the passing result above; not a product defect. |
| Failing-first reproduction | Supplied, not independently replayed | Three methods/five assertions failed before fix, as recorded in changes; current tests and source support the claimed gap. |
| Integrated release/oversight/incident/challenge | Supplied passed with skips | 166 run, 37 skipped; not independently rerun. |
| Full core / API / agents suites | Supplied passed with skips where applicable | Core 1429/186 skipped; API 1131/314 skipped; agents 105 passed. Final supplemental methods are independently covered above, not retroactively included in these counts. |
| Ruff, format and mypy, all three components | Supplied passed | Not independently rerun; supplemental API tests reported Ruff-clean. |
| Full/scoped heavy gate; SQLServer/browser/Azure/paid/provider/live-human checks | Not run | Explicit boundary/prohibition; no receipt, environment parity, effectiveness or operational acceptance inferred. |

## Outcome

* Review execution: Complete.
* Outcome: Residual work.
* Rationale: the bounded engineering patch is conformant on inspected source and independently passing regressions; no introduced code defect was found. The complete supplied acceptance boundary intentionally retains the substantive human/evaluator/coverage/publication work in RV-001 to RV-004. These residuals do not invalidate the binding correction, but prevent child/epic completion and release-readiness claims.
* Severity summary: Critical 0, High 0, Medium 4, Low 0; all four are retained follow-up/control limitations, not new implementation defects.
* Publication recommendation: source patch is suitable for consideration as a narrowly qualified Refs-only engineering PR, not Closes or whole-feature acceptance. Final publication, required checks and merge remain subject to applicable owner gates; this Review supplies neither a gate receipt nor authorization to bypass them. No live release is approved.
* Active review blockers: none. Broader acceptance/publication constraints remain as routed above.

## Closeout Routing Record

| Finding class | Destination | Next owner/action |
| --- | --- | --- |
| Implementation defect | None | No source correction requested. |
| Significant decision divergence | None | No plan revision requested. |
| Material engineering research gap | None | No research rerun requested. |
| Planned residual work | Distinct #222, #223/#221, #220/#224/#440 and publication follow-ups | Owners act on RV-001 to RV-004; parent preserves original outcomes and honest acceptance traceability. |

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/rai-release-218-research.md](.copilot-tracking/research/2026-10-27/rai-release-218-research.md) | Dependency and acceptance evidence. |
| [.copilot-tracking/plans/2026-10-27/rai-release-218-plan.md](.copilot-tracking/plans/2026-10-27/rai-release-218-plan.md) | Current bounded plan and follow-ups. |
| [.copilot-tracking/details/2026-10-27/rai-release-218-phase-details.md](.copilot-tracking/details/2026-10-27/rai-release-218-phase-details.md) | Reconciled implementation details. |
| [.copilot-tracking/plans/2026-10-27/rai-release-218-critique.md](.copilot-tracking/plans/2026-10-27/rai-release-218-critique.md) | Original Revise verdict preserved. |
| [.copilot-tracking/changes/2026-10-27/rai-release-218-changes.md](.copilot-tracking/changes/2026-10-27/rai-release-218-changes.md) | Supplied tests and criterion-level gaps. |
| [.copilot-tracking/reviews/logs/2026-10-27/rai-release-218-review.md](.copilot-tracking/reviews/logs/2026-10-27/rai-release-218-review.md) | This one independent Review. |

## Next Steps

The active parent should reconcile P03 with this original Review, retain RV-001 to RV-004 as distinct follow-ups, and leave all whole-issue acceptance claims open. Resolve owner publication controls before proceeding; any authorized PR is Refs-only. No second Review, full gate, evaluator implementation or human-acceptance claim is authorized by this record.
