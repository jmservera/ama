<!-- markdownlint-disable-file -->
# Changes: Chat focus review follow-up

Task 550-focus-fixes; parent 550; date 2026-10-29.
Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-focus-fixes-plan.md.
Details: .copilot-tracking/details/2026-10-29/chat-widget-550-focus-fixes-phase-details.md.

## Execution

Full follow-up plan in scope. Research executed/Ready; one final-candidate
critique Complete/Revise, PC-001/002/003/004 directly accepted, PC-005 rejected
as worker-only runtime restriction not applicable to parent. Original adverse
Review remains immutable historical evidence; append closure only after new
independent Review. P01 starting; local checks and Review pending.

## Boundaries

Clean existing feat/chat-widget-550 from 9658b51b. No PR. No az, push, paid
model, private data, dependency additions or rubric edits. Existing /tmp/mv
runtime; external evidence under current session files. No publication or
human accessibility/live-site acceptance claimed.

## Implementation and Harness Corrections (P01)

Shared document focusin dismisses without refocus/cancellation; dispose removes
listener. Setup/reply focusInput removed. Access denial recovers only popup-owned
focus. Shared errors explicitly polite, existing inline alert semantics retained.
Removed short-height override so launcher stays separate at 1280x500.
Browser denial matrix exposed transient launcher hidden=true during disposal
blurs it even if reset immediately shows it. Disposal now removes root/listener
only; employee reset retains authority over final launcher visibility.

Employee legacy setup oracle migrates from asynchronously focused input to
unchanged heading. Two resident outside-focus oracles migrate from manual
closing to immediate hidden state, retaining pending/no-agenda/focus checks.
These are compatible implementation-time amendments, not another critique.

First harness runs failed on browser-chrome Tab wrap (body is not a focused
control) and role queries excluding hidden retained logs/errors. Corrected
oracles wait for actual page control and inspect hidden DOM via role attributes.
These failed harness runs are not passes. Production denial failure above was
fixed before Review; no post-Review correction or re-review.

Existing obsolete-operation harness now waits for destination heading and
loading completion before opening replacement chat: real route rendering
legitimately focuses app and would otherwise dismiss the just-opened replacement.
All twelve original stale-result assertions remain, now passing.

## Final Validation (P02-T01)

External evidence root E:
/home/azureuser/.copilot/session-state/ba136591-973c-4ee0-8900-4f986afd68fb/files.
Pinned axe A:
/home/azureuser/.copilot/session-state/0fb34315-ee29-4b90-a777-4a0e8804c6ce/files/axe-4.10.3.min.js.
Existing axe bytes verified by the browser checker against pinned SHA256;
owned servers prove responsive before testing, then clean up through fixtures.

Exact final commands, from src/api with E/A set as above:

```bash
export PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
/tmp/mv/bin/python -m unittest test_resident_chat_api test_resident_chat_agenda test_resident_assistant_api test_resident_demo_api test_resident_assistant_provider test_resident_aoai test_chat_panel test_chat_isolation test_chat_fixture_roles test_loading_feedback test_workspace_scripts test_accessibility_baseline test_design_system test_content_standard test_chat_widget_focus -q
ZF_BROWSER_TESTS=1 /tmp/mv/bin/python -m unittest test_chat_panel -q
/tmp/mv/bin/ruff check .
/tmp/mv/bin/ruff format --check .
/tmp/mv/bin/mypy
/tmp/mv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 checks/chat_widget_browser_check.py
/tmp/mv/bin/ruff format --isolated --line-length 100 --check checks/chat_widget_browser_check.py
node --check src/zava_forward/api/web/chat-widget.js
node --check src/zava_forward/api/web/chat.js
node --check src/zava_forward/api/resident_demo/web/assistant.js
/tmp/mv/bin/python -u -m checks.chat_widget_browser_check --axe "$A" --out "$E/chat-focus-browser"
/tmp/mv/bin/python -m checks.employee_chat_browser_check --axe "$A" --out "$E/employee-browser"
/tmp/mv/bin/python -m checks.resident_assistant_browser_check --axe "$A" --out "$E/resident-browser"
```

| Check | Result and evidence |
| --- | --- |
| Related unittest modules | PASS, 196 tests, one existing opt-in skip; unittest.log |
| Opt-in test_chat_panel | PASS, 38 tests, no skip; opt-in.log |
| New behavioral Node tests | PASS, 2 tests; shared lifecycle and 48 setup/status/thread/ask success/error/403/404 focus combinations |
| Baseline negative proof | Both new tests FAIL as expected on original 9658b51b JS copies; baseline-negative.log; external focus remains visible-popup and setup steals focus |
| Ruff check and format --check | PASS, 59 formatted files; static.log |
| Configured mypy | PASS, 111 source files; static.log |
| Isolated shared browser lint/format | PASS; static.log |
| node --check | PASS, all three modules above; static.log |
| Expanded shared actual-app Playwright | PASS, both apps; browser.log and chat-focus-browser/results.json |
| Existing employee actual-app Playwright | PASS, real fallback, six skills, nine late successes, actual 401/403/404, disposal, axe; employee.log |
| Existing resident actual-app Playwright | PASS, pending/external focus, consent, manual callback, session, axe; resident.log |
| Git diff --check | PASS |

Baseline copies were obtained read-only with git show 9658b51b for chat-widget.js
and chat.js under E/focus-baseline, never checked out over source. The same
unittest class was loaded with WEB bound to that external copy; the runner
asserted testsRun==2, failures==2, errors==0. This is intentionally red evidence,
not a validation failure on the candidate.

Expanded browser oracles prove exact signed-out resident 320x800 Shift+Tab twice
to #signin-button, popup hidden, in-viewport center hit-test and focus preserved;
both audiences forward/reverse Tab exit, retained draft/history; 1280x500 keyboard
launcher hit-testing/single-click toggle. Both audiences cover six held current
reply success/error combinations each (external textarea, visible launcher,
internal heading), with polite log/error and retained-error/cleared-success draft.
Employee adds 48 controlled current setup/status/thread/ask focus/denial cases.
Original twelve obsolete-operation cases, 199/200ms timing, consent generation,
no agenda side effects, layout/reflow and axe still pass.

Visually inspected resident-external-focus-320.png (clear Sign in focus ring,
no overlay) and employee-320.png (bounded chat, pinned composer, visible launcher).
DOM/hit-testing and axe are not human assistive-technology acceptance.

## Pre-Review Reconciliation

P01/P01-T01/P01-T02 and P02-T01 complete, details and README updated.
P02-T02 remains one fresh independent selected-follow-up Review and local commit.
Critique Revise and all dispositions preserved. No source/validation blocker.
Original unrelated mobile summary-height failure remains historical and outside
scope; broader case journey not rerun and no wholly green full-suite claim.
Human acceptance and publication gates remain unperformed. No push authorized.

## Independent Review and Closeout (P02-T02)

One independent Review executed by focus-followup-review:
.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-focus-fixes-review.md.
Execution Complete / outcome Conformant; no new findings. Reviewer independently
ran the two Node behavioral regressions, confirmed both baseline failures,
checked changed JS syntax and diff hygiene; broader requested suite/browser
results assessed from supplied logs/reports and inspected screenshots.

Original RV-001 and RV-002 are Resolved in the bounded engineering candidate.
Original changes/review now append dated follow-up pointers and resolution
table without altering original adverse judgement or earlier chronology.
Original and child state remove resolved defect blockers; residual human,
baseline-layout and future-publication work remain distinct. All plan markers
are complete. No post-Review source edit, correction or second Review.

Privacy-safe GitHub identity resolved with gh api user (id 8036360, login
jmservera); repository-local noreply email used for author and committer.
The local commit containing this final closeout is its execution receipt and
includes the required Copilot coauthor trailer. No push/PR/issue closure,
Azure action, rubric-score edit, dependency installation or real-data/model use.
Full external exact-head publication gate was not run and is not claimed.
