---
title: Resident activation timeout recovery final-candidate plan critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: 563-timeout-recovery-20261030.
* Issue: #563; continuing ops/resident-ai-activation-563 and PR #576.
* Critique date: 2026-10-30.
* Critique execution status: Complete.
* Assessment: exactly one independent final-candidate critique.
* Plan: .copilot-tracking/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/resident-ai-activation-563-timeout-recovery-phase-details.md.

## Inputs and Criterion Boundary

* Read the supplied new research, plan and phase details in full. Read only narrowly necessary named source: src/core/src/zava_forward/core/resident_showcase.py:370-445, src/api/src/zava_forward/api/resident_demo/__main__.py:35-65, src/api/src/zava_forward/api/resident_demo/web/demo.js:315-375 and src/api/README.md:1010-1100.
* Assessed all FR1-FR5, NFR1-NFR3, AC1-AC6, P01-T01, P01-T02 and P02-T01, including their dependency and failure branches.
* Caller decisions control the assessment: owner-approved resident activation and cost monitoring; four additional login submissions total; no ledger read or SQL public access; existing USD20 ceiling and exclusive November 1 inference expiry; redeploy authority through November 15; no employee mutation, additional endpoints or broad identity permissions; min0 and Manual jobs; exact private backup first; failed verification rolls back.
* Assessed credibility of the bounded operational recovery and evidence plan, not actual activation, current cloud state, budget availability, human content acceptance, issue closure or publication approval.
* Historical evidence C1-C3 and operational observations C9 were considered as reported by the supplied research, not independently re-executed or re-certified.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Research C4-C8; FR3 | Covered | Read source confirms a random process nonce signs sessions, startup constructs a new codec, and the browser shows sign-in when signed out. Fresh authentication after rollout addresses the stated failure without changing security. |
| Research C1-C3, C9 | Covered within boundary | Prior timeout and current health/role observations support a targeted hypothesis, not proof of model success. The plan correctly requires separate live evidence. |
| FR1; AC1; P01-T01 | Covered | Exact private backups and hashes precede mutation; expected baseline and permitted delta are checked; employee configuration is read-only. |
| FR2; NFR3; P01-T01 | Covered | Only the two documented enablement variables change. Readiness and anonymous health warming precede credential access, with bounded retries restricted to idempotent operations. |
| FR3; NFR1-NFR2; AC5 | Covered | Persisted submission count, stage and request status evidence, fresh context, explicit sign-in/error handling and stopping on authentication denial constrain both retry expenditure and diagnostic ambiguity. |
| FR4; AC2-AC4; P01-T02 | Covered | Requires actual AI-labelled pest output, source-supported claims, thin label geometry, collapsed known sources, out-of-scope rules/manual fallback, anonymous denial and both client/server no-consent checks. |
| FR5; AC5; P01-T01/P01-T02 | Covered | Any changed-candidate verification failure or unknown mutation state invokes rollback. Restoration includes readiness, health and effective configuration preservation; failed rollback is an urgent blocker, not activation success. |
| Owner cost and authority decisions | Covered | Redeploy authorization is not treated as an extension of inference expiry. No ledger inspection or permissive fallback is proposed; actual rules fallback fails the required AI activation proof. |
| Scope; AC5; NFR1 | Covered | No application security change, source deployment, new settings, RBAC/network changes, employee writes or secret-list operation is authorized. Private evidence exclusions remain explicit. |
| AC6; P02-T01 | Covered | One independent Review, original evidence preservation, local commits only and an actual full local gate attempt are planned. The native runner's equivalent heavy lock is not double-acquired. A missing or invalidated receipt blocks publication. |
| Dependencies and test boundary | Covered | P01-T02 follows backup/activation; reconciliation follows either verified activation or rollback. Existing restart tests and syntax/invariant checks supplement, rather than replace, live semantic proof. |

## Verdict

* Verdict: Pass.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.
* Rationale: The candidate targets the evidenced stale-session automation defect, preserves process-bound authentication and makes enabled success conditional on real semantic, consent and presentation checks. Its failure path restores the narrowly defined baseline. Operational and publication uncertainties are not presented as completed gates.

## Findings

No actionable PC-xxx findings within the supplied criterion boundary. No plan revision or significant/divergent user decision is required. This is the complete finding set for this single critique, not a deferred or serialized assessment.

## Strengths and Residual Risk

* The read source independently supports the restart-invalidates-session contract. Longer waits or weakening the nonce are correctly rejected.
* Health, readiness and an established managed-identity role do not prove reservation or inference success. The plan recognizes this distinction and requires the actual pest answer rather than treating fallback as successful activation.
* Owner monitoring substitutes neither for the existing fail-closed accounting control nor for actual-model evidence. The no-ledger-read decision is respected; unknown remaining capacity can still cause safe verification failure.
* A later process restart may invalidate the fresh session. The plan permits another submission only with observed invalidation and a healthy revision, within the aggregate four-submission cap; it does not authorize replaying inference.
* Rollback remains an operational risk, not a guarantee. The specified ready-revision, health and invariant proofs, plus urgent-blocker handling, are adequate safeguards for this bounded plan without speculative infrastructure changes.
* Safe successful activation is distinct from human resident/content acceptance and whole-issue delivery. Local persistence is distinct from publication: a later commit invalidates an earlier passing receipt, and the coordinator still needs a fresh exact-head/current-main gate and independent exact-head approval.

## Questions or Blocking Evidence Gaps

None for plan credibility. Actual runtime success and restoration evidence must be produced during execution; their absence before execution is not a planning blocker.

## Limitations

* No cloud, network, browser, SQL, credential, test, gate or commit operation was performed.
* No prior private helper, private backup, raw operational log or historical review was opened. The historical helper defect is assessed from the supplied research together with the directly read authentication contract, not from a new examination of private automation.
* This critique does not attest to current cloud configuration, residual model budget, output relevance, successful rollback or accessibility conformance.
* Only this critique artifact was written. Research, plan, phase details and historical outcomes remain unchanged.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this passing critique disposition and continue the authorized ordered RPI loop with P01-T01; do not repeat critique or expand operational authority.
* Decision route: Direct parent finalization; no significant or divergent decision.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/resident-ai-activation-563-timeout-recovery-research.md](.copilot-tracking/research/2026-10-30/resident-ai-activation-563-timeout-recovery-research.md) | Supplied bounded research and C1-C9 evidence pointers |
| [.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan.md](.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/resident-ai-activation-563-timeout-recovery-phase-details.md](.copilot-tracking/details/2026-10-30/resident-ai-activation-563-timeout-recovery-phase-details.md) | Assessed execution and failure branches |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-timeout-recovery-plan-critique.md) | Complete independent critique; Pass |

## Next Steps

The active planning parent may record Pass and proceed to authorized implementation without another critique or user response. This critique stops here; it does not invoke another RPI stage or perform operational work.
