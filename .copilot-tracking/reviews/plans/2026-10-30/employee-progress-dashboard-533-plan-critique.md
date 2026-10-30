---
title: Employee progress dashboard 533 final-candidate plan critique
description: Independent scoped assessment with one complete actionable finding set
ms.date: 2026-10-30
---

## Metadata

* Task ID: 533, Refs only.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/employee-progress-dashboard-533-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/employee-progress-dashboard-533-phase-details.md
* Critique execution status: Complete.
* Assigned branch: feat/employee-progress-dashboard-533.
* Observed HEAD and supplied base: 5634f9a077d175a931c15e3400114665d8c071ee.
* Exactly one independent assessment; no implementation or nested delegation.

## Inputs and Criterion Boundary

* Caller direction: full ordered RPI, local commit only, no push, Azure, deployment, live sign-in, credentials, private datasets, secrets or uv. Preserve existing delivered features; changes target tests, the browser checker, README and dated evidence.
* Read the supplied plan, phase details and .copilot-tracking/research/2026-10-30/employee-progress-dashboard-533-research.md.
* Checked referenced evidence in src/api/tests/test_progress_dashboard.py, src/api/checks/progress_browser_check.py, src/api/checks/design_system_browser_check.py, src/api/src/zava_forward/api/progress.py, src/api/src/zava_forward/api/web/progress.js, src/api/README.md, src/README.md and tools/rpi-checks.py.
* Read the required project context documents and the critique template. Read issue #533 and its owner comment through read-only gh inspection. No PR exists for the assigned branch in the returned branch query.
* Acceptance boundary: daily/weekly flow and four further statistics, table alternatives, filtered/paged archive and boundaries, demonstration labels, and browser/unit checks. Issue scope also retains URL filters and Fluent 2 patterns without a framework swap.
* The first four upstream checkboxes are checked; they are not fresh execution evidence. The owner explicitly leaves the issue open for deployed employee-site verification. That evidence is outside this task's permission.
* The current execution boundary prohibits file operations in temporary system locations. The plan's interpreter, shared lock and external-output assumptions therefore require feasibility reconciliation, not silent execution.
* Existing untracked plan, details, research and session-state files were observed and left untouched. This assessment writes only the requested critique artifact.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1, C2-C3 | Covered at planning level | Existing six-chart/statistic implementation and API/table comparisons are retained; fresh component execution remains planned, not observed here. |
| AC2, C3, C6 | Covered | Existing browser checker opens all six chart tables and compares table/bar values with actual constructed-data API responses. |
| AC3, P01-T01 | Covered | One inherited regression must check combined filters before paging, custom limit, exact stable IDs, totals, complete traversal, no overlap, remainder, clamping and empty page 1 on JSON and SQLite. Distractors failing each filter make the filter order observable. |
| AC3, P01-T02 | Covered | Existing 24-record browser fixture gives 20 first-page records and four final-page records. Planned first/final enabled and unavailable controls, empty controls and explicit beyond-empty page=1 canonicalization match existing runtime semantics. |
| AC4, C3-C4 | Covered | Existing demonstration labels and browser label assertion remain. No production relabelling or redesign is needed. |
| AC5, W1, P02 | Covered with explicit limits | Fresh browser/unit checks are required; deployed-site evidence remains unmet and cannot be inferred from local results. |
| Dependency #529 and scope control | Covered | Supplied research records the dependency as merged. No additional feature dependency or acceptance expansion is introduced. |
| Test ownership lock | Covered | Canonical targets are named, no removals are authorized, and additions are bounded to one inherited Python method and six logical browser boundary assertions in the existing flow. Existing semantic checks remain. |
| P02-T01 execution feasibility | Partial | Planned temporary-system interpreter/lock use and implicit unit scratch conflict with the execution boundary; PC-001. |
| P02-T02 complete gate feasibility | Partial | Existing runner opens a hard-coded temporary-system lock; attempting it is not an allowed way to discover the already visible blocker; PC-001. |
| Review, commit and reporting | Covered subject to PC-001 | One independent Review precedes local commit; original outcomes, human approval gaps, external receipts and publication separation are preserved. No push or issue mutation is authorized. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 0 Medium, 0 Low.
* Rationale: Acceptance scope, narrow regression ownership and expected boundary semantics are credible. The validation phase is not executable as written under the active file-operation boundary. This is a direct feasibility/reporting correction, not a reason to expand issue scope or seek deployment permission.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Resolve prohibited validation paths before promising or attempting execution

* Related IDs: P02-T01, P02-T02, AC5, validation requirements.
* Evidence: The plan requires /tmp/mv/bin Python and flock -w 600 /tmp/ama-rpi-heavy.lock, and phase details repeat both. src/api/tests/test_progress_dashboard.py uses tempfile.TemporaryDirectory() without an explicit scratch root. tools/rpi-checks.py heavy_lock() explicitly opens /tmp/ama-rpi-heavy.lock with create/read-write flags. The active execution boundary excludes those file operations. Neither a fresh external output directory nor avoiding an outer flock changes the runner's internal lock.
* Concern: The plan treats missing tools as possible blockers but does not recognize this already established execution restriction. Its instruction to attempt the complete gate would itself open a prohibited path. Running component tests unchanged also leaves implicit scratch placement unresolved.
* Impact: The implementation parent could either violate the execution boundary or imply that a reproducible validation route exists when the supplied route cannot be used. Replacing the shared lock with an unrelated lock would additionally lose serialization with other heavy users.
* Smallest useful change: Revise P02 and its details to preflight allowed interpreter, scratch, cache, lock and output locations before any execution. Use only a compliant existing validation route that preserves shared serialization. Do not silently relocate the shared lock, patch general gate tooling, create another environment, or expand the implementation scope to solve this restriction. Where no existing compliant route is available, mark the affected component checks and complete gate Blocked before invocation, preserve the concrete reason, and report local AC5 as unproven rather than passed. Preserve the requested local-only commit boundary and all original adverse evidence.
* Action owner: Planning parent; implementation parent executes only the reconciled permitted steps and records any blockers.
* Exact resolving evidence: Plan and phase details explicitly distinguish runnable checks from path-blocked checks; identify allowed locations and an existing supported serialization route for any check still claimed runnable; and replace the unconditional complete-gate attempt with a preflight stop for the runner's known hard-coded lock. Subsequent changes/Review evidence must contain actual results only for executed commands, explicit Not run/Blocked results for prohibited commands, and no fabricated receipt or whole-issue acceptance.
* Decision route: Direct planner correction. No user response is needed to respect the current restriction or report blocked validation. Permission to relax it or change general validation infrastructure is not assumed.

## Strengths and Residual Risk

* Reimplementing merged features is correctly rejected. The narrow additions strengthen acceptance evidence without altering production behaviour, dependencies or design foundations.
* The test contract is substantive rather than a count-only check: exact IDs, complete filtered traversal, non-default limit and distractors protect against filtering after pagination and accidental gaps/duplicates.
* Browser expectations fit the actual fixture and runtime: first/final navigation, a four-record final page, empty results and URL clamping are meaningful existing-behaviour checks. Empty tables contain a placeholder row, so implementation should count case records rather than mistake that placeholder for an archived case.
* The six-logical-assertion ceiling need not weaken coverage: pair enabled/unavailable expectations by boundary and retain existing row-count, history, reload and filter checks.
* A directly related production defect, if actually exposed, requires a recorded amendment before edits. That exception does not authorize an aesthetic overhaul or unrelated repair.
* Historical passing tests, checked issue boxes and source inspection cannot substitute for fresh candidate execution.
* Deployed-site, direct assistive-technology, staff usability, human approval and hosted publication gates remain separate. The supplied plan already preserves those limits; this critique does not add them as local deliverables.
* Fetching main is read-only. A changed origin/main must be reported separately from the fixed reviewed base; the assigned base does not authorize automatic rebase or history rewriting.

## Questions or Blocking Evidence Gaps

* No unresolved acceptance-scope or significant user-choice question.
* The supplied evidence does not establish a compliant alternate interpreter/shared-lock route. The parent must demonstrate one or record the affected checks as Blocked; it must not infer one.

## Limitations

* No tests, browser sessions, scanner checks, complete gate, sign-in or deployment were executed for this read-only critique.
* Research's earlier test count is treated as historical reported evidence, not independently reproduced.
* Current Web Interface Guidelines were not refreshed: no web implementation or UI-conformance review is performed here. The planned implementation/Review refresh remains required.
* This is the complete actionable finding set for the supplied planning boundary, not a security, accessibility-conformance or operational-acceptance assessment.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Reconcile P02's allowed paths and explicit blocked-check handling, record the disposition, then continue the ordered loop only within the permitted boundary.
* User response required: No.
* Do not launch another critique pass. Preserve this original Revise verdict and disposition it directly.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-30/employee-progress-dashboard-533-plan.md | Final-candidate plan assessed, unchanged. |
| .copilot-tracking/details/2026-10-30/employee-progress-dashboard-533-phase-details.md | Phase execution contract assessed, unchanged. |
| .copilot-tracking/research/2026-10-30/employee-progress-dashboard-533-research.md | Supplied research assessed, unchanged. |
| .copilot-tracking/reviews/plans/2026-10-30/employee-progress-dashboard-533-plan-critique.md | Single independent critique and complete finding set. |

## Next Steps

The active planning parent should directly resolve PC-001 and record its disposition without another critique. No user action is required. Do not implement from the unreconciled validation instructions or claim that blocked local checks, a complete gate, deployed acceptance or publication have passed.
