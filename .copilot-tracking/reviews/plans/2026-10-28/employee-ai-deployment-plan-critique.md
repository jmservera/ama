---
title: Employee AI deployment final-candidate plan critique
description: Independent assessment of the bounded employee model deployment plan
ms.date: 2026-10-28
---

## Metadata

* Task ID: employee-ai-deployment-2026-10-28
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/employee-ai-deployment-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/employee-ai-deployment-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique. No implementation
  assessment, nested delegation or repeat critique was performed.

## Inputs and Criterion Boundary

* Assessed the canonical plan, phase details and
  .copilot-tracking/research/2026-10-28/employee-ai-deployment-research.md.
* Current caller direction authorizes full RPI, one capacity-one compatible
  chat deployment on existing aif-cutover-test-rzsrg in ama, and only the
  missing API Cognitive Services OpenAI User assignment. Live app changes,
  inference, other resources and other role changes are excluded.
* Current caller direction requests a pushed topic PR with Refs
  #514/#360/#104/#73 and USD30 additional AI authorization through
  2026-10-31. This is not a hard spending cap or inference authorization.
* The caller explicitly supplies the gate exception: no full --all; at most
  one scoped --changed attempt with a timeout-zero heavy lock. The critique
  does not recommend overriding that decision with the repository's full tier.
* Bounded source evidence: infra/main.bicep;
  infra/modules/foundry.bicep; infra/modules/containerapps.bicep;
  infra/tests/test_bicep_policy.py; infra/tests/test_identity_rbac.py;
  infra/README.md; src/core/src/zava_forward/core/ai.py;
  src/README.md; tools/rpi-checks.py.
* Read the required case-study original/addendum and reference index/memory for
  context. No legal-currentness, resident-journey or application acceptance
  claim is being evaluated.
* Read-only Git inspection found feat/employee-ai-deployment-bicep at
  d783b63acb0e2e59ad52f1c8f999e093c149297b, matching local origin/main,
  with parent-owned untracked RPI artifacts and no PR for that branch.
  No existing work was moved or modified.
* The boundary covers AC1-AC6, C1-C8/W1-W4, P01-P03, future source
  redeployment compatibility, test ownership and publication exceptions.
  It does not establish Azure availability, quota, actual response-model
  identities, test success or deployment success.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1, C1/C3, P01-T01 | Covered with compatibility correction | One small default, scalar parameters and preserved nonempty array overrides are explicit; the existing zero-model bootstrap example needs disposition, PC-005. |
| AC2, C2/C4/C6, P01-T01 | Covered | Positional single/two-model names, dated response identities, a dedicated OpenAI endpoint and all five opt-in API settings are specified. |
| AC5, C5/C7, P01-T02 | Partial | Existing compiled-policy class and six-method ceiling are explicit; actual ARM GUID equivalence lacks an executable proof requirement, PC-003. |
| AC3, W1/W3, P02-T01 | Partial | Exact child, minimum capacity and upgrade/content-filter policy are bounded; fallback lacks source and handover reconciliation, PC-004. |
| AC3/AC4, W2/W4, P02-T01 | Covered with proof correction | Fresh identity/role reads and unchanged-app evidence are required; role-name equivalence needs stronger resolving evidence, PC-003. |
| AC5/AC6, P03-T01 | Partial | One Review, preserved adverse outcomes, privacy-safe commit and Refs-only PR are explicit; executable gate and exact-head verification omissions remain, PC-001/PC-002. |
| C8, safety, dependencies, cost | Covered | Advisory/manual boundaries, no inference/app update, #514 follow-up and non-cap USD30 authorization are preserved. |

## Verdict

* Verdict: Revise
* Severity summary: 2 High, 3 Medium, 0 Critical, 0 Low.
* Rationale: The infrastructure direction is credible and the owner has
  already resolved the scope and full-gate exception. Before implementation,
  make the permitted gate path executable or explicitly unavailable, retain
  exact-head publication controls, and close the bounded redeployment/test
  compatibility gaps below. These are direct planner corrections, not reasons
  to request broader deployment authority or another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The planned gate opens a forbidden filesystem path

* Related IDs: AC6, P03-T01, current execution constraints.
* Evidence: tools/rpi-checks.py:2175-2180 implements heavy_lock by opening
  /tmp/ama-rpi-heavy.lock with O_CREAT. P03-T01 requires inspecting lock
  behavior but still plans a timeout-zero attempt. Current execution
  constraints forbid file operations under /tmp, including tool-induced writes.
* Concern: --lock-timeout 0 prevents waiting; it does not prevent opening or
  creating the lock file. Selecting an external output directory or wrapping
  the command in another lock does not remove this operation.
* Impact: The planned validation attempt is not executable within the active
  filesystem boundary. An implementation agent could violate that boundary
  while believing it is honoring the nonblocking-gate requirement.
* Smallest useful change: Record this known incompatibility before execution.
  With the existing runner unchanged, classify the scoped gate as unavailable
  and disclose the exact reason in Changes and the requested PR. Do not run
  it, add an outer lock, change the runner, or substitute --all. The caller
  permits at most one attempt, not a mandatory unsafe attempt.
* Action owner: Planning parent.
* Exact resolving evidence: P03-T01 names the hardcoded lock operation and
  its unavailable status under current constraints; the eventual Changes/PR
  states that no gate attempt or receipt exists for this reason, without
  claiming full-tier or scoped-gate success.
* Decision route: Direct planner correction. No user response is required to
  record the blocker and use the explicitly requested exception-bearing PR.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Publication omits the retained current-base and receipt checks

* Related IDs: AC5/AC6, P03-T01.
* Evidence: Plan/details P03-T01 specifies Review, commit, one optional gate
  attempt and PR, but no fresh-main receipt-verification step.
  src/README.md:150-158 requires fetching main and verifying immediately
  before exact-head assessment and push. tools/rpi-checks.py:2157-2165 and
  2202 defaults verification to full scope; partial verification requires
  --required-scope partial.
* Concern: Waiving --all does not by itself waive candidate/base identity
  checks. The plan does not distinguish a successful scoped receipt, a
  failed receipt, a busy-lock skip, and an unavailable runner. It also lacks
  a disposition for main moving or a post-gate evidence commit when only
  one gate attempt is allowed.
* Impact: A stale or partial receipt could be presented as evidence for a
  different pushed candidate, or an evidence update could silently invalidate
  the only permitted run.
* Smallest useful change: Add a publication decision table. If a valid scoped
  run becomes executable and succeeds, retain its external receipt and verify
  it using --required-scope partial against freshly fetched origin/main
  immediately before push. If unavailable, skipped, failed or subsequently
  invalidated, publish only under the caller's disclosed exception, with that
  actual status and no valid-gate claim. Do not rerun or resume the gate.
  Preserve the single Review outcome and identify its assessed tree/head;
  do not imply that later changes were independently accepted.
* Action owner: Planning parent.
* Exact resolving evidence: P03-T01 includes fresh-main lookup, the conditional
  verification command, candidate/tree linkage for the single Review, and
  explicit handling of changed head/base and missing/failed receipts. Final
  Changes/PR records the actual pushed SHA, reviewed candidate and gate status
  without upgrading partial or unavailable evidence.
* Decision route: Direct planner correction. The owner has already requested
  the PR and scoped-gate exception; no new user decision or full gate is needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Matching the live assignment to ARM guid has no proof criterion

* Related IDs: AC3/AC5, C5, P01-T02, P02-T01.
* Evidence: infra/modules/foundry.bicep:66-75 names the assignment with
  guid(account.id, principalId, 'openai-user'). P02-T01 asks for a matching
  deterministic UUID, but its completion check reads only principal/role/scope.
  infra/tests/test_identity_rbac.py:48-104 checks role tuples rather than
  assignment UUIDs. infra/tests/test_bicep_policy.py:176 uses a joined-string
  guid stub, not ARM's UUID algorithm.
* Concern: Determinism alone is insufficient. A different namespace, argument
  order, separator or input spelling can create a valid live assignment with
  a name different from future Bicep's resource name. Existing role-matrix
  tests will not detect that difference.
* Impact: The live prerequisite can work while a later source redeployment
  fails on an already-existing principal/role/scope assignment under another
  UUID.
* Smallest useful change: Make exact assignment-name equality an acceptance
  criterion. Before the live role write, record the precise ARM-compatible
  algorithm inputs and an independently supported known-answer check, rather
  than substituting the existing guid stub. Allocate this check within the
  existing six-method policy-test budget or record equivalent bounded local
  validation without introducing another test owner. Read back the assignment
  name as well as principal, role and scope.
* Action owner: Planning parent, then P01/P02 implementer.
* Exact resolving evidence: Revised P01-T02/P02-T01 specifies the true UUID
  fixture/provenance and mismatch rejection. Execution evidence shows the
  exact account ID, principal ID and literal seed used by compiled Bicep,
  the computed expected UUID, the matching live assignment UUID, and no
  duplicate role write.
* Decision route: Direct planner correction; no broader role authorization
  or user response is required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: An authorized model fallback can diverge from the source default

* Related IDs: AC1-AC3/AC6, W3, P01-T01/P01-T02/P02-T01/P03-T01.
* Evidence: P01 fixes the default to gpt-4o-mini/2024-07-18/GlobalStandard/1.
  Details P02-T01 permits evaluating another minimum compatible model after
  provider rejection. Details P03-T01 still mandates both
  gpt-4o-mini-2024-07-18 handover identities, with no fallback reconciliation.
* Concern: The alternative path does not say whether to stop, revise and
  revalidate the source default, or preserve and publish explicit overrides.
  It also does not require the handover to use the model actually accepted.
* Impact: A successful small live deployment could be accompanied by Bicep
  that tries the rejected configuration on redeploy and incorrect model pins
  for the coordinator's later app configuration.
* Smallest useful change: Specify a fail-closed branch: stop with the actual
  rejection unless an in-scope capacity-one compatible replacement is
  supported. If selected, reconcile the source defaults or explicit retained
  parameter override, derived response identities, targeted tests and all
  handover fields before Review/publication. Preserve the original failure.
  Do not increase capacity, create a second child, redeploy the app or infer
  runtime compatibility solely from catalogue availability.
* Action owner: Planning parent, then P02 implementer.
* Exact resolving evidence: Revised fallback completion criteria binds the
  successful live child to a tested source/default-or-override configuration
  and actual AI_* handover values; otherwise Changes records a blocked live
  prerequisite rather than AC3 success.
* Decision route: Direct planner correction. The current compatible-small-model
  authority resolves the choice within scope; broader changes remain excluded.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: The new nonempty contract invalidates the existing bootstrap command

* Related IDs: AC1, future redeployment compatibility, P01-T01.
* Evidence: Plan/details P01-T01 requires nonempty modelDeployments in main
  and deployments in foundry. infra/README.md:439-455 documents the
  environment-only cutover wrapper using --parameter 'modelDeployments=[]'.
* Concern: That documented, intentional zero-model bootstrap will fail the
  new constraint. General statements to document opt-in and retain explicit
  arrays do not identify this existing consumer or explain the new model
  provisioning/cost consequence.
* Impact: A future operator following the current bootstrap instructions
  cannot reproduce the environment; simply dropping the override would
  instead request the new nonzero default without explaining that change.
* Smallest useful change: Explicitly include this bootstrap example in the
  README update. Retire or replace the incompatible empty-array instruction,
  stating that the new nonempty contract provisions a model even for an
  environment-only operation. Require an explicit reviewed model array where
  preserving an existing active model set is necessary. Do not run that full
  wrapper as part of this task.
* Action owner: Planning parent, then P01 implementer.
* Exact resolving evidence: P01-T01 names the affected bootstrap example and
  changed behavior; the final README command and adjacent explanation agree
  with the compiled nonempty-array contract and make provisioning/cost and
  existing-model override implications explicit.
* Decision route: Direct planner correction under the selected nonempty
  contract. Preserving a separate zero-model workflow would be a different
  design choice, not a prerequisite imposed by this critique.

## Strengths and Residual Risk

* The selected capacity-one chat model is bounded as a short exercise choice,
  not a long-term quality recommendation or guaranteed cheapest model.
  W3's Deprecating status and retirement date are not hidden.
* Dedicated OpenAI endpoint wiring preserves the existing generic Foundry
  endpoint for the agent workload. The runtime reads precisely the proposed
  five AI_* variables and checks provider response-model identity.
* Single/two-entry positional binding is explicit, rather than pretending
  that deployment names must remain standard/capable. Source tests should
  exercise actual module-bound override values, as the plan already requires.
* Compiled semantic tests in the existing BicepPolicyTests class, existing
  infra discovery/builds, no test removals and at most six new methods are
  proportionate. No new framework, application edit or broad app suite is
  justified by this source-only wiring change.
* The existing source also grants Foundry User when API AI is enabled.
  Preserving that pre-existing source behavior does not authorize creating
  that role now. The exact child/one-role live operation, not a full Bicep
  deployment, is essential to preserving the current live boundary.
* Fresh deployment/identity/role reads, no keys, private network preservation,
  unchanged app metadata and no inference are appropriate. If fresh state
  contradicts the assumed empty child list or selected identity, the executor
  must stop rather than overwrite unrelated state.
* Quota, eventual provider acceptance, private connectivity, actual response
  identity, release/evaluation and human approval remain unproven. Neither
  a local pass nor the requested exception-bearing PR satisfies those gates.

## Questions or Blocking Evidence Gaps

* No unresolved user decision is identified.
* PC-001 is a known execution blocker for the optional scoped gate, not a
  reason to expand scope or claim full-tier assurance.
* ARM UUID equivalence is an execution proof gap, not evidence that an
  incorrect assignment has already been created.

## Limitations

* This is one plan critique, not an implementation review. No implementation
  existed within the supplied candidate and none was created or tested.
* W1-W4 were assessed as supplied research assertions, not independently
  refreshed Azure observations. No cloud writes or additional cloud reads
  were performed.
* The out-of-workspace brief under /tmp was not opened because the active
  filesystem restriction forbids operations there. Its relevant authority
  was supplied explicitly in the current request and canonical inputs.
* GitHub inspection was limited to the branch PR lifecycle; broader issue/PR
  assertions remain supplied context.
* Only this critique artifact was written. Plan, details, research and other
  review records remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Record the scoped runner's filesystem blocker and
  exception path, then resolve PC-002 through PC-005 directly in plan/details.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/employee-ai-deployment-plan.md](.copilot-tracking/plans/2026-10-28/employee-ai-deployment-plan.md) | Canonical final-candidate plan assessed. |
| [.copilot-tracking/details/2026-10-28/employee-ai-deployment-phase-details.md](.copilot-tracking/details/2026-10-28/employee-ai-deployment-phase-details.md) | Canonical task details assessed. |
| [.copilot-tracking/research/2026-10-28/employee-ai-deployment-research.md](.copilot-tracking/research/2026-10-28/employee-ai-deployment-research.md) | Supplied bounded research evidence. |
| [.copilot-tracking/reviews/plans/2026-10-28/employee-ai-deployment-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/employee-ai-deployment-plan-critique.md) | This original independent critique. |

## Next Steps

The active planning parent should disposition all five findings, revise the
canonical plan/details directly, and finalize without another critique.
No user action is required. Implementation remains parent-owned and must
retain the one-Review, one-small-deployment and publication-exception boundaries.
