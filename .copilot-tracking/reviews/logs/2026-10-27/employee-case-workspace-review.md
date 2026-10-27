---
title: "Review: employee-case-workspace"
description: "Independent post-implementation review of the bounded employee workspace change."
ms.date: 2026-10-27
---

## Scope and Evidence

* Task ID: employee-case-workspace
* Review date: 2026-10-27
* Review scope: One independent post-implementation Review of the complete supplied artifact and source boundary against base f183ba39.
* Plan: .copilot-tracking/plans/2026-10-27/employee-case-workspace-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/employee-case-workspace-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/employee-case-workspace-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/employee-case-workspace-changes.md
* Research: .copilot-tracking/research/2026-10-27/employee-case-workspace-research.md

## Opening Review State

* Interpreted review goal: Assess requirements, implementation, critique dispositions, validation limits and unresolved evidence without implying a fully diagnosed live incident or deployed acceptance.
* Review scope: All supplied task artifacts, complete git diff from f183ba39, and new src/api/checks/employee_workspace_browser_check.py.
* Evidence readiness: Supplied artifacts and dirty topic worktree identified; substantive comparison pending.
* Acceptance basis: Original qualityPanel error, empty employee case list and unavailable AI priorities; reconciled plan markers, acceptance criteria, original critique and implementation evidence.
* First comparison boundary: Read task artifacts, then compare changed source and browser regression coverage.
* Active read-only boundaries: Only this review record may be written. No source fixes, other artifacts, agents, deployment, environment/secrets/private data reads, deletion, uv or full gate.
* Initial blockers: Live upstream failed request and current owner mapping are unproven, as disclosed by the parent; assess their effect on acceptance after artifact comparison.

## Execution Status

* Execution status: Complete.
* This is the one independent post-implementation Review, not implementation self-approval. No additional agents were used.
* Compared the complete supplied artifact set, all six tracked source/document diffs and the complete new 156-line browser check. HEAD is f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc; implementation is currently uncommitted on fix/employee-case-workspace-qualitypanel.
* P01/P02 source execution is complete within its accepted boundary. The original deployed diagnosis and end-to-end operational outcome remain partial. Review completion does not mean deployed acceptance, publication approval or resolution of the original report.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01; AC1-AC2 | Script recovery | Reconciled | Selected-route checks precede dispatch; named dependency failure requests document reload. API exceptions retain route-only retry. |
| P01 / P01-T02; AC4-AC5 | Assignment scope and AI settings | Reconciled | Store changes only empty-template wording. README separates assignment, verified identity continuity, employee settings and activation. |
| P02 / P02-T01; AC1-AC5 | Validation | Reconciled | Six new unittest definitions, no removals, one three-scenario browser module; supplied results and inspected assertions match the lock. |
| AC3 | HTTP/unit checks | Reconciled | Three shell aliases, script order/bytes/MIME/security headers and protected proxy responses covered without changing static authorization. |
| AC6 | Reconciliation and Review handoff | Pending publication | Research, plan, changes and README prominently disclose missing live evidence. Actual PR disclosure cannot be assessed before the parent creates it. Use Refs #73 #360 #104, never Closes. |
| Follow-Up Items | Blockers and remaining work | Reconciled, open | Live request/mapping, authorized redeploy and qualified AI activation remain distinct operator work, not completed implementation. |

Plan task checkboxes, phase-detail status, changes evidence and handoff agree.
The plan's metadata still says "Ready, single critique dispositions applied";
this is planning readiness, not evidence that live acceptance is complete.
There is no checked human/live acceptance claim to undo.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/web/app.js | Checks route-required module exports with safe typeof; names paths and offers native document reload instead of an undefined helper | Guard before selected-route dispatch; location.reload preserves current URL; API catch still calls route | Supplied three Chromium scenarios; independently passed 17 isolated guard assertions, syntax and whitespace | Conformant bounded recovery; not proof of original upstream failure |
| P01-T02 | src/core/src/zava_forward/core/store.py | Clarifies assignment-only empty briefing | Exactly one wording-only line; owner_code equality and closed exclusion unchanged | Added JSON/SQLite assignment and closed-case assertions | Conformant; no ownership, permission or identity broadening |
| P01-T02 | src/api/README.md | Documents verified tenant+OID continuity, employee configuration and later redeploy | Setting names match Ai; endpoint absence distinguished from model deployments, attestation, identity/network and release prerequisites | Source comparison; no inference or Azure operation | Conformant operator guidance, with explicit live limits |
| P02-T01 | src/api/tests/test_ui_support.py; src/api/tests/test_auth.py | Exercises shell aliases, exact script content, MIME, caching/CSP/nosniff and proxy protection | Local synthetic HTTP requests; missing/invalid principal denied, valid fixture allowed | Parent reports 90 focused tests and required full discovery passing | Appropriate regression assertions; no live proxy acceptance |
| P02-T01 | src/api/tests/test_ai_tasks.py | Proves unbound/bound assignment distinction and missing endpoint fallback | Same email does not bind; unique tenant+OID restores workload code; closed case excluded; _chat asserted uncalled; resident/alias settings ignored | Three mixin methods run on JSON and SQLite, plus one configuration method | Covers AC4/AC5 without actual-model calls |
| P02-T01 | src/api/checks/employee_workspace_browser_check.py | Three real-server browser journeys with public constructed fixtures | Healthy quality panel and API retry; ops 404 and keyboard reload; unrelated specialist 404 isolation | Parent reports Chromium 156.0.8078.4 pass; browser assertions inspected | Covers normal/error/recovery distinctions within lock |

### Acceptance and test limits

* AC1: Healthy synthetic case ZF-2026-0597, quality heading, actual shell script responses, JavaScript MIME, order, callable export and absence of pageerrors are asserted. CSP is checked separately by HTTP tests.
* AC2: Ops 404 names /ops.js and prevents partial quality controls. Keyboard reload requests ops twice across the journey and preserves exact URL/search/hash and existing authenticated session. Error reflow is checked at 320/390/1280px. Transient case API 503 uses keyboard Try again with unchanged document/script request list. Missing role-screens.js leaves ordinary case/list usable and gives a named error only on the specialist destination.
* AC3: /app, query-bearing /app and /index.html bytes match; ops precedes app. All shell scripts are compared against installed source bytes with 200/MIME/no-store/nosniff/CSP assertions. Trusted-proxy fixture tests cover anonymous/invalid/valid principal behavior for shell aliases, ops and app. They do not authenticate against Azure.
* AC4: JSON/SQLite fixtures test own versus all permitted cases, email non-binding, tenant+OID continuity, recorded briefing case IDs and exclusion of a closed owned case. No current live owner mapping is read or established.
* AC5: Explicit "AI is not configured" template reason and zero _chat calls are asserted. Employee adapter setting names, both tiers, model versions and resident separation are covered. Release controls are preserved, not reimplemented or newly approved.
* AC6: Source-stage disclosures are present; PR wording and any future exact serving revision are still parent/operator responsibilities.
* Guard assertions establish representative export availability, not general script integrity or recovery from a missing app.js itself. The application cannot render its own recovery view if its entry script never executes. No broader guarantee is claimed.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01; AC2 | Route-specific readiness instead of an all-route prerequisite set | PC-001; preserves ordinary manual case/list access during unrelated specialist/map failure | Current plan, details, guard and third browser scenario agree | Compatible direct critique correction, no material direction change | Justified and implemented |
| P02-T01; AC2 | API retry negative control, complete query/hash, keyboard and session continuity | PC-002; verifies existing recovery promise rather than adding a feature | Plan/details and first two browser scenarios agree | Compatible direct critique correction within three-scenario lock | Justified and implemented |
| Dependencies; P02-T01 | Retained parent's installed isolated environment | PC-003 disposition; caller explicitly distinguishes parent authority from worker restrictions | Original critique preserved; plan and changes record reject the worker-only constraint | No new parent filesystem restriction inferred | Disposition accepted for parent evidence; this worker did not execute that external interpreter |
| P01-T02; AI runbook | Added dated existing employee endpoint and zero deployment observation | Research W4 management-plane metadata; directly clarifies why endpoint configuration alone cannot restore AI | Research, README and changes agree; existing plan already requires real deployment names and release prerequisites | Descriptive evidence refinement, not provisioning/model authority or material scope expansion | Justified; no second critique needed |
| P02-T01; completion evidence | Added full required API discovery, workbench regression and pre-change negative control results | Existing component test requirements and exact-error challenge | Changes and phase details distinguish local passes from live/human acceptance | No test-lock expansion or source-direction change | Reconciled |

## Critique and Material Revision Assessment

* PC-001 [High], accepted: resolved by actual selected-route requirements; independent guard assertions also verify ordinary staff case/list tolerance of absent specialist/map exports and contractor separation.
* PC-002 [Medium], accepted: resolved by API retry versus reload assertions, exact URL preservation, keyboard activation, repeated ops request and no second sign-in.
* PC-003 [Medium], rejected: original critique remains intact. Its worker filesystem restriction does not establish a parent restriction. Supplied parent validation is not rejected for that reason. No new dependency installation or external interpreter execution occurred in this Review.
* No significant unaccepted implementation decision or invalidated product assumption was found. W4 strengthens existing configuration guidance rather than authorizing AI activation. No material revision requiring a fresh plan/critique is evidenced.
* Dependent-work pause: current records show compatible PC-001/002 dispositions applied before completed implementation handoff; no evidence of work continuing across an unresolved material decision. Original critique remains Complete / Revise, not rewritten to Pass.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Authenticated deployed script status/console and current permitted owner mapping | No authenticated deployed evidence or live owner data within authorized source/synthetic scope | Owner/operator supplies permitted observations | Open; RV-001, distinct evidence follow-up |
| Owner-authorized redeploy and qualified employee AI activation | Deployment, provisioning and actual-model calls expressly excluded | Operator and authorized model/release owners approve and verify separately | Open; RV-002, distinct operational follow-up |

These are not implementation defects or new active Pxx tasks. Missing live
evidence prevents an exact original-cause or restored-live-service claim,
not review of the demonstrated recovery defect.

## Web Interface Guidelines Assessment

Fresh source retrieved successfully on 2026-10-27 from
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
before reading the changed web file. The complete app.js was read, with the
diff and relevant shell/style context used to bound introduced findings.
All fetched rule categories were screened for applicability to the changed
recovery flow; this is not a clean-bill audit of untouched application code.

### src/api/src/zava_forward/api/web/app.js

* Pass for changed recovery lines 143-164, 187 and 206-210: native named buttons, explicit type, semantic h1, text/alert feedback, existing polite workspace status, main focus via show(), and existing visible focus/hover styles. No new form, icon/image/media, animation, locale formatting, hydration, drag, destructive operation, layout measurement or large list is introduced.
* Pass for navigation/state: explicit document reload preserves current location instead of reconstructing it; generic API retry stays route-only; ordinary case/list do not require unrelated specialist/map modules.
* Existing Fluent token/focus/reduced-motion styling and plain-language/ASCII conventions take precedence over generic title-case and curly-quote suggestions. No aesthetic redesign or Fluent adoption completion is claimed.
* No introduced web-rule defect found. Keyboard activation and reflow results are supplied browser evidence, not independently rerun here. Screen-reader announcement timing, visual focus across browsers, text resize, zoom, hybrid touch and real-user comprehension remain untested; no WCAG conformance or human acceptance is inferred.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Original live failure and owner assignment explanation remain unverified

* Related scope: Research Q1/Q2, AC6, first plan Follow-Up Item.
* Evidence: Research W2 shows serving revision 0000006 already wires matching ops.js before app.js. W3 and changes demonstrate healthy synthetic rendering and an ops-404 negative control reproducing exactly "qualityPanel is not defined", with ineffective pre-change Try again. Neither identifies the original authenticated failed HTTP/execution request. Assignment source/tests prove exact owner_code and tenant+OID semantics; current live owner mapping remains unobserved.
* Impact: Synthetic recovery cannot establish the upstream cause, explain this owner's actual queue state conclusively, or prove that deployed behavior is repaired. Original user priorities remain operationally unresolved.
* Destination: Distinct owner/operator evidence follow-up, not rpi-implement or a new active plan task.
* Smallest useful next action: With owner authorization, obtain authenticated Network/Console evidence for the failed dependency and permitted current /api/me and own/all assignment observations. Reconcile those observations before claiming live diagnosis. If they reveal a new material cause, use a separately bounded rpi-research continuation.
* Blocking classification: Non-blocking for this source Review; blocking for exact live diagnosis and whole-issue acceptance.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Employee AI activation and deployed recovery need separate operator acceptance

* Related scope: Research Q3/W1/W4, AC5/AC6, second plan Follow-Up Item.
* Evidence: Supplied deployed environment-name metadata omits AI_ENDPOINT and both deployment names; W4 reports an OpenAI endpoint on aif-cutover-test-rzsrg but zero model deployments. README explains both deployment tiers, model attestations, managed identity/RBAC/network and per-task release/budget/incident controls. No model was called and no image was deployed.
* Impact: Setting an endpoint alone cannot restore inference; local source passes do not demonstrate authorized AI or acceptance on the serving image. Borrowing resident configuration/resources is not an approved remedy.
* Destination: Distinct owner-authorized deployment and model/release-owner follow-up.
* Smallest useful next action: Separately authorize the reviewed immutable API image, intended employee model deployments/resource and release evidence; preserve existing identities/data/configuration and verify serving digest, authenticated assets, case controls, assignment counts and approved registered model task only under that authorization.
* Blocking classification: Non-blocking for bounded source Review; blocking for claims of deployed recovery or working employee AI.

## Defects

* No implementation defect or unaccepted decision gap found in the supplied boundary.
* Severity summary: 0 Critical, 0 High, 2 Medium residual follow-up findings, 0 Low. The two Medium entries are not source defects.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct evidence follow-up | Owner/operator provides permitted authenticated request and assignment observations | Explicitly deferred live evidence, not an implementation correction |
| RV-002 | Distinct operational follow-up | Deployment operator and authorized employee model/release owners | Deployment/activation outside current authority |

Later implementation of any separately routed defect does not require this
Review to run again.

## Residual Work

* RV-001 and RV-002 remain outside active implementation and acceptance claims.
* Parent publication remains later: commit task implementation and original dated evidence on the topic branch, push normally and create one PR with Refs #73 #360 #104, not Closes. Include unproven original HTTP/execution cause, unobserved current owner mapping, no deployment, missing employee deployments/configuration, test skips and separate acceptance limits. This Review neither performs nor proves publication or replaces applicable publication/hosted approvals.

## Blockers and Remaining Work

* Review blockers: None; a credible bounded source verdict is supported.
* Remaining active P01/P02 work: None identified.
* Operational acceptance blockers: RV-001/RV-002. No .env, secret/private-data reads, Azure deployment/deletion, uv, full gate, implementation correction or repeat review was performed.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| API: PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest test_ui_support test_auth test_ai_tasks -q | Focused HTTP/auth/task suites | Passed, parent-reported | 90 tests; inspected added tests; not rerun |
| Required API unittest discovery | Complete API component suite | Passed, parent-reported | 1130 tests in 411.838s; 314 explicit opt-in skips, not 1130 executed passes |
| python3 -m checks.employee_workspace_browser_check | Three synthetic real-server scenarios | Passed, parent-reported | Chromium 156.0.8078.4; complete new check read |
| Existing workbench browser check | Eight roles and shared navigation/queues | Passed, parent-reported | No pageerrors; not independently rerun |
| Pre-change app.js plus ops.js HTTP 404 negative control | Exact error and ineffective retry | Passed, parent-reported | Original ReferenceError text reproduced; ops request count remained 1 after Try again; not proof of original live cause |
| Changed-file Ruff; mypy browser module/core Store | Changed Python | Passed, parent-reported | Initial generic-dict type error corrected; final pass without exemptions reported |
| node --check src/api/src/zava_forward/api/web/app.js | Changed JavaScript | Passed, independently executed | Exit 0 |
| git diff --check f183ba39 | Tracked implementation diff | Passed, independently executed | Exit 0; new browser file additionally read in full |
| Inline Node vm assertions against actual requireWorkspaceScripts source | Route dependency matrix | Passed, independently executed | 17 assertions: case-required modules, unrelated module tolerance, dedicated routes, query-bearing screens/coordinator, contractor list/case separation |
| Fresh Web Interface Guidelines plus changed-flow source/shell/style review | Changed app.js recovery | Completed independently | No introduced finding; not automated accessibility or complete application acceptance |
| Raw external parent validation logs | Supplied command-result claims | Unavailable to this Review | Changes/details and caller report outcomes; no raw log paths supplied or independently inspected |
| Repeat runtime unit/browser suite | Redundant validation | Skipped | Existing reported component/browser runs plus direct source/static checks sufficient for bounded Review; no full suite rerun or dependency restoration |
| Full local gate; SQL Server/live integration; deployed regression; real AI | Publication/integration/operational acceptance | Not performed | Explicit scope exclusions or opt-in prerequisites; no receipt or live result inferred |
| Screen reader, Firefox/Safari, zoom/text resize, actual staff/resident acceptance | Accessibility/user acceptance | Not performed | Beyond supplied local Chromium engineering evidence |

Deployment digest/static-byte/account observations are supplied research
evidence, not newly repeated management-plane measurements by this reviewer.
The new browser harness uses constructed fixtures, loopback password sign-in,
sanitized server settings and blocks non-loopback page requests; no real user,
provider or private dataset is part of its proof.

## Outcome

* Outcome: Residual work.
* Outcome rationale: The bounded source implementation and validation design conform to the reconciled plan, including compatible PC-001/002 corrections. No source defect or unaccepted material divergence was found. Two explicitly deferred operator follow-ups prevent the broader original live report from being described as fully diagnosed, deployed or accepted. This outcome is not Not accepted for the source correction and is not unconditional acceptance of the original user outcome.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement correction identified |
| Decision gap or invalid assumption | None | No rpi-plan revision identified |
| New material evidence gap in active plan | None | No immediate rpi-research handoff; deferred live work is RV-001 |
| Non-blocking residual work | Distinct owner/operator follow-ups | RV-001 evidence capture; RV-002 authorized deployment/model activation |

* Execution status: Complete.
* Outcome: Residual work.
* Validation coverage: Parent-reported component/browser/lint/type checks assessed; independent Node syntax, whitespace and 17 route assertions passed; fresh guideline/source review completed.
* Blockers: None to bounded Review; original live diagnosis and operational acceptance remain blocked by RV-001/RV-002.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/employee-case-workspace-research.md](.copilot-tracking/research/2026-10-27/employee-case-workspace-research.md) | Compared C1-C5 and W1-W4 evidence and live limitations |
| [.copilot-tracking/plans/2026-10-27/employee-case-workspace-plan.md](.copilot-tracking/plans/2026-10-27/employee-case-workspace-plan.md) | Compared requirements, AC1-AC6, markers and follow-ups |
| [.copilot-tracking/details/2026-10-27/employee-case-workspace-phase-details.md](.copilot-tracking/details/2026-10-27/employee-case-workspace-phase-details.md) | Compared implementation/validation details |
| [.copilot-tracking/reviews/plans/2026-10-27/employee-case-workspace-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/employee-case-workspace-plan-critique.md) | Preserved original critique; assessed all dispositions |
| [.copilot-tracking/changes/2026-10-27/employee-case-workspace-changes.md](.copilot-tracking/changes/2026-10-27/employee-case-workspace-changes.md) | Compared implementation and parent validation record |
| [src/api/src/zava_forward/api/web/app.js](src/api/src/zava_forward/api/web/app.js) | Reviewed changed web file against fresh rules |
| [src/api/tests/test_ui_support.py](src/api/tests/test_ui_support.py) | Reviewed shell/script regression additions |
| [src/api/tests/test_auth.py](src/api/tests/test_auth.py) | Reviewed protected-asset regression addition |
| [src/api/tests/test_ai_tasks.py](src/api/tests/test_ai_tasks.py) | Reviewed assignment/configuration additions |
| [src/api/checks/employee_workspace_browser_check.py](src/api/checks/employee_workspace_browser_check.py) | Reviewed complete new three-scenario browser check |
| [src/core/src/zava_forward/core/store.py](src/core/src/zava_forward/core/store.py) | Reviewed wording-only change and unchanged assignment selection |
| [src/api/README.md](src/api/README.md) | Reviewed assignment/AI/redeploy runbook additions |
| [.copilot-tracking/reviews/logs/2026-10-27/employee-case-workspace-review.md](.copilot-tracking/reviews/logs/2026-10-27/employee-case-workspace-review.md) | This single independent Review |

## Next Steps

Return this result to the active parent for later topic-branch/PR continuation,
preserving all live limitations and Refs #73 #360 #104. No source correction,
additional agent or repeat Review is requested. Owner/operator follow-ups
RV-001/RV-002 require separate authority; no immediate user action is required
for this completed Review.
