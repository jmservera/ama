<!-- markdownlint-disable-file -->
# RPI Plan Critique: hazard-referral-controls-85

## Metadata

* Task ID: hazard-referral-controls-85; issue #85.
* Critique date: 2026-10-17.
* Plan: .copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/hazard-referral-controls-85-phase-details.md
* Critique execution status: Complete.
* Execution boundary: one independent final-candidate assessment; no nested agents, source edits, plan edits or state edits.

## Inputs and Criterion Boundary

* Caller requirements: automatic ordered RPI; preserve the four already basic-delivered criteria; correct unregistered/stale actors, case-only independent-release bypass and failed-save success audit. Preserve manual intake, external service categorisation, clocks and closure, and stock/provider/finance hooks.
* Supplied research: .copilot-tracking/research/2026-10-17/hazard-referral-controls-85-research.md, including C1-C12 and its reported counterexamples against b5d4c840.
* Supplied candidate: plan and phase details above, including P01-T01, P02-T01 and P03-T01.
* Bounded executable evidence inspected: src/core/src/zava_forward/core/change_provenance.py; hazard methods and staff lookup in src/core/src/zava_forward/core/workflows.py; save, discard, synchronization and lock-exit paths in src/core/src/zava_forward/core/sqlstore.py; JSON save/audit paths in src/core/src/zava_forward/core/store.py; existing decision-scope pattern in src/core/src/zava_forward/core/stock.py; transaction adapter in src/core/src/zava_forward/core/mssqlstore.py; src/core/tests/test_hazard_referral.py; src/api/tests/test_hazard_api.py; opening harness/factory definitions in src/api/tests/test_mssqlstore.py; configured check declarations in the core/API pyproject.toml files.
* Project context: original case study, bounded addendum and knowledge-base index, owner memory and housing-association primer. Memory was treated as context, not evidence. No legal-currentness assessment was performed.
* Decisions and dependencies: reuse canonical `_actor` and a hazard-owned module, one additive SQL validator hook, no quality.py or finance.py changes, no fixture redesign or copied generated suite. P02 depends on P01; P03 depends on P02. No new issue dependency is justified.
* Acceptance boundary: unchanged four-criterion journey; trustworthy current identities and historical independence; durable failure evidence; canonical JSON/SQLite semantics and actual task-owned loopback MSSQL parity; configured ruff/format/mypy and relevant existing regressions.
* Test ownership: retain all existing tests, at most 12 new semantic methods and at most three harness adapter methods. Findings below must fit that budget through parameterized/subtest cases and canonical reuse.
* Review/publication boundary: one independent implementation Review, at most two authorized correction cycles, no parent self-verification relabelled as independent Pass; owned commits, normal push and main-targeted PR only. No merge, issue closure, private data, other worktrees, Azure, legal activation or communications.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Criterion 1: create/link to existing hazard service | Covered | Existing raise/refer methods and closed-record/manual-intake regression are retained, not replaced with a second service workflow. |
| Criterion 2: separate sent, receipt and acceptance | Partial | Existing sequence, immutable history and sender follow-up are covered; current referral-destination validation needs the explicit commitment in PC-001. |
| Criterion 3: accountable home hold and independent release | Covered | Fixed case/home scope, independent email/code/nonempty-OID comparison, historical identities and eligible independent happy path are specified. Existing progression/sibling/consent/building gates remain regression obligations. |
| Criterion 4: visible external response/resident-update times | Covered | Existing four timing observations, unknown values, post-release observation and external service ownership are retained; no clock calculation or UI change is planned. |
| C6/C8/C12: current actor and alias defects; P01-T01 | Partial | Canonical actor and independent identity strategy is credible. Recipient is a separate authority subject, not established merely by checking the caller; PC-001. |
| C7/C12: failed-save audit; P01-T01 | Partial | SQL quarantine is explicit, but JSON's separate audit file and eager SQL discard require backend-specific details and acceptance evidence; PC-002 and PC-003. |
| P02-T01: SQL parity and failure probes | Covered with revisions | Actual isolated loopback MSSQL, canonical semantic reuse and nonportable SQLite trace separation are required. Add the finding-specific assertions without a copied suite. |
| P02-T01: fixture and documentation integrity | Covered | No dataset.py edit expected; exact-hash validation and conditional refresh preserve provisional eleven-profile/nine-workflow authority. Core/API contracts, existing synthesis/index/log are named. |
| P02-T01: checks and evidence | Covered | Relevant regressions, configured lint/format/types, actual command counts, failed attempts and skips are required. No browser claim is made without web changes. |
| P03-T01: independent Review, corrections and publication | Covered | Single independent Review, preserved adverse findings, authorized bounded corrections, privacy-safe commit identity and exact final head/PR are specified. |
| Exclusions and human/service boundaries | Covered | No new operational delegation, actual receipt verification, categorisation, clock ownership, hazard closure, real approval or legal acceptance is inferred. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 2 High, 1 Medium, 0 Low.
* Rationale: the architecture and scope are credible, but three source-backed execution gaps could leave false referral authority or false/erased audit evidence while apparently satisfying the broad acceptance bullets. They are direct planning corrections within the authorized scope, not reasons to reopen business or legal decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Bind the referral destination to fresh authority, including at SQL commit

* Related IDs: C3, C6, C7, C12; current destination requirement; criterion 2; P01-T01; P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md:51-56 requires current caller and destination, but only explicitly promises SQL revalidation of the mutation's registered identity. .copilot-tracking/details/2026-10-17/hazard-referral-controls-85-phase-details.md:22-36 describes a context retaining current actor and independent identities, without naming a destination validation subject. src/core/src/zava_forward/core/workflows.py:151-157 resolves `_staff_person` from cached `store.staff`; `refer_hazard` resolves that destination before its case lock. src/core/src/zava_forward/core/sqlstore.py `_sync` only initially populates staff when the cache is empty. src/core/src/zava_forward/core/change_provenance.py `_actor` is the available fresh SQL lookup.
* Concern: checking the caller through `_actor` does not prove that a different nominated recipient is still registered or still has an eligible safety role. An implementation that retains the existing destination lookup and merely adds caller/release validation can refer to a removed or changed recipient even with a fully current caller. The same gap exists if the recipient is checked once but changes before the writer transaction.
* Impact: a durable Sent record can assign accountability to stale staff; receipt/acceptance can then be impossible or associated with a recycled staff code. This undermines the plan's current-designated-staff requirement.
* Smallest useful change: explicitly add the referral destination as a validation subject in the hazard context. Resolve it from current registered evidence through canonical `_actor` reuse, check its eligible role, and repeat that validation under the existing SQL writer transaction before committing the referral. Specify receipt/acceptance binding against persisted destination identity rather than code alone; do not build a new authority registry or alter delegation policy.
* Action owner: planning parent for P01-T01/P02-T01 revision; implementer for the resulting named validation subject.
* Exact resolving evidence: revised details name caller versus destination checks and transaction placement. Canonical subtests use a valid unchanged caller while the target is removed, loses its eligible role or is replaced under the same code, both before invocation and between precheck and SQL save. SQLite and actual owned MSSQL results show refusal, unchanged durable referral/history/audit, and a subsequent valid recipient journey. These cases must not pass merely because the caller was rejected.
* Decision route: direct planner correction. The user already requires current designated staff; no significant or divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Define JSON failure ordering instead of treating SQL quarantine as cross-backend proof

* Related IDs: C3, C4, C12; failed-save success-audit defect; atomicity acceptance; P01-T01; P02-T01.
* Evidence: src/core/src/zava_forward/core/workflows.py `_hazard_event` appends history, calls `audit` and then calls `save`; emergency intake also emits an audit before that event. src/core/src/zava_forward/core/store.py:102-115 saves JSON by file replacement but immediately appends audit to a separate file. The plan's functional failure requirement at .copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md:57-58 only names staged SQL mutations/audits, while :66-74 and the phase-details completion criteria describe durable failure/JSON/SQLite validation without specifying the JSON failure contract.
* Concern: JSON has no SQL pending-audit buffer to discard. Wrapping the existing hazard event in a SQL-oriented scope leaves a durable success audit if JSON save fails before replacement; the mutated in-memory hazard may also remain. Conversely, moving audit after JSON save avoids that false-success path but does not make the two files one transaction: a later audit-write failure may follow a committed hazard.
* Impact: the same failed-save success-evidence defect can remain on the supported JSON path, or validation can incorrectly claim durable unchanged state after an operation whose JSON save already committed.
* Smallest useful change: state the bounded JSON ordering and recovery contract in P01 and its tests. For a known pre-save/pre-replacement failure, restore the in-memory hazard snapshot and avoid emitting successful hazard/emergency audit entries before persistence succeeds. For an audit failure after successful JSON replacement, explicitly preserve/report an uncertain or partially persisted outcome rather than promise rollback. Do not add a journaling subsystem, new schema, ledger truncation or shared persistence rewrite.
* Action owner: planning parent for backend-specific acceptance wording; implementer for hazard-local event ordering and recovery.
* Exact resolving evidence: revised details distinguish SQL atomic rollback, JSON pre-replacement refusal and JSON post-save audit failure. Within canonical semantic tests, injected JSON pre-replacement save failure leaves reopened state/audit unchanged and prevents an in-memory ghost or next-request leak; a post-save audit-failure probe demonstrates the documented durable outcome and original error/uncertainty behavior. Existing valid JSON audit-chain and emergency/manual-intake tests remain. Actual MSSQL evidence is reported separately, not used as JSON proof.
* Decision route: direct planner correction within the existing failed-save defect and no-new-persistence requirement. No user decision is required; full cross-file transactional durability is not requested by this finding.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Test prior pending audit preservation across the existing eager SQL discard

* Related IDs: C7, C12; prior-audit/original-exception requirement; P01-T01; P02-T01.
* Evidence: .copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md:57-58 explicitly requires preservation of prior audit. src/core/src/zava_forward/core/sqlstore.py `save` catches ConflictError/GateError/PermissionError and invokes `_discard()` unless stock/procurement context is active. A new hazard context is not currently one of those exceptions. `_discard(pending=())` replaces the pending list before recovery I/O; `_finish` can subsequently flush remaining pending entries. Phase details :22-27 and :53-54 do not identify a pre-operation pending baseline or a preservation assertion.
* Concern: generic injected write failures and authority/conflict failures traverse different recovery paths. By the time a hazard wrapper catches a transaction-time authority error, existing `save` may already have cleared earlier pending audit. A wrapper that captures the baseline too late, or copies the existing stock `_discard()` pattern without a baseline, cannot satisfy the stated preservation requirement.
* Impact: unrelated earlier staged audit can disappear, even when the failed hazard's success audit is correctly removed. Empty-baseline failure tests would miss that regression.
* Smallest useful change: explicitly capture an independent copy of the pre-operation pending-audit baseline before staging any hazard audit and define how the hazard wrapper preserves/restores it despite `save`'s existing eager discard. Keep quarantine ahead of recovery reads, preserve the original exception and restore/clear the hazard context in a finally path. Retain the additive-hook constraint and existing validators; no finance.py or quality.py changes are necessary.
* Action owner: planning parent for the failure matrix and context-lifecycle detail; implementer for hazard-owned baseline handling.
* Exact resolving evidence: revised P01/P02 details name the baseline and both error branches. A parameterized SQL regression starts with a distinguishable earlier pending audit, then exercises transaction-time PermissionError/conflict and a generic save/audit-write failure, including recovery-read failure. After lock exit and durable reopen, the earlier audit remains exactly once with an intact chain, failed hazard success entries and mutations are absent, the original exception is retained, and the next unrelated operation is not subject to stale hazard validation. Run applicable semantics on SQLite and actual owned MSSQL within the existing method budget.
* Decision route: direct planner correction implementing an already explicit requirement, not a significant or divergent user decision.

## Strengths and Residual Risk

* All four basic criteria are treated as existing behavior to preserve, not claimed as a newly delivered hazard service.
* Canonical current-actor reuse, durable historical code/email/OID and conservative legacy fallback are appropriate. Alias tests should use valid current registered identities so they genuinely exercise independence rather than only caller rejection.
* A dedicated hazard context and named additive SQL hook preserve stock/provider/finance/change boundaries and shared-path discipline.
* Actual task-owned MSSQL, canonical reuse, retained tests, bounded additions and explicit SQLite-only trace limitations are credible validation controls.
* No web edits are planned; no browser run is required for this scope. A later web scope change would reopen the relevant skill/browser obligations, not justify a present accessibility claim.
* The candidate explicitly leaves operational authority/timing ratification, verified communications, legal activation and live/human acceptance outside this task. These are accepted engineering boundaries, not independent evidence that those approvals exist.
* The independent implementation Review and up to two authorized correction cycles are distinct from this plan critique. Parent reconciliation cannot manufacture an independent Pass.

## Questions or Blocking Evidence Gaps

* No user response or new external research is required for the three findings.
* Research C12 is a supplied report of executed counterexamples, not a stored formal fail-before test transcript inspected in this critique. The planned formal failing assertions remain necessary implementation evidence.
* Actual current-head MSSQL parity, regression/check results and implementation Review do not exist as completion evidence in the candidate materials. They are future phase gates, not grounds for claiming implementation acceptance now.

## Limitations

* This was a bounded plan credibility assessment, not an implementation review, vulnerability audit, legal-currentness check or full repository audit.
* No tests, database containers, browser sessions or deployed services were executed. Source inspection supports the identified call-order risks; it does not assert new runtime reproduction beyond the supplied research.
* No private datasets, other worktrees, quality.py or finance.py implementation, Azure resources or real communications were inspected.
* Existing untracked research/plan/details/state artifacts were present on fix/hazard-referral-controls-85. They were read only as authorized and not moved, committed or modified. Only this requested critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001, stale referral-destination authority despite a valid caller.
* Action owner: active planning parent.
* Smallest next action: revise P01-T01/P02-T01 to name the destination validation subject, backend-specific failure contract and pre-operation SQL audit baseline; map their cases into the existing bounded canonical test budget and disposition PC-001 through PC-003.
* User response required: no.
* Stop: this single independent critique is complete. Return the Revise verdict to the active automatic RPI parent; do not launch another critique or peer stage from this worker.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/hazard-referral-controls-85-research.md](.copilot-tracking/research/2026-10-17/hazard-referral-controls-85-research.md) | Supplied bounded research and reported counterexamples. |
| [.copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md](.copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md) | Assessed final-candidate plan, unchanged. |
| [.copilot-tracking/details/2026-10-17/hazard-referral-controls-85-phase-details.md](.copilot-tracking/details/2026-10-17/hazard-referral-controls-85-phase-details.md) | Assessed phase details, unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-17/hazard-referral-controls-85-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/hazard-referral-controls-85-plan-critique.md) | Complete single critique; Revise with three direct-correction findings. |

## Next Steps

No user action is required. The active planning parent should directly revise and record disposition of PC-001 through PC-003, then finalize planning without another critique and continue only through the authorized RPI gates. This worker stops after this artifact; it does not invoke Implement or Review.
