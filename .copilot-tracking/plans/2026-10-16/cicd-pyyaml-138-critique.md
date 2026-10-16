---
title: CI infra dependency repair final-candidate critique
description: One bounded assessment of PR 357 planning for Refs 138
ms.date: 2026-10-16
---

## Metadata

* Task ID: 138-ci-pyyaml, PR #357, Refs #138.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/cicd-pyyaml-138-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/cicd-pyyaml-138-phase-details.md
* Critique execution status: Complete.
* This is one final-candidate assessment, with no further agents or critique loop.

## Inputs and Criterion Boundary

* Read the complete supplied plan, phase details and research:
  .copilot-tracking/research/2026-10-16/cicd-pyyaml-138-research.md.
* Read the relevant implementation evidence only:
  .github/workflows/mvp-validation.yml,
  .github/workflows/src-ci.yml and infra/tests/test_pipeline.py.
* Assess the authorized test-only PyYAML==6.0.3 choice, dependency-install
  ordering, dependency-removal regression, preservation of removed-control
  detection, clean-venv baseline followed by explicit pinned installation,
  integration dependencies, documentation, review and publication boundaries.
* The caller permits pinned PyYAML rather than requiring stdlib parsing.
  No user decision about that choice remains outstanding.
* No source changes, test executions, dependency installation, Azure access,
  private datasets, environment files, editor settings, retired-directory
  reads or issue updates were performed. Only this critique is written.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Research C1-C3; functional requirements; P01-T02 | Covered | Unconditional yaml import explains the missing prerequisite. The validate step lacks it; source namespace CI installs the exact pin before discovery. |
| Install ordering; P01-T02; test ownership | Covered | The candidate explicitly requires installation before discovery in both consumers. The current global source-CI substring assertions do not establish ordering; replacing or supplementing them with the planned shared ordering assertion is necessary implementation work, not evidence of an already-complete repair. |
| Dependency-removal detection; P01-T02 | Covered | Deep-copied workflow documents and removal from each consumer are explicitly required. Two test methods and one shared helper can cover both consumers with subtests. |
| Removed pipeline controls; research C5; P01-T02; P02-T01 | Covered | Existing deep-copy mutations reject write permissions, removed environment protection, hosted privileged runners, excess permissions, unpinned actions, secret echo and expression injection. The candidate preserves all of them and runs full discovery and targeted mutations. |
| Clean baseline then explicit test dependency; acceptance criteria; P02-T01 | Partial | The research reports 131 tests with one yaml import error using source packages only. The details prescribe reuse of a prohibited system temporary path; see PC-001. |
| Test-only scope; non-functional requirements; P01-T03 | Covered | The selected change belongs in the failing infra-test step, matching the existing source CI pin, with no production manifest or packaging change. The complete local recipe must document the same prerequisite. |
| P01-T01 integration dependency | Covered | Merge precedes repair and validation; both append-only log histories must survive without rewriting. Current branch matches the named workstream. Remote ancestry and PR lifecycle are supplied evidence, not independently refreshed here. |
| P01-T03; research C4; documentation | Covered | Complete recipe, existing reference routing and append-only log updates are included. README omission is reported research evidence, not separately inspected. |
| P02-T01 quality and local probe | Covered | Ruff/format, helper mypy and the real installed local API probe are required. The inspected probe uses constructed data and explicit local runtime configuration, rather than private working data. Scratch placement needs the PC-001 correction. |
| P02-T02 review and acceptance audit | Covered | One bounded review, explicit unexecuted checks and preservation of all six unmet live acceptance criteria prevent local tests from becoming Azure/OIDC acceptance claims. |
| P02-T03 publication | Covered | Existing PR reuse, privacy-safe local identity, required trailer, no force push, no merge and no issue checkbox updates are explicit. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0, High 0, Medium 1, Low 0.
* The dependency repair and regression strategy are credible. One direct
  planner correction is required before execution: replace the prohibited
  validation location and make the baseline-to-pinned-test sequence reproducible
  within the permitted workspace.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Validation details direct execution in a forbidden temporary location

* Related IDs: P02-T01; clean-venv acceptance criteria; research cycle step 2.
* Evidence: .copilot-tracking/details/2026-10-16/cicd-pyyaml-138-phase-details.md
  instructs installation into the already-created venv under
  `/tmp/ama-138-clean-e18c47d4`. The active execution constraints prohibit
  operations there and require scratch files to remain in the project.
  infra/tests/test_pipeline.py also uses TemporaryDirectory without an explicit
  directory, so relocating only the venv does not control test scratch placement.
* Concern: An implementer following the candidate literally would access a
  forbidden path. Reusing the reported baseline environment also leaves the
  final post-integration baseline dependent on an earlier environment's state.
* Impact: The specified validation cannot be executed as written under the
  active constraints, and the baseline-to-fixed comparison would not have a
  self-contained, repeatable setup.
* Smallest useful change: Revise P02-T01 and the planned local recipe to create
  a fresh, non-system-site-packages venv and scratch root using explicit
  project-relative paths. Set TMPDIR to that project-local scratch root for
  the validation processes and child processes. Install only the required
  editable source distributions first and run complete infra discovery,
  recording the expected yaml import failure. Then install PyYAML==6.0.3
  explicitly into that same venv and rerun the identical discovery command.
  Install separate lint/type tools only after this comparison. Preserve the
  earlier research result as historical reported evidence, not an instruction
  to revisit the prohibited location. Keep scratch untracked and clean it up
  after recording results.
* Action owner: Planning parent.
* Exact resolving evidence: Updated phase details specify the project-relative
  venv/scratch locations, propagated TMPDIR and exact ordered baseline/install/
  rerun commands. Implementation validation subsequently records the source-only
  dependency inventory, missing-yaml failure, explicit pinned installation and
  successful full discovery in the same interpreter, with expected local-only
  skips distinguished from executed tests. The discovery total may increase
  with new regression tests; do not hardcode the historical 131 count.
* Decision route: Direct planner correction. No significant or divergent user
  decision is required.

## Strengths and Residual Risk

* The chosen pin is already used by source CI and explicitly authorized.
  Retaining yaml.BaseLoader avoids an unnecessary bespoke parser and preserves
  the existing handling of the YAML on key.
* No ImportError skip or weaker structural validator is proposed.
* Existing source-CI wiring checks establish only string presence today.
  The planned assertion must scope installation and discovery to the executing
  job and compare their order, including command order within a multiline run
  step. Presence elsewhere in the workflow is not resolving evidence.
* At implementation review, inspect the diff for preservation of every existing
  control mutation and verify that each dependency-removal mutation invokes
  the same assertion used for the unchanged workflows. An expected assertion
  failure must demonstrate rejection, not silently bypass the check.
* Local checks cannot establish live OIDC/RBAC, environment approval, deployment,
  registry or runtime acceptance. The candidate correctly preserves this boundary.

## Questions or Blocking Evidence Gaps

* None requiring a user response. PC-001 can be resolved directly by the
  planning parent within the authorized approach.

## Limitations

* This is a plan credibility assessment, not implementation validation.
  The supplied baseline result was read, not independently reproduced.
* No remote branch/PR state, production dependency manifests, README contents
  or other evidence outside the bounded inputs and three relevant CI/test files
  was inspected. Those completion checks remain implementation responsibilities.
* Supplied untracked plan, details, research and state artifacts were left
  untouched. No existing critique content was read or incorporated.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: Planning parent.
* Smallest next action: Correct P02-T01's workspace-local baseline and pinned
  prerequisite sequence, then finalize the plan directly without another critique.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-16/cicd-pyyaml-138-plan.md | Complete candidate plan assessed |
| .copilot-tracking/details/2026-10-16/cicd-pyyaml-138-phase-details.md | Phase details containing PC-001 |
| .copilot-tracking/research/2026-10-16/cicd-pyyaml-138-research.md | Supplied dependency-failure evidence |
| .copilot-tracking/plans/2026-10-16/cicd-pyyaml-138-critique.md | This single final-candidate critique |

## Next Steps

The active planning parent should resolve PC-001 directly, retain the authorized
test-only pin and finalize without another critique loop. No user action is
required. This critique stops here and does not invoke implementation or review.
