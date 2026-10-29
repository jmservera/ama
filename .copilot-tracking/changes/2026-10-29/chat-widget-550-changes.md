<!-- markdownlint-disable-file -->
# RPI Changes: Shared chat widget

## Metadata

Task ID: 550; implementation date: 2026-10-29.
Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-plan.md.
Details: .copilot-tracking/details/2026-10-29/chat-widget-550-phase-details.md.

## Execution Status

Implementation and local validation complete for P01/P02/P03-T01; documentation
complete for P03-T02. One independent Review and local commit remain. Source is
src-only with external tests/checks and directly related documentation.
No Azure/push/rubric edits.

## Execution Summary

Implement shared native widget and conservative resident intent fix using current
APIs and audience-owned consent/session invalidation. One critique executed with
original Revise outcome preserved; all three findings directly resolved in plan.

## Completed Work

### Shared widget and resident routing (P01-T01, P02-T01)

One shared native JS/CSS factory is served by both real applications; thin
audience adapters retain current APIs and authority. Employee header launcher
and resident stacked layout are replaced. Thread survives hide/reopen; input is
separate from scrolling log. Consent withdrawal and context/session disposal
invalidate pending continuations. Sources use native collapsed details; rules/
workflow output is not relabelled as AI-generated. Callback handoff is explicit.

Resident home routing now matches explicit supported record intents rather than
any mention of "home". Seven negative free-text cases include the rat example;
real HTTP tests prove human handoff, no home/address leakage and no model call.
Existing hazard precedence, consent-before-lookup and access checks are unchanged.

### Browser-driven corrections (P03-T01)

Initial real-browser axe scan found li children of a role=log list lost list
semantics; use native article messages in a named log instead. Delayed send
found that disabling a focused submit lost Escape handling: focus moves into
the composer before native disabling. Context reset found a stale launcher
handler: reset now restores the current opener. The combined browser check
passed both actual apps after these corrections. Expanded-source 200% testing
then exposed inflexible intro/composer sizing; allow those sections to shrink,
while retaining separate scrolling and minimum thread space.

Harness development also corrected Playwright callback signatures (second
positional parameter is Request), exact metadata selection after existing rules
turns, strict mypy annotations and measured clock assertions. The real-time
installed clock could advance during assertion transport; explicitly freeze it
before the 199/200ms test and resume before axe, whose asynchronous scan needs
timers. A paused wait_for_timeout was removed. These failed or stopped harness
runs were not source acceptance passes.

## Implementation-Time Plan and Detail Updates

Immediately relevant updates: native article log instead of ol role=log for
valid semantics; employee shared-file recovery is chat-only rather than blocking
the whole workspace. Existing browser selectors/topic-picker expectations are
migrated to Send/textarea, explicit callback handoff and nonmodal focus behavior,
preserving access, session, manual agenda and obsolete-result assertions.
No new user decision or repeated critique needed.
Related-surface reconciliation found the older case-specific generic composer.
It now opens the same popup instead of retaining a third chat implementation.
Proposal/regulatory controls remain separate and unchanged in authority. The
shared employee popup loads /api/chat/status and disables typing until the
server warning arrives. Draft dirty/unload guards move with that composer;
opt-in privacy browser and case-reconstruction checks are migrated, not removed.

## Validation Record

The following exact command setup uses the existing environment. E is external
session evidence, not repository source:

```bash
cd src/api
export PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
E=/home/azureuser/.copilot/session-state/0fb34315-ee29-4b90-a777-4a0e8804c6ce/files
/tmp/mv/bin/python -m unittest test_resident_chat_api test_resident_chat_agenda test_resident_assistant_api test_resident_demo_api test_resident_assistant_provider test_resident_aoai test_chat_panel test_chat_isolation test_chat_fixture_roles test_loading_feedback test_workspace_scripts test_accessibility_baseline test_design_system test_content_standard -q
ZF_BROWSER_TESTS=1 /tmp/mv/bin/python -m unittest test_chat_panel -q
/tmp/mv/bin/ruff check .
/tmp/mv/bin/ruff format --check .
/tmp/mv/bin/mypy
/tmp/mv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 checks/chat_widget_browser_check.py
/tmp/mv/bin/ruff format --isolated --line-length 100 --check checks/chat_widget_browser_check.py
/tmp/mv/bin/python -u -m checks.chat_widget_browser_check --axe "$E/axe-4.10.3.min.js" --out "$E/chat-widget-browser"
/tmp/mv/bin/python -m checks.employee_chat_browser_check --axe "$E/axe-4.10.3.min.js" --out "$E/employee-chat-legacy"
/tmp/mv/bin/python -m checks.resident_assistant_browser_check --axe "$E/axe-4.10.3.min.js" --out "$E/resident-assistant-legacy"
/tmp/mv/bin/python -m checks.case_journey_browser_check --axe "$E/axe-4.10.3.min.js" --out "$E/case-journey"
node --check src/zava_forward/api/web/chat-widget.js
node --check src/zava_forward/api/web/chat.js
node --check src/zava_forward/api/resident_demo/web/assistant.js
```

| Check | Final result and evidence |
| --- | --- |
| Related unittest modules | PASS, 194 tests, one existing opt-in browser skip; unit-final.log |
| Opt-in chat privacy browser/unit module | PASS, 38 tests, no skip; warning failure blocks typing/sending, visible error, retained draft |
| Ruff check/format | PASS, 58 repository-formatted Python files |
| Configured CI mypy | PASS, 110 source files |
| New check isolated lint/format | PASS |
| Node syntax | PASS on all three changed JS modules; app.js also passed earlier and is unchanged |
| Shared real-app browser | PASS, both applications and identical asset bytes; browser-run.log, chat-widget-browser/results.json and screenshots |
| Employee existing browser | PASS, six choices, real workflow fallback, nine controlled late successes and nine endpoint denials; employee-run.log |
| Resident existing browser | PASS after source/target-size corrections, multi-tab/session isolation and manual callback controls, axe; resident-run.log |
| Existing workspace-script browser | PASS earlier, recovery/exhaustion/late lexical loading; workspace-run.log; shell source unchanged |
| Case journey | FAIL at existing 320px summary <=1600px oracle: measured 1705.96875px. All migrated generic/regulatory chat lifecycle/dirty/unload cases passed earlier in the run; case-run.log |
| Baseline comparison for case failure | Same 1705.96875px with HEAD index.html/style.css/chat.js served via Playwright route overrides and current assets, using journey_data/sign_in at ZF-4/history, 320x800. Original files obtained read-only with git show HEAD:src/api/src/zava_forward/api/web/{index.html,style.css,chat.js}. No unrelated fix or changed oracle |

The final shared check additionally proves fast success and fast error cancel
their loading timers, exact 199/200ms delay, 12 obsolete employee success/rejection
combinations, hidden current completion without focus, dependency recovery and
exhaustion, rat refusal, consent-before-request, pending withdrawal/re-consent,
pinned composer, keyboard/IME, errors, reduced motion, axe and 320/390/1280 reflow.
Final employee-320 and resident-1280 screenshots were visually inspected.
Historical 141-test and earlier browser passes are superseded by these final runs.
No boundary assertion was removed. No dependencies installed, Azure calls,
real data or paid inference used.

## Pre-Review Reconciliation

Ready for one read-only independent Review of the locally validated source
boundary. P01/P02/P03-T01 are checked; P03-T02 remains open only for Review and
commit. Details reflect native log/articles, adapter-owned chat-only script
recovery, shared case entry, admission warning and dirty guards. Original
critique Revise and all PC dispositions remain unchanged. Baseline failure is
recorded rather than hidden; no full-suite/publication/operational claim.

## Blockers

No source implementation blocker. The broader baseline failure prevents claiming
a wholly green case-journey run. Human accessibility/live-site acceptance and the
full exact-head publication gate are unavailable/unperformed in this local-only
task and remain future publication blockers.

## Remaining Work

One independent Review, then requested privacy-safe commit without push.

## Follow-Up Items

* Owner human accessibility/live-site acceptance; not proven by axe/browser checks.
* Before future publication, run full external exact-head local gate and obtain
  independent exact-head/human/hosted approvals. It was not run here; no push is
  authorized and no publication/operational readiness is claimed.
* Owner-maintained case-journey baseline summary-height failure, unchanged by
  this work. Investigate separately without weakening its existing assertion.

## Selected Focus Follow-Up (2026-10-29)

Historical implementation and original adverse Review evidence above is
preserved. Owner-selected task 550-focus-fixes resolves original RV-001 and
RV-002 through a separate short research/plan/implementation/Review loop.
Outside-focus dismissal preserves work; async setup/replies no longer focus
input, all chat updates explicitly polite, short-window launcher stays visible,
and access-loss cleanup preserves deliberately external/surviving launcher focus.

Regression module: src/api/tests/test_chat_widget_focus.py (2 tests with
48 controlled employee combinations), both expected to fail on original source.
Expanded shared Playwright check proves exact 320px Sign in focus visibility,
both short-window launchers, bidirectional external traversal, current replies
and 48 current employee setup/send/denial combinations. Existing employee and
resident checks migrated only obsolete focus oracles; all prior safety
assertions retained. Final requested local validation passes: 196 tests/one
opt-in skip, separate 38 opt-in, Ruff check/format, mypy111, Node syntax, shared
and both existing audience browser checks.

Full follow-up evidence and commands:
.copilot-tracking/changes/2026-10-29/chat-widget-550-focus-fixes-changes.md.
Independent Review:
.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-focus-fixes-review.md,
Complete / Conformant, no new defects. Original RV-001/RV-002 are resolved;
baseline-layout, human/live acceptance and publication follow-ups remain.
Owner-authorized local commit only, no push/Azure/rubric-score edits.
