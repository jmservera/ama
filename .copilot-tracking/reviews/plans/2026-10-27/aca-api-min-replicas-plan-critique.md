<!-- markdownlint-disable-file -->
---
title: API minimum replicas independent plan critique
description: Original final-candidate assessment of implementation and offline validation
ms.date: 2026-10-27
---

# RPI Plan Critique: API minimum replicas

## Metadata

* Task ID: aca-api-min-replicas-2026-10-27
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate critique; original verdict retained here.

## Inputs and Criterion Boundary

* Caller requirements: replace only the shared API minimum hardcode with an integer
  parameter defaulting to 0; permit explicit production 2; forward through main and
  three parameter examples; update related documentation/tests and preserve other
  infrastructure.
* Canonical research: .copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md,
  including C1-C9, accepted alternatives and publication limitation.
* Canonical candidate: the plan and phase details named above, including P01-T01,
  P01-T02, P02-T01, acceptance criteria and locked test ownership.
* Direct corroboration: infra/modules/containerapps.bicep, infra/main.bicep,
  infra/tests/test_bicep_policy.py, infra/tests/test_resident_demo_deploy.py,
  infra/README.md quality gates and src/README.md local RPI gate.
* Repository context: original case study, addendum, reference index and owner
  memory read; none is treated as evidence of deployed scaling behavior.
* Execution constraints: existing offline infra tests and local Bicep build/lint
  only; no full gate, live what-if, deployment, secret access, uv, external
  temporary storage or prohibited system temporary-directory writes.
* Boundary: assess implementation credibility, verification feasibility,
  preservation, dependencies and honest local/publication readiness. No runtime,
  cost, deployed-state or publication acceptance is established.
* Worktree inspection: fix/aca-api-min-replicas; tracked inputs unchanged.
  Existing untracked research, plan, details and state are supplied task evidence,
  not unrelated work to discard or move.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Default 0, explicit 2; C1, Q3, P01-T01 | Covered | Integer default and bounds 0..4 in both schemas; scale uses parameter. |
| Complete forwarding; C2-C3, Q1, P01-T01 | Covered | Main module params and all three committed examples explicitly addressed. |
| Production independence; C3-C4, P01-T02 | Covered | Security profile remains independent; private production override and cold starts documented. |
| Preserve other infrastructure; C1, C7, P01 | Covered | Max 4, concurrency 50, probes, agents, jobs and standalone resident scale explicitly retained. |
| Compiled semantic checks; C6, P01-T02 | Covered | Main/module schemas, forwarding evaluation for 0/2 and compiled example values required. |
| Test ownership and removals; C6-C7 | Covered | Two stale assertions replaced, no methods removed, at most two new policy methods. |
| Offline execution feasibility; C9, P02-T01 | Partial | PC-001: storage instructions conflict with execution constraints and existing tempfile usage. |
| Dependencies and validation claims; C5, C9, P02 | Covered | Existing helpers/tools, conditional pip only, no wrapper changes or live what-if claims. |
| Publication dependency; C8, acceptance criteria | Covered | Local implementation/commit separated from blocked push/PR; full gate is not bypassed. |
| Dated evidence and independent Review | Covered | Candidate calls for original critique, changes and one post-implementation independent Review. |

## Verdict

* Verdict: Revise
* Rationale: the functional design and bounded regression strategy are credible.
  One execution-path correction is required before following the validation
  instructions in this environment. It is planner-owned and does not change
  owner-selected functionality or authorize broader validation.
* Severity summary: Critical 0; High 0; Medium 1; Low 0.
* Publication remains Blocked independently of this planning verdict.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Make validation storage comply with the execution boundary

* Related IDs: P02-T01; locked generated-target contract; offline validation
  acceptance criterion; C9.
* Evidence: .copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md:126
  specifies a disposable external venv and :138 permits external temporary
  storage. .copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md:67-72
  gives unqualified discovery and external disposable-environment instructions.
  infra/tests/test_bicep_policy.py:305-306 and
  infra/tests/test_resident_demo_deploy.py:173 create temporary directories
  without choosing a project-relative location. Current execution instructions
  prohibit system temporary-directory writes and require project-relative
  intermediate files.
* Concern: the candidate permits a forbidden storage path and does not ensure
  that existing Python tempfile consumers avoid prohibited default locations.
  The dependency-install branch has the same external-storage mismatch.
* Impact: otherwise correct implementation can encounter denied writes or
  violate the execution boundary during mandatory offline discovery; the
  candidate cannot yet substantiate its validation completion criterion.
* Smallest useful change: revise only the plan/details validation instructions
  to use an explicitly selected project-relative working area for permitted
  intermediates and any conditionally needed venv. Configure Python tempfile
  resolution for the discovery process and inherited subprocesses to remain
  within that area, with no fallback to prohibited locations. Require Bicep
  build/build-params output on stdout. Preserve the existing test ownership,
  test count and dependency-install-on-failure rule; do not rewrite the
  existing tests merely to relocate their working files.
* Action owner: planning parent.
* Exact resolving evidence: matching P02-T01 instructions in the canonical
  plan and phase details identify the project-relative working path,
  tempfile-routing environment and stdout-only Bicep output, and remove
  external temporary/venv instructions. Subsequent implementation evidence
  records the effective storage configuration and exact existing discovery
  command/result without prohibited-directory writes, generated ARM in git,
  weakened tests or a full-gate claim. No test execution is required to
  record this planner correction.
* Decision route: direct planner correction. Existing instructions already
  resolve the storage choice; no significant/divergent user decision required.

## Strengths and Residual Risk

* The default and production paths are tested semantically rather than solely
  by matching Bicep text, using existing compiled-template helpers.
* Test preservation is explicit: existing edge/probe checks and standalone
  resident isolation remain, with only the obsolete minimum assertions replaced.
* Bounds match the unchanged maximum, and security profile selection does not
  silently introduce always-on cost.
* Cold-start latency and actual cost/runtime behavior remain unmeasured under
  the accepted no-deployment boundary; documentation must not imply otherwise.
* The no-full-gate instruction and mandatory infrastructure publication gate
  are correctly treated as a publication blocker, not as permission to push
  after scoped tests. This is not an additional plan defect.

## Questions or Blocking Evidence Gaps

* No unresolved functional decision or decision-critical research gap.
* Publication requires later authorization and satisfaction of the mandatory
  gate and exact-head assessment; no bypass is proposed.

## Limitations

* Read-only assessment of supplied evidence and directly relevant local code.
  No tests, builds, dependency installation, cloud calls or secret reads run.
* The caller's clean pre-evidence branch statement is consistent with the
  current tracked-clean/untracked-evidence inspection; no historical clean
  state was independently reconstructed.
* This critique does not replace implementation verification or independent
  exact-head Review. Plan, details, research, state and source remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: reconcile the P02-T01 storage instructions in plan
  and details, disposition this original finding, then finalize planning
  without another critique.
* User response required: No for the planner correction or scoped local
  implementation; publication remains blocked under the existing scope.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md](.copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md) | Canonical research and C1-C9. |
| [.copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md](.copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md](.copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md) | Assessed task details. |
| [.copilot-tracking/reviews/plans/2026-10-27/aca-api-min-replicas-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/aca-api-min-replicas-plan-critique.md) | Original independent critique and complete finding set. |

## Next Steps

The active planning parent should resolve PC-001 directly, preserve this original
Revise outcome, record its disposition and finalize without another critique.
No user action is required for that correction. Stop this critique here;
push/PR remain blocked while the required full gate is outside authorized scope.
