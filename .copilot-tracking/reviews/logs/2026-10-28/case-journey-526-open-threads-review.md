<!-- markdownlint-disable-file -->
# Review: Case journey 526 open threads

## Scope and Evidence

* Task ID: 526-pr529-open-threads-20261028
* Review date: 2026-10-28
* Review scope: Sole independent post-implementation Review for active parent.
* Assessed boundary: Nine supplied changed source/test/documentation paths against HEAD 454fc49f4f8c5d7e4119ead247725990b2fa5c0c, associated task artifacts and external validation evidence. No implementation or publication authority.
* Plan: .copilot-tracking/plans/2026-10-28/case-journey-526-open-threads-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/case-journey-526-open-threads-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-28/case-journey-526-open-threads-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-28/case-journey-526-open-threads-changes.md
* Other evidence considered: Supplied research, session state and external open-threads-validation evidence; comparison pending at opening.

## Opening Review State

* Interpreted review goal: Independently assess the implemented five requirements and tightly coupled discard/error-retention behavior, preserving stepper semantics and distinguishing code acceptance from publication eligibility.
* Review scope: P01 and P02 implemented source, tests and validation; P02-T02 Review and coordinator commit/handoff bookkeeping.
* Evidence readiness: All six supplied artifact paths exist; nine modified implementation paths match the supplied boundary. Their contents and external validation have not yet been assessed.
* Acceptance basis: Supplied five requirements, current plan/details, critique dispositions, changed-code correctness and refreshed Web Interface Guidelines under repository ASCII/content rules.
* First comparison boundary: Reconcile task markers, changes, critique and session state before comparing the bounded diff and external validation evidence.
* Active read-only boundaries: Only this canonical review record may be written. No source/tracking-input edits, agents, repeat Review, heavy suite reruns, az, Azure, secrets, .env, paid models, publication or remote mutations.
* Initial blockers: Full publication gate is reported blocked because it invokes forbidden az. This is not yet a code verdict. Initial journey zoom failure must be preserved alongside the reported unchanged-source successful retry.

## Execution Status

* Execution status: Complete.
* Review execution evidence: One independent Review on 2026-10-28. Opening state was persisted before substantive comparison. Read the current research, plan, phase details, original critique, changes and session state; inspected the entire nine-file diff and directly relevant surrounding code, tests and retained validation logs/results. No agents, implementation fixes, tracking-input edits, heavy reruns, Azure commands or remote writes.
* Assessed identity independently verified: HEAD 454fc49f4f8c5d7e4119ead247725990b2fa5c0c; nine-path git diff --binary SHA256 211caf8060ab3beeb50294bb8fbcc1c8197f869bb0dc2450e2b3de0c2559747e, unchanged at final comparison.
* Existing topic branch: feat/case-journey-ux-526, continuing PR #529 per supplied research and parent direction. No fresh hosted-thread status or approval was inferred.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Shared live/cached dirty predicate and isolated route VM | Reconciled | Route and unload share reconciliation; retained tab-only navigation precedes the guard. |
| P01-T02 | Immutable review dispatch and record-bound newer-value recovery; sibling replacement/error retention | Reconciled | Successful review clears only unchanged submitted controls; later values stay copyable/dirty and completed actions cannot resubmit. |
| P01-T03 | Query-preserving native links and exact receipt contract | Reconciled | Selection/render and actual in-place pagination synchronize links; verifier and fixtures agree on 38. |
| P01 | All three tasks marked complete | Reconciled | Source and owning regression evidence support completion. No stepper semantic change found. |
| P02-T01 | Required local checks complete, first browser failure retained and unchanged-source retry passed | Reconciled | Final focused checks and browser retry cover final source; full API discovery overlapped the last error-retention adjustment, explicitly disclosed rather than represented as an exact-final full rerun. |
| P02-T02 / P02 | Review and authorized local commit/handoff remain unchecked | Reconciled | Marker correctly describes remaining bookkeeping, not incomplete source. This record supplies the one Review; parent owns marker/state updates and commit. |
| Follow-Up Items | Conditional coordinator publication | Reconciled | Remains outside local acceptance and cannot bypass the prohibited full-gate prerequisite. |

Historical "validation in progress" prose in the changes record and earlier session decisions is superseded by their explicit completed-validation and Pre-Review Reconciliation sections. The current plan/details, latest state decision and handoff agree; no stale marker prevents this Review.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/src/zava_forward/api/web/app.js; src/api/tests/test_workspace_scripts.py; src/api/tests/test_case_journey.py | Reuse rememberCaseFields before checking DOM flags/pendingFields; provide extracted route VM globals | app.js:209,231,971 and route tab-only fast path; pending-only cancellation, actual unload callback and clean-live retirement regressions | Independent focused 14 passed | Conformant |
| P01-T02 | src/api/src/zava_forward/api/web/app.js; src/api/tests/test_case_journey.py; src/api/checks/case_journey_browser_check.py | Freeze reason/text at dispatch; preserve newer fields as readonly, record-labelled recovery; disable duplicate/completed review actions | app.js:329-363,788 and documentsPanel submitted replacement callback; tests cover unchanged/text/reason/both/failure and delayed DOM response | Focused 14 passed; retained journey verifies immutable payload, submitted paragraph, later values and refresh survival | Conformant |
| P01-T02 sibling boundary | src/api/src/zava_forward/api/web/app.js | Confirm explicit discard before resident/template/document output replacement; append alerts instead of removing dirty intervening output on error | app.js:624-642,805-810,1181-1200; existing retained draft/document boxes and pending-key reconciliation inspected | Actual browser rejection of document replacement preserves later text; error paths inspected directly | Conformant; no speculative wider redesign |
| P01-T03 | src/api/src/zava_forward/api/web/case-workspace.js; src/api/src/zava_forward/api/web/panels.js; src/api/tests/test_case_journey.py; src/api/checks/case_journey_browser_check.py | Preserve non-tab parameters and native anchor behavior after pagination | case-workspace.js:99-121 and panels.js:281; repeated/encoded parameters tested; browser pages actual challenge history before clicking a journey link and traversing back/forward | Focused pass; browser asserts no confirm, same workspace node and retained dirty value | Conformant |
| P01-T03 | tools/rpi-checks.py; tools/test_rpi_checks.py | Require exactly 38 scans with matching positive fixture and adverse 37/39/serious cases | rpi-checks.py:959-964; test_rpi_checks.py:594-600 updates result/receipt hashes before verification, exercising result semantics rather than merely stale digests | Retained tooling suite 31 passed; independently inspected predicate and tests | Conformant |
| P02-T01 | src/api/README.md and owning checks | Document new guard/recovery/link behavior and bounded heavy admission; preserve adverse evidence | Guide matches implementation; three added unit methods are within the eight-method maximum, no removed tests or added scans | API 1168; focused 14; tooling 31; journey 153/38; assistants 30 | Conformant within stated local boundary |

The six ordered step names, stage mappings, earlier-evidence exceptions, blocker/current/closed semantics, native link elements, tab roles, keyboard behavior and focus handling are unchanged. Existing executable semantic tests passed independently.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 | Added discard confirmation and dirty-output error retention for resident/document replacement siblings | Direct sibling inspection found replacement could remove unsubmitted nodes; user explicitly required sibling inspection and edit preservation | Scope, phase details and changes describe the amendment and its rationale; source remains inside listed app.js boundary | Intent-preserving correction, no material architecture/scope/autonomy decision or new critique required | Reconciled |
| P02-T01 | Retried unchanged browser source with a shorter owned scratch path after real-zoom launch failed | Retained journey-01 fatal socket-path evidence; parent/user-approved shared-lock direction recorded | Separate attempt logs, environment/admission evidence, original failure, successful result hash and final diff identity retained | Validation-environment correction, not an implementation workaround or silent skip | Reconciled |
| P02-T02 / acceptance | Explicitly stop acceptance on unresolved in-scope findings or failed mandatory checks | PC-002 and original requirement to correct all five defects | Current plan acceptance, details and handoff distinguish source completion, findings, local commit and publication | PC-002 applied; original critique Revise unchanged | Reconciled |
| P02-T01 / PC-001 | Parent rejected worker-specific filesystem inference while retaining required shared admission | Supplied confirmed parent/user direction and recorded disposition | Plan/details/changes preserve rejection and rationale instead of rewriting critique | No new user-intent divergence established in this Review; reviewer did not execute any scratch/lock operation or write to /tmp | Reconciled at supplied authority boundary |

## Critique and Material Revision Assessment

* Latest critique dispositions: Original Complete / Revise, 1 High and 1 Medium, preserved verbatim. PC-001 is explicitly rejected by the planning parent with rationale and confirmed direction; it is not misrepresented as applied. PC-002 is applied to acceptance and handoff.
* Material revisions: No significant divergent scope, architecture, approval authority, dependency or test-budget change found. The sibling amendment is directly required by existing intent; the scratch-path retry changes validation environment only. Current plan/details and descriptive evidence cover both.
* Dependent-work pause assessment: The artifacts record critique disposition and plan readiness before implementation. This Review found no evidence of an unresolved material planning decision being bypassed; no fresh critique or second Review is requested.
* Justification assessment: Supported for this bounded local candidate. Parent execution-history paths are assessed as evidence, not permission for this reviewer to reproduce restricted filesystem actions.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Coordinator publication after complete current-base exact-head gate | User prohibits az/Azure; required full gate invokes az and was not run | Coordinator may commit the validated local candidate and original dated evidence; hold publication until a permitted, complete gate and immediate receipt verification are possible | Open distinct conditional follow-up; no current permission to invoke Azure, push, reply or resolve threads |

This follow-up is not an implementation defect or a new active source task.

## Findings

No substantive in-scope implementation defect, unaccepted decision gap or material research gap was established. No RV-xxx entry is fabricated for the known publication blocker, preserved adverse commands, manual acceptance limitations or open bookkeeping.

### Refreshed Web Interface Guidelines assessment

Source refreshed in full during this Review: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.

#### src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:209 - pass: reconciled pending/DOM navigation and beforeunload warnings; mounted tab-only path exempt.

src/api/src/zava_forward/api/web/app.js:335 - pass: native labelled controls, async status, immutable submitted values, copyable readonly later edits and disabled completed review actions.

src/api/src/zava_forward/api/web/app.js:805 - pass: explicit discard confirmation for dirty output replacement; rejected confirmation preserves nodes and cache.

src/api/src/zava_forward/api/web/app.js:1197 - pass: explicit alert retains dirty intervening document output; analogous resident error path at line 639.

#### src/api/src/zava_forward/api/web/case-workspace.js

src/api/src/zava_forward/api/web/case-workspace.js:93 - pass: native anchors and decorative aria-hidden glyphs retain existing stepper semantics.

src/api/src/zava_forward/api/web/case-workspace.js:99 - pass: URLSearchParams preserves non-tab/repeated values; no click-only navigation substitute.

#### src/api/src/zava_forward/api/web/panels.js

src/api/src/zava_forward/api/web/panels.js:281 - pass: synchronize hrefs after actual history.replaceState, retaining existing pagination status/focus behavior.

All fetched rule categories were considered for the changed boundary: accessibility, focus, forms, animation, typography, content handling, images, performance, navigation/state, touch/interaction, layout/safe areas, theming, locale, hydration, hover, content/copy and listed anti-patterns. Existing labels, native keyboard behavior, status/error semantics and CSS focus/wrapping/reduced-motion support remain in use. No new media, imagery, fonts, animation, theme, hydration, locale formatting, gesture, large-list renderer or layout/sticky-overlay behavior is introduced. Generic curly punctuation, ellipsis, title-case and ampersand advice does not override repository ASCII/plain-language rules. No visual redesign or whole-app audit was performed.

No new substantive changed-web guideline finding identified. This does not certify WCAG, manual contrast, screen-reader, staff/resident usability or production acceptance.

## Defects

* None established in the assessed nine-file boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | No rpi-implement, rpi-plan or rpi-research handoff | Active parent continues authorized bookkeeping | No actionable in-scope defect, decision gap or material research gap |

Later implementation of any separately identified finding would not require repeating this Review.

## Residual Work

* Existing conditional coordinator publication follow-up remains open, separate from code acceptance.
* Manual accessibility/contrast, screen-reader, staff/resident usability, deployed verification and hosted/human approval remain their existing owner-controlled acceptance activities, not new active implementation tasks. The retained axe result has 37 incomplete color-contrast rule results across its 38 scans; these are manual-check limitations, not reported automated violations or proof of conformance.

## Blockers and Remaining Work

* Publication blocker: Full rpi-checks.py --all and current-base exact-head receipt verification were not executed because the gate invokes prohibited az. No cloud fallback, skipped-prerequisite success, protection change or publication eligibility is asserted.
* Remaining active work: Parent-owned P02-T02 Review/state/plan completion bookkeeping, authenticated noreply local commit with required trailer and Refs #526, and explicit local-only coordinator handoff. This reviewer does not perform those mutations.
* No unresolved in-scope source work was established. P02 remains unchecked for the above bookkeeping only.
* No push, thread reply/resolution, merge, hosted approval or human acceptance is authorized or established by this record.

## Validation Evidence

External evidence root, workspace-relative: ../../../.copilot/session-state/e7894362-b3b0-4580-89f4-7ed23a4bf20b/files/open-threads-validation/.

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Existing API unittest discovery; api-unit.log and heavy-results.log | API package | Passed, retained parent execution independently read | 1168 tests in 423.616s, 316 explicit opt-in skips, exit 0. Skips are not SQL/browser/live acceptance. Run overlapped final sibling error-path adjustment, as disclosed. |
| PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -B -m unittest test_workspace_scripts test_case_journey -q, from src/api | Final source; independent lightweight Review execution | Passed | 14 tests in 1.891s. Parent focused-final.log separately records 14 passed in 1.990s after final adjustment. |
| tools/test_rpi_checks.py; tool-unit.log | Receipt verifier and fixtures | Passed, retained parent execution independently read | 31 tests in 12.502s; interruption-probe KeyboardInterrupt/TimeoutExpired is expected suite evidence, not a silently ignored suite failure. Tool suite not rerun by reviewer. |
| case_journey_browser_check.py, journey-01.log and heavy-results.log | Functional/browser/axe, first attempt | Failed, preserved | 38 axe scan assertions passed; separate real-zoom Chromium launch aborted with Socket path too long; JOURNEY_EXIT=1. Original attempt is not relabelled passed. |
| Same unchanged journey harness, journey-02.log and browser-retry-results.log | Final-source browser retry | Passed, retained execution independently verified | 153 PASS assertions; 38 scans, zero violations, zero page errors; Chromium 156.0.8078.4; actual chrome.tabs.setZoom=2; innerWidth<=640. |
| journey-02/results.json SHA256 and axe source SHA256 | External evidence identity | Passed, independent read | Results 79be0afa1f705756f0ede4b8ed97d4e0cf7b7a52a4cea6cae2564abb003cfac1. Axe 4.10.3 bytes 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb match the source pin. |
| assistants.log and browser-retry-results.log | Existing assistants browser suite | Passed, retained parent execution independently read | 30 checks; no page errors; no billable provider/private-data acceptance inferred. |
| Heavy admission and retry logs | Execution coordination | Recorded, not rerun | Separate admissions at 22:34:19Z and 22:42:15Z. Parent records actual shared flock -n with <=2400-second bounded retry and no foreign resource mutation; reviewer inspected evidence without manipulating locks/processes/scratch. Short owned retry TMPDIR is recorded in browser-retry-environment.log. |
| .venv/bin/ruff check --no-cache src/api; .venv/bin/ruff format --no-cache --check src/api | API owning lint/format | Passed, independent no-write Review execution | All checks passed; 48 files already formatted. |
| .venv/bin/ruff check --no-cache --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 tools/rpi-checks.py tools/test_rpi_checks.py; isolated format --check | Owning tooling lint/format | Passed, independent no-write Review execution | All checks passed; 2 files already formatted. |
| API mypy; api-types.log; tooling mypy in supplied changes/parent evidence | Types | Passed as recorded, not rerun | API log confirms 95 source files. Tooling 2-file result is supplied execution evidence; no separate tooling type log was present in the external inventory. |
| Earlier root-config tooling Ruff | Unrelated baseline | Failed, preserved as reported | Nine pre-existing findings outside changed lines; owning isolated lint passes. No unrelated fixes or blanket root-lint success claimed. |
| node --check on app.js, case-workspace.js, panels.js; git diff --check | Changed JS and whitespace | Passed, independent execution | No parse or whitespace errors. |
| AST-read WORKFLOW_HASHES compared with actual .github/workflows bytes | Five workflow pins | Passed after corrected reviewer probe | Initial reviewer probe incorrectly treated basename keys as root-relative and raised FileNotFoundError for src-ci.yml; corrected read-only prefix verified all five true. No workflow/pin edits. |
| Full local publication gate, SQL/scanner/hosted/manual acceptance | Publication and wider acceptance | Not run / unavailable in this Review | User prohibits az; local focused/browser evidence is not a full receipt or hosted/human approval. No heavy suite rerun or forbidden command performed. |

Browser artifact `incomplete` contrast results are explicitly retained above. Automated zero violations are not substituted for their manual determination.

## Outcome

* Outcome: Conformant.
* Outcome rationale: The five requirements and tightly coupled discard/error-retention amendment are implemented coherently, with executable owning regressions and credible retained final-source browser evidence. Independent focused tests, no-write lint/format, parse, whitespace, result/pinned-byte checks passed. No substantive in-scope defect or unaccepted decision divergence was established.
* Acceptance boundary: Code/local-task acceptance only. Review execution is Complete while P02-T02 commit/handoff bookkeeping remains parent-owned. Publication is blocked, and hosted/manual/human acceptance remains unperformed. The preserved critique Revise, first browser failure and adverse lint/probe outcomes are not rewritten.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No source correction required by this Review |
| Decision gap or invalid assumption | None | No new planning decision required |
| Material evidence gap | None for local assessed scope | Wider full-gate evidence remains explicitly unavailable, not passed |
| Non-blocking residual work | Existing distinct coordinator publication and manual/hosted acceptance activities | Coordinator/owner retains gates and approval authority |

* Execution status: Complete.
* Outcome: Conformant.
* Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low substantive findings.
* Validation coverage: All five requirements and stepper preservation inspected; independent focused 14 and owning lint/parse/identity checks passed; API/tooling/browser/assistants evidence independently read within stated limits.
* Blockers: Full publication gate prohibited by az boundary; no push/reply/resolution eligible. No source blocker established.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/case-journey-526-open-threads-research.md](.copilot-tracking/research/2026-10-28/case-journey-526-open-threads-research.md) | Five-thread evidence and alternatives |
| [.copilot-tracking/plans/2026-10-28/case-journey-526-open-threads-plan.md](.copilot-tracking/plans/2026-10-28/case-journey-526-open-threads-plan.md) | Current scope, markers and follow-up |
| [.copilot-tracking/details/2026-10-28/case-journey-526-open-threads-phase-details.md](.copilot-tracking/details/2026-10-28/case-journey-526-open-threads-phase-details.md) | Phase criteria and amendments |
| [.copilot-tracking/reviews/plans/2026-10-28/case-journey-526-open-threads-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/case-journey-526-open-threads-plan-critique.md) | Original Complete / Revise preserved |
| [.copilot-tracking/changes/2026-10-28/case-journey-526-open-threads-changes.md](.copilot-tracking/changes/2026-10-28/case-journey-526-open-threads-changes.md) | Implementation, validation and adverse history |
| [.copilot-tracking/rpi-sessions/2026-10-28/case-journey-526-open-threads-state.json](.copilot-tracking/rpi-sessions/2026-10-28/case-journey-526-open-threads-state.json) | Active parent state, unchanged by reviewer |
| [.copilot-tracking/reviews/logs/2026-10-28/case-journey-526-open-threads-review.md](.copilot-tracking/reviews/logs/2026-10-28/case-journey-526-open-threads-review.md) | Sole independent Review record |

## Next Steps

Active parent: consume this sole Review, complete authorized P02-T02 bookkeeping and the validated local commit/handoff. Preserve the publication blocker and manual/hosted approval boundaries; do not invoke az, push, reply or resolve threads. No additional Review or user action is required for this local code assessment.
