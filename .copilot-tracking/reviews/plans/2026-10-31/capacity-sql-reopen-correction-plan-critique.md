---
title: "RPI Plan Critique: Capacity SQL reopen correction"
description: One independent final-candidate assessment of the bounded external-test correction
ms.date: 2026-10-31
ms.topic: reference
---

## Metadata

* Task ID: pr-605-capacity-sql-reopen-correction
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/capacity-sql-reopen-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/capacity-sql-reopen-correction-phase-details.md
* Research: .copilot-tracking/research/2026-10-31/capacity-sql-reopen-correction-research.md
* Critique execution status: Complete
* Candidate source HEAD: e5f36c13dca8c9fcff34af6ab6c7a1d92b6b1da7
* Branch/context: fix/capacity-page-523; PR #605, Refs #523.
* Execution count: Exactly one critique; no delegated agents or repeat assessment.

## Inputs and Criterion Boundary

* Assessed the supplied plan, details, research C1-C6/W1, caller decisions, AC1-AC7, P01-T01/P01-T02, dependencies and locked change budget.
* Checked the exact named external regression and SQL override, the cited non-wiping handoff precedent, SQL/file initialization, separate application-owned law lifecycle, missing-law HTTP tests, API tool configuration and supplied CI workflow.
* Read the required project specification and knowledge-base context. No regulatory rule, legal conclusion or new company claim is needed for this test correction.
* Current caller direction resolves publication strategy: CI, not the complete local gate; full dated RPI loop, one subsequent independent Review and non-force push. This critique does not recommend a complete local gate, production changes, new law fixtures, new test files or removed tests.
* Protected image mcr.microsoft.com/mssql/server:2022-latest and container ama-350-feedback-sql must not be removed. Research identifies the isolated session database ama_605_reopen_20261031_0845339f. No SQL, container operation, test execution, installation or remote mutation was performed.
* The candidate is a plan, not an implemented diff. Tracked source was unchanged at intake; the plan, details, research and parent state were already untracked and were left untouched.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1, C2, W1; AC1 | Covered | Source confirms make_store wipes SQL and the shared regression hardcodes synthetic.sqlite. Named CI and local reproduction results are supplied research evidence, not independently rerun results. |
| C3, C4; AC5 | Covered | App.law is separate; main supplies LawStore.from_env. Existing missing-law tests establish 503/unknown, error and human safe_route. The plan adds focused assertions without invented law loading. |
| C5, C6; AC2, AC3; P01-T01 | Covered with concern | Non-wiping SQL reopen follows an existing fixture precedent; file Store prefers live.json. Seed removal, actual original marker and independent connection are credible. Audit continuity needs an explicit pre-reopen oracle: PC-001. |
| AC4; P01-T01 | Covered with concern | Repeated projections retain null contract version and Unknown appointment status; the existing denied action checks procurement equality. Audit equality after that action must also be explicit: PC-001. |
| AC6; P01-T02; interpreter dependency | Partial | API ruff/format/mypy scope and procurement/rule-alert/real-SQL suites match the correction. Specified interpreter and default fixture file locations conflict with the execution file boundary: PC-002. |
| AC7; P01-T02; branch/publication decisions | Covered | Original critique and later Review, required commit trailer and non-force push are planned. Hosted success and human approval are not inferred from local results. |
| Locked change budget and protected-resource dependencies | Covered | Two fixture methods plus focused assertions in the existing regression; no production edits, test removals or new test files. Dedicated SQL isolation is required before any wiping suite runs. |
| Risks and alternatives | Covered | Rejecting both production law initialization and a path-only relaxation is supported by source. Missing law remains fail-closed; SQL connectivity and hosted outcomes remain future execution evidence. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 0 High, 2 Medium, 0 Low actionable findings.
* Rationale: The selected fixture-only root-cause correction is credible and fits the locked budget. Two planner-direct clarifications are needed to make the audit acceptance proof and validation execution boundary complete. Neither requires a significant or divergent user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Audit preservation lacks an explicit pre-reopen oracle

* Related IDs: AC2, AC3, AC4, P01-T01; C1.
* Evidence: src/api/tests/test_procurement_api.py:163-203 captures procurement before reopening, but captures audit only after reopening at line 178. Subsequent repeated-read assertions compare against that post-reopen baseline. The final denied appointment assertion checks procurement only. Plan Functional Requirements and details P01-T01 require preserved audit without specifying these missing comparison points.
* Concern: Carrying forward the existing audit snapshot placement proves only that later reads do not alter whatever audit survived. It does not prove that reopening retained the original audit history, or that a refused appointment action left audit unchanged.
* Impact: A regression could lose audit during reopening while the stated audit acceptance evidence still passes. Procurement continuity and seed removal do not independently prove audit continuity.
* Smallest useful change: Specify capturing a detached, nonempty audit baseline after legacy state is saved and before seed removal/reopening. Compare reopened audit to that original baseline immediately, after repeated reads and after the denied appointment action. Keep procurement comparisons at these boundaries. These are focused assertions within the existing test, not another helper or test.
* Action owner: Planning parent, then implementer of P01-T01.
* Exact resolving evidence: Revised P01-T01 explicitly names the pre-reopen nonempty audit oracle and final refusal audit comparison; the subsequent diff places that oracle before reopen_store and uses it at each boundary; the existing named regression passes on SQLite, file and real SQL with the seed absent.
* Decision route: Direct planner correction. Existing caller direction already requires unchanged audit; no user response or scope expansion is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Validation commands and fixture defaults use forbidden file locations

* Related IDs: AC6, P01-T02, plan Dependencies; execution file-operation boundary.
* Evidence: Plan Dependencies selects /tmp/mv/bin/python; details P01-T02 repeats that interpreter. src/api/tests/test_procurement_api.py:38 uses tempfile.TemporaryDirectory() without an explicit directory, and SQL suites also use tempfile. The supplied execution constraints prohibit /tmp and /var/tmp file operations and require scratch files to be repository-relative.
* Concern: Validation as written depends on a forbidden interpreter location and leaves default fixture storage liable to use /tmp. Pip-only and protected SQL reuse do not resolve this separate file-location constraint.
* Impact: Required checks can be blocked by the runtime or create fixture files outside the permitted boundary even when the correction itself is sound.
* Smallest useful change: Select a permitted interpreter outside forbidden locations, with existing required project distributions and tools verified. Run tests with TMPDIR pointing to a repository-owned scratch area established before Python starts, and direct generated validation files there. Use pip only if the chosen validation fails for missing dependencies. Do not relocate or delete the existing environment, alter production/tests to solve this, or remove historical evidence.
* Action owner: Planning parent for the execution instructions; implementation parent for environment verification and validation.
* Exact resolving evidence: Revised dependency and P01-T02 instructions name the permitted interpreter and repository-relative scratch setup. Validation records its executable and confirms tempfile.gettempdir() resolves beneath the worktree before running suites, followed by the requested check exits and test counts. No forbidden-location file operations or protected-resource removal occur.
* Decision route: Direct planner correction under the existing execution constraint. No significant or divergent user decision is required.

## Strengths and Residual Risk

* Correctly separates the terminal SQLite-specific assertion failure from incidental post-commit law logs, while fixing the additional SQL reset-on-reopen defect.
* Removing the synthetic seed plus checking persisted package/workorder state prevents recreated seed data from masquerading as persistence.
* Actual original backend marker and distinct connection assertions are preferable to weakening the test to accept arbitrary SQL paths.
* Missing law remains explicitly unknown with HTTP 503 and a human safe route; missing contract authority still denies appointment actions with HTTP 403.
* Existing non-wiping reopen precedent makes the two-helper budget credible. No production lifecycle change is justified by the supplied evidence.
* Hosted CI and human approval remain pending, as explicitly accepted by the planning parent. Local passes must not be represented as hosted approval or as a complete local-gate receipt.

## Questions or Blocking Evidence Gaps

* No decision-critical user question. Both findings are planner-owned corrections within the selected scope.
* Before SQL validation, the implementation parent must verify that the existing runtime runner targets only the named isolated session database. The runner and credentials were not supplied or opened here; this critique does not authorize running wipe against any other database.

## Limitations

* W1 terminal counts and AC1 baseline reproduction are assessed from the supplied research, not independently fetched logs or rerun tests.
* No implemented candidate exists at this source HEAD. Future passing tests, exact-head Review, protected-resource identity and hosted CI status are not established by this planning critique.
* No open-ended repository research, destructive SQL operation, full local gate, second critique or delegated review was performed.
* Only this original critique artifact was written; plan, details, research, production and tests remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Resolve PC-001 and PC-002 directly in plan/details, preserve this original Revise outcome, then finalize and hand P01-T01 to implementation without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/capacity-sql-reopen-correction-plan.md](.copilot-tracking/plans/2026-10-31/capacity-sql-reopen-correction-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/capacity-sql-reopen-correction-phase-details.md](.copilot-tracking/details/2026-10-31/capacity-sql-reopen-correction-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-31/capacity-sql-reopen-correction-research.md](.copilot-tracking/research/2026-10-31/capacity-sql-reopen-correction-research.md) | Supplied C1-C6/W1 and baseline results |
| [.copilot-tracking/reviews/plans/2026-10-31/capacity-sql-reopen-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/capacity-sql-reopen-correction-plan-critique.md) | Original independent critique |

## Next Steps

No user action is required. The active planning parent owns the two direct corrections, disposition and finalization; it then continues the requested RPI loop and CI-gated non-force publication. This critique stops here; do not invoke another critique.
