---
title: "RPI Plan Critique: Fabric PR 558 reconciliation"
description: Single independent final-candidate assessment of the bounded local reconciliation plan
ms.date: 2026-10-30
---

## Metadata

* Task ID: 558
* Task slug: fabric-rebase-558
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/fabric-rebase-558-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/fabric-rebase-558-phase-details.md
* Critique execution status: Complete
* Assessment count: exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: full RPI loop for the authorized local rebase of docs/fabric-rebase-558, tracking jmservera/fabric-research for PR 558. Preserve both documentation sides, append-only log, index, upstream rubric and manifest. Restrict changes to documentation/tracking, use src source and externally owned package tests, reuse the specified existing interpreter with local import precedence, run focused static/unit validation, and retain original critique/Review evidence.
* Authority boundary: this assessor may write only this artifact. No implementation, rebase, Git mutation, tests, installation, Azure operation, publication, merge or remote lifecycle change was performed. No prohibited issue-closing keyword is requested.
* Research considered: .copilot-tracking/research/2026-10-30/fabric-rebase-558-research.md, including Q1-Q3, C1-C7 and W1. W1 is supplied research evidence, not freshly verified GitHub metadata.
* Referenced evidence read: docs/case_study_48_original.md; relevant opening context in docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md; docs/reference/method/tracking-retention-policy.md; src/README.md; src/core/pyproject.toml; src/api/pyproject.toml; .github/workflows/src-ci.yml; relevant src/core/tests/test_scenario_manifest.py and tools/rename-zava-tests.py content.
* Read-only Git evidence: branch/status, original commit file list and shared-document patches, tracking configuration, current origin/main identity, and changes since the research base. These are local observations, not a network refresh.
* Decisions and dependencies assessed: P01 before P02; one critique and one independent Review; AC1-AC7; seven new tracking records; no new tests/helpers/features; local Conventional Commit with authenticated privacy-safe identity and required coauthor trailer; publication receipt and exact-head publication assessment deferred to an authorized coordinator.
* Assessment boundary: credibility of the supplied plan and its requirements, preservation predicates, validation selection and shared-environment safeguards. This is not an implemented-candidate Review, execution result, fresh product research or publication approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C5, W1, P01-T01, AC1/AC7 | Partial | Branch and tracking match; live local base differs from the details' named base. PC-001. |
| Q2, C3-C5, P01-T01, AC2 | Covered | Upstream log must remain an exact prefix; original Fabric block and both Fabric index additions must survive; upstream navigation and single frontmatter date retained. |
| C5-C6, P01-T01, AC3 | Covered | Original six standalone documents protected; rubric tree and scenario manifest must equal selected main, regardless of whether a conflict occurs. |
| Q3, C1/C6/C7, P02-T01, AC4 | Partial | Component static checks, local-origin guards and focused units are appropriate; filesystem output confinement is incomplete. PC-002. |
| Source/test ownership and locked budget | Covered | No executable changes, new tests, removals or helper framework; tests remain in src/core/tests and src/api/tests. |
| Heavy-lock and environment safeguards | Partial | Full API discovery is unnecessary and excluded; existing editable installs must not be mutated. Migration temporary-file handling needs PC-002. |
| P02-T01, AC5 | Covered | Exact commands, exits, skips, adverse attempts and original independent Review must be retained. |
| AC6 | Covered | New local Conventional Commit, noreply author/committer, trailer, final status/ancestry and unchanged remote branch required; no amend or push. |
| AC7 and publication boundary | Covered | Local readiness is explicitly separate from publication receipt, hosted checks, exact-head publication assessment and human merge approval. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 0 High, 2 Medium, 0 Low.
* Rationale: the preservation strategy and focused validation budget are credible, but the implementation base needs an unambiguous binding and validation must not implicitly write to prohibited/shared locations.
* Bounded readiness: suitable for direct planner correction, not implementation-ready as written. Neither finding requires a new owner decision, broader suites, cloud work or publication. The parent should disposition this complete finding set without commissioning another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Bind the reconciliation and preservation checks to one refreshed main identity

* Related IDs: Q1, C5, P01-T01, AC1-AC3, AC7.
* Evidence: .copilot-tracking/details/2026-10-30/fabric-rebase-558-phase-details.md:20-22 names 91e890e07af036263316c153cbc7ceff780cdaa2 as fetched main. Read-only inspection resolves current origin/main to ffd8f35e63b24905b9aeb937dbf2a7fe9968747f, two commits later. Their only changed path is docs/capstone/thought-leadership/everything-but-the-software/anc/package-lock.json. The plan requires fetched/current main but does not state how this drift changes the execution baseline.
* Concern: the historical research base, execution base and moving origin/main reference are not explicitly separated. Rebase against the old literal could miss AC1; preservation checks against different base identities could support inconsistent claims.
* Impact: an otherwise correct documentation reconciliation could be presented as current-main-ready using stale or mixed evidence.
* Smallest useful change: retain the original research identity as historical evidence. Require the parent to refresh origin/main under existing authority, capture one execution BASE_SHA, compare changes since the research base, and use that identity consistently for rebase, log-prefix/index preservation, upstream tree equality and final ancestry. Detect later ref movement and report/reconcile it before claiming current-main readiness. The observed lockfile-only drift does not justify expanding the selected component tests.
* Action owner: planning parent; implementation parent records the actual refreshed identity and results.
* Exact resolving evidence: revised P01 details distinguish historical and execution bases and bind checks to BASE_SHA; the later changes record contains fetch/result identity, bounded drift inspection, main-ancestry result and preservation comparisons against that same SHA. Do not rewrite the original research observation.
* Decision route: direct planner correction. Existing owner direction already authorizes fetching and rebasing current main; no significant or divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make validation filesystem writes explicit and safe

* Related IDs: C3, C7, P02-T01, AC4-AC6, locked validation budget.
* Evidence: .copilot-tracking/details/2026-10-30/fabric-rebase-558-phase-details.md:50-55 requires unspecified external mypy caches and the migration runner. .copilot-tracking/plans/2026-10-30/fabric-rebase-558-plan.md:138 also places validation outputs externally. tools/rename-zava-tests.py:73 and subsequent tests use tempfile.TemporaryDirectory() without a directory argument. The supplied execution constraints forbid new writes in system temporary locations and require newly created intermediates to be project-relative.
* Concern: the commands do not constrain temporary-file defaults, caches or bytecode output. In particular, running the migration runner as described can create files under the system temporary root. Reusing the authorized existing /tmp/mv interpreter does not authorize creating scratch outputs there or modifying its shared installations.
* Impact: the required validation can violate filesystem/shared-environment safeguards despite passing. Ad hoc output handling can also defeat the clean final-candidate and finite change-budget claims.
* Smallest useful change: replace the unspecified external-output instruction for this local task with an explicit finite task-owned, repository-relative validation-output location. Before running validation, set TMPDIR for the migration subprocess, disable or redirect bytecode and Ruff caches, and bind distinct mypy cache paths to the owned location. Keep generated outputs out of the committed deliverable and identify only the newly created owned paths eligible for cleanup; preserve existing tracking, adverse evidence and unrelated files. Do not change test source or reinstall shared editable projects.
* Action owner: planning parent; implementation parent owns runtime setup and evidence.
* Exact resolving evidence: revised P02 details name the output/cache policy and subprocess environment; the later changes record contains effective tempfile/cache paths, exact commands/exits and bounded owned-output accounting, plus final status showing no unintended candidate changes. A default system-temporary-directory run does not resolve this finding.
* Decision route: direct planner correction to comply with existing constraints, not a significant or divergent user decision. No additional heavy suite, dependency installation or shared-lock intervention is requested.

## Strengths and Residual Risk

* The log predicate is stronger than heading presence: complete upstream bytes remain a prefix and the original Fabric suffix is appended intact, followed by the new reconciliation entry. Compare against original f009d37faea91c2b164f9de1dcb55860c1f5cc03, not a reconstructed prose summary.
* The index must retain both original Fabric additions: the opening assessment paragraph and the research-table row. Preserve all upstream additions and its duplicate-frontmatter repair, allowing only the planned single date update and Fabric insertions. Git's automatic merge alone is not evidence that these predicates pass.
* The six byte-protected paths are the assessment at docs/reference/research/microsoft-fabric-fit-assessment.md, the parent research at .copilot-tracking/research/2026-10-29/microsoft-fabric-project-fit-research.md, and the four original fabric-*-subagent-research.md files listed by the original commit under .copilot-tracking/research/subagents/2026-10-29/. The supplied original commit enumerates their finite membership.
* Upstream equality covers the complete .github/rubric tree, including membership, and docs/reference/research/retrofit-synthetic-data/scenario-manifest.json. It must not be limited to conflicted files or repaired by changing the manifest's pinned hashes.
* Existing scenario-manifest and separate core/API dependency-rule modules provide relevant regression coverage. Execute each identically named dependency module in its owning project context and verify resolved local source/test origins first. No additional source or test change is justified.
* Full API discovery is explicitly unnecessary. Its omission is scope selection, not a failed test or a complete-suite claim. Do not acquire or disturb a foreign heavy-lock holder merely for this candidate.
* The seven-file tracking allowance is internally coherent. Original research and adverse critique/Review outcomes remain immutable. No cleanup authority over historical material follows from this task.
* Required shared-vhost, SQL, browser, scanner, hosted and human approval evidence remains unclaimed. The local candidate can become ready for coordinator handoff, not authorized for publication or acceptance.

## Questions or Blocking Evidence Gaps

* No unresolved owner choice. Both findings can be resolved directly by the planning parent.
* Actual rebase conflicts, installed-tool execution, source-origin verification and validation results remain implementation evidence, not facts established by this critique.

## Limitations

* No network refresh, tests, rebase, commit, receipt verification or fresh hosted check observation was performed.
* Product/regulatory claims in the preserved Fabric assessment were not re-researched; preserving their dated qualifications is the selected task.
* Git ref observations are time-bound to this critique. PC-001 requires implementation-time binding rather than assuming these observations remain current.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: revise P01 base binding and P02 output confinement, disposition PC-001/PC-002 in the plan, then proceed through the already-authorized parent loop.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/fabric-rebase-558-plan.md](../../../plans/2026-10-30/fabric-rebase-558-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/fabric-rebase-558-phase-details.md](../../../details/2026-10-30/fabric-rebase-558-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-30/fabric-rebase-558-research.md](../../../research/2026-10-30/fabric-rebase-558-research.md) | Supplied original research |
| [.copilot-tracking/reviews/plans/2026-10-30/fabric-rebase-558-plan-critique.md](../../../reviews/plans/2026-10-30/fabric-rebase-558-plan-critique.md) | This single independent critique |

## Next Steps

The active planning parent should resolve both planner-direct findings and finalize without another critique. No user action is required. This assessor stops here; no implementation or publication action is authorized by this artifact.
