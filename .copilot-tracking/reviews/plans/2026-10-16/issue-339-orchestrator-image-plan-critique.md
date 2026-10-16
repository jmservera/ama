---
title: Issue 339 orchestrator image plan critique
description: One bounded independent assessment of the final planning candidate
ms.date: 2026-10-16
---

## Metadata

* Task ID: issue-339
* Task slug: issue-339-orchestrator-image
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/issue-339-orchestrator-image-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/issue-339-orchestrator-image-phase-details.md
* Critique execution status: Complete
* Assessment count: one; no delegation or implementation.

## Inputs and Criterion Boundary

* Caller requirements: trim explicit whitespace-only input and resolve an empty
  result or reject it; offline validation only; no real Azure commands,
  setup-entra.py changes, legacy/private data, environment/editor configuration
  edits or GitHub issue tracking changes. Deliver README/log and RPI evidence,
  with a PR referencing `Refs #339` and no issue ticks.
* Primary evidence: supplied plan, phase details and
  .copilot-tracking/research/2026-10-16/issue-339-orchestrator-image-research.md;
  direct reads of infra/scripts/deploy.py and infra/tests/test_deploy.py.
* Required context: original case study, opening addendum context, reference
  index and owner memory. No regulatory or customer interpretation is needed.
* Decisions assessed: empty input follows existing discovery; normalization is
  explicit-input-only; existing authentication, discovery and exit behavior
  remain unchanged. P01-T02 follows P01-T01; critique gates implementation.
* Test ownership is locked to infra/tests/test_deploy.py, no removals and at
  most one additional test method, with existing methods expanded.
* Boundary: implementation readiness and planned evidence for AC1-AC5, not a
  claim of completed implementation, passing tests or operational acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Issue #339; AC1 | Covered | Current truthiness branch accepts whitespace. Stripping once before selection addresses the defect without a new image policy. |
| AC2 | Covered | Blank-input matrix includes existing-job and no-image outcomes, exact source and placeholder warnings. Existing registry precedence/error regressions remain. |
| AC3 | Covered | Padded explicit tag, digest and placeholder inputs must be trimmed and bypass image discovery, not the authentication guard. |
| AC4; P01-T01 | Covered | Both actions are required for blank-resolution cases, with exact forwarding and discovery sequence assertions; existing authentication and exit-code tests remain. |
| P01-T01 test budget | Covered | Static AST count is 19 existing test methods. Zero removals and maximum one addition permit a final count of 19 or 20; subtest expansion supplies the matrix. |
| AC5; P01-T02 | Covered | README, append-only log, changes/review/criterion evidence, published commit and PR URL are explicitly required; no merge or issue ticks. |
| Offline validation; P01-T01/P01-T02 | Partial | Fake az is isolated, but scratch placement and missing-tool provisioning need the constrained execution recipe in PC-001. |
| Research, dependencies and scope | Covered | Supplied source supports normal discovery rather than rejection. No new product decision, service change, live acceptance or expanded research is necessary. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 0; Medium 1; Low 0.
* The functional design and test ownership/budget are credible and simple.
  One execution-boundary correction is needed before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Pin workspace-local, offline validation provisioning

* Related IDs: P01-T01, P01-T02; non-functional requirements; AC5 evidence.
* Evidence: plan non-functional requirements, lines 57-59, prescribe pip
  installation of missing tools in an unspecified temporary venv.
  infra/tests/test_deploy.py:60 and :409 use TemporaryDirectory without a
  directory argument. Phase details require the full module but do not specify
  workspace-local scratch routing. Current execution instructions prohibit
  system temporary paths and require offline work.
* Concern: the candidate does not establish that tests and tool provisioning
  remain inside the worktree and offline. Unconfigured Python scratch creation
  can use a system temporary directory; unqualified pip installation can
  contact a package index. This is a missing execution safeguard, not evidence
  that a prohibited command has already run or that tools are unavailable.
* Impact: otherwise-correct regression evidence could be obtained through a
  prohibited path or network dependency.
* Smallest useful change: replace the unspecified provisioning instruction
  with a workspace-relative scratch/venv recipe. Route Python scratch through
  a command-scoped TMPDIR pointing into that workspace directory, without
  editing persistent environment configuration or adding a harness. Use
  installed tools first; only after a missing-tool failure, restore from
  locally available artifacts with network access disabled. Record a blocked
  tool check if no offline source exists. Clean up only task-created scratch.
* Action owner: planning parent.
* Exact resolving evidence: plan and phase details name the workspace-relative
  scratch/venv location, command-scoped scratch routing, offline-only fallback
  and missing-tool blocked disposition. Subsequent changes evidence records
  exact test/lint/format/type/help commands, outcomes and cleanup, without
  changing the locked test ownership, removals or method budget.
* Decision route: direct planner correction; no significant or divergent user
  decision is needed because the execution constraints are already explicit.

## Strengths and Residual Risk

* Normalizing only explicit input avoids changing discovery semantics or
  introducing validation unrelated to the issue.
* Existing assert_selection hardcodes what-if. The details correctly name
  run_deploy for the expanded action matrix, so apply can be exercised without
  weakening fake-command matching or adding a new harness.
* Red/green evidence must distinguish newly failing whitespace/padded subcases
  from unchanged empty/unpadded controls. Record method counts separately from
  matrix/subtest counts; no execution counts are claimed here.
* Live deployment is deliberately unperformed and outside acceptance. A fake
  `az` command named create is local simulation, not an Azure deployment.

## Questions or Blocking Evidence Gaps

* No unresolved product question. Tool availability remains untested, not an
  assumed failure; PC-001 defines how to handle either outcome.

## Limitations

* No tests, linters, installation, Azure, GitHub or publication commands were
  run. The only Python check parsed the existing test source to count methods.
* Remote branch/PR lifecycle and research assertions about prior PRs were not
  independently queried, consistent with the bounded offline assessment.
* Existing untracked planning inputs were preserved. Only this critique
  artifact was written; source plans, research and implementation are unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: correct the validation recipe directly, record its
  disposition and finalize the plan without another critique.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/issue-339-orchestrator-image-plan.md](.copilot-tracking/plans/2026-10-16/issue-339-orchestrator-image-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-16/issue-339-orchestrator-image-phase-details.md](.copilot-tracking/details/2026-10-16/issue-339-orchestrator-image-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-16/issue-339-orchestrator-image-research.md](.copilot-tracking/research/2026-10-16/issue-339-orchestrator-image-research.md) | Supplied research |
| [.copilot-tracking/reviews/plans/2026-10-16/issue-339-orchestrator-image-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-16/issue-339-orchestrator-image-plan-critique.md) | This independent critique |

## Next Steps

The active planning parent should resolve PC-001 directly and finalize the
candidate without another critique. No user action is required. This bounded
critique stops here; no implementation or peer stage was invoked.
