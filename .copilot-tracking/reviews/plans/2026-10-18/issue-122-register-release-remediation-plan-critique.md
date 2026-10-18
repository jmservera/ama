---
title: Issue 122 register and release remediation final-candidate plan critique
description: Single independent critique of the new owner-authorized bounded RPI plan
ms.date: 2026-10-18
---

## Metadata

* Task ID: issue-122-register-release-remediation.
* Critique date: 2026-10-18.
* Plan: .copilot-tracking/plans/2026-10-18/issue-122-register-release-remediation-plan.md.
* Phase details: .copilot-tracking/details/2026-10-18/issue-122-register-release-remediation-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate critique; no second pass, implementation, delegation, commit, integration or remote mutation.
* Output: .copilot-tracking/reviews/plans/2026-10-18/issue-122-register-release-remediation-plan-critique.md.

## Inputs and Criterion Boundary

The caller authorizes a NEW full RPI loop for both coordinator findings, not a
third historical correction. The prior independent Not accepted remains adverse
historical evidence. This critique assesses planning credibility, not a corrected
implementation or release acceptance.

Read the exact supplied inputs:

* .copilot-tracking/research/2026-10-18/issue-122-register-release-remediation-research.md.
* .copilot-tracking/research/2026-10-18/issue-122-register-release-remediation-coordinator-evidence.json, including both original message contents, event IDs, timestamps, exact reviewed head/base and completion boundary.
* The plan and phase details identified above.
* Relevant existing source and tests identified below, plus the required case-study, KB index/memory and component-guide context.

The coordinator's exact evidence concerns High register disclosure to Programme
Support Officers and Quality Inspectors, and Medium false completeness for an
unreferenced release exported with event_limit=0. The original completion message
explicitly says Complete / Not accepted with both historical correction cycles
exhausted. Neither research readiness nor this new planning assessment replaces
that verdict.

The decision boundary includes the production-only continuity.py restriction,
task-owned continuity tests, additive documentation, unchanged projection policy
and canonical evidence, same-document mutation responses, every retained release,
unsupported versus absent evidence, externally held heads, genuine API-constructed
positive histories, no test removals and at most 12 new semantic test methods.
No shared fixture, server/web, queue, procurement, schema or release-writer
implementation change is authorized.

Read-only local Git inspection confirmed:

| Reference | Observed full hash |
| --- | --- |
| Current branch fix/continuity-epoch-export-122 HEAD | 1144647c8d539716e8ddddf9daa47407c9bd00ac |
| Local origin/fix/continuity-epoch-export-122 tracking reference | 1144647c8d539716e8ddddf9daa47407c9bd00ac |
| Local origin/main tracking reference | 9c648b2006e8b2e563823ea7d5aabdf7f1ac7096 |

These are local references, not a fresh remote lease check. The planned exact-base
integration remains a prerequisite BEFORE implementation. This critique neither
performs nor waives it. The existing dirty paths were the five new task artifacts;
no existing work was moved, staged or rewritten.

Input byte identities captured before authoring:

| Input | SHA-256 |
| --- | --- |
| Research | 6f8310cd5eb59cb1045ca25bf9064904b68fe80dae69988d7321940d14f68b5f |
| Coordinator evidence JSON file | cbfad85c175ea333bced57c6567fa35ce8f80424a6b3428354eec5cd040edc88 |
| Plan | ef6331d9aa3cca8fa7583d886298cf5eae9cacffe8480a0f7602bbee78a959d0 |
| Phase details | fa986a7bb6770fbd7a408d0f424612d953a30d21cc491895dbf0d3c83c4993ff |

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| New authorization and frozen historical Not accepted; C1/C6 | Covered | Task separation and historical preservation are explicit; no extra historical correction is proposed. |
| P01-T01 exact-base integration and ownership | Covered | Exact base, expected old head, conflict stop, upstream parity and historical hash checks are specified. |
| C2; P02-T01 recorded-need register and mutation privacy | Partial | Correct existing policy and closed-summary approach; field/operation acceptance contract remains incomplete, PC-004. |
| C3/C4; P02-T02 every retained release | Partial | Per-record traversal is explicit, but reachable shape-validation order and lifecycle semantics need PC-001/PC-003. |
| C3; P02-T02 source completeness | Partial | Required distinction is stated but unchanged JSON producer and missing SQL release-source behavior are not reconciled, PC-002. |
| Canonical heads, full/limited proof and unanchored rewrite limits | Covered | No canonical redaction, no full proof for limited exports, reference checks and authenticity caveat retained. |
| C5; P01-T02/P03-T01 positive and negative test ownership | Partial | Correct intention, but all inherited bare records and existing manually fabricated lifecycle setup require an explicit migration map, PC-005. |
| P03-T01 local SQL, installed hardened image and static checks | Covered with dependency | Existing owned SQL adapters and runtime boundaries are named; fresh results remain future work, dependent on corrected test setup. |
| P03-T02/P03-T03 single Review and publication boundary | Covered | One new original Review, draft/Refs-only publication and subsequent independent coordinator review; no self-acceptance or merge. |
| Human authority, resident/manual/hazard boundaries | Covered with residual limits | Required IDs/status need PC-004; operational authority, Azure and old-image gates remain unmet rather than waived. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 0 High, 5 Medium, 0 Low actionable planning findings.
* Rationale: The selected remedies and scope are sound. Five source-grounded design/validation gaps leave credible paths to either exceptions or success-shaped defaults, rejection of legitimate lifecycle evidence, loss of permitted operation context, and misleading full-proof fixtures. These are direct planner corrections within already confirmed direction, not new owner decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Validate raw source shapes before producer normalization and reference traversal

* Related IDs: C3; P01-T02; P02-T02; functional requirement for explicit malformed-evidence problems.
* Evidence: .copilot-tracking/details/2026-10-18/issue-122-register-release-remediation-phase-details.md:52-60 promises validation before indexing. In src/core/src/zava_forward/core/continuity.py:274-313, continuity_export first calls assistants.get, indexes proposals/total, converts proposal members, dereferences proposal capability and replaces a falsey task_releases value with an unavailable default. In continuity.py:418-459, release_problems dereferences proposal envelope/provenance, AI-record envelopes, release metadata and record IDs before comprehensive shape guards.
* Concern: Validation only before the release index is too late. Values such as task_releases=[], null, false or an empty object can be normalized away; nonempty scalar/list metadata, records=[null], unhashable IDs, non-list events, or scalar nested envelope/provenance members can raise before a problem is recorded. Existing proposal-metadata tests principally exercise the serialized verifier, not those producer entry paths. The broad plan requirement does not specify how both reachable paths satisfy it without hiding malformed input.
* Impact: Moving lifecycle checks into the record loop can leave malformed source inputs falsely acceptable when unreferenced, or turn the export endpoint/offline verifier into an exception path rather than an explicit incomplete/invalid result.
* Smallest useful change: Expand P02-T02 with a raw-input validation order that precedes producer coercion/defaulting and all reference/event dereferences. Distinguish missing from falsey malformed values. Define minimum dictionary/list/member/string-ID types before hashing/indexing, including unreferenced record/snapshot/event association. Preserve explicit nonsensitive problems rather than silently turning malformed evidence into empty evidence. Limit guards to the source and relationship structures this task traverses.
* Action owner: Planning parent, then continuity implementation owner.
* Exact resolving evidence: Revised details name the early producer and verifier guard sites. A bounded parameterized matrix exercises missing/null/scalar/list/object source values, malformed collection members, unhashable IDs, nested envelope/provenance shapes, exact boolean/count types, nonfinite/boolean timestamps and malformed event bodies through BOTH production and serialized verification. Producer results are explicitly incomplete and verifier results invalid with nonempty problems, without exceptions. Serialized negatives recompute the ordinary digest/complete flag and retain the separately copied unchanged ledger head.
* Decision route: Direct planner correction. No significant or divergent user decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Specify unsupported JSON release-source semantics separately from missing SQL evidence

* Related IDs: C3/C4; P02-T02; known-empty/unsupported/absent source acceptance criteria.
* Evidence: src/core/src/zava_forward/core/assistants.py:525-529 returns explicitly unsupported empty proposal evidence for JSON but NO task_releases key. Its SQL return at assistants.py:548-561 includes supported task-release metadata even when empty. continuity.py:296-298 currently synthesizes an unavailable release source for a missing/falsey value. continuity.py:445-449 requires support only when references exist. src/api/tests/test_continuity.py:226-245 expects the real JSON path to verify, whereas test_continuity_epoch_export.py:620-631 changes proposal metadata on an SQL-derived bundle rather than exercising the actual JSON release-source shape.
* Concern: The plan requires absent sources to reject and genuine unsupported JSON to remain usable, but P02-T02:59-60 does not define the normalization/serialized contract that makes both possible without editing Assistants.export. Requiring task-release metadata unconditionally rejects the existing legitimate JSON path; permitting an absent release source whenever references are empty repeats the completeness blind spot for SQL.
* Impact: The implementation can either regress supported JSON-store operation or certify unknown/missing release evidence as complete. A fabricated unsupported note or zero records alone must not excuse contradictory known evidence.
* Smallest useful change: Record a source decision table for producer AND verifier: supported/available SQL with a known-empty complete collection; missing/unavailable/malformed SQL release source even without references; positively identified unsupported JSON with no known release records/references; and unsupported declarations contradicted by records, counts or references. Define the emitted task-release representation and scope statement for the actual JSON path within continuity.py, without requiring new fields from the out-of-scope writer or conflating source-scoped unsupported evidence with audience-limited export.
* Action owner: Planning parent, then continuity implementation owner.
* Exact resolving evidence: Revised P02-T02 specifies accepted and rejected serialized states, including how genuine JSON absence becomes explicit unsupported-source evidence rather than generic unavailable evidence. Tests invoke the unchanged Assistants.export JSON branch and a real JSON Store; an empty supported SQL export remains valid, missing SQL release metadata rejects without proposals, contradictory unsupported claims reject, and limited audience bundles still cannot prove the full ledger.
* Decision route: Direct planner correction implementing current requirements; no user policy decision or production-scope expansion.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Define a lifecycle validator compatible with repeated suspension and timestamp ties

* Related IDs: C3/C4; P02-T02; unreferenced active/suspended/revoked positives and status/order negatives.
* Evidence: src/core/src/zava_forward/core/assistant_release.py:116-139 records a release, permits active or already suspended records to change to suspended or revoked, increments revision for repeated suspension, and stores random UUID event IDs with the supplied clock value. src/core/src/zava_forward/core/assistants.py:551-556 serializes events ORDER BY at,id, not insertion sequence. P02-T02:56-58 requires a consistent sequence and acknowledges same-time events but supplies no executable ordering rule or repeated-suspension acceptance case.
* Concern: Requiring release-recorded to be array-first or requiring strictly increasing times rejects legitimate events sharing a timestamp, because UUID ordering can place a subsequent event first. Treating suspension as allowing only one event rejects the writer's repeated-suspension path. Conversely, checking only one initial event and a matching latest status can accept impossible histories such as a strictly later suspension after revocation or a recording event later than its state changes.
* Impact: A completeness fix can reject real API-produced retained histories, or continue certifying contradictory histories. An invented strict ordering would claim evidence not present in the persisted schema.
* Smallest useful change: Define the allowed state transitions, including active -> suspended, suspended -> suspended, active/suspended -> revoked and no transition out of revoked. Specify what timestamps establish and what ties cannot establish. For tied events, validate a permissible ordering consistent with the retained evidence/current status rather than treating UUID lexical order as chronology; do not add a sequence schema or claim authenticated historical order. Apply initial-event task/identity consistency independently of proposal references.
* Action owner: Planning parent, then continuity implementation owner.
* Exact resolving evidence: Revised details state the transition/tie rule. Real record_release/change_release positives include active, repeated suspension, suspension then revocation, automatic supersession and fixed-clock equal timestamps with adversarial UUID ordering. Negatives include duplicate/missing initial events, mismatched initial task, an initial event strictly later than a state change, a strictly later event after revocation and an impossible final status. Every case is tested unreferenced, serialized and checked against the unchanged separately retained head.
* Decision route: Direct planner correction constrained by the existing writer; no significant user decision.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Lock the limited register and mutation operation contract, not just a generic summary

* Related IDs: C2; P02-T01; required human IDs/status/communication-sent acceptance.
* Evidence: src/core/src/zava_forward/core/continuity.py:146-157, 177-200, 222-239 and 257-266 return persisted suspension/change records or derived register structures. continuity_view includes effective_versions keys containing arbitrary subjects and values containing declared versions. The existing limited_export summary at continuity.py:339-349 has no operation IDs and recognizes suspension/proposal states, not change statuses Applied/Blocked/Reversed. src/api/src/zava_forward/api/server.py:839-842 serializes each of the five continuity mutation returns directly. P02-T01:42-47 names a shared summary and safe fields but does not enumerate per-operation or derived top-level outputs.
* Concern: A generic record helper can omit required IDs, proposal/decision state, change reversal relationships or change statuses; preserving records while overlooking effective/suspended derived structures can instead leak subjects/versions or unexpected nested text. The plan's test statement does not explicitly bind each mutation return and its operation lifecycle to the limited field contract.
* Impact: Privacy can remain bypassable through an overlooked response structure, or a limited Programme Support Officer/Quality Inspector can lose the safe references and state needed to complete permitted human controls. Passing GET canary tests alone proves neither property.
* Smallest useful change: Add a field-level allowlist for the register root/derived structures and suspension, restart-proposal/decision, change and reversal responses. Specify ID/link fields, registered scope/task values, all applicable enum states, epoch and proposal-presence/decision indicators, communication.sent and applicable affected counts/truncation. Hold arbitrary names, subjects, versions, reason/evidence/reference text and unknown nested fields; do not copy free text merely because it is under an ID/status-like key. Do not reuse the export-only summary unchanged or broaden its proof claims.
* Action owner: Planning parent, then continuity implementation owner.
* Exact resolving evidence: A response contract in revised P02-T01 and task-owned HTTP assertions for suspend, restart-propose, restart-decide including Keep suspended and Restart, change and change-reverse. Limited actors use returned safe IDs/epochs to finish their permitted workflows; known status/communication flags remain usable. Canaries cover arbitrary nested fields and effective subject/version keys, both override directions, and existing denied roles. Full readers retain canonical control fields; snapshots of persisted control documents prove response projection does not redact storage or alias-mutate it.
* Decision route: Direct planner correction. Existing owner direction already settles policy and human-operation preservation.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Account for every inherited bare fixture in full-proof test setup

* Related IDs: C5; P01-T02; P03-T01; Test Ownership Lock.
* Evidence: src/api/tests/test_assistants.py:94-98 installs shared releases in every Base setup. src/core/tests/release_support.py:45-62 directly inserts multiple releases with revision=1 and no release-recorded events. Creating another release through the API revokes an active prior fixture but does not create its missing initial history. OfflineTests.bundle at src/api/tests/test_continuity_epoch_export.py:419-434 and the full HTTP proof at :653-705 create one genuine lifecycle while retaining those other bare releases. The existing legacy positive at :600-616 manually inserts a release-recorded event after direct fixture installation. Full-proof tests in test_continuity.Changes also inherit the bare records.
* Concern: The plan correctly requires genuine positives but does not identify how task-local setup replaces ALL retained bare records before a full-proof assertion. Merely adding a genuine lifecycle for the referenced release is insufficient under the new every-record rule. The existing manual event insertion directly conflicts with genuine-through-APIs positive setup. A broad setup conversion without explicit negative isolation could erase the required absent-history controls.
* Impact: Correct production validation makes existing full positives fail; expedient synthetic backfilling, record omission or relaxed assertions could then make the suite green without proving the intended behavior. The unallocated 12-method budget also leaves no auditable completeness check for the added matrix.
* Smallest useful change: Add a test-local setup migration map for the two owned modules. Identify every full-proof consumer, remove/replace inherited bare records only in those isolated synthetic positive stores BEFORE API lifecycle construction, and construct every retained positive record through record_release/change_release. Replace the manual lifecycle-event insertion. Keep separate explicit negative cases using untouched bare shared fixtures; never modify the shared installer, retrofit production histories or discard exported records. Map new semantic methods/subtests to requirements and show the total remains <=12 with zero removals.
* Action owner: Planning parent, then task-owned test implementer.
* Exact resolving evidence: Revised P01-T02/P03-T01 names the affected Changes, OfflineTests and HttpTests setup consumers, legacy setup and MSSQL inheritance path. The resulting ownership inventory has zero removed methods and <=12 added semantic methods. Each complete-proof bundle contains only retained records constructed via release APIs with genuine lifecycle events; bare-fixture tests explicitly assert incomplete/invalid rather than silently losing fixtures. Focused SQLite and inherited owned-MSSQL executions preserve the existing atomicity/epoch/privacy assertions. Exact commands, heads, pass/skip/failure counts and source/test hashes are recorded for the installed host and image.
* Decision route: Direct planner correction within the authorized test files; no user response or shared-fixture change.

## Strengths and Residual Risk

* Both actual coordinator findings, including the same-document mutation bypass, are in scope. The plan does not substitute route denial, role-policy expansion, narrative pattern filtering or canonical evidence redaction.
* Per-retained-record validation is correctly separated from proposal/legacy reference resolution. Digest/version/task/active-snapshot checks must remain in that separate resolution path.
* The exact main integration is correctly gated before source implementation, with source-conflict stop conditions, upstream parity, additive documentation reconciliation and frozen historical artifacts.
* Full ledger heads remain canonical. Audience-limited exports remain explicitly incomplete and unverifiable as full proof even if ordinary digest/completeness fields are recomputed.
* An externally retained application-ledger head detects what that ledger binds. It does not authenticate a wholly rewritten, internally consistent unanchored release history; no finding asks the implementation to claim otherwise.
* No local evidence here satisfies genuine OQ-017 authority, witnessed drills, immutable external Azure-head custody, Azure SQL drills or enforceable pre-gate-image exclusion. Those operational gates remain unmet.
* Research contains original-head reproductions. When adding red regression controls after P01 integration, record their actual integrated head separately; do not relabel a post-integration test execution as an original-head execution. Preserve the supplied original-head evidence distinctly.

## Questions or Blocking Evidence Gaps

No unresolved owner decision is necessary to resolve PC-001 through PC-005.
Existing direction already establishes the privacy policy, authorized branch/base,
source boundary, test ownership and genuine-evidence standard. The planner must
resolve implementation-contract gaps directly, not request scope expansion or
another critique.

## Limitations

* This is a source-grounded plan assessment, not implementation verification. No application tests, HTTP probes, SQL containers, image builds, lint/type checks or live inference were executed in this critique.
* Source reads were bounded to continuity production/verification, release writing/export, recorded-need policy, direct API response routing, shared fixture construction and the two owned test modules plus their inherited setup. No open-ended web/repository audit or private data inspection was performed.
* Original coordinator runtime results were read as supplied exact evidence, not claimed as independent executions by this critic. The source JSON file hash above differs intentionally from its two embedded message-content hashes.
* Tracked working/index diffs were empty before writing this artifact. Historical records, supplied research, plan, phase details and state were not edited. All planned validation and final acceptance remain future work.

## Recommended Next Action

* Highest-impact finding: PC-001, because validation after producer dereference/defaulting cannot guarantee the promised explicit fail-closed results.
* Action owner: Planning parent.
* Smallest next action: Directly revise P02-T02 with pre-normalization guards and the source/lifecycle decision tables, then reconcile P02-T01 and task-local setup/test ownership with PC-004/PC-005.
* User response required: No.
* Handoff: Return Complete / Revise to the active planning parent. Resolve this complete finding set directly and finalize planning without another critique. Do not implement before exact-base integration, overwrite the prior Not accepted or start an extra historical correction.

## Relevant Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-18/issue-122-register-release-remediation-research.md](.copilot-tracking/research/2026-10-18/issue-122-register-release-remediation-research.md) | New bounded research and source pointers. |
| [.copilot-tracking/research/2026-10-18/issue-122-register-release-remediation-coordinator-evidence.json](.copilot-tracking/research/2026-10-18/issue-122-register-release-remediation-coordinator-evidence.json) | Exact original findings and adverse completion evidence. |
| [.copilot-tracking/plans/2026-10-18/issue-122-register-release-remediation-plan.md](.copilot-tracking/plans/2026-10-18/issue-122-register-release-remediation-plan.md) | Assessed final-candidate plan, unchanged. |
| [.copilot-tracking/details/2026-10-18/issue-122-register-release-remediation-phase-details.md](.copilot-tracking/details/2026-10-18/issue-122-register-release-remediation-phase-details.md) | Assessed task design and validation details, unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-122-register-release-remediation-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-122-register-release-remediation-plan-critique.md) | This single Complete / Revise critique. |

## Next Steps

Active planning parent: resolve PC-001 through PC-005 directly in the new plan and
phase details, preserve historical artifacts and this critique unchanged, and
finalize without a second critique. No user action is required. This independent
critique stops here; it does not invoke implementation, Review or publication.
