<!-- markdownlint-disable-file -->
# Review: gate-chat-test-572

## Scope and Evidence

* Task ID: 572
* Date: 2026-10-31
* Scope: single original independent Review of this task's complete diff from 368d3bb8.
* Integrated source head: b9a0db4511411bb16f0c15b46ed162f405634951.
* Plan: .copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md
* Details: .copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-31/gate-chat-test-572-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-31/gate-chat-test-572-changes.md
* Research: .copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md
* Assessed boundary: complete nine-file committed task diff from 368d3bb8 to b9a0db4511411bb16f0c15b46ed162f405634951, current uncommitted task-evidence reconciliation, AC1-AC4, P01-P03 and original PC-001 disposition. Relevant unchanged gate command inventory, runtime dispatch, suite accounting, receipt fixtures and exact chat-panel browser test were inspected.
* Other evidence: tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md, src/api/tests/test_chat_panel.py and its synthetic Matrix fixture; the unchanged 2026-10-30 original chat-panel Review; parent-supplied validation results.
* Repository original/addendum, knowledge-base index and owner memory were consulted as context, not validation or customer acceptance evidence. Issue/PR intake and dependency-restoration facts are supplied task evidence, not freshly network-verified facts.

## Opening Review State

* Goal: assess exact named browser success proof, preserved skips, regression semantics, plan reconciliation and actual acceptance evidence.
* Evidence readiness: complete source/artifacts available; 39 tooling tests and static checks passed after main integration.
* Acceptance basis: issue AC1-AC4, current plan and resolved PC-001.
* First comparison: both parser call sites, trusted exact selector, receipt mutations and inherited local Chromium ownership.
* Read-only boundary: only this review record may be written; no source/other artifact edits, Git mutation or runtime tests.
* Initial blockers: restored API/browser could not obtain shared lock in two 600s attempts; no actual Chromium result or final full receipt.

## Execution Status

* Review execution status: Complete. This single original independent Review compared all current acceptance criteria, planned markers, source changes, critique dispositions and supplied validation once on 2026-10-31.
* Implementation-plan execution status: Partial. P01 is complete; P02-T01 has passing tooling/static checks but missing successful restored API and actual Chromium execution. This record completes the P02-T02 Review deliverable only; its checklist/state reconciliation belongs to the parent. P03-T01 remains pending.
* Actual restored API/browser execution: Blocked at admission by foreign shared-lock contention. Publication is Blocked until required execution and a fresh complete exact-head gate/verification and eligible independent exact-head assessment exist.
* Complete source review does not mean complete implementation acceptance. No tests, network calls, credential/private-data access, source/other-artifact edits or Git mutations were performed by this reviewer.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Optional exact-ID enforcement in check_skips and both call sites | Reconciled | Source implements selected direction; generic default retained |
| P01-T02 | Two new methods, five semantic receipt cases, both fixtures corrected, guide clarified | Reconciled | No test removal, UI/runtime/workflow change or new harness |
| P02-T01 | Tooling/static passes; initial API dependency errors; two restored admission timeouts | Partial, accurately recorded | Actual restored API and exact Chromium remain unavailable, RV-001 |
| P02-T02 | One independent original Review with separate execution/outcome | Completed by this record | Parent-owned markers remain unchecked until parent reconciliation; original outcome must be preserved |
| P03-T01 | Final evidence commit, complete gate, verification, assessment and publication | Pending as planned | Missing final receipt is a post-Review obligation, not a sequencing defect, RV-002 |
| Follow-Up Items | None in plan, details or changes | Reconciled | Remaining P02/P03 obligations are not silently moved outside acceptance |

The current plan, details, changes and session state agree on source completion,
two blocked restored attempts, Review now and final gate later. Committed
checkpoint wording is historical; current uncommitted evidence explicitly
reconciles it. No stale full-success claim prevents a credible boundary.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01; AC1/AC3 | tools/rpi-checks.py:1034-1073 | Add default-None expected_test, derived from the existing complete verbose ID | Exact branch requires reported total 1, no skips and the complete result-line list equal to one expected ID with status ok | Parent reports 39 tooling tests pass | Conformant source implementation; actual Chromium not established |
| P01-T01; AC1/AC2 | tools/rpi-checks.py:940-952, 1307-1320 | Apply identical parser rule in verify_commands and Runner.command | Both select expected ID using exact CHAT_PANEL_BROWSER_SELECTOR argv membership; verifier first binds trusted argv/cwd/env/suite/integration and log digest | Parser/runtime/receipt regressions covered | Runtime/verifier parity supported |
| P01-T01; AC2 | tools/rpi-checks.py:64-103, 1040-1064 | Preserve discovery and integration rules | Allowlist and exact SQL_NOT_APPLICABLE pair unchanged; chat reason allowed only for exact ID in non-integration project-api; skipped totals must match enumerated reasons | Existing exact discovery, dependency/integration and count regressions retained | No broadened skip exception |
| P01-T02; AC3 | tools/test_rpi_checks.py:117-225 | Extend owned regressions within two-method ceiling | New parser method tests exact pass, unrelated generic compatibility and rejection of wrong/expected-failure status; new Runner.command method tests actual child-output parsing with exact-selector argv | Parent reports 39 tests pass after integration | Synthetic child-output exercise is not actual browser execution |
| P01-T02; AC3 | tools/test_rpi_checks.py:117-185 | Reject wrong, missing, duplicate, additional success lines and wrong totals | Five cases update log bytes, row counts and skips, row sha256 and receipt files hash before verify_commands; saved original log restored after each subtest | Existing mutation method retained and extended | Rejection exercises semantics, not stale digest/count rejection alone |
| P01-T02; AC3 | tools/test_rpi_checks.py:387-392, 727-732 | Correct scoped and complete successful receipt fixtures | Only exact chat command receives required verbose ID; other suites retain generic fixture success; verifier positive paths remain covered | Parent tooling pass includes both fixture owners | No unrelated suite contract changed |
| P01-T02; scope | src/README.md:180-188 | Explain exact named success proof and limits | Guide matches one exact successful result, one reported test, zero skips and rejection despite matching hashes | Direct diff/Markdown review | Directly related documentation only |

### Inherited command and semantic ownership

* tools/rpi-checks.py:90-96 keeps the exact selector and derives its verbose ID without a second spelling. required_checks:707-714 and Runner.browser:1639-1645 still agree on `-m unittest -v`, that exact method, API cwd, `ZF_BROWSER_TESTS=1`, suite and integration flags. API/core/agents fixture paths and the existing safety-path handling remain unchanged.
* Existing Chromium installation precedes the required command. coverage_rows continues to include browser in the project workflow equivalence. There is no task-local workflow or inventory weakening.
* The unchanged src/api/tests/test_chat_panel.py:563-630 owns actual semantics: opt-in local Chromium, keyboard expansion/opening/submission and focus, status/request-failure feedback, enabled/disabled send state, privacy description, refusal, polite live conversation log, unsent-question preservation and mobile visibility. It aborts off-origin requests and asserts no model prompts.
* PanelTests/Matrix uses constructed fixture data and a loopback server, not a private working dataset. Inspection confirms ownership and scope, not a browser pass, production service behavior, human accessibility acceptance or live model acceptance.
* Generic suite behavior is preserved: with expected_test=None all pre-existing accounting/allowlist/summary checks and return structure are unchanged. Exact enforcement is not activated for ordinary API discovery, unrelated suites or SQL suites.

## Acceptance Criteria Assessment

| Criterion | Source/regression assessment | Execution and acceptance state |
| --- | --- | --- |
| AC1 | Conformant source: inherited exact selector/flag/path/coverage retained; both runtime and verification now reject aggregate-only unrelated success | Partial. No actual opted-in Chromium output proving one exact executed test and zero skips; RV-001 |
| AC2 | Supported by unchanged fail-closed rules and retained negative regressions, including dedicated chat skips and unexpected dependencies/integration skips | Tooling evidence supports source contract. Initial API suite failed; restored API and complete integration execution unproven. No actual all-suite pass claimed |
| AC3 | Conformant at tooling level: two new methods, five semantic mutations with recomputed evidence, corrected fixtures, inherited dispatch/discovery tests and no removals | Parent reports all 39 tooling tests passed after merge in 12.506s; reviewer did not rerun. Synthetic regressions do not satisfy AC1/AC4 |
| AC4 | Conformant sequencing design: preserve original Review, commit final evidence candidate, fetch main, run complete gate, verify and assess exact head before publication | Unmet at this boundary. No final committed candidate receipt, actual complete browser/MSSQL result, receipt verification or eligible exact-head assessment; RV-002 |

No AC1/AC4 completion, issue closure, publication eligibility, human approval or
hosted approval is established by this Review.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01/T02 | Exact-ID branch and bounded tests/guide completed | C3/C4 aggregate-only weakness; no new user decision | Current plan completion markers, detail completion paragraphs and changes P01 agree | Selected direction unchanged | Reconciled |
| P02-T01 | Restore existing declared package extras; preserve failed API result and two blocked attempts | Missing azure.eventhub and API metadata, then two 600s lock-admission timeouts; no pin/source change or new decision | Plan executive summary/handoff, details status/current evidence, changes validation/blockers and current session state agree | Operational evidence update, not material scope revision | Reconciled; execution still incomplete |
| P02-T02/P03-T01 | Permit source Review after bounded failed admission; retain real validation and post-Review final gate obligations | Known absent execution; caller requires one original Review and no correction loop | Current plan/details explicitly distinguish credible source review from acceptance; changes remaining work mirrors them | PC-001-compatible sequencing clarification; no new significant decision | Reconciled; no weakened criterion |
| P03-T01; current-main integration | Intermediate checkpoint f8c40802 followed by merge b9a0db45 from current reviewed main 368d3bb8 | Main drift recorded in changes; ancestry needed for final gate | Plan/details permit checkpoint and non-rewriting topic merge; changes record completion/base | No source-scope or acceptance revision | Reconciled |

Git history shows b9a0db45 has parents f8c40802 and 368d3bb8: the topic retains
checkpoint ancestry and incorporates the reviewed main without rewriting.
The base-to-head diff contains only nine task files. The first-parent tooling
delta retains upstream staff_blob lint/type inventory and src-ci hash changes;
the task diff against 368d3bb8 does not alter those upstream contracts or the
workflow. The final original-evidence candidate commit has not happened.
Current origin/main freshness was not network-checked here and must be fetched
again by the publication parent.

## Critique and Material Revision Assessment

* The original 2026-10-31 critique remains Complete / Revise with PC-001 [High], unchanged. Its adverse original verdict is not rewritten as an approval.
* PC-001's direct-compatible disposition is supported: P02-T02 and P03-T01 in both plan and details explicitly stop publication for unresolved blocking current-task source/acceptance findings, authorize obtaining the deliberately later final gate evidence in P03, and require explicit nonblocking-residual disposition without weakening criteria. P03 also requires an eligible independent exact-head assessment.
* This resolves the planning ambiguity, not runtime acceptance. No unsupported material design change or significant/divergent decision requiring rpi-plan was found. No dependent source work is shown continuing before that compatible rule was recorded.
* The unchanged 2026-10-30 original Review remains adverse as to actual execution and complete exact-head acceptance. Its findings are not closed by this task's fixture/static passes. Its separate prior PC-001 disposition is not confused with the current PC-001 or re-litigated as a lock-location source defect.
* Missing final receipt is not an original-Review source defect or a reason to prohibit planned P03 evidence gathering. Conversely, missing actual execution still prevents acceptance/publication until proved. No foreign contention is classified as a browser assertion failure.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| None | No plan follow-up is recorded | Parent retains P02-T01 and P03-T01 | These are active remaining acceptance obligations, not newly deferred source tasks |

Unresolved execution/acceptance obligations remain in their existing markers.
Human/hosted approvals retain their existing owners outside this local source
assessment; no new follow-up artifact or active task is created by Review.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Successful restored API and actual exact Chromium evidence remain unavailable

* Related scope: P02-T01, AC1 and execution coverage of AC2.
* Evidence: current changes Validation Record and Blockers, current details P02-T01, current plan unchecked P02-T01, and supplied parent results. Initial API discovery ran 1368 tests in 577.333s with three import/metadata errors and 320 skips. After declared dependency restoration, two API/browser attempts each timed out after 600s on the foreign shared lock, with empty logs before execution.
* Impact: tooling/dispatch/parser fixtures prove neither successful restored API discovery nor one real opted-in exact browser test with zero skips. AC1 remains partial and full execution acceptance is unavailable. The evidence demonstrates contention, not a source defect or failed browser assertions.
* Destination: material evidence gap, rpi-research evidence category; active parent/execution coordinator owns collection through existing P02-T01. No new research invocation, source correction or current-task Review loop is requested.
* Smallest useful next action: obtain admission without bypassing the shared lock or interrupting its holder; run the requested restored API discovery and exact opted-in Chromium command and preserve actual logs/counts externally. Retain the original failed and blocked results alongside any later evidence.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Complete final exact-head acceptance and publication remain unestablished

* Related scope: P03-T01, AC4 and the current PC-001 publication rule.
* Evidence: plan/details P03-T01, changes Remaining Work and src/README.md Local RPI gate. Reviewed source is b9a0db4511411bb16f0c15b46ed162f405634951 with current task-evidence updates uncommitted; no final original-evidence candidate commit or successful full receipt/verification is supplied.
* Impact: premature publication or whole-issue acceptance would violate AC4. This is a planned later evidence prerequisite, not a blocking source defect and not a demand to run the final committed gate before this Review.
* Destination: material acceptance-evidence gap, rpi-research evidence category; active publication parent owns the already planned P03-T01 execution and verification. It is not a new rpi-implement task or an out-of-scope deferral.
* Smallest useful next action: preserve this original Review and critique, reconcile parent-owned evidence state, commit the final candidate/original evidence, fetch current main and run fresh --all under the runner's own unchanged lock into a new external directory. Require actual browser/MSSQL and every required group, verify against freshly fetched current main immediately before publication and obtain eligible independent exact-head assessment. Any later commit/base/tool/image/input change invalidates the gate. A failed/unavailable result stops publication.

## Defects

* No blocking source implementation defect or unaccepted design divergence was found in the assessed frozen diff. No rpi-implement correction is requested.
* Severity summary: Critical 0; High 1 planned acceptance-evidence prerequisite; Medium 1 execution-evidence gap; Low 0. Neither finding alleges a source defect.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-research evidence category; existing P02-T01 | Active parent/execution coordinator collects actual API/browser results after admission | Known material execution evidence gap, not source correction |
| RV-002 | rpi-research evidence category; existing P03-T01 | Active publication parent commits final evidence candidate and obtains/ verifies complete exact-head gate and independent assessment | Planned post-Review acceptance prerequisite, not pre-Review sequencing defect |
| Implementation defect | None; no rpi-implement route | None | No source defect found |
| Decision gap or invalid assumption | None; no rpi-plan route | None | PC-001 directly reconciled; no unresolved significant choice |
| Nonblocking out-of-scope residual | None; no distinct follow-up route | None | Required remaining execution is still active plan/acceptance scope |

Later collection of evidence or implementation of a routed finding does not
require another original Review. This record's original outcome is preserved.

## Residual Work

* Required remaining work: actual successful restored API discovery and exact Chromium evidence in P02-T01, followed by P03-T01 complete committed gate, receipt verification and eligible independent exact-head assessment/publication gates.
* No nonblocking out-of-scope source residual or new follow-up item was identified. These remaining obligations are not removed from AC1-AC4.

## Blockers and Remaining Work

* Shared heavy-lock contention blocks restored API/browser execution after two bounded admission attempts. Availability is unknown; no lock bypass, foreign-process interruption or fabricated execution status is authorized.
* Actual Chromium, successful restored API and complete final browser/MSSQL gate are unproven. Final receipt deliberately follows original Review and the final evidence commit; its absence does not block source-review completion.
* Parent must reconcile P02-T02/state using this record without changing its original findings/outcome. P02-T01 stays incomplete until its required execution evidence exists; P03-T01 remains pending.
* Publication and whole acceptance remain blocked. Independent exact-head assessment is separate from this original Review; neither replaces human or hosted approval.

## Validation Evidence

| Command or check | Scope | Status | Summary and limit |
| --- | --- | --- | --- |
| Tooling unittest discovery for tools/test_rpi_checks.py | Existing gate regressions | Passed, parent-supplied | 39 tests after integration in 12.506s; prior pass 14.536s. Reviewer ran no tests |
| Targeted Ruff check and format check | tools/rpi-checks.py, tools/test_rpi_checks.py | Passed, parent-supplied | Rerun successfully after integration; earlier line-length failure corrected before frozen boundary |
| Strict mypy | Two tooling files | Passed, parent-supplied | Supplied integrated validation; no reviewer rerun |
| Pinned API Ruff check and format check | src/api | Passed, parent-supplied | 65 files; static result does not imply API/browser execution |
| Requested API unittest discovery with supplied fixture paths | src/api/tests | Failed, parent-supplied | Ran 1368 in 577.333s, errors=3, skipped=320; two modules missing azure.eventhub and one missing API distribution metadata |
| pip restoration of existing core/agents/API declared extras | External parent venv | Completed, parent-supplied prerequisite step | No manifest/pin changes; installation does not establish suite success |
| Restored API/browser attempts | Existing shared heavy admission | Unavailable: blocked before execution | Two 600s admission timeouts, both logs empty; no enclosed test executed |
| Exact test with ZF_BROWSER_TESTS=1 and unittest -v | Actual local Chromium | Unavailable | No real browser result, named successful line or execution counts supplied |
| Final --all and --verify-receipt | Every required group, browser/MSSQL, final committed head/current main | Unavailable, planned P03 | No full receipt or verification yet; not inferred from mocked complete fixture |
| Independent exact-head assessment / hosted and human approval | Publication boundary | Unavailable | Later distinct gates, not performed here |
| Diff/source/artifact comparison | Frozen task boundary | Complete reviewer inspection | No tests, network, source/other-artifact or Git mutation |

The 320 initial API skips are observed failure-run counts, not a newly approved
allowlist or proof that complete integration accounting passes. Missing
dependencies were the supplied cause of the three initial errors; no claim
of successful restored API or Chromium is made.

## Outcome

* Source disposition: Conformant within the assessed frozen implementation and tooling-evidence boundary. No blocking source defect found.
* Overall task outcome: Residual work. AC1 actual execution is partial and AC4 acceptance/publication evidence is unavailable; whole-task acceptance is Not accepted at this boundary.
* Review execution: Complete, separate from Partial plan execution and Blocked runtime/publication.
* Rationale: narrow parser/runtime/verifier parity and semantic regressions satisfy source intent without weakening skips or generic contracts. Planned remaining execution cannot be replaced by source inspection, passing fixtures, dependency availability or completion of the one original Review.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No source correction handoff |
| Decision gap or invalid assumption | None | No new rpi-plan handoff; retain original PC-001 direct disposition |
| Material evidence gap | rpi-research evidence category; active P02-T01/P03-T01 continuation | Parent obtains required real execution and fresh final exact-head evidence, RV-001/RV-002 |
| Nonblocking residual work outside scope | None | No new follow-up scope; required work remains active |

* Execution status: Complete for this original Review; implementation plan Partial.
* Outcome: Residual work overall; source Conformant; whole acceptance Not accepted.
* Validation coverage: parent-supplied 39 tooling tests and tooling/API static checks pass; initial API failed; restored API/browser and final full gate/verification unavailable.
* Blockers: foreign shared-lock admission and missing actual/final acceptance evidence.
* Publication consequence: no blocking source finding prevents gathering planned later evidence, but publication remains forbidden until requirements and all independent/human/hosted gates pass. No current-task correction/review loop is authorized.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md](.copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md) | Current plan and acceptance obligations |
| [.copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md](.copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md) | Current phase evidence and sequencing |
| [.copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md](.copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md) | Bounded original research |
| [.copilot-tracking/reviews/plans/2026-10-31/gate-chat-test-572-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/gate-chat-test-572-plan-critique.md) | Immutable original Complete / Revise critique |
| [.copilot-tracking/changes/2026-10-31/gate-chat-test-572-changes.md](.copilot-tracking/changes/2026-10-31/gate-chat-test-572-changes.md) | Implementation and supplied adverse/passing validation |
| [.copilot-tracking/rpi-sessions/2026-10-31/gate-chat-test-572-state.json](.copilot-tracking/rpi-sessions/2026-10-31/gate-chat-test-572-state.json) | Current parent-owned Review handoff state |
| [.copilot-tracking/reviews/logs/2026-10-31/gate-chat-test-572-review.md](.copilot-tracking/reviews/logs/2026-10-31/gate-chat-test-572-review.md) | This single original independent Review |
| [.copilot-tracking/reviews/logs/2026-10-30/chat-panel-test-in-gate-572-review.md](.copilot-tracking/reviews/logs/2026-10-30/chat-panel-test-in-gate-572-review.md) | Preserved prior original adverse execution/acceptance findings |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Runtime, trusted inventory and receipt verification |
| [tools/test_rpi_checks.py](tools/test_rpi_checks.py) | Owned regressions and corrected receipt fixtures |
| [src/api/tests/test_chat_panel.py](src/api/tests/test_chat_panel.py) | Unchanged exact Chromium semantic owner |
| [src/api/tests/test_role_matrix.py](src/api/tests/test_role_matrix.py) | Unchanged synthetic loopback fixture |
| [src/README.md](src/README.md) | Gate guide and exact evidence contract |

## Next Steps

Return this one original Review to the active parent. Parent owns evidence-state
reconciliation and clearing RV-001 through existing P02-T01, then the final
candidate/evidence commit and fresh complete gate/verification/independent
exact-head assessment under P03-T01. Preserve all original adverse evidence and
this outcome; no second original Review or source correction loop is requested.
If required execution or publication gates remain unavailable or fail, stop
publication and report the blocker. No user command or source-defect handoff is
required by this source disposition. This Review stops here.
