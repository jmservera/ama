---
title: Orchestrator image resolution final-candidate plan critique
description: One bounded correctness assessment for task 322
ms.date: 2026-10-16
---

## Metadata

* Task ID: #322
* Slug: orchestrator-image-322
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/orchestrator-image-322-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/orchestrator-image-322-phase-details.md
* Critique execution status: Complete
* Review count: One bounded final-candidate assessment.

## Inputs and Criterion Boundary

* The supplied owner decision controls: an empty Bicep image selects the
  placeholder; the new deploy helper preserves an existing real job image,
  otherwise selects the newest registry tag, otherwise selects the placeholder,
  and prints its choice. No existing deploy helper is assumed.
* The implementation request includes offline tests and mutations, documentation,
  commit, push and PR publication with Refs #322 only. These are assessed as
  parent delivery requirements, not authorization for this critique to implement
  or publish.
* Primary evidence: the supplied plan and phase details; infra/main.bicep;
  infra/modules/containerapps.bicep; infra/modules/registry.bicep;
  infra/tests/test_bicep_policy.py; infra/README.md; and
  docs/adrs/0006-src-layout-and-cutover.md.
* Repository context: docs/case_study_48_original.md;
  docs/case_study_48_addendum.md, purpose and status;
  docs/reference/README.md; and docs/reference/memory.md.
* Criterion boundary: actionable correctness, requirement coverage, task
  sequencing, dependencies, acceptance evidence and delivery safeguards.
  Test ownership and scope are locked. Formatting preferences and unrelated
  architecture or application changes are excluded.
* No Azure calls, Docker execution, private data, .env, .vscode,
  .copilot-tracking/github-issues access, external research or other workers
  were used.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner decision: empty Bicep image means placeholder | Covered | P01-T01 changes the main parameter default and conditional module argument; P01-T02 and acceptance criteria require compiled default, empty, tag and digest checks. |
| Existing real image before registry before placeholder | Covered | Functional Requirements require all three target jobs, ignoring placeholders, rejecting conflicting real images, and ordering registry tags by update time. |
| Discovery identity and deployment identity agree | Covered | Functional Requirements require explicit workload/environment and protected final parameters; P01-T01 specifies exact job names and explicit resource-group/registry/environment scope. |
| Absence differs from query failure | Covered | P01-T01 permits registry absence, no tags and named repository-not-found fallback while requiring authorization, networking and malformed-output failures to stop deployment. |
| Explicit image and printed selection | Covered | Functional Requirements include intentional explicit placeholder selection; details require source, final image and a placeholder warning before deployment. |
| P01-T01 implementation boundary | Covered | main.bicep currently forwards its placeholder-valued parameter directly. The module has three orchestrator-image consumers. One new standard-library helper plus the entrypoint change fits the two-production-file limit without application changes. |
| P01-T02 locked test ownership | Covered | infra/tests/test_deploy.py owns actual-CLI fake-az tests; infra/tests/test_bicep_policy.py owns compiled assertions. Existing compile/evaluate helpers and job assertions are available to extend. |
| P02-T01 validation and mutation evidence | Covered | Acceptance criteria require default, fallback and resolver mutations to fail intended assertions; details require read order, no deployment on failure, final argument checks, infra suite, local compilation, Ruff and mypy. |
| P02-T01 documentation | Covered | README deployment examples and raw-Bicep semantics, append-only KB log and index routing pointer are explicitly included. |
| P02-T02 delivery and dependencies | Covered | Implementation precedes validation and one post-implementation Review; privacy-safe identity, normal push and main-targeted Refs #322 PR follow. Hosted checks and owner merge remain separate. |
| Deferred pipeline and operational acceptance | Covered | Pipeline #138, Azure deployment, private data and application/image-build changes remain outside scope. |

## Verdict

* Verdict: Pass
* Rationale: The candidate is credible for implementation within its locked
  scope. It covers the owner-directed bootstrap/redeploy distinction, discovers
  across the actual three image consumers, fails closed on conflicting images
  and query failures, and prevents parameter forwarding from changing the
  identity used for discovery. Offline subprocess tests, compiled wiring checks
  and mutations provide complementary acceptance evidence.

## Findings

No actionable findings. This is the complete finding set for the supplied
boundary: Critical 0, High 0, Medium 0, Low 0. No PC-xxx correction or unresolved
user decision is required.

## Strengths and Residual Risk

* The owner explicitly resolves the apparent tension between preserving real
  images through the helper and retaining placeholder semantics for empty raw
  Bicep input. Changing Bicep to discover images would contradict that decision.
* Conflicting real images require explicit operator selection rather than an
  arbitrary winner. The helper's explicit-image path also preserves the owner's
  ability to intentionally choose the placeholder.
* Existing module names are job-${prefix}-orchestrator,
  job-${prefix}-auth-renewal and job-${prefix}-ledger-verify, with prefix derived
  from workload and environmentName. The plan requires exact-name discovery,
  not an unsafe first-job or substring match.
* Existing compiled job assertions cover auth-renewal and ledger-verify.
  Requiring all three consumers in the candidate acceptance criteria supplies
  the additional orchestrator assertion without changing test ownership.
* Offline validation cannot prove live permissions, private registry
  connectivity or deployment success. The plan correctly separates those
  operational concerns from local acceptance and does not authorize Azure
  execution.
* Implementation must honor the supplied workspace-only file-operation
  constraint when creating disposable fixtures, generated templates and the
  pip venv. Existing test helpers use TemporaryDirectory, so their execution
  must use a project-local scratch root rather than the system temporary root.
  This is an execution constraint, not a change to locked test ownership or scope.

## Questions or Blocking Evidence Gaps

None within the supplied criterion boundary. The caller's owner decision is
sufficient; retrieving the issue again is unnecessary.

## Limitations

* This is a plan assessment, not implementation acceptance. No tests,
  compilation, mutations, Azure discovery or deployments were executed.
* The absence of a deploy helper is supplied context and agrees with the
  inspected infra/scripts inventory. No open-ended repository research was
  performed.
* The current worktree contains the supplied untracked plan and details.
  They were not altered, staged, moved or committed. No other artifact is
  written by this critique.
* A Pass does not establish that future code satisfies the plan; the prescribed
  post-implementation Review must assess actual test and mutation evidence.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Active rpi-quick planning parent.
* Smallest next action: Record this passing critique disposition and continue
  the confirmed implementation request under P01, preserving locked test
  ownership and scope.
* Resolving evidence for delivery: The implementation diff, passing offline
  resolver and compiled-template tests, failing intended mutations, Ruff/mypy
  results, updated documentation and one post-implementation Review, followed
  by the Refs #322 PR. These remain future delivery gates, not open findings.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/orchestrator-image-322-plan.md](.copilot-tracking/plans/2026-10-16/orchestrator-image-322-plan.md) | Assessed final-candidate plan, unchanged |
| [.copilot-tracking/details/2026-10-16/orchestrator-image-322-phase-details.md](.copilot-tracking/details/2026-10-16/orchestrator-image-322-phase-details.md) | Assessed implementation and delivery details, unchanged |
| [.copilot-tracking/reviews/plans/2026-10-16/orchestrator-image-322-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-16/orchestrator-image-322-plan-critique.md) | Complete bounded critique and finding set |

## Next Steps

The active parent may finalize the plan and proceed to implementation, tests,
mutations, documentation, one post-implementation Review and authorized
commit/push/PR publication. No second critique or user response is required.
This worker stops after delivering the critique.
