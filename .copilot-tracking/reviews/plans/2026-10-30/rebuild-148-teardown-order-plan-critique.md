---
title: Rebuild teardown dependency plan critique
description: Independent final-candidate assessment for the bounded PR 511 ordering correction
ms.date: 2026-10-30
---

## Metadata

* Task ID: pr-511-teardown-order-2026-10-30
* Task slug: rebuild-148-teardown-order
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/rebuild-148-teardown-order-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/rebuild-148-teardown-order-phase-details.md
* Critique execution status: Complete
* Assessment count: one independent final-candidate critique; no nested delegation.

## Inputs and Criterion Boundary

* Caller requirements: fix the quoted PR #511 finding on feat/rebuild-148,
  Refs #148; preserve safety behavior; add an orchestrator regression; run
  Ruff lint, Ruff formatting, mypy and complete orchestrator tests using the
  prescribed environment; preserve dated RPI evidence and commit locally with
  a Conventional Commit and Copilot trailer. No push or Azure access.
* Research considered:
  .copilot-tracking/research/2026-10-30/rebuild-148-teardown-order-research.md,
  especially C1-C6.
* Candidate considered: the exact plan and phase-details paths above, including
  FR1-FR3, AC1-AC5 and P01-T01 through P02-T02.
* Source checked:
  src/orchestrator/src/zava_forward/orchestrator/rebuild.py,
  src/orchestrator/tests/test_rebuild.py and infra/modules/edge.bicep.
  src/orchestrator/pyproject.toml and src/orchestrator/README.md confirm the
  component check configuration and source-only documentation boundary.
* Selected decision: profile tier 1, environment tier 2, apps/jobs tier 0
  and WAF tier 3. No graph, generated targets or fixture expansion.
* Change budget: no test removals; at most one new test method plus assertions
  in one existing method. Canonical source/test targets remain locked.
* Boundary: assess implementation credibility and executable validation
  prerequisites, not live Azure deletion, all issue #148 criteria, historical
  findings or the complete publication gate. No implementation or validation
  was performed during this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2, FR1 | Covered | The sorter compares tier before depth and lowercased ID; the Bicep origin targets environmentId through sharedPrivateLinkResource. Moving the profile to tier 1 resolves the reported tie. |
| C3, C5, AC1-AC2, P01-T01 | Covered | One test method can exercise both input permutations with a fresh MemoryBackend each time, mixed-case kind, exact resource deletion order and empty final inventory. It must compare against an independently specified expected sequence. |
| FR2, P01-T02 | Covered | A single ORDER-entry change leaves canonical admission, readback checks, budgets and other tiers intact. Existing dependency and safety tests remain in scope. |
| FR3, AC3 | Covered | dry_run derives its advertised kinds from ORDER; extending test_cli_dry_run_no_workspace_or_backend_reads covers the second affected surface without another test method. |
| C4, C6, AC4, P02-T01 | Partial | Current-worktree package provenance is recognized, but the prescribed installation and test execution conflict with the execution environment's filesystem restrictions; PC-001. |
| AC5, P02-T02 | Covered | One original independent Review, local commit, actual identity readback and required trailer are specified. Review findings remain visible rather than being erased by a repeated Review. |
| Scope, dependencies and change budget | Covered | Targets are canonical and bounded; package setup is explicitly required before P01 test execution, even though its fuller description is in P02. |
| Publication and historical evidence boundary | Covered | The plan expressly excludes push, Azure, issue closure and publication-gate acceptance; historical findings remain unchanged. |

## Verdict

* Verdict: Revise
* Rationale: the source correction and regression design are credible and
  appropriately small. The candidate must explicitly reconcile a concrete
  validation execution blocker instead of treating its prescribed environment
  as available for installation and complete test execution.
* Severity summary: 0 Critical, 1 High, 0 Medium, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Prescribed validation requires prohibited filesystem operations

* Related IDs: C4, C6, AC1, AC4, P01-T01, P02-T01.
* Evidence: the supplied execution environment prohibits file operations under
  /tmp and temporary directories. The plan requires installing the current
  core/orchestrator packages into /tmp/mv, and the details require using that
  environment for the complete component checks. In addition,
  src/orchestrator/tests/test_rebuild.py uses tempfile.TemporaryDirectory for
  SQLite regressions, and the synthetic CLI in
  src/orchestrator/src/zava_forward/orchestrator/rebuild.py creates a temporary
  workspace. Research reports that the prescribed environment is not already
  correctly installed.
* Concern: this is not only a missing-package setup action. The specified
  installation and full test execution cannot be carried out under the current
  filesystem restrictions. Neither a different virtual environment nor redirected
  temporary storage may silently be treated as fulfilling the user's exact
  validation request.
* Impact: implementation could otherwise be reported as locally validated or
  complete without executable evidence for the mandatory checks. The complete
  test command also has workspace-creation behavior absent from the in-memory
  ordering regression.
* Smallest useful change: the planning parent must mark the affected validation
  steps and AC4 as blocked by the execution boundary, distinguish any genuinely
  permitted checks from unperformed checks, and prevent an all-criteria-complete
  closeout. Preserve the requested commands as requirements; do not install,
  access or execute under the prohibited paths, rewrite the suite, or silently
  substitute an environment to bypass the restriction.
* Action owner: planning parent.
* Exact resolving evidence: revised plan/details explicitly record the blocked
  installation and complete-suite prerequisite and the resulting incomplete AC4
  status. Eventual AC4 satisfaction requires an execution context that permits
  the requested operations, verified current-worktree package provenance and
  actual zero-exit output for all four required checks; absent that evidence,
  validation remains blocked and must be reported as such.
* Decision route: direct planner correction to execution/readiness reporting.
  No new user choice is needed to acknowledge the blocker, and user approval
  must not be presented as overriding the filesystem restriction.

## Strengths and Residual Risk

* Distinct consumer/target tiers are sufficient for this fixed modeled contract;
  a dependency graph is unnecessary for the supplied finding.
* Forward/reversed inventories and mixed casing fit the single-method test
  budget. Exact expected ordering, actual backend deletions and empty readback
  jointly exercise the sorter and executor rather than only ORDER constants.
* The dry-run assertion is a useful independent regression surface. Both it and
  the new dependency test should fail on the original tier map.
* The local fixture remains at ten resources; the new test supplies the missing
  profile/WAF coverage without changing fixture scope.
* No live Azure deletion or managed Private Link cleanup is established.
  This residual limitation and the historical publication blockers are explicitly
  outside the local commit claim.
* An original Review may record unresolved findings; committing that evidence
  locally must not be described as Review acceptance when its outcome says
  otherwise.

## Questions or Blocking Evidence Gaps

* No unresolved design decision for the ordering correction.
* Permitted execution of the prescribed validation is not established.
  PC-001 is the complete actionable finding set for this supplied boundary.

## Limitations

* This is a read-only assessment of the candidate and named source, not a
  failing-first run, implementation Review or validation receipt.
* Package-state observations and PR lifecycle are supplied research evidence;
  no /tmp access, package installation, Azure access or remote mutation occurred.
* Only this critique artifact was added. Research, plan, phase details, source
  and session state were not modified.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: record the validation execution blocker and affected
  acceptance status directly, then continue only permitted work with explicit
  incomplete validation reporting. Do not repeat this critique.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/rebuild-148-teardown-order-research.md](.copilot-tracking/research/2026-10-30/rebuild-148-teardown-order-research.md) | Supplied focused research, C1-C6. |
| [.copilot-tracking/plans/2026-10-30/rebuild-148-teardown-order-plan.md](.copilot-tracking/plans/2026-10-30/rebuild-148-teardown-order-plan.md) | Assessed final candidate. |
| [.copilot-tracking/details/2026-10-30/rebuild-148-teardown-order-phase-details.md](.copilot-tracking/details/2026-10-30/rebuild-148-teardown-order-phase-details.md) | Assessed execution details. |
| [.copilot-tracking/reviews/plans/2026-10-30/rebuild-148-teardown-order-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/rebuild-148-teardown-order-plan-critique.md) | This original independent critique. |

## Next Steps

The active planning parent owns the direct PC-001 correction and truthful
validation status. No user action is required. This critique stops here; it
does not implement, modify planning inputs, launch another review or authorize
prohibited filesystem operations.
