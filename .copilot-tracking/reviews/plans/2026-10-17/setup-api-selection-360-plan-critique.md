---
title: Setup API selection final-candidate plan critique
description: Independent bounded assessment of task 360 discovery and read-only safety
ms.date: 2026-10-17
---

## Metadata

* Task ID: 360/setup-api-selection-360
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/setup-api-selection-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/setup-api-selection-360-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique. No additional critique requested or performed.

## Inputs and Criterion Boundary

* Caller requirements: Prefer the uniquely explicitly configured direct demo while retaining the old API; honor exact --container-app overrides; refuse true ambiguity; preserve single legacy and Front Door behavior. Check/read-only operation must make no cloud, SQL or Graph writes, including failure paths. Reuse the evidenced legacy workload=api plus zava-forward-ingress=direct metadata without adding a persistent selector.
* Planning inputs: The supplied research, plan and phase-details paths for setup-api-selection-360, including research C1-C4/W1-W2, acceptance criteria 1-4 and tasks P01-T01 through P02-T02.
* Supplied implementation evidence inspected: infra/scripts/setup-entra.py; relevant discovery, read-only, generation and SQL tests in infra/tests/test_setup_entra.py; transport integration and expiry tests in infra/tests/test_staff_azure.py; applicable transport advice in infra/README.md. Repository case-study context, reference index and memory were read as context, not new operational evidence.
* Decisions and dependencies: Same topic branch and existing PR; preserve historical ACR receipts and Review; red-first offline tests; no removals and at most six new test methods; one later independent implementation Review; ordinary source publication only. Live setup, cloud mutation, image/runtime acceptance and old-edge retirement remain outside authorization.
* Boundary: Assess the credibility of the proposed changes against supplied evidence, not implementation completion. W1/W2 are supplied read-only observations, not independently reverified deployments. No Azure calls, source edits, test execution, package installation or remote publication occurred during this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2, W1-W2; legacy direct compatibility | Covered | Existing workload API compatibility and the explicit deployed ingress tag support the proposed filter. Deployment parameters are correctly rejected as an alternate selector. No new tag/config is necessary. |
| Acceptance 1-2; P01-T01/P01-T02; unique selection and ambiguity | Partial | Exact override, reversed ordering, unrelated ingress and conflicting role cases are specified. Mixed modern-role and legacy-workload direct candidates remain vulnerable to choose's global tag priority; PC-002. |
| Acceptance 1; legacy/Front Door preservation | Covered | Explicit old selection and single legacy edge regressions are required; existing post-selection subscription, environment and origin validation stays in place. |
| C4; acceptance 3; P01-T02; check/dry-run guard | Covered | Current azure_staff guards only dry_run. The plan explicitly adds args.check before payload preparation/execute and retains mutation-mode transport. That is the right choke point for both candidate and SQL-check fallback. |
| Acceptance 3; all setup read-only paths | Partial | setup also treats --list-staff as read-only, but the proposed central guard omits it; PC-001. |
| Acceptance 3-4; existing suite compatibility | Partial | The current reusable-credential Azure --check expectation is success, inconsistent with the new mandatory blocked result; PC-003. |
| Test ownership, removals, maximum and generated coverage | Partial | Semantic canonical tests and no generated/golden production output are explicit. A bounded allocation and exact affected existing assertions are provided below; incorporate PC-001 through PC-003 without removals or exceeding six new methods. |
| P01-T03; documentation and preservation | Covered | Runbook transport correction, KB routing/additive log and byte-preservation of prior ACR evidence are required. Apply the correction to active examples as well as prose. |
| P02-T01/P02-T02; independent Review/publication | Covered | One later independent Review, bounded concrete corrections and ordinary existing-topic publication are appropriate. Nothing in this critique authorizes cloud actions, history rewriting or acceptance claims. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 1 Medium, 0 Low.
* Rationale: The deployed compatibility diagnosis and check guard direction are credible, but the plan leaves a currently reachable read-only cloud-write path, does not resolve mixed valid direct-candidate ambiguity, and overlooks an existing test expectation invalidated by its new contract. All three are direct planner corrections under current user direction, not reasons to request another user decision or critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Cover the existing list-staff read-only path at the transport guard

* Related IDs: C4; acceptance 3; functional no-write requirement; P01-T01/P01-T02/P01-T03.
* Evidence: infra/scripts/setup-entra.py:921-951 guards only args.dry_run before payload/transport; :1527 includes args.list_staff in readonly; :1567-1576 calls candidate_staff for listing. candidate_staff at :617-623 reaches azure_staff after local failure or explicit Azure selection. infra/tests/test_staff_azure.py:598-603 and :646-656 currently expect Azure candidate requests from --list-staff. The proposed P01-T02 guard names args.check and dry_run only.
* Concern: Adding args.check fixes the named check paths but leaves --list-staff, which the same entry point explicitly classifies as read-only, able to create temporary jobs/secrets on explicit Azure selection or local-connectivity failure. This violates the caller's no-cloud-writes-in-read-only requirement; successful cleanup does not make a write read-only.
* Impact: A nominal read-only listing can still transfer a request and mutate cloud resources, including during failure handling.
* Smallest useful change: Explicitly include --list-staff in the no-write transport boundary before payload preparation or execute. Preserve local read-only listing and mutation-mode candidate/bootstrap transport. Specify blocked/incomplete output and an authorized private-connected-host read-only handoff for unavailable listing; remove active runbook advice that presents Azure listing job/secret writes as read-only.
* Action owner: Planning parent for P01-T01/P01-T02/P01-T03; implementation owner applies the revised boundary.
* Exact resolving evidence: Revised plan/details explicitly cover --list-staff. Existing SetupAzureTests listing methods gain explicit-Azure and failed-local subcases asserting no new transport requests, job lifecycle calls, tag writes, Graph writes, SQL apply/restart or secret payload creation, and a non-success result without claiming SQL verification. The existing local listing success test remains passing. Assertions must observe attempted calls, not only an empty final jobs dictionary.
* Decision route: Direct planner correction. The caller already requires read-only no-write behavior; no new user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Refuse a mixed modern and legacy pair of valid direct APIs

* Related IDs: C1; research Contrarian/selected recommendation; acceptance 1-2; P01-T01/P01-T02.
* Evidence: infra/scripts/setup-entra.py:370-376 chooses tagged or legacy candidates, not their union. discover at :394-401 passes the direct candidate pool through that helper. The proposed filter admits both role=api direct resources and absent-role/workload=api direct resources, while plan functional requirements and P01-T02 also say to preserve modern selection priority. Research says multiple eligible direct targets retain refusal.
* Concern: If both modern-role and compatible legacy-workload APIs explicitly advertise direct ingress, filtering admits both, but choose silently selects the modern-role API. Both satisfy the new direct contract; modern tag presence does not establish which direct workload the operator intends. Duplicate tests containing only one tag generation will miss this case.
* Impact: A migration can target an unintended valid direct API rather than refuse true ambiguity, despite list-order independence.
* Smallest useful change: Make the direct-pool rule explicit: absent an exact override, more than one eligible direct API refuses before modern/legacy helper priority can hide a candidate. Preserve modern-role authority over workload within each resource, excluding a conflicting explicit role. Preserve existing generic legacy/edge discovery behavior outside this direct-pool rule.
* Action owner: Planning parent for selection semantics and P01-T01/P01-T02; implementation owner adds the cardinality rule and assertions.
* Exact resolving evidence: Revised plan/details distinguish per-resource role authority from global selection preference. A canonical selection test covers one modern-role direct API plus one legacy-workload direct API in both orders, expects refusal and no writes, then proves either exact --container-app override selects that exact resource. Existing unique direct, conflicting-role, single legacy/edge and explicit-old tests still pass.
* Decision route: Direct planner correction. The caller's true-ambiguity refusal and research recommendation resolve the rule; no new selector or user decision is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Reconcile the existing Azure check success expectation without weakening credential coverage

* Related IDs: Acceptance 3-4; test ownership contract; P01-T01/P01-T03.
* Evidence: infra/tests/test_staff_azure.py:971-1008, SetupAzureTests.test_arm_generated_and_legacy_kv_reuse_retains_upstream_expiry_boundaries, expects exit 0 for reusable credentials under --run-in-azure --check at :1000. Acceptance 3 and P01-T02 require that explicit Azure check cannot claim private SQL verification and returns blocked/incomplete.
* Concern: The candidate says to run the existing staff suite and extend existing methods as appropriate, but does not identify this incompatible success assertion or distinguish valid credential reuse from overall SQL verification. A correct new transport guard necessarily changes this subcase even when credentials are reusable.
* Impact: The required regression run will fail, or an implementer may weaken expiry/reuse checks or relax the transport guard to preserve the old success result.
* Smallest useful change: Name this existing method as an intentional assertion update: reusable credentials remain unchanged and independently valid, but overall explicit Azure --check is incomplete because SQL transport is prohibited. Retain all generated/legacy expiry cases and subsequent mutation-mode reuse/rotation assertions.
* Action owner: Planning parent for P01-T01/P01-T03 test ownership; implementation owner updates the existing canonical method.
* Exact resolving evidence: Revised test disposition lists this method as modified, not removed. Its check subcases assert the blocked/incomplete result and no new cloud/Graph/SQL writes or secret payloads relative to the initialized baseline, while preserving credential count, old credential bytes and mutation-mode reuse/rotation expectations. Combined test_setup_entra/test_staff_azure/test_initialize_api_auth validation passes.
* Decision route: Direct planner correction under the already selected check contract; no user response required.

## Test Ownership and Bounded Disposition

* Canonical owners are SetupTests in infra/tests/test_setup_entra.py and SetupAzureTests in infra/tests/test_staff_azure.py. The latter is the actual class name; the plan's AzureSetupTests label refers to that existing owner, not a new suite.
* Removals: None. No existing credential, legacy delegate, worker or transport test is to be deleted to satisfy the new contract.
* New-method ceiling: Six total across the changed canonical test files, not six per file. Existing-method extensions do not require duplicating equivalent tests.

| New canonical test allocation | Owner and required subcases |
| --- | --- |
| 1. Observed legacy direct migration pair | SetupTests: workload-only old and explicitly direct workload-only replacement; both orders; exact selected name/ID/FQDN; no edge discovery. |
| 2. Direct eligibility and ambiguity matrix | SetupTests: modern and compatible legacy candidates, conflicting modern role, unrelated ingress-only entry, duplicate and mixed-tag direct ambiguity; both orders where relevant. |
| 3. Exact override and legacy preservation | SetupTests: explicit old and either ambiguous direct target; wrong exact name refuses; single legacy still uses its linked Front Door. Extend existing methods instead if equivalent. |
| 4. Central transport guard | SetupAzureTests: check/dry-run/list-staff and candidates/check/apply operation entry points fail before payload preparation/execute; no attempted job/secret transfer. Existing mutation-mode tests retain real fake transport coverage. |
| 5. Check fallback/failure matrix | SetupAzureTests: explicit Azure and local candidate/SQL failures, including exception/timeout paths, produce no writes and cannot claim private verification. Retain successful local read-only checks and generation preview coverage. |
| 6. Read-only listing matrix | SetupAzureTests: explicit Azure/local-failure listing blocks safely, local success preserved. Prefer extending the two existing listing methods, making this slot unnecessary. |

* Existing methods intentionally modified: SetupAzureTests.test_azure_candidates_are_count_only_and_cleaned_up and test_candidate_auto_fallback_and_missing_image_exact_private_host_fallback for PC-001; SetupAzureTests.test_arm_generated_and_legacy_kv_reuse_retains_upstream_expiry_boundaries for PC-003. Retain their relevant privacy, fallback and expiry assertions; adapt only superseded read-only Azure-success expectations.
* New canonical versus generated coverage: All new semantic assertions belong in the existing hand-maintained test modules. Fictional fixtures and bounded subcases are inputs, not generated production or acceptance evidence. No new golden/generated outputs or separate coverage suite are needed. Existing generated-versus-legacy credential and generated-roster tests remain canonical regression coverage.
* Red-first ownership: Selection tests must fail against the current modern-only direct filter; check transport tests must fail against the current dry-run-only guard. Capture the failing assertion and subsequent targeted green result before the combined regressions. A guard test that only mocks azure_staff itself does not exercise the central boundary; exercise the real wrapper and fail lower-level payload/transport preparation if reached.

## Strengths and Residual Risk

* The supplied metadata supports compatibility with an existing explicit ingress selector; choosing a new persistent selector, name suffix or resource ordering would be unjustified.
* The plan correctly retains subscription/resource-group, external ingress/environment and origin checks after selection, plus exact override and old-stack preservation.
* The proposed central azure_staff check guard is necessary even when the SQL worker operation itself is read-only: temporary job/secret lifecycle and result transport are cloud writes.
* Mutation-mode Azure preflight operation named check is not the same as user --check mode. Preserve its transport when the enclosing command is authorized to mutate; do not prohibit all operation="check" requests globally.
* Actual laptop setup, deployed browser/SQL/Graph behavior and image/runtime acceptance are intentionally unproved. Historical ACR receipts and the existing Review remain outside this new assessment.

## Questions or Blocking Evidence Gaps

* No user decision or additional deployment metadata is needed to correct these findings. The evidence supports revision rather than a Blocked verdict.

## Limitations

* This is a plan assessment, not a fresh implementation Review, live no-write demonstration or passing test receipt.
* No source/tests/runbook edits or Azure calls were made. Supplied historical cloud observations were not re-executed.
* Existing ACR receipt/Review contents were not reassessed or modified. The requested critique artifact is the only file written.

## Recommended Next Action

* Highest-impact finding: PC-001, the omitted list-staff read-only transport path.
* Action owner: Planning parent.
* Smallest next action: Revise the no-write predicate and its existing test dispositions, resolve mixed direct-pool cardinality under PC-002, and name the existing expiry expectation update under PC-003. Then finalize the plan without a second critique and continue the authorized implementation/red-first gates.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/setup-api-selection-360-research.md](.copilot-tracking/research/2026-10-17/setup-api-selection-360-research.md) | Supplied research and metadata observations |
| [.copilot-tracking/plans/2026-10-17/setup-api-selection-360-plan.md](.copilot-tracking/plans/2026-10-17/setup-api-selection-360-plan.md) | Final candidate assessed without modification |
| [.copilot-tracking/details/2026-10-17/setup-api-selection-360-phase-details.md](.copilot-tracking/details/2026-10-17/setup-api-selection-360-phase-details.md) | Phase details assessed without modification |
| [.copilot-tracking/reviews/plans/2026-10-17/setup-api-selection-360-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/setup-api-selection-360-plan-critique.md) | This single complete critique |

## Next Steps

Planning parent revises PC-001 through PC-003 directly, finalizes without another critique, and proceeds only through the authorized implementation and independent Review gates. No user action is required. This critique stops here; it does not activate implementation or alter existing ACR evidence.
