---
title: Employee briefing manager visibility RPI Review
description: Original independent post-implementation review
ms.date: 2026-10-28
---

## Scope and Evidence

* Task ID: employee-briefing-manager-visibility.
* Review date: 2026-10-28.
* Review scope: one independent full bounded implementation Review, AC1-AC8 and PC-001/PC-002.
* Source base: 98b0bb98f2424dd23c00e386378f44892a7a79e0.
* Plan: .copilot-tracking/plans/2026-10-28/employee-briefing-manager-visibility-plan.md.
* Details: .copilot-tracking/details/2026-10-28/employee-briefing-manager-visibility-phase-details.md.
* Research: .copilot-tracking/research/2026-10-28/employee-briefing-manager-visibility-research.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-28/employee-briefing-manager-visibility-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-28/employee-briefing-manager-visibility-changes.md.
* State: .copilot-tracking/rpi-sessions/2026-10-28/employee-briefing-manager-visibility-state.json.

## Opening Review State

* Interpreted goal: verify the exact owner decision, "Show all programme cases to manager roles on the briefing", without broadening assignment, consent, home scope or approval authority.
* Scope: complete changed source/tests/docs and relevant permission, identity, store and browser-harness context.
* Evidence readiness: one unambiguous canonical artifact set is present; P01/P02 checked and P03 legitimately pending. Changes declares source hashes and external validation logs; these require comparison.
* Acceptance basis: FR1-FR7, AC1-AC8, existing MANAGER_ROLES and original critique dispositions.
* First comparison boundary: complete source diff against the supplied base, then permission/projection/cache implementation and validation evidence.
* Active read-only boundaries: only this review record may be written. Existing dirty implementation and planning artifacts belong to the parent and will not be changed, committed or moved. No nested agents, repeat Review, Azure, secrets, private data or broad gate.
* Initial blockers: none identified before substantive comparison.

## Execution Status

* Execution status: Complete.
* Exactly one independent Review completed against the supplied source base and current working-tree candidate. No nested agent, repeated Review, correction implementation, source mutation, commit or publication was performed.
* P01/P02 implementation execution is complete on the available evidence. P03-T01 was legitimately unchecked at assessment because it includes this Review; P03-T02 publication is still pending. That sequence is not an implementation defect.
* Read the complete tracked source/test/documentation diff, the complete new browser check, changed Python/JavaScript source and test files, the complete changed README section with surrounding configuration/recovery context, and relevant permission/identity/store/task/release/browser-harness context. This is not a whole-repository audit or renewed verification of unrelated historical README claims.

## Candidate Identity and Evidence Boundary

* HEAD and reviewed base both resolve to 98b0bb98f2424dd23c00e386378f44892a7a79e0; implementation is presently uncommitted on fix/employee-briefing-manager-visibility. Read-only GitHub inspection found no existing PR for this branch.
* The source boundary contains five tracked modified files plus the new browser check. No permission, identity, consent, home-scope, approval, prompt-registry, dependency-manifest or schema file is changed.
* All six SHA-256 values independently matched Changes:

| File | Verified SHA-256 |
| --- | --- |
| src/core/src/zava_forward/core/store.py | d7d0a0cb284a6ca425032ea8849dc870a9ddb1649616d5f4418c3e0eb62a2d7f |
| src/api/src/zava_forward/api/web/app.js | 37aa87d572ffa6aa14cbf9e53dd9819425f38803d5c1318077566fe5f07460ee |
| src/api/tests/test_ai_tasks.py | 44901ab14c2dbf4de3ec06d96a0eed50207dfc15ea72966e690fe990b928e12d |
| src/api/tests/test_assistant_release.py | 976f29a86281f8782210bad3038548b837d251000064be66a4ee996ece4e9725 |
| src/api/checks/employee_briefing_browser_check.py | b5501eb878fa4547314d12843485a6a8a7a8436432fda38086452b477e0b299c |
| src/api/README.md | 604a0451ce634cb0b6ca04fc350fc527f3bb172cbceaadf1a19078d77b2a2727 |

* External final logs directly inspected: briefing-api-discovery.log, briefing-tasks-pass.log, briefing-release-role-pass.log and briefing-browser-final-pass.log in the caller-supplied session files directory.
* Original adverse focused evidence was also inspected in briefing-focused-final.log. Its 124-test run ended FAILED with one SQL fixture-persistence assertion, not PASS. Changes preserves this outcome and explains the correction; the subsequent 58-test task and 66-test release/role runs pass separately. Do not relabel the old run because its filename contains "final".
* The separate focused-core result of 18 tests in 4.163s with one opt-in skip is supplied by the caller and recorded in Changes. A standalone passing core log was not among the named final logs; this Review does not claim independent observation of that original command's console output.
* No full suite was repeated. Reviewer-executed checks were file-free Python AST/test-budget checks, Node syntax, git diff whitespace validation and 14 in-memory assertions against the actual Store.briefing with task persistence mocked. These do not replace the supplied JSON/SQLite suites or real browser evidence.

## Plan-to-Change Reconciliation

| Current plan scope | Changes summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01; FR1-FR3, FR5-FR7 | Guarded role-dependent permitted read, projected facts and expanded cache identity | Reconciled | Existing role constants and list_cases boundary retained; no authorization or assignment mutation |
| P01-T02; FR4 | Scope subheading, full/selected counts, neutral wording and polite async region | Reconciled | Briefing-only change; My cases and its navigation remain personal |
| P01-T03 | Employee briefing README and date | Reconciled | Documentation describes the two managers, top-eight cap, personal queue distinction and local evidence limits |
| P02-T01 | Nine new paired-store tests and two cache-internals reference adjustments | Reconciled | AST comparison confirms nine added TasksMixin test methods and zero removals; existing release assertions retain their behavioral purpose |
| P02-T02 | One synthetic real-server browser check | Reconciled | Seven staff roles, unassigned manager, personal queue IDs, keyboard workflow path and narrow reflow |
| P02-T03 | Discovery, focused core/release/role checks and source checks | Reconciled | Final pass logs distinguished from earlier failed fixture runs and opt-in/live omissions |
| P03-T01/T02 | Original independent Review, then conditional parent publication | Correctly pending at assessment | This artifact supplies the one Review; parent owns original-outcome preservation, administrative closeout and later publication prerequisites |
| Follow-Up Items | Historical PR #514 live diagnosis/deployment/model and human/accessibility limits | Reconciled | Explicitly outside active implementation and acceptance claims; no issue closure inferred |

## Completed Work Assessment

| Marker and acceptance criterion | Files and evidence | Assessment |
| --- | --- | --- |
| P01-T01/P02-T01; AC1 | store.py briefing; test_existing_managers_brief_all_permitted_open_cases_without_assigning on JsonTasks/SqlTasks | Both existing MANAGER_ROLES select all permitted open rows; another owner's work is included, closed ZF-2 excluded and hazard-first ZF-4 retained |
| P01-T01/P02-T01; AC2 | _filtered, counts, identity.bind; other-staff, bound/unbound and unbound-manager regressions | Non-manager briefing selection remains exact owner_code equality. Unbound non-manager briefing is empty; unbound managers retain zero personal assignments despite programme visibility |
| P01-T01/P02-T01; AC3 | projection.allowed, server.py authenticated GET guard, permitted-read and denied-role tests | Store guard precedes both selection and cache. Restricted selected IDs, full/summary counts, record IDs and captured prompt remain restricted. Contractor, administrator-only and unsupported roles cannot dispatch or reuse a briefing |
| P01-T01/P02-T01; AC4 | Full briefing cache condition, actor/role/mode and reason-policy tests, permitted-set regression, release tests | Key binds code/email/role/tenant/object, current reason visibility, full ordered eligible IDs and workflow mode. Every call re-reads current permitted scope before cache admission. Version, release and continuity/epoch checks remain intact |
| P01-T01/P02-T01; AC5 | Projected page_cases status paired with each top case; test_expanded_briefing_uses_projected_status_and_reason_policy_cache | Held private waiting reason does not enter Programme Support Officer facts. Export-field validation and per-role citation-source handling remain. Controlled case records are unchanged, with all-case equality and specific private-field assertions |
| P01-T01/P02-T01; AC6 | permitted-read/top-eight fixture; actual list_cases ranking | Eleven eligible cases produce full count 11 and selected count 8. Removing the non-top-eight permitted case at unchanged starting version refreshes count to 10 while selected IDs remain unchanged; hazard-first order retained |
| P01-T02/P02-T02; AC7 | app.js aiBox; employee_briefing_browser_check.py; final browser log | Both managers show exact "All programme cases"; five other staff show "My assigned cases". API and rendered counts agree, personal queue IDs are unchanged, and the zero-owned Programme Support Officer still has programme briefing |
| P02-T03; AC8 | Required discovery and final focused/browser evidence; Changes | Required local outcomes are recorded, including 314 discovery opt-ins and one focused-core skip. Live SQL Server, real inference, Azure and human/accessibility acceptance are not claimed |

### Permission, identity and store trace

* src/core/src/zava_forward/core/workflows.py defines only Retrofit Programme Manager and Programme Support Officer in MANAGER_ROLES. The implementation uses that existing constant rather than a new role list or identity-binding heuristic.
* src/core/src/zava_forward/core/projection.py permits briefing only for STAFF_ROLES; Application Administrator can read only me, contractors cannot read briefing and unknown roles default-deny. src/api/src/zava_forward/api/server.py retains its authenticated endpoint guard as well as the new Store-level guard.
* Store.list_cases delegates to page_cases, which excludes closed cases, applies owner filtering for mine and preserves ranking and projected waiting status. Current staff all-case reads already exist; the change selects that permitted view only for manager briefings, not for other-role briefing reads.
* SqlStore inherits briefing and list_cases. Its unlimited page_cases path delegates to Store.page_cases; therefore these tests establish SQLite/JSON shared semantics, not an independently exercised native SQL paging path or production SQL Server result.
* identity.principal and identity.bind retain verified tenant/object identity and role independently of roster continuity. Binding cannot grant role or ownership. None of those sources changed.
* ai_tasks.run_text_task retains export validation, reason-aware source labels, citation analysis, comparison records, Not reviewed status, continuity publication and release admission. Briefing generation records a proposal/audit, not consent, operational instructions, work authorization or approval.
* SqlStore._case/_touch/_finish/save explains the fixture correction: persistent changes must be touched under the lock. The corrected test uses the existing persistence mechanism instead of weakening production behavior.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and decision | Reconciliation and assessment |
| --- | --- | --- | --- |
| FR7/P01-T01/P02-T01 | Full ordered eligible IDs replace selected-only cache context | PC-001; accurate scope/counts already required by owner intent | Current plan, details, Changes, source and paired-store test agree. Research's earlier selected-ID alternative remains historical, not the current implementation specification |
| P03-T01/T02 | Explicit stop for unresolved acceptance-blocking Review findings | PC-002; no new user choice needed | Plan/details and Changes preserve original outcome and conditional publication; no premature publication is claimed |
| P02 fixtures | Correct SQL touched-record seeding and capture the model's user-prompt argument | Preserved failed focused runs | Corrections stay within nine new methods; no test removed, production fallback introduced or accepted direction changed |
| P02 browser fixture | Add synthetic document names in the briefing-specific fixture | Original browser source_labels KeyError from shared fixture | Scoped fixture correction is reflected in Changes and the new check. No general source_labels fallback or unrelated runtime repair |
| P01-T02/P02 | Intl count formatting and polite async status | Applicable fresh web rules | Final browser and Node evidence cover the final web bytes; discovery predates only this web-only formatting edit |
| Validation/publication boundary | Bounded local checks; no --all or --changed invocation | Explicit caller restriction | Preserved rather than silently running a prohibited gate. No complete local-gate receipt, blanket publication-policy waiver, deployed acceptance or hosted approval is inferred |

No material implementation decision diverges from the confirmed manager-briefing scope. No fresh planning, critique or owner decision was necessary for the recorded fixture and presentation adjustments.

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with PC-001 Medium and PC-002 High. It has not been rewritten into a pass.
* PC-001: resolved in current implementation direction. Full eligible ID tuple is in the actual key, and the test changes 11 to 10 permitted cases outside the selected eight without a preceding store-version change. Both stores retain the same correct top-eight record IDs.
* PC-002: resolved in plan/details. Publication is conditional on this original Review and unresolved blocking findings stop it. Parent must retain this outcome and any exact-head changes rather than infer that evidence retention alone permits publication.
* These were direct, compatible planner corrections. No significant scope expansion, unaccepted alternative, premature dependent work or material revision requiring another critique was found.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Historical PR #514 live failure diagnosis | This task changes local manager briefing scope, not the original deployed script failure | Existing deployment/support workstream; preserve actual authenticated diagnostic evidence | Justified nonblocking residual for this bounded source Review |
| Deployment, Entra mapping, production SQL Server and real employee-model activation | No live access or activation authorized; local fixtures cannot prove operational acceptance | Deployment/identity/release owners under separate authorization and controls | Distinct existing follow-up; not a new P01/P02 task or evidence of live completion |
| Human, screen-reader and accessibility acceptance | Engineering browser checks establish only bounded behavior/reflow | Product/accessibility owner arranges named-user/assistive-technology validation when separately scoped | Distinct follow-up; not a WCAG or user-acceptance claim |

These are existing out-of-scope residuals, not implementation defects or missing active acceptance tasks. Hosted checks and parent publication closeout are pending process work, not residual source fixes.

## Web Guidelines Review

* Refreshed the current public rules on 2026-10-28 from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md; retrieval succeeded with the complete rule body, not a partial source.
* Reviewed complete aiBox and adjacent aiNotes/listView/control context against all fetched categories. Existing Fluent styles, focus-visible rules, reduced-motion handling, overflow wrapping, skip link and native control behavior were inspected.
* New h3 scope follows the existing h2; server text uses text-node insertion rather than HTML. Counts use Intl.NumberFormat. Scope/count text is explicit and bounded, empty states are intentional and retry/manual workflow paths remain available. No new image, animation, gesture, large rendered list, destructive action, theme or hydration surface is introduced.
* The checkbox retains its associated clickable label and native keyboard semantics. Global focus and hover rules remain; browser evidence covers Space activation and 320/390/1280px reflow, not focus restoration or screen-reader announcement quality.
* Exact owner label "All programme cases", existing sentence-case product copy and repository ASCII loading punctuation intentionally take precedence over generic title-case/Unicode typography preferences. This is justified, not a finding or authority to redesign the app.
* Existing adjacent review-input and other whole-file UI conventions were not changed; this bounded Review does not assert a fresh whole-file accessibility pass.

### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:257 - pass: no substantive changed-surface violation found under the explicit owner-label and ASCII conventions.

## Findings

No substantive RV finding was established within AC1-AC8 and the supplied implementation boundary.

* Severity counts: Critical 0; High 0; Medium 0; Low 0.
* No finding ID is manufactured for a historical, explicitly scoped-out acceptance boundary or an earlier corrected fixture failure.
* No implementation acceptance blocker, unresolved decision gap or material research gap was found.

## Defects

* None identified in the reviewed candidate.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| None | No rpi-implement, rpi-plan or rpi-research handoff | Parent continues administrative closeout | No substantive actionable finding requires those stages |

Later work, if separately authorized, must preserve this original Review rather than create a repeat Review for this task.

## Residual Work

* The three distinct existing follow-up boundaries above remain open and justified as nonblocking for local source acceptance.
* No additional active implementation task or new residual code defect is created by this Review.

## Blockers and Remaining Work

* Unresolved acceptance-blocking Review findings: none. Under PC-002, any unresolved authorization, disclosure or required-check failure would have stopped advancement; no such current failure is evidenced.
* Publication is not executed or approved by this read-only Review. Parent still owns P03 marker/state/Changes reconciliation, preservation of original evidence, commit identity, exact candidate inspection, base/currentness checks and any remaining applicable publication prerequisites.
* No --all or --changed gate ran, per explicit caller restriction; no full receipt exists in this review evidence. This artifact neither represents that gate as passed nor authorizes bypass of a separate publication requirement.
* Parent states no post-Review source changes are planned. Final evidence/administrative closeout may be committed by the parent; source changes or a changed source base would fall outside this exact assessed candidate and must not silently inherit its hash-bound claims.
* Hosted checks, real deployment, SQL Server opt-ins, inference/release activation and human/accessibility approval remain separate and unestablished. They are not falsely presented as acceptance blockers for this intentionally local bounded change, nor as completed publication/live gates.

## Validation Evidence

| Check | Status | Evidence and limitation |
| --- | --- | --- |
| API: PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q | Passed, prior implementation run independently inspected | briefing-api-discovery.log ends Ran 1148 tests in 435.711s; OK (skipped=314). Expected negative startup/law/release diagnostics do not change the terminal result |
| API test_ai_tasks | Passed, prior implementation run independently inspected | briefing-tasks-pass.log: 58 tests in 10.124s, OK; JsonTasks and SqlTasks cover shared semantics |
| API test_assistant_release test_role_matrix test_role_endpoint_inventory | Passed, prior implementation run independently inspected | briefing-release-role-pass.log: 66 tests in 35.526s, OK |
| Core test_sensor_privacy and dataset.ImproveTests.test_briefing_cached_until_data_changes | Passed, supplied implementation evidence | Caller and Changes report 18 tests in 4.163s, one opt-in skip; no independent original passing console log inspected |
| checks.employee_briefing_browser_check | Passed, prior actual browser log independently inspected | Final source including Intl counts; Chromium 156.0.8078.4, all seven staff roles; responsive owned loopback server, exact personal IDs, workflow keyboard toggle, 320/390/1280px reflow and no uncaught page errors |
| Original focused run | Failed, historical and corrected | briefing-focused-final.log: 124 tests in 37.352s, one SQL test fixture persistence failure; retained rather than suppressed |
| Original browser attempt | Failed, historical and corrected | Changes records missing synthetic document name; new check fixes only its fixture callback and final real-server browser evidence passes |
| Changed-file Ruff and mypy | Passed, supplied implementation evidence | Changes reports Ruff, three API Python files and core store mypy; not independently rerun |
| node --check src/api/src/zava_forward/api/web/app.js | Passed, reviewer-executed | No syntax errors on current candidate |
| git diff --check | Passed, reviewer-executed | No tracked diff whitespace errors |
| File-free Python AST/hash/test-budget checks | Passed, reviewer-executed | All six hashes match; changed Python parses; exactly nine added TasksMixin test methods and zero removals |
| File-free actual Store.briefing assertions | Passed, reviewer-executed | 14 in-memory assertions for current manager/non-manager/denied roles, projected prompt text, cache reuse and full-count refresh beyond eight; task persistence mocked, no files/network/model |
| Fresh web-guideline retrieval and bounded source inspection | Passed, reviewer-executed | Full public source retrieved and applicable changed-surface rules assessed, with explicit copy conventions above |
| SQL Server opt-ins/live Entra/model/Azure | Skipped or unavailable by scope | Not enabled or accessed; SQLite and synthetic browser evidence cannot establish these outcomes |
| Human/user/screen-reader/WCAG acceptance | Not performed | No such acceptance is claimed |
| --all / --changed publication gate | Not performed, expressly prohibited for this task | No receipt or equivalent full-gate success inferred |

## Outcome

* Outcome: Conformant.
* Rationale: the reviewed bounded source implements the confirmed manager programme-briefing decision, preserves non-manager assignments and existing authorization/approval boundaries, resolves both critique dispositions and has the required recorded local validation. Earlier failed fixtures are reconciled without erasing their outcomes.
* This is local implementation conformance, not deployment, live authorization, whole-issue acceptance, human approval or a publication-gate receipt. The explicit local validation restriction and copy conventions are already part of the accepted current plan, not unaccepted implementation divergence.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement handoff required |
| Decision gap or invalid assumption | None within the bounded implementation | Parent retains any separate publication-policy responsibilities |
| Material evidence gap | None preventing this bounded verdict | Supplied focused-core result is expressly distinguished from directly inspected logs |
| Nonblocking residual work | Existing distinct live-diagnosis, deployment/release and human/accessibility follow-ups | Existing operational/product owners under separate authorization; no active plan expansion |

* Execution status: Complete.
* Outcome: Conformant.
* Validation coverage: required local outcomes recorded; four final logs independently inspected; fresh web source review and file-free focused checks completed.
* Acceptance-blocking Review findings: none.
* Next owner: parent for original-evidence preservation and administrative P03 continuation, without source changes, prohibited gates, repeat Review or inferred publication/live approval.
