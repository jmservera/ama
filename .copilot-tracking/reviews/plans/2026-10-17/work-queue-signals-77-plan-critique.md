<!-- markdownlint-disable-file -->
# RPI Plan Critique: work-queue-signals-77

## Metadata

* Task ID: 77
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/work-queue-signals-77-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/work-queue-signals-77-phase-details.md
* Critique execution status: Complete
* Execution count: Exactly one final candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: assess actual completeness and assumptions, not style. Write only this critique; no implementation, nested workers, source changes or further critique.
* Candidate inputs: the plan and phase details above, and .copilot-tracking/research/2026-10-17/work-queue-signals-77-research.md.
* Supplied evidence considered: research C1-C7/W1, the cited PRD requirements, API guide, queue contract, filter predicates, app.js, existing browser harness and its manifest. The harness's directly referenced constructed dataset and assertion helper were inspected to check test assumptions. Required project context and the customer/design-system boundaries were also read.
* Exact issue criterion boundary, as supplied by the candidate: visible signal definitions; displayed active perspective/workflow/search/all-cases scope; versioned-default reset result set/order/scope; selected-case rationale/proposed-owner refresh.
* Related requirements: FR-004/032/034, with AC-006/034/036/040 as traceability context, not a claim to deliver their entire historical scenario matrix.
* Decisions retained: #76 is hierarchy only, with no ordering dependency. Authenticated role is perspective; Stage is the workflow-stage filter, not AI workflow-only mode. Existing native controls and Fluent foundations remain. No redesign, role picker, ranking changes, #97 form/core/domain work, or #360/#358 infrastructure work.
* Test/runtime ownership: src/api/checks/workbench_browser_check.py only, maximum one new helper, no new test files or test removals; runtime changes only in src/api/src/zava_forward/api/web/app.js, plus directly related documentation/tracking.
* Execution constraints retained: fail-before behavioral browser evidence against the actual local app/API and tiny constructed fixtures; no private stock, live AI, Azure or live SQL. Full operational, human accessibility and live-platform acceptance are not inferred.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Criterion 1; FR-004; C3/C5; P01-T01/T02 | Covered | Preserve six server definitions; add definitions for all five existing Show only predicates. No additional queue or authority is needed. |
| Criterion 2; FR-032; C4/C7; P01-T01/T02 | Covered | Explicit role/stage/query/own-all scope and narrowing semantics are planned, with actual browser checks. |
| Criterion 3; FR-032; C3/C6; P01-T01/T02 | Partial | Alternate view=all is an appropriate regression seam, but identical resident names undermine the name-order oracle (PC-001). First-page evidence is unspecified for a three-case fixture (PC-003). |
| Criterion 4; FR-034; C4/C6; P01-T01/T02 | Covered | Real API comparisons for two selected cases and bounded empty-suggestions coverage preserve reviewer/owner distinctions. Existing request cancellation need not be reimplemented. |
| Fail-before actual-app behavior; P01-T01/T02 | Covered with correction | The approach uses the existing real-server browser harness. The ordering oracle must first become discriminating; screenshots alone remain insufficient. |
| Ownership and exclusions | Covered | Existing harness/app.js boundary and tiny synthetic-only execution are explicit; no need for domain, infrastructure or framework changes. |
| Review and persistent delivery; P02-T01 | Partial | Single-review execution is respected, but blanket deferral of material findings lacks a completion gate (PC-002). |
| Human/live acceptance and hierarchy | Covered as limitations | Existing gates remain unmet and disclosed; #76 creates no execution dependency. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the implementation scope is credible and appropriately narrow. Three planner-owned corrections are needed to make the promised reset evidence discriminating and the completion disposition dependable. No significant or divergent user decision is necessary.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The alternate name-sort oracle has no distinct resident names

* Related IDs: Criterion 3; FR-032; C6; P01-T01.
* Evidence: .copilot-tracking/details/2026-10-17/work-queue-signals-77-phase-details.md:14-19 promises an independently expected resident-name order for default.view=all and sort=name. src/api/checks/workbench_browser_check.py:18-55 constructs ZF-1/ZF-4/ZF-5 without changing resident names. src/core/tests/dataset.py:12-34 names every one Pat Test. src/core/src/zava_forward/core/insights.py:77-86 sorts name by the final name token.
* Concern: all three name keys are identical. A hardcoded expected order would test incidental tie behavior rather than demonstrate restoration of a genuinely different server-default order. Comparing only the selected sort value, a sort=name request or the default version also cannot prove displayed ordering.
* Impact: the promised behavioral regression can pass despite an incorrect displayed order, or fail because an assumed tie order differs. Criterion 3 would lack convincing evidence.
* Smallest useful change: explicitly authorize distinct, deterministic resident surnames in the existing harness's synthetic_data function, retaining the same three cases and relevant existing search matches. Choose a name order different from the urgent manifest order, then declare the exact expected ID sequence independently. No shared fixture, manifest, API/domain or extra test file is needed.
* Action owner: Planning parent, for P01-T01 specification; implementation parent, for the existing harness edit.
* Exact resolving evidence: phase details specify three unequal surname sort keys and an exact name-order ID list different from [ZF-4,ZF-1,ZF-5]. The existing browser harness compares rendered links to that list after resetting an overridden queue to the intercepted versioned all/name default. Recorded pre-edit browser failure exposes the missing default-view behavior; post-edit browser evidence confirms exact scope, membership and order, alongside unchanged ordinary-default assertions.
* Decision route: Direct planner correction. This stays inside the locked synthetic fixture and test ownership; no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Single review is incorrectly coupled to deferring every material finding

* Related IDs: P02-T01; all four issue criteria; ordered RPI completion.
* Evidence: .copilot-tracking/plans/2026-10-17/work-queue-signals-77-plan.md:89-94 says to route findings to later work. .copilot-tracking/details/2026-10-17/work-queue-signals-77-phase-details.md:42-49 says to record any material findings as follow-ups and then commit/push/create the PR.
* Concern: there is no distinction between accepted out-of-scope acceptance gaps and a review finding that the new reset is wrong, the new definitions contradict predicates, selection leaks stale context, or a regression check fails. One review does not imply that an in-scope defect should remain unfixed.
* Impact: the delivery can be marked complete despite a known failure of one of its exact criteria. Honest gap disclosure prevents overclaiming but does not resolve the in-scope defect.
* Smallest useful change: retain exactly one planned review, but require disposition of its findings. Correct in-scope implementation/test defects within the allowed files and rerun affected checks without commissioning another critique or review loop. Defer only explicitly out-of-scope concerns or accepted residual risks. If an in-scope blocker cannot be corrected, record delivery as blocked/incomplete rather than completed; any PR must retain that status.
* Action owner: Planning parent, for the P02 completion gate; implementation parent, for review-finding disposition and verification.
* Exact resolving evidence: matching plan/details text distinguishes blocking in-scope failures from deferred operational/live/human gaps. The eventual changes/phase log records each material review finding's disposition and relevant passing rerun, or explicitly records an unresolved blocker and incomplete acceptance.
* Decision route: Direct planner correction. No new scope, second critique or significant user decision is requested.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: First-page reset is promised without an observable pagination check

* Related IDs: Criterion 3; FR-032; P01-T01/T02.
* Evidence: .copilot-tracking/details/2026-10-17/work-queue-signals-77-phase-details.md:14-19 promises verification of first page using three cases. src/api/src/zava_forward/api/web/app.js:332-372 uses PAGE=50, local cursor/rows state and offset/after request parameters. Existing harness checks in src/api/checks/workbench_browser_check.py:270-475 cover reset membership, controls, focus and stale responses but do not assert reset pagination parameters.
* Concern: three rendered cases and null selection cannot distinguish a verified page-one request from an unexercised pagination assumption. The candidate names the outcome but not how the locked tiny fixture makes it observable.
* Impact: delivery could report first-page reset as behaviorally verified when the check only established membership and scope on a fixture that never paginates.
* Smallest useful change: specify an assertion on the actual post-reset /api/cases request: expected view/sort/default filters, offset=0 and no after cursor, followed by independently expected rendered IDs and the existing stale-response protection. Keep the three-case fixture and existing file. Describe this accurately as first-page request/reset-state evidence, not a real multi-page journey.
* Action owner: Planning parent, for the P01-T01 oracle; implementation parent, for the existing browser assertion.
* Exact resolving evidence: phase details name the observed request and its offset=0/no-after oracle. Passing real-app browser output ties that request to reset and the expected rendered default results, and the final evidence does not claim a page-two journey that was not run.
* Decision route: Direct planner correction. No larger dataset, new test helper/file or domain change is required.

## Strengths and Residual Risk

* The candidate correctly identifies gaps in an existing queue rather than inventing another queue system.
* Testing an alternate server default catches the current hardcoded own-scope reset. Normal-default tests and real selected-case API comparisons preserve existing behavior.
* Explicit unknown reviewer wording does not imply assignment or accepted ownership.
* Existing native Fluent foundations, permission intersections, deterministic ranking and cancellation boundaries are preserved.
* Complete owner-approved definitions, full scenario/profile matrices, full Fluent component adoption, human WCAG acceptance and actual AI/SQL/Azure acceptance remain outside this offline slice. This critique does not reopen those accepted boundaries.
* The existing browser fixture has intentionally narrow coverage. Positive operational outcomes or production readiness cannot be inferred from it.

## Questions or Blocking Evidence Gaps

* None requiring user input for this boundary. Exact expected name order and the pagination oracle are planner-owned test specifications, not product decisions.

## Limitations

* This is a plan critique, not implementation review or test execution. No browser, suite, lint, type or live-platform checks were run.
* The supplied four criteria are the issue boundary; the remote issue was not independently refetched. Research W1 was considered as recorded provenance, not freshly retrieved or a fresh UI conformance review.
* Source inspection was bounded to supplied inputs and directly referenced evidence needed to resolve test assumptions. No open-ended research was performed.
* Existing untracked plan/research/session artifacts were preserved. No source, plan, phase-details, research, session-state or prior review record was edited.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: specify distinct surnames and independent alternate-default ID ordering in P01-T01, incorporate PC-002/PC-003 directly, then finalize the plan without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/work-queue-signals-77-plan.md](.copilot-tracking/plans/2026-10-17/work-queue-signals-77-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-17/work-queue-signals-77-phase-details.md](.copilot-tracking/details/2026-10-17/work-queue-signals-77-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-17/work-queue-signals-77-research.md](.copilot-tracking/research/2026-10-17/work-queue-signals-77-research.md) | Supplied research and evidence pointers |
| [.copilot-tracking/reviews/plans/2026-10-17/work-queue-signals-77-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/work-queue-signals-77-plan-critique.md) | Single completed critique |

## Next Steps

Planning parent: directly resolve PC-001 through PC-003 and finalize without another critique. Continue the ordered RPI only after recording those dispositions. No user action is required. This critique stops here.
