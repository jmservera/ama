---
title: Resident showcase batch selection plan critique
description: Independent final-candidate credibility assessment for task 521-pr590-batch-selection
ms.date: 2026-10-30
---

## Metadata

* Task ID: 521-pr590-batch-selection
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/resident-showcase-batch-selection-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/resident-showcase-batch-selection-phase-details.md
* Critique execution status: Complete
* Severity summary: Critical 0; High 0; Medium 2; Low 0.

## Inputs and Criterion Boundary

* Caller requirements: correct both stale render(USER)[2] calls using a small
  content-based helper; inspect every other indexed renderer use; prove rejection
  of the wrong batch; run focused file unit tests and Ruff check/format from
  src/core; preserve dated evidence and independent Review; create a local
  Conventional Commit with the required Copilot trailer and Refs #521 only.
  No push, Azure access, production changes, removed tests or more than two added
  test methods.
* Research: .copilot-tracking/research/2026-10-30/resident-showcase-batch-selection-research.md,
  C1-C5.
* Source evidence: src/core/tests/test_resident_showcase_sql.py;
  infra/sql/resident-showcase.sql; infra/scripts/resident_showcase_sql.py;
  src/core/pyproject.toml.
* Decisions and dependencies: content matching and single-match unpacking selected;
  HOME-A/[] distinguishes the optional-table projection; P01-T02 depends on
  P01-T01; SQL remains explicitly opt-in. The caller authorizes this critique
  artifact only, not implementation, execution, commits or delegation.
* Assessment boundary: assess the supplied candidate once against these
  requirements, research claims, tasks, acceptance criteria, dependencies,
  decisions and execution constraints. No open-ended research or operational
  acceptance assessment.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2; P01-T01; exact view selection | Covered | The only indexed renderer calls are at test module lines 357 and 373. The migration precedes the view batch; content selection removes that dependency. |
| C3; P01-T01; empty-table semantics | Covered | SQL fallback projects NULL/[]; the optional-table branch projects the body's HOME-A even with empty sensor tables. |
| C4; P01-T01; test ownership and coverage lock | Covered | Single-match unpacking already exists in the module; relocation and missing/duplicate cases fit two methods using subtests. No removals or production edits are planned. |
| P01-T02; wrong-batch rejection | Partial | A mutation experiment is required but its target, executable non-SQL path and expected failure are unspecified; PC-001. |
| C5; P01-T02; focused validation | Covered | Named unittest discovery and both Ruff commands match the requested file and working directory. SQL skips must be reported separately. |
| P01-T02; environment and heavy-run controls | Partial | The optional lock and dependency-restoration locations conflict with the current filesystem boundary; PC-002. |
| Local commit, evidence and independent Review | Covered | Plan records dated changes evidence, local Conventional Commit, required trailer, Refs #521, and one independent post-implementation Review. No push or Azure is authorized. |

## Verdict

* Verdict: Revise
* Rationale: The proposed correction is technically sound and appropriately
  bounded. Resolve two execution details before handoff: make the negative
  experiment falsifiable without silently depending on skipped SQL tests, and
  remove incompatible filesystem instructions. Neither needs a new user choice.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Define an executable wrong-batch rejection experiment

* Related IDs: C3, P01-T02, wrong-batch acceptance requirement.
* Evidence: The plan requires a bounded mutation experiment; phase details do
  not identify its mutation target or failure oracle.
  src/core/tests/test_resident_showcase_sql.py:213-214 skips SqlBoundaryTests
  unless SQL is opted in. The proposed always-run tests exercise helper
  relocation and cardinality, not necessarily the empty-table assertion.
* Concern: Mutating an integration call back to the migration batch while
  running ordinary discovery can leave all executing tests green because the
  affected method is skipped. Mutating only the helper can prove selector
  behavior without proving that the empty-table assertion rejects NULL/[].
* Impact: Changes evidence could claim the requested negative coverage without
  executing the relevant failure path.
* Smallest useful change: Specify the mutation target and exact failure oracle
  in P01-T02. Establish a passing baseline, force the wrong migration batch or
  fallback NULL/[] result through the actual affected test/assertion path,
  require the expected assertion failure, restore the candidate and rerun the
  focused checks. Provide a bounded mock-backed route if SQL is unavailable,
  within the existing two-method ceiling, and label that evidence as simulated
  rather than real SQL execution.
* Action owner: Planning parent.
* Exact resolving evidence: Revised phase details name the callable/path,
  controlled mutation, expected failure and restoration check. Subsequent
  changes evidence records baseline pass, expected negative failure, restored
  pass, and actual SQL execution or explicit SQL skips separately.
* Decision route: Direct planner correction. The user already requires
  wrong-batch rejection; no significant or divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Keep optional validation within the filesystem boundary

* Related IDs: P01-T02, test ownership and coverage lock, environment constraints.
* Evidence: The plan names flock -w 600 /tmp/ama-rpi-heavy.lock, and phase details
  propose an owned external venv. Current execution instructions prohibit
  /tmp file operations and require newly created files to be relative to the
  working directory.
* Concern: Following these fallback instructions can create files outside the
  permitted locations. An ownership label does not override the path boundary.
* Impact: A missing-dependency or optional-heavy-run branch of the plan cannot
  be followed as written in this environment.
* Smallest useful change: Put any newly created dependency environment and
  mutation scratch artifacts in an explicitly owned project-relative location,
  subject to retention rules. Omit optional heavy SQL execution for this bounded
  correction unless an already-authorized shared serialization mechanism
  compatible with the filesystem boundary exists. Do not silently substitute
  a different lock and claim it coordinates with the original shared lock.
* Action owner: Planning parent.
* Exact resolving evidence: Plan and phase details contain no instruction to
  create files in /tmp or a new external venv; focused validation and mutation
  paths remain executable within the project, and heavy SQL is explicitly
  unperformed unless compatible shared serialization is established.
* Decision route: Direct planner correction. Focused non-heavy validation is
  already authorized; omitting the optional heavy lane requires no user response.

## Strengths and Residual Risk

* The exact view-definition marker selects the whole dynamic view batch,
  preserving optional-table binding, rather than extracting only its inner SQL.
* Setup and restoration both receive the correction.
* Inspection confirms no other indexed renderer selections. Unrelated row,
  tuple and path indexing does not need modification.
* Empty sensor fixtures remain empty; the HOME-A assertion closes the
  otherwise indistinguishable [] fallback.
* Real SQL remains opt-in. Mock-backed negative evidence cannot establish
  database-engine behavior or operational acceptance.

## Questions or Blocking Evidence Gaps

* No unresolved user decision. PC-001 is a planner-owned validation definition,
  not a request for broader research or additional production scope.

## Limitations

* Read-only source inspection only. No tests, Ruff, SQL, heavy checks,
  dependency installation, Azure operations, commits or delegation performed.
* Existing candidate inputs were untracked on the supplied topic branch.
  They were not changed, moved, staged or committed.
* No independent post-implementation Review or implementation outcome is
  implied by this plan critique.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define the negative experiment and correct the
  filesystem instructions, record dispositions for both findings, then
  finalize the plan without another critique pass.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/resident-showcase-batch-selection-plan.md](.copilot-tracking/plans/2026-10-30/resident-showcase-batch-selection-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-30/resident-showcase-batch-selection-phase-details.md](.copilot-tracking/details/2026-10-30/resident-showcase-batch-selection-phase-details.md) | Assessed implementation and validation tasks |
| [.copilot-tracking/research/2026-10-30/resident-showcase-batch-selection-research.md](.copilot-tracking/research/2026-10-30/resident-showcase-batch-selection-research.md) | Supplied focused research |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-showcase-batch-selection-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-showcase-batch-selection-plan-critique.md) | Complete independent finding set |

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly and
finalize the candidate without another critique. No user action is required.
