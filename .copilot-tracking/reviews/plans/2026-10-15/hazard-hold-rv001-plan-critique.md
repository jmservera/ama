---
title: Transactional hazard hold final-candidate plan critique
description: Single bounded credibility assessment for hazard-hold-rv001, PR 314 and issue 85
ms.date: 2026-10-15
---

## Metadata

* Task ID: hazard-hold-rv001
* Critique date: 2026-10-15
* Plan: .copilot-tracking/plans/2026-10-15/hazard-hold-rv001-plan.md
* Phase details: .copilot-tracking/details/2026-10-15/hazard-hold-rv001-phase-details.md
* Critique execution status: Complete
* Execution boundary: exactly one final-candidate assessment; no implementation, nested agents, source changes or delivery actions.

## Inputs and Criterion Boundary

* Authoritative caller requirements: portable transaction-local persisted hazard reload for every guarded transition, existing serialized writer and rowversion protocol, actual two-store completion regression, honest unratified release/timing policy, original acceptance criteria unchecked, core/API suites and requested ruff/mypy environment, src-only code, same-branch delivery through existing PR 314.
* Research: .copilot-tracking/research/2026-10-15/hazard-hold-rv001-research.md, Evidence and Boundaries.
* Supplied reproduction and decisions: .copilot-tracking/reviews/logs/2026-10-15/src-hazard-referral-85-review.md, RV-001 through RV-003 and Parent Reproduction Command. These are prior evidence, not tests rerun during this critique.
* Transaction evidence: src/core/src/zava_forward/core/sqlstore.py:80-112, 286-305, 318-423; src/core/src/zava_forward/core/mssqlstore.py:55-56, 157-176.
* Guard and regression evidence: src/core/src/zava_forward/core/store.py:335-338, 367-381; src/core/src/zava_forward/core/procurement.py:126-219; src/core/src/zava_forward/core/signoffs.py and quality.py shared-guard call sites; src/core/tests/test_hazard_referral.py:23-74, 319-370.
* Related documentation: src/core/README.md and src/api/README.md hazard sections. Project framing considered from docs/case_study_48_original.md, relevant safety/acceptance context in docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md.
* Locked test boundary: P01-T02 owns src/core/tests/test_hazard_referral.py, at most eight new test methods using subtests, no removals or generated targets. This assessment does not expand that boundary.
* Assessment determines implementation-plan credibility, not correctness of an unwritten fix, legal policy ratification, live SQL Server behavior or operational acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-001 / P01-T01: close procurement dependency race | Covered | Plan lines 54-56 and details lines 17-21 require a separate dependency read before mutation inside save's writer transaction. This addresses sqlstore.py:360-362 skipping unchanged case bodies, rather than relying on touching a case. |
| RV-001 / portable serialization and concurrency | Covered | Plan lines 63-64 preserves parameterized portable reads/version checks. sqlstore.py:353 starts the existing writer transaction; mssqlstore.py:55-56, 157-176 maps it to the transaction-owned exclusive application lock and SQL Server commit/rollback. No new lock, schema or driver-error assumption is proposed. |
| P01-T01: all guarded transitions | Covered | The five procurement, two quality and one technical shared-guard call sites inherit dependency registration. Details line 25 explicitly adds advancement, whose current store.py:367-381 path instead uses aggregated gate reasons. Existing advancement explanations are preserved. |
| P01-T01: refusal atomicity and lifecycle | Covered | Plan lines 57-59 and details lines 22-24 cover rollback, case/procurement discard, pending audit removal and dependency cleanup on successful save and outer lock exit. This directly addresses sqlstore.py:328-348 flushing pending audit and save's current ConflictError-only discard branch at lines 387-394. |
| P01-T02: actual two-store reproduction and durability | Covered | Plan lines 68-72 and details lines 32-36 require independent SQLite stores, the exact completion race, absent refused-transition audit, retained hold after reopen, stale clear-case conflict and transaction-local reload verification. Database results are not replaced by mocked store behavior. |
| P01-T02: bounded tests and preserved behavior | Covered | Details lines 30-36 fixes ownership and maximum additions, prohibits removals and requires in-memory as well as persisted procurement rollback. Plan line 59 preserves withdrawal, referral and unrelated-home writes; existing sequential/sibling/referral tests remain. |
| RV-002 / P01-T02: release and timing authority | Covered | Details lines 37-38 requires explicit unratified authority/timing wording in both component READMEs. Plan lines 102-103 assigns ratification to Repairs/Safety/Housing; no statutory clock or approval is invented. |
| P02-T01: local gates and evidence | Covered | Details lines 46-51 specifies the requested interpreter/tool environment, empty core PYTHONPATH, API fixture paths, targeted then full core/API suites, lint/format/types and recording initial failures as well as final results. No live/shared-data tests or unprompted dependency installation is proposed. |
| P02-T02: authorized delivery | Covered | Plan lines 32-40 and details lines 56-61 preserve the existing branch and PR 314, verified noreply identity, required trailer, Refs #85 and readiness only after local correction/gates. No new PR, merge, history rewrite or acceptance checkmark is authorized. |
| Scope / RV-003: evidence and approval boundary | Covered | Plan lines 36, 48-50, 74 and 104 restrict code to src, retain unchecked original criteria and separate local repair from service/model/SQL Server/Azure and human acceptance. |

## Verdict

* Verdict: Pass
* Rationale: The candidate directly addresses the reproduced unchanged-dependent-case race using the existing transaction and concurrency contract. It supplies bounded, executable regression objectives and cleanup requirements without confusing local engineering readiness with policy or platform acceptance.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings within the supplied final-candidate boundary.
No significant or divergent user decision is needed to implement this plan.

## Strengths and Residual Risk

* Persisted hazard inspection and rowversion comparison are required inside the serialized transaction, before mutations, not merely at request entry or by forcing an unchanged case into the touched set.
* The plan separately tests an active hold refusal and a stale but clear case conflict. Pending audit cleanup is part of refusal, avoiding a misleading completion ledger entry at outer lock exit.
* All guarded paths can be exercised through subtests within the locked eight-method addition ceiling; no new test owner or removal is necessary.
* RV-002 remains an explicit Repairs/Safety/Housing ratification dependency. RV-003 remains an explicit live-platform/service/human evidence dependency. These are retained acceptance limits, not grounds to block this authorized local correction.

## Questions or Blocking Evidence Gaps

None for the bounded implementation decision. Operational authority and live-platform evidence remain open follow-ups, not decisions delegated to this critique.

## Limitations

* No suites, lint/type checks, SQL Server integration or concurrency experiment were executed during this read-only assessment. The passing verdict applies to the plan, not the existing defective code or a future implementation.
* The SQL Server portability assessment is based on the supplied adapter contract, not an actual SQL Server run.
* Remote PR state and CI were not queried. Same-branch commit/push/readiness are later parent actions, not outcomes of this critique.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: active RPI planning parent.
* Smallest next action: record this passing critique, finalize the candidate and proceed to P01-T01/P01-T02 within the existing authorization. Preserve the locked test boundary and subsequently execute the planned gates and single post-implementation review.
* Decision route: direct-compatible parent continuation; no significant or divergent decision.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/hazard-hold-rv001-plan.md](.copilot-tracking/plans/2026-10-15/hazard-hold-rv001-plan.md) | Final-candidate plan assessed without modification |
| [.copilot-tracking/details/2026-10-15/hazard-hold-rv001-phase-details.md](.copilot-tracking/details/2026-10-15/hazard-hold-rv001-phase-details.md) | Locked tasks, tests and delivery boundary |
| [.copilot-tracking/research/2026-10-15/hazard-hold-rv001-research.md](.copilot-tracking/research/2026-10-15/hazard-hold-rv001-research.md) | Supplied transaction research |
| [.copilot-tracking/reviews/logs/2026-10-15/src-hazard-referral-85-review.md](.copilot-tracking/reviews/logs/2026-10-15/src-hazard-referral-85-review.md) | RV-001 reproduction and RV-002/RV-003 limits |
| [.copilot-tracking/reviews/plans/2026-10-15/hazard-hold-rv001-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-15/hazard-hold-rv001-plan-critique.md) | This single completed critique |

## Next Steps

No user action is required. Return Pass to the active parent for finalization
and authorized implementation; do not request another critique. This critique
stops here without implementation or delivery actions.
