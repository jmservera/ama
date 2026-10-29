---
title: Progress dashboard and closed cases Review
ms.date: 2026-10-29
---

Task #533, progress-dashboard-533. One independent substantive assessment.
Source remained frozen. No workers or implementation corrections were invoked.

## Scope and Evidence

* Review scope: final staged src/api implementation, including newly staged files.
* Starting HEAD: 6d2c2dc4ce4b2e9bf99853698ac5b71e24c02c1c, verified with git rev-parse HEAD. This replaces the incorrect initial skeleton abbreviation.
* Assessed source: git diff --cached -- src/api against that HEAD, plus complete staged progress.py, progress.js, progress.css, test_progress_dashboard.py and progress_browser_check.py. Integration, documentation and modified regression files were included.
* Source diff SHA256: e79f806638643586483ebd0649dd5634eb19905b5584a0ce20d9cbb115723991, computed from git diff --cached -- src/api. No unstaged src/api differences were present during comparison.
* Requirements: issue #533 body retrieved read-only with gh issue view 533 --json title,body; all five acceptance criteria and the detailed scope below.
* RPI inputs: .copilot-tracking/plans/2026-10-28/progress-dashboard-533-plan.md; .copilot-tracking/details/2026-10-28/progress-dashboard-533-phase-details.md; .copilot-tracking/plans/2026-10-28/progress-dashboard-533-critique.md; .copilot-tracking/research/2026-10-28/progress-dashboard-533-research.md; .copilot-tracking/changes/2026-10-28/progress-dashboard-533-changes.md; initial skeleton at this canonical Review path.
* Context: original case study, relevant addendum/index/customer-primer context and owner memory; no new regulatory claim or company-performance assertion was made.
* UX basis: docs/reference/research/ux/design-system.md, docs/reference/research/ux/wcag-conformance-baseline.md and docs/reference/research/ux/content-standard.md.
* Fresh web rules: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md retrieved successfully for this assessment. Changed app.js/index.html integration and the complete new progress.js/progress.css were read against those rules. Repository ASCII punctuation, sentence-case/plain-language content and the owner-selected Fluent direction take precedence over conflicting generic typography/capitalization preferences.
* Exclusions: resident-parent integration, private datasets, secrets, environment files, Azure/az, deployment, full publication gate, hosted approvals and human accessibility acceptance.

## Opening Review State

* Interpreted goal: assess the frozen final staged implementation once and preserve all conclusions in this one canonical Review.
* Evidence readiness: plan, details, original critique, research, changes and initial Review were available. P01/P02 and P03-T01 were reported complete; P03-T02 included this Review and a still-pending parent-owned commit.
* Acceptance basis: issue requirements, current plan criteria, PC-001 through PC-006 dispositions, fresh web rules and repository UX baselines.
* First comparison boundary: read models and integration, then changed web files, regression changes and validation claims.
* Read-only authority: only this Review may change. No source, plan, critique, details, research, changes or index edits; no staging, commit, branch change, workers or heavy tests.
* Initial blockers: full publication gate unavailable under the az prohibition; updated parent ancestry unresolved. External evidence under /tmp cannot be opened under this reviewer's filesystem restriction; supplied results and directly inspected evidence must remain distinguishable.

## Execution Status

* Execution status: Complete.
* This means the bounded substantive assessment is complete, not that implementation, publication or human acceptance is complete.
* Compared the full staged src/api boundary and every supplied RPI artifact. Ran only read-only whitespace/syntax checks and lightweight in-memory numerical probes. No package suite or browser was rerun.

## Plan-to-Change Reconciliation

| Current plan scope | Changes and current implementation | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 | Separate progress.py aggregation/archive read models | Reconciled | Synthetic admission, lifecycle replay, date cohorts, current-view measures and archive semantics match the revised contract. |
| P01-T02 | Two GET routes, existing permission kinds, direct checks and semantic/HTTP tests | Reconciled | Stats permission plus explicit staff gate; archive additionally checks manager roles; refreshed store lock retained. |
| P02-T01 | Separate progress.js/progress.css; small script/router/navigation integration | Reconciled with findings | Functional coverage present; invalid-field and loading semantics have RV-001/RV-002 gaps. |
| P02-T02 | Focused synthetic browser harness, public fixtures and README | Reconciled with evidence limits | Endpoint/chart/table parity, history, paging, failure/retry, cancellation and reflow are implemented in the harness. Reported run results were not independently opened. |
| P03-T01 | Targeted checks, API suite, Ruff/mypy/JS evidence | Reconciled as reported | Full discovery preceded two final backend safeguards; the subsequent 50-test run and final browser run cover the later candidate. Do not describe the earlier full run as a new full-suite run after those safeguards. |
| P03-T02 | This independent Review; local commit remains parent-owned | Partial delivery task, complete assessment | Leave plan markers untouched. The parent must preserve this verdict and commit evidence separately; no publication is authorized. |
| Follow-Up Items | Human screen-reader/user acceptance and full Fluent adoption | Reconciled | Explicit existing residual work, not new active implementation tasks or claims of #533 acceptance. |

## Completed Work and Requirement Assessment

| Requirement | Evidence | Assessment |
| --- | --- | --- |
| Synthetic-only case admission | progress.py:62-70,177-179,274-277; test_progress_dashboard.py:193-227 | Explicit false overrides history; otherwise explicit true or a nonempty wholly synthetic-marked history qualifies. Both views exclude unmarked cases. No read-model dataset-file operation. |
| Daily/weekly openings, closures and backlog | progress.py:73-113,184-218; tests:124-191,229-264 | Initial opening and each reopen count as opened; reopened also reported separately. Consecutive same-state repeats are deduplicated. Backlog carries pre-range state and applies each day's net change; weeks begin Monday and clip to selected dates. |
| Duration episodes | progress.py:184-194,224-243; tests:157,179-191 | Calendar-date differences reset at reopen; closures ending in range supply samples even when opened earlier. Sorted samples yield ordinary median and nearest-rank p90. Missing samples return null, rendered Unknown. |
| Dates and unknown lifecycle | progress.py:37-59,73-129,232-237; tests:169-191,229-264,323-345 | Strict query dates; inclusive range, last-30-day default, maximum 366 days; unsupported/repeated filters rejected. Missing/contradictory lifecycle excluded with coverage, not inferred from stage_since. |
| Current journey, stalled/overdue and workload | progress.py:15-33,219-250; progress.js:96-113,130-131 | Six groups match the existing case workspace. Open cases only; Unknown fallback; owner roles rather than staff names. Stalled uses the existing 60-day threshold and overdue reuses recorded task clocks. Explicit current recorded view, dataset date and non-compliance caveats. |
| AI provenance and date cohort | progress.py:136-169,252; tests:266-281; progress.js:114-119,132-133 | Recommendation itself must be synthetic; every nonempty case link must be admitted. Briefing/source=ai only for outcomes. Accepted/Edited/Rejected uses resolved_at UTC dates, Edited displayed Changed; unknown dates, unreviewed and rules/templates separated. Only aggregates returned, no reviewer/output fields. |
| Dashboard statistics and chart alternatives | progress.js:39-59,89-133; browser check:53-80 | Daily/weekly charts plus backlog, journey, team and AI charts; median/p90/current/stalled/overdue facts exceed the four-additional-statistics criterion. Each chart/table derives from the same rows; text labels/counts do not depend on colour. |
| Archive status/date/team/text | progress.py:256-314; progress.js:135-175; tests:283-301 | Exact recorded stage rather than legacy constant Completed, exact owner role, casefolded authorised reference/resident/address/town/postcode search. Latest observed closure, Unknown stage/date handling, unbounded default includes undated cases; either date bound excludes them with a visible all-archive unknown-date count. |
| Paging and URL/history | progress.py:265-271,315-329; progress.js:8-37,147-178; tests:303-321; browser check:109-156 | Stable ID sort; default 20 and limit <=100; zero results page 1/1; clamp past-last requests. Tests include 0/1/20/21/40/41 rows, full/last/beyond pages and combined filters. Submitted filters omit page; real previous/next links preserve filters; hash reload/back/forward and effective-page canonicalization supported. |
| Roles and projection | server.py route permission additions; progress.py:116-118,257-259; tests:347-405; role inventory | Existing stats/cases permissions retained. Contractors, unknown roles and application administrators cannot bypass the explicit staff gate; only managers access archive summaries. Response whitelists omit phone, reasons, owner names and raw activity. Summary safety flag retained. |
| Isolation and no mutation | staged file list; progress.py; tests:354-361; browser harness:15,218 and reused isolated harness | No briefing/map/case-workspace source edits, framework swap or runtime dependency change. Read methods make no save/audit calls; archive copies stage fallback before summary. Browser fixture/server ownership is public synthetic/loopback with isolated model/data environment. |
| Browser/unit checks | new focused tests/harness; supplied changes and caller results | Relevant checks reported passed; direct reviewer checks below passed. No human acceptance, SQL Server coverage or full gate is inferred. |

### Numerical comparison

The public episode example gives duration samples 4, 1 and 2 days: sorted
1/2/4, median 2 and p90 4. Across 28 September to 7 October, end-of-day backlog
is 1/1/1/2/1/2/1/2/2/1. Weeks starting 28 September and 5 October respectively
have opened/closed/reopened/backlog values 3/2/0/1 and 1/1/1/1.
A range beginning 6 October correctly carries backlog 2.

Read-only execution of the staged module in memory, with minimal explicit
Store/permission/insights stubs and constructed cases, confirmed those values,
latest-closure filtering and unknown-date coverage. An additional AI timestamp
of 4 October 00:30 +02:00 counts on 3 October UTC, and false/mixed-link activity
contributes nothing. These probes are not installed-package, persistence,
HTTP, browser or full-suite evidence.

## Implementation-Time Plan and Detail Update Assessment

| Update | Trigger and reconciliation | Assessment |
| --- | --- | --- |
| PC-002 through PC-006 contract corrections | Critique supplied provenance, imported reopen, status, archive-date and AI-cohort corrections; plan disposition table/details and implementation agree | Applied under the existing synthetic-only/date/filter intent; no significant new product decision identified. |
| Explicit false admission override and missing-stage fallback | Changes records the final two safeguards; progress.py:63-64,278-295 and new assertions cover them | Compatible hardening, no scope expansion. Final narrow and browser results are separately reported rather than backdating the earlier suite run. |
| SQL test writer correction | Changes describes using the canonical _case/stage_since path; test_progress_dashboard.py:411-419 retains external-writer refresh assertion | Fixture correction, not removal of the SQL refresh requirement. |
| 320px layout and CSP-compatible axe injection | Changes records initial failures; progress.css has min-width:0, browser check uses DevTools evaluation | Preserves production CSP and required reflow; original adverse results are reported retained. |
| Browser readiness retry | browser check:56-58 uses retrying six-chart expectation | Synchronization correction, not a weakened expected result. |
| Navigation/safety harness and mypy adjustments | Endpoint inventory adds both routes; manifest/capacity expectations reflect new destinations; role_screens targets the replacement renderer; one test module permits existing untyped APIs | No removed tests, canaries, safety/name/status assertions or broad type-check suppression. Structural row/link assertion changes are consistent with the new semantic table. |
| Browser denied-role coverage placement | Focused browser harness signs in as a manager only; HTTP tests and existing all-role inventory supply denial coverage instead | Bounded coverage-layer divergence, not browser denial evidence. Server enforcement is inspected and directly tested; no authority relaxation or new owner decision. |
| State/handoff prose | Research Q1-Q4 table still says Open, while its readiness section says answered; plan retains pre-critique readiness wording despite complete disposition table; changes explicitly leaves Review/commit pending | Editorial staleness does not prevent a credible boundary. Use the actual evidence/dispositions and this Review, not those older readiness labels, for continuation. |

## Critique and Material Revision Assessment

Original critique is preserved unchanged: execution Complete, outcome Revise,
with High 3 / Medium 3 findings. This Review does not replace that outcome.

| Critique | Recorded disposition | Assessment |
| --- | --- | --- |
| PC-001 | Rejected by the planning parent as a worker-only filesystem restriction versus caller-required shared lock | This reviewer has not verified the earlier caller/parent instruction scope and cannot endorse historical path operations. The reviewer's own restriction is enforced: no /tmp evidence access, environment reuse or heavy check. This procedural disposition does not establish a source defect or authorize prohibited commands. |
| PC-002 | Accepted/applied | Explicit recommendation provenance, nonempty all-admitted links, aggregate-only output implemented. False, mixed and empty fixtures plus the explicit-true condition establish fail-closed admission. |
| PC-003 | Accepted/applied | Imported Reopened - aftercare plus controlled reopen replayed; openings/reopen counts, backlog and per-episode duration verified. |
| PC-004 | Accepted/applied | API facets, exact filtering and visible Recorded case status (stage) agree; Withdrawn/Excluded/Unknown are not relabelled completed works. |
| PC-005 | Accepted/applied | Latest observed closing transition used; undated cases included unbounded, excluded bounded, counted; stage_since never supplies closure. |
| PC-006 | Accepted/applied | resolved_at UTC review cohort, Changed mapping, missing-date/unreviewed/template separation implemented and numerically checked. |

No material product-direction revision or unaccepted architectural decision
was found. Current plan/details record the compatible corrections; no second
critique or review loop is requested. Historical execution ordering and
external log contents are not independently certified.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner/next action | Assessment |
| --- | --- | --- | --- |
| Human screen-reader/user acceptance | Existing explicitly open cross-workflow acceptance; automation cannot provide it | Owner/accessibility acceptance participants | Keep distinct; include new surfaces, announcement/focus, zoom/text resize and the reported clipped/offscreen contrast incomplete. |
| Full Fluent implementation adoption | Existing #150 foundation-versus-runtime gap, not authorization for a framework swap in #533 | Design-system owner under #150 | Keep open; this slice checks native patterns/tokens without claiming full Fluent adoption or native-only owner acceptance. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Date-range validation is not associated with the invalid fields

* Related scope: P02-T01, native form/error semantics and fresh web rules.
* Evidence: src/api/src/zava_forward/api/web/progress.js:15-18 creates fields without validation association; :71-75 renders every server validation failure only as a page-level alert alongside the unchanged controls. A reversed or >366-day dashboard range is accepted by the native date inputs, then rejected by progress.py:127-128. No aria-invalid, aria-describedby or invalid-field focus is set. The shared show implementation in app.js:51 focuses main instead.
* Impact: The message is visible and announced as an alert, and recovery is possible, but the affected date controls are not programmatically identified or linked to the explanation. This falls short of the repository field-error contract and the fetched inline-error/first-invalid-focus rules.
* Destination: later rpi-implement, within the accepted direction; do not fix during this frozen assessment.
* Smallest useful next action: associate range errors with the relevant date controls, expose invalid state and focus the first relevant invalid field, preserving editable values and generic read-failure retry. Add a focused assertion for the reversed/oversized range states.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Loading requests omit the repository busy-state semantic

* Related scope: P02-T01, request/loading states.
* Evidence: src/api/src/zava_forward/api/web/progress.js:60-62 supplies visible Loading demonstration data and role=status, but no aria-busy on the pending request region. Both new pages use this function. docs/reference/research/ux/design-system.md requires visible loading text and aria-busy.
* Impact: Visible loading and a status announcement are present, so this is not a blank/loading-versus-empty failure. The busy lifecycle required by the repository pattern is nevertheless absent.
* Destination: later rpi-implement, alongside RV-001 without reopening unrelated source.
* Smallest useful next action: mark the pending region busy, clear/replace that state on success/error, and retain the existing status text/cancellation behavior with a focused semantic assertion.

## Changed Web File Findings

### src/api/src/zava_forward/api/web/progress.js

src/api/src/zava_forward/api/web/progress.js:73 - range error not linked to invalid date fields; no first-invalid focus (RV-001).

src/api/src/zava_forward/api/web/progress.js:61 - loading region lacks aria-busy required by the repository pattern (RV-002).

### src/api/src/zava_forward/api/web/progress.css

No additional substantive finding in this bounded source inspection.
Reported clipped/offscreen bar-text contrast incomplete remains manual work,
not a passed colour-contrast assessment.

### src/api/src/zava_forward/api/web/app.js

No additional substantive finding in the changed routing/script/renderer-removal hunks.

### src/api/src/zava_forward/api/web/index.html

No additional substantive finding in the changed stylesheet/script integration.

This is a source review against freshly fetched rules and project baselines,
not a complete accessibility audit or a fresh manual rendered-page acceptance.

## Defects and Routed Findings

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001, Medium | rpi-implement | Parent schedules the bounded validation association/focus correction later | Implementation defect under the accepted native form contract. |
| RV-002, Low | rpi-implement | Parent schedules the pending-region busy semantic later | Local request-state pattern gap. |

No Critical or High source defect identified. No material decision gap routed
to rpi-plan and no material research gap routed to rpi-research. Later
implementation does not require this Review to run again.

## Residual Work, Blockers and Remaining Work

* Human acceptance and Fluent adoption remain the distinct follow-ups above, not defects added to active #533 plan scope.
* Publication is blocked independently of RV-001/RV-002. The complete tools/rpi-checks.py gate was not run because it invokes prohibited az/Bicep commands; no receipt exists. Do not substitute targeted tests, inherited opt-in skips, browser scans or this Review for the exact-head gate. No push or PR is authorized by this assessment.
* Supplied ancestry evidence: parent PR #529 is open at 73e365e618d8cf701a12434e4cd0c2f2affb07f1, but the starting worktree and updated parent are 12 ahead/12 behind. Employee patches are reported equivalent; the parent gained resident #525. This review did not re-query/rebase/retarget/integrate that parent.
* Coordinator must resolve lineage with owner authority and satisfy the complete exact-head gate under permitted prerequisites before publication. Source/base/commit/input changes invalidate prior gate claims. Missing permission for az is a blocker, not a skip or cloud-fallback authorization.
* P03-T02 local commit/evidence preservation remains parent-owned. Only this canonical Review was written, without staging or rewriting the critique.
* External raw logs/results were not opened because all /tmp filesystem operations are prohibited for this reviewer. Counts/version/hash/scan details below are explicit caller and changes-record attestations, not independently inspected raw results.

## Validation Evidence

| Check/evidence | Status | Coverage and limitation |
| --- | --- | --- |
| git rev-parse HEAD; staged diff/full added files; diff SHA256 | Inspected | Exact starting commit and complete supplied source boundary recorded above. |
| git diff --cached --check -- src/api | Passed directly | Whitespace check only. |
| node --check progress.js and app.js | Passed directly | JavaScript parse check only; no browser or source writes. |
| In-memory staged Python numerical probes | Passed directly | Actual aggregation/date/episode/AI function execution with explicit minimal stubs and public constructed records; not package, persistence or HTTP integration. |
| api-suite-final.log | Passed as supplied | 1192 tests, 316 inherited opt-in/non-applicable skips; earlier than the two final backend safeguards. No new test reported skipped; not SQL Server or full-gate coverage. |
| targeted-final-2.log | Passed as supplied | 50 tests after final backend safeguards; 9.346 seconds per changes. |
| browser-final-3.log and browser-final-3/browser.json | Passed as supplied | Real endpoint/table/bar comparison, six charts, filters/page reset/URL/history, empty/error/retry/cancellation, keyboard and 320/390/1280 reflow. Harness inspected; no reviewer rerun or raw-result access. |
| browser-final-3/dashboard-axe.json; closed-cases-axe.json | Zero violations as supplied, incomplete/manual boundary retained | Chromium 156.0.8078.4; axe 4.10.3, SHA256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb. Dashboard color-contrast incomplete for clipped/offscreen bar text; archive zero incomplete reported. Not manual acceptance or full conformance. |
| Package Ruff, strict mypy and formatter | Passed as supplied | Strict mypy 98 configured files; test-only untyped-call allowance inspected. Not rerun. |
| Browser denied-role scenarios | Not exercised by the focused harness | HTTP role-denial tests and all-role inventory provide the relevant enforcement coverage; no fresh browser-denial claim. |
| Complete local gate and receipt verification | Not run / blocked | Prohibited az prerequisite; no receipt, push or PR. |
| Human screen-reader, zoom/text-resize and usability acceptance | Not performed by this Review | Existing open acceptance remains open; reflow and axe reports do not replace it. |

The reported original failed attempts remain historical evidence: SQL fixture
writer, 320px min-content overflow, CSP injection, endpoint inventory/old
renderer harness and browser readiness. This assessment neither removes those
outcomes nor treats their later reported corrections as full-gate acceptance.

## Outcome

* Outcome: Defects found.
* Rationale: Core synthetic admission, temporal arithmetic, AI provenance/cohort, archive filtering/paging, roles, isolation and substantive regression coverage match the issue and revised plan. Two bounded native-form/request semantic gaps remain: Medium RV-001 and Low RV-002. No evidence supports treating the new surfaces as fully accepted against the stated UX baseline while these remain.
* Source implementation acceptance is distinct from publication: even after any later bounded correction, publication still needs authorized lineage reconciliation, the full exact-head gate, hosted checks and owner/human decisions. This Review grants none of those approvals.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defects | Later rpi-implement | Parent routes RV-001/RV-002; no source correction in this assessment and no repeated Review required. |
| Decision gap or invalid assumption | None identified in the product implementation | Parent retains existing scope; lineage authorization remains a publication prerequisite. |
| Material research gap | None identified | Raw validation logs remain uninspected and explicitly attributed; do not claim independent log certification. |
| Non-blocking residual work | Existing human acceptance and #150 Fluent follow-ups | Owner/accessibility/design-system participants, outside immediate #533 completion claims. |
| Publication blockers | Coordinator/owner prerequisite resolution | Preserve no-push/no-PR boundary; resolve ancestry and permitted complete-gate execution without bypass. |

* Review execution: Complete.
* Outcome: Defects found.
* Severity: Critical 0, High 0, Medium 1, Low 1.
* Validation coverage: directly inspected frozen source/tests and lightweight checks; broader supplied results qualified above.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/progress-dashboard-533-plan.md](.copilot-tracking/plans/2026-10-28/progress-dashboard-533-plan.md) | Current scope, markers and critique dispositions. |
| [.copilot-tracking/details/2026-10-28/progress-dashboard-533-phase-details.md](.copilot-tracking/details/2026-10-28/progress-dashboard-533-phase-details.md) | Phase contracts and validation recipe. |
| [.copilot-tracking/plans/2026-10-28/progress-dashboard-533-critique.md](.copilot-tracking/plans/2026-10-28/progress-dashboard-533-critique.md) | Original Complete / Revise critique, preserved. |
| [.copilot-tracking/research/2026-10-28/progress-dashboard-533-research.md](.copilot-tracking/research/2026-10-28/progress-dashboard-533-research.md) | Research evidence and native-module direction. |
| [.copilot-tracking/changes/2026-10-28/progress-dashboard-533-changes.md](.copilot-tracking/changes/2026-10-28/progress-dashboard-533-changes.md) | Implementation history, supplied validation and blockers. |
| [.copilot-tracking/reviews/logs/2026-10-28/progress-dashboard-533-review.md](.copilot-tracking/reviews/logs/2026-10-28/progress-dashboard-533-review.md) | This single independent substantive assessment. |

## Next Steps

Return this one Review to the active parent. Preserve the frozen source and
original critique; route RV-001/RV-002 to a later rpi-implement invocation
without another assessment loop. Parent owns evidence commit and the separate
lineage/gate/human follow-ups. Do not push, open a PR, rebase or bypass a gate.
