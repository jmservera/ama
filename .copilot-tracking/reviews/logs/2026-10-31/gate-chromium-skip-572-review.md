---
title: Independent RPI Review for issue 572 Chromium discovery skips
description: One bounded post-implementation review preserving broader acceptance gaps
ms.date: 2026-10-31
---

## Scope and Evidence

* Task ID: #572, gate-chromium-skip-572.
* Review date: 2026-10-31.
* Review scope: caller-authorised exact enumeration of both Chromium reasons, unknown-skip rejection, preserved chat test-ID/project-api restriction and unchanged required browser dispatch.
* Assessed boundary: uncommitted source diff in tools/rpi-checks.py, tools/test_rpi_checks.py and src/README.md; original source context and the supplied task artifact set. No publication, real browser, SQL, Azure or complete gate acceptance.
* Plan: .copilot-tracking/plans/2026-10-31/gate-chromium-skip-572-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/gate-chromium-skip-572-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/gate-chromium-skip-572-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-31/gate-chromium-skip-572-changes.md
* Research: .copilot-tracking/research/2026-10-31/gate-chromium-skip-572-research.md

## Opening Review State

* Interpreted review goal: perform the task's single independent Review, reconcile the supplied evidence and judge the bounded correction without inventing whole-issue acceptance.
* Review scope: the exact supplied source and artifact boundary; existing browser tests and workflows remain read-only.
* Evidence readiness: supplied artifact paths are resolved; branch fix/gate-chromium-skip-572 has the three expected modified source files and untracked original task artifacts. Content reconciliation is pending.
* Acceptance basis: caller-confirmed exact reason enumeration and fail-closed behavior, existing scope restrictions, unchanged required dispatch, reconciled plan/critique and accurately bounded validation.
* First comparison boundary: compare plan markers and original critique dispositions against changes and the complete three-file diff, then inspect original parser/receipt/dispatch context.
* Active read-only boundaries: only this canonical review record may be written. No source/artifact fixes, nested delegation, heavy execution or additional review.
* Initial blockers: none identified at opening; full issue acceptance remains outside scope.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one independent comparison of the supplied artifact set, complete bounded working-tree diff and relevant original source context on 2026-10-31. HEAD is 4cb5964f7acce89668a37b5a56c3e125e26f6d21 on fix/gate-chromium-skip-572. The implementation is uncommitted; this is not an exact-head committed-candidate or receipt assessment.
* Additional evidence: issue #572 title/body retrieved read-only using gh issue view 572; tools/rpi-checks.py constants, check_skips, verify_commands, required_checks and Runner.browser; tools/test_rpi_checks.py retained and added contracts; src/api/tests/test_browser_asset_urls.py launch/skip behavior and src/api/tests/test_chat_panel.py decorator. Repository case-study/context documents informed boundaries, not validation claims.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Exact Chromium recognition and retained chat scope | Reconciled | Both strings are enumerated; separate chat identity/group predicate and independent integration rejection remain. |
| P01-T02 | Asset parser and receipt regressions | Reconciled | Two added test methods, one changed membership assertion, preserved existing tests and nine guide lines fit the budget. |
| P02-T01 | Validation Record | Reconciled | Four requested commands reported passed; workflow digest independently matches. No actual browser/SQL/full-gate claims. |
| Critique Disposition | Implementation-Time Plan and Detail Updates | Reconciled | Original Revise/PC-001 retained; explicit caller direction supports rejection of worker-local procedural restriction. |
| Follow-Up Items | Follow-Up Items and Pre-Review Reconciliation | Reconciled | Asset execution, complete gate/receipt and later approval remain separate from checked active markers. |
| Handoff and local commit acceptance | Ready for one independent bounded Review | Reconciled, pending parent continuation | This record supplies the one Review. Local commit is not yet present and is not claimed by the changes record. |

The checked P01/P02 markers and phase-detail completion statuses match the
implemented and reported validated scope. The research document retains early
`In progress` and Q1-Q3 `Open` labels, but its explicit Parent Synthesis and
Disposition and Planning Readiness answer those questions with C1-C7 and state
executed/Ready. These historical labels do not obstruct a credible comparison
or support an additional active research task. No artifact edits are made here.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | tools/rpi-checks.py | Enumerate both exact reasons without widening chat discovery or required integration acceptance | Complete diff and original predicate context | Reported 37-unit pass; static predicate comparison | Conformant within authorised boundary |
| P01-T02 | tools/test_rpi_checks.py | Add exact asset parser and synthetic receipt coverage; retain chat negatives and dispatch contracts | Two new methods; retained identity, flag, zero-execution and skip-rejection tests | Reported unit/Ruff/mypy passes | Test ownership and budget preserved |
| P01-T02 | src/README.md | Explain discovery recognition, exact chat boundary, skip accounting and no later asset execution proof | Complete nine-line addition and surrounding gate guide | Independent git diff --check passed | Accurate bounded documentation; no web implementation change |
| P02-T01 | .copilot-tracking/changes/2026-10-31/gate-chromium-skip-572-changes.md | Record focused validation and exclusions | Command/result table, shared critical-section summary and synthetic-output caveat | Caller and changes-record evidence; no rerun | Adequate bounded evidence, not a publication receipt |

The predicate preserves previous chat behavior for every group/test/integration
combination: its newly admitted reason is independently rejected unless both
project-api and the exact CHAT_PANEL_DISCOVERY_SKIP pair match. Integration
continues to reject every non-SQL_NOT_APPLICABLE pair before reason membership
can admit it. The asset reason is intentionally exact-reason-based in general
discovery, not test-ID-bound. Near-match/unknown rejection is preserved.

The mixed synthetic asset suite reports two tests, one executed and one skipped.
verify_commands recomputes these values from the hashed log and rejects an
altered receipt skip list; unchanged verification rejects zero execution.
The synthetic receipt fixture is not an actual browser execution or real gate
receipt. Existing required_checks and Runner.browser still install Chromium
before the exact chat selector, retain ZF_BROWSER_TESTS=1, test paths, suite=True
and integration=True. The complete diff changes no dispatcher, workflow,
WORKFLOW_HASHES, browser test, dependency or browser behavior.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| Critique Disposition and P02-T01 | Parent rejected PC-001 instead of substituting the prescribed shared lock | Caller explicitly prescribed flock and confirmed worker-local restriction is absent from parent constraints | Plan disposition and changes summary agree; original critique remains unchanged | One original final-candidate critique retained; no material source-design revision | Justified procedural disposition, no unresolved parent decision |
| P01/P02 markers, phase statuses and Handoff | Completion and validation summaries updated after implementation | Three-file diff and reported four-command pass | Plan/details/changes align on completion and exclusions | No significant or divergent design change; no fresh planning/critique required | Reconciled |
| Follow-Up Items | Preserve unproven browser/gate/publication acceptance | Research contrarian wave and original issue requirements | Research, plan, details and changes distinguish recognition from execution | Outside active phases throughout | Reconciled, routes below |

## Critique and Material Revision Assessment

* Latest critique dispositions: original verdict Revise and High PC-001 are preserved verbatim. PC-001 is recorded as rejected, not retroactively passed or erased.
* Material revisions: none in the source direction. Enumeration was expressly caller-authorised; keeping scoped chat safeguards and unchanged dispatch follows the accepted plan.
* Dependent-work pause assessment: P01/P02 followed the completed critique and recorded parent disposition. No evidence of affected work proceeding with an unresolved design decision.
* Justification assessment: the caller confirms the lock instruction is authoritative for parent execution and the critique's worker-local prohibition is not a parent constraint. That supports rejecting PC-001, including its derivative scratch/log concern; this Review does not invent such restrictions for the parent. No lock command or restricted scratch operation was executed by this reviewer.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Required asset browser execution evidence | Recognition fix cannot prove subsequent execution; required inventory presently owns chat, not the asset regression selector | Parent/coordinator to commission separately authorised owned-browser coverage and execution evidence before publication | Open, distinct follow-up RV-001; not an active-plan defect |
| Fresh complete exact-head gate, receipt verification and human/hosted approval | Caller prohibits heavy/full checks and publication in this task; candidate is uncommitted | Publication coordinator after final committed candidate and appropriate authorisation | Open, distinct follow-up RV-002; no current gate or issue closure |

Unresolved follow-ups remain separate from P01/P02 and do not make a known,
authorised discovery exception an implementation defect.

## Findings

No substantive implementation defect, unaccepted decision gap or material
research gap was found in the supplied correction. The following entries route
the preserved, non-blocking residual acceptance work once.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Actual browser execution and later asset ownership remain unproven

* Related scope: plan Follow-Up Items; original #572 owned execution and execution-regression criteria.
* Evidence: tools/rpi-checks.py required_checks and Runner.browser retain exact chat selector dispatch; src/api/tests/test_browser_asset_urls.py skips missing Chromium before installation. Research explicitly states the asset case is not a dedicated required later selector. No real browser run was authorised.
* Impact: static dispatch and synthetic regression evidence cannot establish actual chat execution or later asset execution. Whole browser acceptance remains open, without blocking this bounded parser correction.
* Destination: distinct follow-up, owned Chromium coverage/execution evidence.
* Smallest useful next action: parent/coordinator authorises separate browser work to establish owned later asset execution and collect actual chat/asset execution evidence; retain existing fail-closed contracts.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Complete exact-head publication evidence remains outstanding

* Related scope: plan Follow-Up Items; original #572 complete gate/receipt acceptance.
* Evidence: changes record excludes complete gate, actual MSSQL and publication receipt; git status shows uncommitted implementation and untracked original evidence. This Review is a working-tree assessment.
* Impact: no fresh browser/MSSQL complete gate or verified exact-head receipt exists for this candidate in the supplied evidence. Publication, approvals and issue closure remain unavailable.
* Destination: distinct follow-up, final-candidate publication validation.
* Smallest useful next action: publication coordinator, only after authorised final candidate preparation, runs the required complete gate and verifies its external receipt against current main immediately before publication, with independent exact-head and human/hosted approval gates preserved.

## Defects

* None within the accepted source/implementation boundary. No rpi-implement correction is requested by this Review.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001, Low | Distinct owned-browser follow-up | Parent/coordinator commissions coverage and real execution evidence | Original, explicitly excluded residual acceptance work |
| RV-002, Low | Distinct publication-validation follow-up | Publication coordinator establishes final-candidate complete gate/receipt and approvals | Original, explicitly excluded final-head acceptance work |

Later implementation of a routed finding does not require another Review of
this task.

## Residual Work

* RV-001 and RV-002 preserve the original browser/asset and complete gate/receipt gaps, respectively; neither is newly demanded inside this task.
* Local commit including original dated evidence and this Review remains parent-owned continuation. No commit, push, issue checklist update, closure or approval was performed here.

## Blockers and Remaining Work

* Blockers: none for the credible bounded Review or authorised implementation correction.
* Remaining active P01/P02 work: none evidenced.
* Full plan acceptance: independent Review supplied by this record; local commit remains pending. Whole issue acceptance and publication remain unproven as routed above.

## Validation Evidence

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| python3 -m unittest discover -s tools -p test_rpi_checks.py | Gate contracts | Passed, reported | Caller and changes record report 37 tests in 12.563s, OK |
| ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 tools/rpi-checks.py tools/test_rpi_checks.py | Two changed Python files | Passed, reported | All checks passed |
| ruff format --isolated --line-length 100 --check tools/rpi-checks.py tools/test_rpi_checks.py | Two changed Python files | Passed, reported | Two files already formatted |
| mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py | Two changed Python files | Passed, reported | No issues in two source files |
| git diff --check | Current bounded source diff | Passed, independently executed | No whitespace errors |
| sha256sum .github/workflows/src-ci.yml | Pinned workflow | Passed, independently executed | 94730d9a7c926613827fcbda312185720e80c51f304815f00d8f9ef17c89f076, unchanged from supplied hash |
| Actual browser/SQL/Azure/scanner and complete local gate/receipt verification | Broader acceptance | Skipped | Explicit caller prohibition; not substituted with synthetic gate tests |
| Targeted command reruns | Existing implementation evidence | Skipped | No repeat execution needed for this bounded read-only comparison |

The four implementation checks are attributed to the caller and original
changes record, not fresh reviewer execution. The changes record names external
gate-chromium-skip-572-validation.log; its full path/raw bytes were not supplied
or independently inspected. The reported common flock critical section and
exit zero are retained as reported evidence. Synthetic failed-group and VERIFIED
messages do not represent application failures or a successful actual gate.

## Outcome

* Outcome: Conformant.
* Outcome rationale: the authorised bounded correction meets its parser, accounting, receipt-regression, documentation and preservation requirements with reported focused checks passing. PC-001 rejection is justified by confirmed caller authority, not an unresolved divergence. Residual work remains distinct, and local-commit/full-issue/publication acceptance is not asserted.
* Severity summary: zero Critical, High or Medium findings; two Low residual-routing findings; zero source defects.
* Proven within this boundary: exact enumeration of both reasons; preserved scoped chat handling; fail-closed changed/unknown and integration skips; skip counts distinct from execution; synthetic receipt recomputation/tamper rejection; unchanged owned chat dispatch and pinned workflow; focused validation as reported; one preserved critique with recorded disposition and one independent Review.
* Unproven: actual chat/asset browser execution, asset later-selector ownership, a fresh complete browser/MSSQL gate, verified final-head receipt and publication approvals. Local commit acceptance is pending parent continuation.
* Original #572 criteria: owned chat selector/flag/inventory is present but real execution evidence is absent; fail-closed handling is supported without disabling tests or adding skip tokens; dispatch/negative regressions are present but do not prove real execution; complete exact-head gate/receipt criterion is unmet. Use Refs #572, not issue closure.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No correction requested |
| Decision gap or invalid assumption | None | Recorded PC-001 rejection supported |
| Material evidence gap inside bounded scope | None | Reported focused validation is sufficient for this scoped verdict |
| Non-blocking residual work | RV-001 owned-browser follow-up; RV-002 publication-validation follow-up | Parent/coordinator owns later authorisation and evidence |

* Execution status: Complete.
* Outcome: Conformant within the bounded correction.
* Validation coverage: reported unit/Ruff/mypy passes; independently inspected diff, context and workflow digest. No actual browser, SQL or full gate run.
* Blockers: none for Review; broader acceptance remains open.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/gate-chromium-skip-572-research.md](.copilot-tracking/research/2026-10-31/gate-chromium-skip-572-research.md) | Compared original research and residual limits |
| [.copilot-tracking/plans/2026-10-31/gate-chromium-skip-572-plan.md](.copilot-tracking/plans/2026-10-31/gate-chromium-skip-572-plan.md) | Compared scope, markers and dispositions |
| [.copilot-tracking/details/2026-10-31/gate-chromium-skip-572-phase-details.md](.copilot-tracking/details/2026-10-31/gate-chromium-skip-572-phase-details.md) | Compared implementation and validation details |
| [.copilot-tracking/reviews/plans/2026-10-31/gate-chromium-skip-572-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/gate-chromium-skip-572-plan-critique.md) | Preserved original Revise and PC-001 |
| [.copilot-tracking/changes/2026-10-31/gate-chromium-skip-572-changes.md](.copilot-tracking/changes/2026-10-31/gate-chromium-skip-572-changes.md) | Compared completion and reported check evidence |
| [.copilot-tracking/reviews/logs/2026-10-31/gate-chromium-skip-572-review.md](.copilot-tracking/reviews/logs/2026-10-31/gate-chromium-skip-572-review.md) | The single independent Review record |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Reviewed parser, receipt and dispatch context |
| [tools/test_rpi_checks.py](tools/test_rpi_checks.py) | Reviewed synthetic regression contracts |
| [src/README.md](src/README.md) | Reviewed related gate documentation |
| [src/api/tests/test_browser_asset_urls.py](src/api/tests/test_browser_asset_urls.py) | Unchanged asset launch/skip source |
| [src/api/tests/test_chat_panel.py](src/api/tests/test_chat_panel.py) | Unchanged chat opt-in context |
| [.github/workflows/src-ci.yml](.github/workflows/src-ci.yml) | Independently matched unchanged pinned digest |

## Next Steps

Return this single Review to the active parent for local-commit continuation
within its authority. Keep Refs #572 and both distinct residual follow-ups.
No new user action, source correction or second Review is required here.
Stop after this record; no publication or prohibited execution is authorised.
