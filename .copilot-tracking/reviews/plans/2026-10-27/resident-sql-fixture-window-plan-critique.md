---
title: Resident SQL fixture authorization window plan critique
description: Independent final-candidate assessment for PR 479 fixture-only correction
ms.date: 2026-10-27
---

## Metadata

* Task ID: pr-479-resident-sql-fixture-window
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/resident-sql-fixture-window-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/resident-sql-fixture-window-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: correct only the shared SQL fixture; retain the November SQL ceiling and December application semantics; search other consumers; use worktree source roots plus shared test roots; own regression coverage in one new API harness unit module with at most three tests and no removals. Assertions must observe actual insert arguments, not source strings.
* Execution requirements: current branch and PR 479, foreground scoped Docker/browser/image checks under the named shared lock with zero wait, no uv or secrets, normal commit and pull --rebase before normal push, reply to and resolve the review thread, no merge.
* Supplied evidence: .copilot-tracking/research/2026-10-27/resident-sql-fixture-window-research.md, including C1-C7; the supplied plan and phase details; repository instructions.
* Inspected evidence: src/api/checks/resident_demo_browser_check.py, src/api/checks/resident_demo_image_check.py, infra/sql/resident-showcase.sql, relevant resident core tests and sensor-check uses, src/api/tests/test_regulatory_ux_check.py, src/api/pyproject.toml, src/README.md, and scoped gate selection/publication behavior in tools/rpi-checks.py.
* Dependencies: P02 follows P01; P03 follows P02. Acceptance covers red/green behavioral regression, both residents, independent caps, cleanup, runtime-only imports, focused tests and check outcomes, independent Review, and remote thread disposition.
* Assessment boundary: planning credibility and implementation/publication safeguards, not implementation acceptance, legal approval, live authorization renewal, or parent-PR acceptance. Only this critique artifact is writable.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2; fixture-only requirements; P01-T01 | Covered | database() currently inserts rs.AUTHORITY_END; SQL explicitly requires valid_to <= 2026-11-01T00:00:00. A separate UTC constant converted at insertion is coherent. |
| C3-C5; consumer search | Covered | Image checks import database(); their application expiry and sensor in-memory uses should remain unchanged. Core SQL fixture already uses November 1. |
| C6; locked test ownership | Covered | Existing core tests cover the December ceiling and expiry. The proposed new API module owns actual fixture insert parameters and teardown, with at most three tests and no removals. |
| Runtime-only discovery; P01-T01 | Covered | Current shared harness eagerly imports Playwright. Planned lazy runtime import and blocked-import regression follow the regulatory test precedent without global package substitution. |
| P02-T01; scoped checks | Covered | Explicit source/test roots, real SQL readiness, labeled disposable resources, zero-wait shared lock and exact-resource cleanup are specified. Owner scope excludes a full-matrix fallback. |
| C7; P03-T01; final candidate freshness | Partial | Focused scope is justified, but Review precedes synchronization and final freshness requirements are underspecified; PC-001. |
| P03-T01; authenticated commit identity | Partial | Plan requires dynamic identity derivation, but phase details prescribe a fixed account email; PC-002. |
| Publication and parent acceptance boundaries | Covered | PR 479 is open on chore/resident-live-acceptance targeting main. Normal push, remote publication before thread resolution, no merge and preserved parent blockers are explicit. |

## Verdict

* Verdict: Revise
* Rationale: the technical correction and regression ownership are credible. Two direct planning corrections are needed to prevent stale final-candidate evidence and account-specific commit attribution. Neither requires changing owner scope or an additional critique.
* Severity summary: Critical 0; High 0; Medium 2; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Bind validation and independent assessment to the synchronized publication candidate

* Related IDs: C7, P02-T01, P03-T01; independent Review and publication acceptance criteria.
* Evidence: P02 schedules the independent Review before P03 commits and runs pull --rebase. P03 says only to rerun "affected focused checks" if rebase changes inputs, and otherwise to "verify final candidate" without defining the required evidence. src/README.md, Local RPI gate, requires refreshed evidence after later commits/rebases, fetching main before final verification, and independent exact-head review before push.
* Concern: the plan permits publishing a new synchronized head with the original pre-synchronization Review and selectively reused checks, without an explicit final head/base binding or independent assessment of the publishable candidate.
* Impact: a successful pre-rebase test or Review can be mistaken for acceptance of the actual pushed candidate. This is separate from the deliberately bounded test scope.
* Smallest useful change: specify the final synchronization, candidate identification, scoped validation and independent exact-head assessment order. Preserve the original Review; place the required final assessment after synchronization and candidate validation. Record final HEAD, fetched origin/main SHA and the evidence applicable to that candidate. Any later candidate/base change invalidates that binding and blocks push until refreshed. Preserve the owner's scoped-only direction; do not silently substitute a full matrix or launch a broader changed-path selection.
* Action owner: Planning parent; implementer executes the corrected P02/P03 sequence.
* Exact resolving evidence: plan and matching phase details explicitly define final synchronization and fresh scoped validation before independent exact-head assessment and normal push; retained execution evidence identifies the final candidate/base and applicable check results, with no later mutation presented as already reviewed.
* Decision route: Direct planner correction. The owner already authorized scoped correction and publication; no divergent decision or user response is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Derive commit attribution rather than prescribing a fixed authenticated account

* Related IDs: P03-T01; privacy-safe commit identity requirement.
* Evidence: the plan says to configure identity from gh api user, whereas phase details prescribe the literal 8036360+jmservera@users.noreply.github.com. Repository instructions require deriving the email from the current authenticated response and explicitly prohibit hardcoding a user's email in instructions.
* Concern: the executable details can override the dynamic identity rule with an account-specific value. A shared environment or changed authenticated session need not represent that account.
* Impact: the resulting commit can be attributed to an account not established by the current authenticated operation, despite using a privacy-safe domain.
* Smallest useful change: replace the fixed address in phase details with derivation of {id}+{login}@users.noreply.github.com from the current gh api user response, configured repository-locally and used for both author and committer.
* Action owner: Planning parent; implementer verifies identity immediately before committing.
* Exact resolving evidence: phase details contain no prescribed account-specific email and match the plan's dynamic derivation; execution records the derivation step and verifies author/committer identity without reading secrets or changing global Git configuration.
* Decision route: Direct planner correction. No user decision is required.

## Strengths and Residual Risk

* The intended change preserves the independent SQL and application authorization boundaries rather than widening either one.
* The regression directly executes database() with fake SQL boundaries, checks both inserts with a substituted application cap, and retains teardown coverage. Existing core tests remain the owner of December behavior.
* The import-isolation adjustment is directly coupled to runtime-only discovery, not an unrelated refactor.
* The finite SQL window intentionally expires on November 1. Research explicitly accepts fail-closed behavior afterward; this critique does not recommend extending authority or adding new application-semantic tests.
* Missing Docker/browser prerequisites may be recorded as concrete blockers under the supplied scope. They must not be reported as passed checks or as clearing parent live-acceptance blockers.

## Questions or Blocking Evidence Gaps

* None requiring a user response. The two findings are planner-owned corrections.

## Limitations

* This was a read-only source and planning assessment, not a test execution or independent implementation Review.
* Docker availability, cached image identity and missing tool versions reported in research were not revalidated; those are execution prerequisites, not demonstrated results here.
* PR metadata was checked read-only. The supplied review-thread identifier and reported comment were not independently re-fetched; no thread state was changed.
* No production, test, plan, phase-detail, research or other review artifact was changed. No subagent was delegated.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: record dispositions and revise the final synchronization/validation/review ordering and identity derivation in the existing plan and phase details.
* User response required: No.
* Critique stop: this is the complete actionable finding set for the supplied boundary. Return to the active parent for direct disposition and finalization without another critique.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/resident-sql-fixture-window-plan.md](.copilot-tracking/plans/2026-10-27/resident-sql-fixture-window-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/resident-sql-fixture-window-phase-details.md](.copilot-tracking/details/2026-10-27/resident-sql-fixture-window-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-27/resident-sql-fixture-window-research.md](.copilot-tracking/research/2026-10-27/resident-sql-fixture-window-research.md) | Supplied C1-C7 evidence |
| [.copilot-tracking/reviews/plans/2026-10-27/resident-sql-fixture-window-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/resident-sql-fixture-window-plan-critique.md) | Complete independent critique |

## Next Steps

The active planning parent should apply the two direct corrections, record their dispositions and finalize without another critique. No user action is required. This critique stops here.
