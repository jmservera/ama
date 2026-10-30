<!-- markdownlint-disable-file -->
# Review: Nonblocking regulatory usage refresh

## Scope and Evidence

* Task ID: reg208-pr506-usage-refresh-2026-10-29
* Task slug: regulatory-usage-refresh
* Review date: 2026-10-29
* Scope: full bounded task P01, not the entire PR.
* Baseline: 7e8ab4d5290177ef48b17d27ea8d64a4f39e8c73.
* Plan: .copilot-tracking/plans/2026-10-29/regulatory-usage-refresh-plan.md
* Details: .copilot-tracking/details/2026-10-29/regulatory-usage-refresh-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/regulatory-usage-refresh-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-29/regulatory-usage-refresh-changes.md
* Research: .copilot-tracking/research/2026-10-29/regulatory-usage-refresh-research.md

## Opening Review State

* Goal: independently assess the nonblocking lookup fix and focused regression
  against caller requirements and the reconciled full plan.
* Evidence readiness: all implementation markers complete; red/green, 69
  selected tests, Node syntax and focused Ruff results recorded.
* Acceptance basis: question/control recovery before usage settlement,
  failure containment, preservation of answer and changed-field state.
* First comparison boundary: implementation diff in chat.js,
  test_case_journey.py and API README; then original RPI evidence consistency.
* Active boundary: read-only except this single review record. No source or
  plan modification; no repeated critique, Review or closure loop.
* Initial blockers: none.

## Execution Status

* Original pending-opening record, preserved verbatim: "Pending the single independent reviewer assessment. No verdict is asserted."
* Execution status: Complete.
* On 2026-10-29, one independent post-implementation Review compared the full
  bounded P01 evidence with the three-file working-tree diff against the
  stated baseline. HEAD and branch match the supplied boundary.
* The pending statement above records intake, not the current verdict.
* Only this canonical review file was edited. Source, tests, planning,
  critique, research, changes and workflow state remain read-only.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | One deferred usage regression, original-code red result and four scenarios | Reconciled | Exactly one method added; real chat.js and shipped field helpers execute; existing methods retained |
| P01-T02 | Cleanup before nonawaited usage refresh; owning API guide updated | Reconciled | Diff changes only the intended ordering/await and four documentation lines |
| P01-T03 | Selected modules, Node syntax, focused Ruff and diff checks | Reconciled | Recorded green evidence independently reproduced; all P01/detail markers agree |
| P01 and handoff | No active implementation work; one Review and local commit parent-owned | Reconciled | This Review completes assessment, not the later local commit |
| Follow-Up Items | None | Reconciled | Plan, details, changes and state identify no active follow-up |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/tests/test_case_journey.py | Deferred secondary usage success/failure crossed with edited/unchanged question | New method checks pending-answer disable, displayed answer, settled submit, enabled button, focus, raw value/dirty state and independent usage result | Focused two-test run passed; full selected 69-test run passed | Complete; test can detect the original blocking await |
| P01-T02 | src/api/src/zava_forward/api/web/chat.js | Clear unchanged submitted text, call void refreshUsage(), then reach existing finally without secondary latency | chat.js:394-398; refreshUsage catches request/render errors at chat.js:322-325 | New strict-rejection regression and retained duplicate/failure regression passed; syntax passed | Complete; existing answer and failure owners preserved |
| P01-T02 | src/api/README.md | Describe answer/control recovery independently of usage latency/failure | Four-line addition in existing audit-only usage paragraph | Scoped diff/documentation review | Accurate and bounded |
| P01-T03 | Dated task evidence | Reconcile completed tasks and actual validation | Complete plan/details, critique disposition, changes and Review-active state agree | Independent checks below | Complete for local implementation/assessment scope |

The test holds usage unresolved while asserting recovery, so it cannot hide the
defect by waiting for usage before checking the form. It uses deterministic
event-loop turns, native deferred promises, a 30-second subprocess timeout and
Node --unhandled-rejections=strict. Both rejection cases must render explicit
usage failure while retaining answer success. Existing tests still exercise
pending duplicate suppression, answer/thread failures and whitespace edits.

The fixture does not load AsyncAction. This is an honest unit-test boundary,
not evidence of browser-level busy-state acceptance. Direct inspection of
shipped h() and AsyncAction.run confirms the shared wrapper follows the handler
promise; the added settled-submit assertion proves the dependency removed by
this fix. No wrapper code changed.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 prerequisite | Current-worktree dependency restoration | Recorded system-Python ModuleNotFoundError; restoration anticipated by accepted plan | Changes records editable source installs and pinned Ruff; validation used existing .venv without installation by reviewer | Existing Complete / Pass critique covers this prerequisite | Compatible, no material divergence |
| P01-T01 through P01-T03 | Pending markers and handoff advanced to completed implementation | Recorded original-code assertion failure, implementation diff and passing checks | Plan, phase details and changes agree; state correctly remains Review active | No changed acceptance basis or new critique required | Reconciled |

No material implementation-time scope, requirement or architecture revision was
found. No divergent decision or paused dependent work requires routing.

## Critique and Material Revision Assessment

* The one original independent critique is preserved as Complete / Pass,
  Critical 0, High 0, Medium 0, Low 0, with no PC-xxx findings.
* Its accepted decisions were implemented: reuse caught refresh and raw-field
  guard; require red before fix; test deferred outcomes and preserve adjacent
  regressions; keep local-only delivery and human boundaries.
* No material revision or undisposed critique finding was identified.
* The reported red result is specific to the disabled-button assertion on the
  original source, not a dependency failure. It is recorded implementation
  evidence, not claimed as independently re-executed by this reviewer.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| None | No implementation-discovered follow-up recorded | None | No distinct follow-up route required |

Research and critique explicitly acknowledge that overlapping advisory usage
reads can finish out of order. This bounded audit-text uncertainty is outside
the requested lifecycle fix; it is not misrepresented as resolved, an active
plan task, a compliance control or an actionable finding of this Review.

## Fresh Changed-Web Review

* Activated web-design-guidelines and freshly fetched the complete current
  https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
  on 2026-10-29 before substantive comparison.
* Read shipped chat.js and assessed the changed lifecycle against all fetched
  rule groups: accessibility, focus, forms, animation, typography, content
  handling, images, performance, navigation/state, touch/interaction,
  safe-area/layout, theming, locale, hydration, interactive states, copy and
  anti-patterns. Groups without an affected surface are not new acceptance
  claims. Unchanged unrelated design/copy was not expanded into findings.
* Existing labelled native controls, polite usage live text, answer log,
  explicit failure route, dirty-text protection and finally-owned focus remain
  intact. No visual, motion, semantic or locale change was introduced.

### src/api/src/zava_forward/api/web/chat.js

src/api/src/zava_forward/api/web/chat.js:394 - pass: changed scope.

This source review is not browser, assistive-technology, staff usability or
whole-application WCAG conformance evidence.

## Findings

None. Severity counts: Critical 0; High 0; Medium 0; Low 0.
No actionable RV-xxx finding was identified within the assessed task boundary.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | Parent receives this one Review result | No implementation defect, decision gap or material evidence gap found |

## Residual Work

* No residual implementation work within P01.
* Parent-owned local commit and workflow handoff remain delivery actions,
  not defects or acceptance evidence already completed by this Review.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active implementation markers: none.
* No source fix, repeat Review, new critique or delegated investigation is
  requested.

## Validation Evidence

Commands below were independently run by this reviewer unless marked recorded.
Python unittest commands ran from src/api; other commands ran from repository
root.

| Command or assessment | Scope | Status | Summary |
| --- | --- | --- | --- |
| PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_case_journey.CaseJourney.test_regulatory_answer_releases_form_before_usage_refresh_settles test_case_journey.CaseJourney.test_both_chat_submissions_clear_only_successful_unchanged_raw_questions -q | New deferred regression and retained adjacent behavior | Passed | 2 tests, 0.126s, OK |
| PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_case_journey test_chat_panel test_regulatory_chat_api test_regulatory_ux_check -q | All four selected modules | Passed | 69 tests, 26.557s, OK; synthetic missing-law-store/provider fallback warnings, no failures or skips |
| node --check src/api/src/zava_forward/api/web/chat.js | Changed shipped JavaScript | Passed | Exit 0 |
| .venv/bin/ruff check src/api/tests/test_case_journey.py | Touched Python | Passed | All checks passed |
| .venv/bin/ruff format --check src/api/tests/test_case_journey.py | Touched Python | Passed | 1 file already formatted |
| git diff --check | Tracked working-tree diff | Passed | Exit 0 |
| Original-code focused regression, recorded in changes | P01-T01 red | Failed as expected, recorded | Disabled-button assertion, 1 test, 0.039s; not rerun by reviewer |
| Fresh Web Interface Guidelines source review | Changed chat.js scope | Passed | Complete source fetched and rule groups assessed; no changed-scope finding |
| Browser, screen reader, voice control, full project suite, live/hosted/publication/human approval | Outside local task acceptance | Skipped | Not requested or established; no push or publication authorized |

## Outcome

* Outcome: Conformant.
* Rationale: the narrow fix releases cleanup, control/focus recovery and handler
  settlement from advisory usage latency while retaining existing independent
  failure handling. The four-scenario regression, retained tests, documentation
  and reconciled P01 evidence support the specified local outcome.
* This outcome does not establish operational, regulatory, browser or
  publication acceptance, nor claim that the parent-owned commit already exists.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement handoff |
| Decision gap or invalid assumption | None | No rpi-plan handoff |
| Material evidence gap | None | No rpi-research handoff |
| Non-blocking residual work | None | No new follow-up item |

* Execution status: Complete.
* Outcome: Conformant.
* Validation coverage: independent 69 selected tests, focused two-test run,
  Node syntax, Ruff lint/format, diff check and fresh changed-web source review.
* Findings and blockers: none.
* Return this canonical result to the active parent; no closure fixes or
  additional Review were performed.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-29/regulatory-usage-refresh-plan.md | Full assessed P01 plan |
| .copilot-tracking/details/2026-10-29/regulatory-usage-refresh-phase-details.md | Reconciled task details |
| .copilot-tracking/reviews/plans/2026-10-29/regulatory-usage-refresh-plan-critique.md | Preserved original independent Pass |
| .copilot-tracking/changes/2026-10-29/regulatory-usage-refresh-changes.md | Implementation and original red/green evidence |
| .copilot-tracking/research/2026-10-29/regulatory-usage-refresh-research.md | Accepted decisions and bounded uncertainty |
| .copilot-tracking/rpi-sessions/2026-10-29/regulatory-usage-refresh-state.json | Read-only parent workflow state at review |
| .copilot-tracking/reviews/logs/2026-10-29/regulatory-usage-refresh-review.md | This single independent Review |

## Next Steps

No user action or finding-remediation command is required. Parent owns recording
this Complete / Conformant result and the authorized local-only commit/handoff.
Do not push or treat these targeted checks as publication or human approval.
This reviewer stops here.
