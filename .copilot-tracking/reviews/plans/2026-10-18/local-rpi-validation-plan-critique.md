<!-- markdownlint-disable-file -->
# RPI Plan Critique: Local-first validation and Actions budget

## Metadata

* Task ID: actions-budget-local-rpi
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/local-rpi-validation-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: One final-candidate, read-only critique of the local RPI validation plan. The owner needs all locally reproducible checks before PR push and a safe, evidence-based workflow cost reduction. No workflow/settings changes, implementation, remote operations, or extra critique pass are authorized.
* Research and evidence considered: .github/workflows/src-ci.yml; .github/workflows/mvp-ci.yml; .github/workflows/mvp-validation.yml; .github/workflows/infra-plan.yml; .github/workflows/src-deploy.yml; .github/workflows directory inventory; src/check-container.py; infra/tests/actionlint.yaml; relevant SQL Server test fixtures in src/api/tests/test_mssqlstore.py, src/api/tests/test_assistants.py, and src/api/tests/test_lawstore.py; .github/agents/ama-backlog-delivery-coordinator.agent.md.
* Decisions, dependencies, and acceptance criteria considered: The owner has not approved workflow disabling, protection changes, or local-only acceptance. Unknown required contexts block retirement. Local execution must be fail-closed, resource-isolated, source-bound, and distinct from GitHub/Azure authenticated controls. Unique checks must remain covered, and no existing domain tests may be removed.
* Assessment boundary: Assessed the supplied plan and phase details against their cited workflow and test evidence for material safety, completeness, and credibility. Did not verify live GitHub settings, account billing, current runner/tool readiness, Azure controls, or execute proposed checks. No claims are made about those unobserved states.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| User request: locally run all checks before PR push | Covered | P01-T01/P01-T02 specify the broad local matrix, explicit required gates, failure behavior, and real SQL/browser/image runs. |
| FR: preserve unique automated checks | Covered | Workflow evidence confirms unique SQL Server, SPDX, migration, compile, logo-permission, and infrastructure controls are named for retention or migration. |
| FR: distinguish local from hosted-only controls | Covered | P03-T01/P03-T02 and the cloud boundary retain hosted OIDC, approvals, Azure what-if, release, and deployment as separate controls. |
| P01-T01: workflow-to-local coverage | Covered | Tracked native workflow inventory and cited YAML align with the listed suites and unique check families; no discovered check is silently proposed for removal. |
| P01-T02: receipt identity and fail-closed execution | Partial | Receipt verification binds HEAD and tracked-tree identity but does not explicitly reject untracked code/config/test inputs that can affect the executed result. See PC-001. |
| P02-T01: exact-source push gate | Partial | The tracked-source binding is sound in principle, but the clean-state contract needs to exclude untracked candidate inputs too. See PC-001. |
| P03-T01/P03-T02: safe hosted transition | Partial | Protection uncertainty, owner approval, rollback, manual dispatch, and hosted-only controls are handled safely. The plan's “once for final PR revisions” wording does not state that the current pull_request trigger runs on matching PR updates. See PC-002. |
| Test ownership and change limits | Covered | The candidate limits new orchestration tests, allows narrowly bounded infra contract updates, prohibits existing test removals, and preserves the existing container helper. |

## Verdict

* Verdict: Revise
* Rationale: The candidate is substantially safe and unusually explicit about preserving unique coverage, owner approval, and hosted-only controls. Before it is ready for implementation, the receipt must establish that tested candidate inputs are exactly those in the committed source, and the hosted-run cadence must be stated accurately so cost expectations do not imply a single run per PR when the current trigger runs on matching PR updates.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Receipt verification omits untracked candidate inputs

* Related IDs: P01-T02, P02-T01; FR: source-bound receipt and no uncommitted work at push
* Evidence: .copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md states that verification rechecks “clean tracked state” and binds a full tracked-tree SHA. .copilot-tracking/plans/details/2026-10-18/local-rpi-validation-phase-details.md likewise requires tracked content not to change mid-run. Both leave untracked candidate source, tests, or configuration outside the receipt identity. The proposed output directory is already outside the checkout.
* Concern: A newly added but untracked module or test can affect imports, package discovery, configuration, or test results while HEAD and the tracked-tree hash remain unchanged. The subsequent push contains only committed files, so the receipt could authorize a different source state than the one tested.
* Impact: This breaks the central exact-source assurance promised by the local gate and can allow a passing receipt to precede a push whose committed tree was not the tree actually validated.
* Smallest useful change: Require the gate and `--verify-receipt` to reject untracked candidate-input files as well as tracked modifications. Alternatively, run the matrix from a clean isolated checkout of the recorded HEAD. Keep outputs outside the checkout and avoid logging private path names. Explicitly define any harmless ignored/generated files that may remain without becoming test inputs.
* Action owner: Planning parent
* Exact resolving evidence: Revised plan/details specify the untracked-input or isolated-checkout rule; focused runner tests show an untracked source/test/config input blocks both receipt creation and verification, while permitted non-input scratch does not; a full matrix receipt is verified against the exact commit tree.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Hosted cadence is not explicit about matching PR updates

* Related IDs: P03-T02; owner requirement to reduce Actions spend
* Evidence: .github/workflows/src-ci.yml triggers on `pull_request` with path filters and does not restrict activity types to a final-only event. The plan describes one hosted run “on final PR revisions” and recommends final PR validation, but does not explicitly distinguish one consolidated run per matching PR update from one run total per PR.
* Concern: Under the current trigger, matching PR pushes/rebases can start the consolidated validator repeatedly. The plan's no-main-push proposal still reduces duplicate hosted workflows, but its cadence and savings should not be read as one hosted run per PR unless an approved trigger design actually provides that behavior.
* Impact: The owner could make a budget decision using an understated run count, and a proposed later trigger change could inadvertently affect required check availability or final-review evidence.
* Smallest useful change: State the expected policy as one consolidated hosted run per eligible PR update while retaining the existing trigger, and model savings using that cadence. If the intended policy is truly a single final run per PR, specify the trigger and required-check consequences as an owner decision before implementation; do not silently assume the current YAML behaves that way.
* Action owner: Planning parent
* Exact resolving evidence: The finalized plan explicitly names the chosen PR event cadence and a cost comparison based on its number of eligible updates; any final-only alternative is separately owner-approved with its required-check implications documented.
* Decision route: Direct planner correction for accurate cadence and estimate; significant or divergent user decision only if changing the PR trigger from the existing behavior

## Strengths and Residual Risk

* The candidate correctly retains the only real SQL Server contract gate, four source-image contracts and scans, SPDX generation, migration tests, and infrastructure validations rather than treating similar workflow names as equivalent coverage.
* Local tests are not represented as proof of GitHub required-check enforcement, OIDC, Azure approvals/what-if, deployment, publication, or real AI acceptance.
* The 403 response for protection/ruleset APIs is treated as unknown state that blocks removal of required jobs; no owner approval or settings change is presumed.
* The plan avoids claiming actual account remaining minutes or billed totals from job execution duration, and it keeps emergency local-only mode separate and approval-gated.
* Residual risk remains that local validation cannot eliminate changes between a final local check and merge; the plan acknowledges this and retains the hosted merge gate.

## Questions or Blocking Evidence Gaps

* No decision-critical evidence gap blocks critique. Live required-check configuration and actual billing remain unverified and are correctly identified as owner/implementation gates, not established facts.

## Limitations

* This critique did not inspect live GitHub branch protection/rulesets, billing records, Actions usage for managed workflows, or the VM. It did not run tests, workflow transitions, or any remote operation.
* Evidence was limited to the supplied planning artifacts and their directly relevant workflow, helper, test-fixture, and coordinator sources. No broader knowledge-base review was needed for this plan-credibility assessment.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: Planning parent
* Smallest next action: Amend the receipt contract to reject untracked candidate inputs (or execute from a clean checkout), then state the actual per-update hosted cadence in P03-T02.
* User response required: No for the direct plan clarifications. Yes only if the planner elects to change existing PR trigger semantics rather than retain the current per-update behavior.

| [.copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md](.copilot-tracking/plans/2026-10-18/local-rpi-validation-plan.md) | Candidate plan assessed |
| [.copilot-tracking/details/2026-10-18/local-rpi-validation-phase-details.md](.copilot-tracking/details/2026-10-18/local-rpi-validation-phase-details.md) | Candidate phase details assessed |
| [.copilot-tracking/reviews/plans/2026-10-18/local-rpi-validation-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/local-rpi-validation-plan-critique.md) | Complete final-candidate critique |

## Next Steps

The planning parent should resolve PC-001 and clarify PC-002 directly before finalizing the plan. No user action is required unless a change to the existing PR trigger behavior is proposed.
