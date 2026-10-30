---
title: Resident showcase batch selection RPI Review
description: Independent bounded post-implementation review for task 521-pr590-batch-selection
ms.date: 2026-10-30
---

## Opening Review State

* Task: 521-pr590-batch-selection.
* Interpreted goal: assess the single test-file correction against the supplied dated RPI artifacts and local-only requirements.
* Scope: both stale renderer indexes, other indexed renderer uses, semantic negative coverage, focused validation and artifact reconciliation.
* Evidence readiness: supplied artifact paths and unstaged source diff identified; detailed comparison pending.
* Acceptance basis: caller requirements, current plan and details, original critique with dispositions, changes evidence and research.
* First comparison boundary: current test diff against renderer and SQL batch semantics, then all dated artifacts.
* Read-only boundaries: only this review record may be written; no implementation, other artifact mutation, commit, Azure, push, nested delegation or second Review.
* Initial blockers: none identified. This worker cannot access forbidden temporary-directory tools; lightweight reruns are optional, not assumed.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one independent post-implementation assessment on 2026-10-30 of the complete supplied task boundary. Source, SQL, renderer, all five dated inputs and branch lifecycle were inspected.
* Implementation execution: P01-T01 and P01-T02 are complete on the supplied evidence; the requested local commit remains the parent's subsequent handoff action, not an action performed or claimed by this Review.

## Scope and Evidence

* Task ID: 521-pr590-batch-selection.
* Slug: resident-showcase-batch-selection.
* Assessed requirements: replace both stale calls with a small content helper; inspect every other indexed renderer use; reject the wrong batch; retain empty sensor fixtures; add no more than two test methods; preserve existing tests and SQL opt-in isolation; run focused discovery and both Ruff checks from src/core; preserve dated RPI evidence, Refs #521 and the local-only boundary.
* Research: .copilot-tracking/research/2026-10-30/resident-showcase-batch-selection-research.md.
* Plan: .copilot-tracking/plans/2026-10-30/resident-showcase-batch-selection-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/resident-showcase-batch-selection-phase-details.md.
* Original critique: .copilot-tracking/reviews/plans/2026-10-30/resident-showcase-batch-selection-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-30/resident-showcase-batch-selection-changes.md.
* Implementation: unstaged diff and complete src/core/tests/test_resident_showcase_sql.py.
* Context: infra/sql/resident-showcase.sql; infra/scripts/resident_showcase_sql.py; src/core/src/zava_forward/core/resident_showcase_sql.py; src/core/src/zava_forward/core/synthetic/sensor_backfill.py; src/core/pyproject.toml.
* Repository context: docs/case_study_48_original.md; docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md. No legal, company, accessibility or operational acceptance claim is introduced.
* Branch inspection: chore/resident-authority-extension-521 matches open PR 590, targeting main. The one-file source diff is unstaged, with no staged diff. Existing untracked evidence was left untouched.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 [x] | Private selector, two call replacements, two RenderTests and HOME-A/[] assertion | Reconciled | Exact source diff matches scope and two-method ceiling. |
| P01-T02 [x] | Focused discovery, Ruff check/format, simulated negative and restored checks | Reconciled | Recorded commands, counts, expected failures and SQL skips are explicit. |
| Acceptance and handoff | Dated evidence and independent Review pending | Reconciled | This record supplies the one Review; local commit follows under parent ownership. Neither was falsely claimed complete in changes. |
| Follow-Up Items | None | Reconciled | No implementation-discovered source follow-up or active task is omitted. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/tests/test_resident_showcase_sql.py | `_view_batch() -> str` returns the unique batch containing the exact view-definition marker | Single-match unpacking rejects zero/multiple matches; both rebuild and finally-restoration use the helper | Two added always-run methods exercise every batch position and zero, irrelevant-only and duplicate outputs | Conformant |
| P01-T01 | src/core/tests/test_resident_showcase_sql.py | Query and expected tuple require sensor_home_id HOME-A plus empty JSON | SQL optional-table branch projects stock_id even without rows; fallback projects NULL. No sensor inserts, test removal or cleanup weakening | Actual-method negative experiment documented separately from SQL | Conformant |
| P01-T01 | Complete test module and renderer | Other indexed renderer uses checked | All render calls inspected, including local `batches` uses: remaining consumers join, iterate or content-select. Remaining numeric indexes select paths, rows or columns, not renderer batches | Direct source inspection and targeted search | Conformant |
| P01-T02 | Dated changes record | Exact command and mutation evidence | 40 discovered = 13 executed passing + 27 explicit skips; both Ruff commands exit 0 | Reported implementation execution, not independently rerun here | Sufficient for bounded acceptance |

The renderer splits nonempty batches on standalone GO and substitutes principal and authority values. SQL batch 2 is the constraint migration, not view creation. Selecting the whole view-containing batch preserves dynamic optional-table binding and the final sp_executesql call. The original code could leave the NULL/[] fallback in place and still satisfy its former []-only assertion. The new tuple rejects that state.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 and coverage lock | Name the actual affected method, simulated projected/fallback results, expected AssertionError, restoration and old-index mutation | PC-001; existing wrong-batch requirement, no new user decision | Plan, details and exact changes-record experiment agree | Original Revise preserved; accepted disposition recorded | Compatible clarification, not material scope divergence |
| P01-T02 environment controls | Reuse existing validation environment; retain caller's exact shared lock for heavy work | PC-002 rejection and caller-supplied parent instruction context | Plan, details and changes agree; no installation or heavy run claimed | Original finding preserved, explicit rejection rather than silent deletion | Parent-context rationale is supported by this task's supplied boundary; not authority for this worker to access temporary paths |
| P01 / completion prose | Mark implementation and focused checks complete | Recorded source and command results | Checklist, details completion and changes handoff agree | No amendment or material revision requiring a new decision identified | Reconciled |

## Critique and Material Revision Assessment

* Original critique execution Complete and verdict Revise remain preserved, with both Medium findings intact.
* PC-001 is applied: the changes record provides executable code directly invoking test_empty_sensor_tables_preserve_valid_empty_history with mocked database methods/results. It establishes HOME-A/[] pass, forces the migration/NULL fallback, catches the expected assertion containing HOME-A, restores and passes, then rejects the old indexed helper and passes restored RenderTests.
* Calling the method directly bypasses unittest's class-level skip wrapper; the negative is not an apparent success caused by skipped SQL tests. Mocked q/as_user do not establish that a database ran or that migration SQL causes the returned fallback. That limit is explicitly disclosed.
* PC-002 is rejected with a recorded parent-specific reason. The supplied task expressly distinguishes that parent's authorized lock/environment from this worker's stricter filesystem constraint. No heavy run occurred, so the disputed lock was never taken. This Review performs no temporary-directory access and makes no wider filesystem authorization claim.
* Dependent-work readiness: PC-001 is incorporated in the current plan/details and execution evidence; no unresolved significant decision or material divergence is apparent. No second critique or second Review is required or performed.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| None | Plan and changes both explicitly state none | None | No residual item to route |

Real SQL, live acceptance and a full publication gate are explicitly excluded validation lanes, not newly discovered defects or added active plan tasks. Any future publication or live exercise remains a separate authorization and evidence boundary.

## Findings

No substantive RV-xxx findings. Severity summary: Critical 0; High 0; Medium 0; Low 0.

## Defects

* None identified within the assessed boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | None | No implementation defect, decision gap or material evidence gap identified |

## Residual Work

* No source or plan follow-up. The parent still owns the requested local Conventional Commit containing implementation and dated evidence, with Refs #521 and the required trailer. It is not performed or represented as delivered by this pre-commit Review.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active P01 implementation: none.
* Local commit: subsequent parent action; no commit, staging, push or Azure operation performed here.
* SQL engine behavior and live acceptance: unverified, not required for this bounded local-only correction.

## Validation Evidence

| Command or assessment | Scope | Status | Summary |
| --- | --- | --- | --- |
| `python -m unittest discover -s tests -p test_resident_showcase_sql.py -v`, with ZF_TEST_MSSQL unset using existing validation venv | src/core | Passed, implementation-reported | Exact executable command in changes; 40 discovered, 13 executed passing, 27 opt-in loopback SQL skips. Caller corroborates results. Not independently rerun here. |
| `ruff check tests/test_resident_showcase_sql.py` | src/core | Passed, implementation-reported | Exact existing-venv command in changes; exit 0. No rerun here. |
| `ruff format --check tests/test_resident_showcase_sql.py` | src/core | Passed, implementation-reported | One file already formatted, exit 0. No rerun here. |
| Exact in-memory actual-method and old-index experiment in changes | Affected assertion and selector path | Passed, implementation-reported | Expected negative failures and restored passes explicitly documented; process-local patches, not SQL execution. Reviewed for a credible failure oracle, not rerun. |
| `git diff --check` | Current unstaged source diff | Passed, independently executed | No whitespace errors. |
| Complete module inspection and renderer-use search | Named test module, SQL and renderer | Passed, independently performed | Both stale calls replaced; no other indexed renderer selection remains; only two new test methods. |
| Optional independent focused reruns | Tests, Ruff and negative experiment | Skipped | Available tools are under a temporary-directory path forbidden to this worker. No installation, environment creation or unauthorized access attempted; supplied exact evidence suffices. |
| Real SQL integration | SQL Server | Skipped | 27 opt-in tests; no owned database/container run or SQL engine validation claimed. |
| Heavy checks, full publication gate and live acceptance | Outside bounded task | Not run | Not part of this local-only correction. No lock, Azure or cloud fallback used by this Review. |

Initial system missing-package/tool failures are prerequisite failures, not final candidate failures: changes distinguishes them from successful existing-environment checks. Expected refusal-test stderr is documented rather than mistaken for a database connection. No claim is made to have independently observed implementation command execution.

## Outcome

* Outcome: Conformant.
* Rationale: source correction, regression ownership, semantic oracle, recorded focused checks, critique dispositions and dated artifact state agree with the confirmed bounded requirements. The PC-002 disposition does not expand source scope or authorize this worker's filesystem access. No substantive defect or unresolved decision was found.
* Acceptance limit: local test correction only; not SQL engine, whole-issue #521, live resident, publication, hosted-check or approval acceptance.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No correction needed |
| Decision gap or invalid assumption | None | No replanning needed |
| Material evidence gap | None | No research handoff needed |
| Non-blocking residual work | None | No distinct source follow-up |

* Execution status: Complete.
* Outcome: Conformant.
* Findings: none at any severity.
* Validation coverage: independent source/context assessment and diff hygiene; supplied successful focused tests/Ruff and simulated negative evidence; real SQL and independent reruns not performed.
* Blockers: none for the Review; local commit remains parent-owned.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/resident-showcase-batch-selection-research.md](.copilot-tracking/research/2026-10-30/resident-showcase-batch-selection-research.md) | Assessed focused research |
| [.copilot-tracking/plans/2026-10-30/resident-showcase-batch-selection-plan.md](.copilot-tracking/plans/2026-10-30/resident-showcase-batch-selection-plan.md) | Assessed current plan and dispositions |
| [.copilot-tracking/details/2026-10-30/resident-showcase-batch-selection-phase-details.md](.copilot-tracking/details/2026-10-30/resident-showcase-batch-selection-phase-details.md) | Assessed task details |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-showcase-batch-selection-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-showcase-batch-selection-plan-critique.md) | Preserved original Revise |
| [.copilot-tracking/changes/2026-10-30/resident-showcase-batch-selection-changes.md](.copilot-tracking/changes/2026-10-30/resident-showcase-batch-selection-changes.md) | Assessed exact validation evidence |
| [src/core/tests/test_resident_showcase_sql.py](src/core/tests/test_resident_showcase_sql.py) | Reviewed one-file correction |
| [infra/sql/resident-showcase.sql](infra/sql/resident-showcase.sql) | Batch and projection semantics |
| [infra/scripts/resident_showcase_sql.py](infra/scripts/resident_showcase_sql.py) | Renderer context |
| [src/core/src/zava_forward/core/resident_showcase_sql.py](src/core/src/zava_forward/core/resident_showcase_sql.py) | Reader projection context |
| [src/core/src/zava_forward/core/synthetic/sensor_backfill.py](src/core/src/zava_forward/core/synthetic/sensor_backfill.py) | Empty sensor table DDL context |
| [src/core/pyproject.toml](src/core/pyproject.toml) | Existing tooling configuration |
| [docs/case_study_48_original.md](docs/case_study_48_original.md) | Original project context |
| [docs/case_study_48_addendum.md](docs/case_study_48_addendum.md) | Current project scope boundaries |
| [docs/reference/README.md](docs/reference/README.md) | Knowledge-base entry point |
| [docs/reference/memory.md](docs/reference/memory.md) | Owner context, not evidence |
| [.copilot-tracking/reviews/logs/2026-10-30/resident-showcase-batch-selection-review.md](.copilot-tracking/reviews/logs/2026-10-30/resident-showcase-batch-selection-review.md) | Task's single independent Review |

## Next Steps

Return this record to the active parent for its authorized local-only commit and closeout. No corrective RPI handoff or user decision is required. Do not push, access Azure, infer publication acceptance or run a second Review.
