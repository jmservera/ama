---
title: Employee chat skills 530 changes
description: Implementation evidence and validation boundaries
ms.date: 2026-10-29
---

## Scope and status

Full P01-P03 implementation under explicit full-loop direction. Research Ready;
one critique Complete / Revise, dispositions applied in plan, no repeated critique.
Source implementation complete; validation partial; ready for independent
Review. Source baseline d70ee60ab3d7346a9991cf64382d9985f4d09f2e.

## P01-P02 implementation

P01: ChatPanel accepts explicit general or five registry skill IDs, retains
legacy omission behavior, narrows skill categories over existing projected
case facts, adds trusted workflow sources and visibility limits, and records
question sequence/skill/outcome without raw question text in the ledger.
Existing agents ChatModel adapter reused unchanged.
P02: Header launcher and native modal across employee routes; existing case
and regulatory panels preserved. AsyncAction busy feedback, abort/disposal on
route/login/denial, bounded latest exchange, labelled cited/unverified answers.

## Validation and blockers

Focused API/core chat tests: 37 passed. Initial test failure used the wrong
audit fixture location; corrected to actual audit_entries. Initial core mypy
found mixed registry value inference; public purpose now explicitly string.
API/core Ruff and formatting pass; core 157 files and API 107 files pass mypy.
Initial browser/axe found invalid list role and nested scroll region; fixed
with native list inside live-region wrapper and one outer dialog scroll.
Next browser run reached focus assertions; replaced unsupported exact native
wrap assumption with actual in-dialog traversal assertions.

Nonblocking heavy lock initially admitted targeted browser runs. A subsequent
`flock -n /tmp/ama-rpi-heavy.lock ...employee_chat_browser_check...` exited 1
with no test output: busy admission. No queued/repeated full-suite admission,
foreign container use or interruption. Full suites and actual disposable SQL
are blocked by shared lock; continue independent targeted checks only.
Actual lock owner observed with lslocks: PID 771340, python3, canonical path.
Do not inspect/reuse its evidence or container.

Final permitted results, all explicit worktree source/test PYTHONPATH:

* From src/api: /tmp/mv/bin/ruff check .; ruff format --check .; mypy:
  all pass, 107 source files typed.
* From src/core: /tmp/mv/bin/ruff check .; ruff format --check .; mypy:
  all pass, 157 source files typed.
* API unittest selectors test_chat_panel test_chat_isolation
  test_chat_fixture_roles test_role_endpoint_inventory test_workspace_scripts:
  82 tests pass. Initial workspace test failure was an obsolete case-only
  chat.js readiness expectation; corrected for global staff chat.
* Core unittest selectors test_chat_panel test_chatthreads test_chat_privacy:
  54 tests pass, including JSON/SQLite storage, not real SQL Server.
* Agents unittest selectors test_chat_model test_chat_provenance test_chat_fixture:
  16 tests pass; existing adapter unchanged.
* New employee_chat_browser_check with pinned axe-core 4.10.3 SHA-256
  880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb:
  pass on constructed loopback server. Actual unavailable-model fallback;
  six intercepted selection/rendering states; global route reachability;
  case/no-case disclosure; keyboard containment/Escape/return focus;
  320/390/1280px reflow; reduced motion; route/session/403/404 disposal;
  aborted delayed response does not populate replacement context.
  Two actual dialog-scoped axe states each have zero violations and 20 passes.
  No live model or site inference.
* JavaScript syntax and git diff --check pass. Public scenario-manifest
  SHA-256 pins all match; none of its pinned sources was edited.

Browser output and logs retained externally under session
8df83efd-d268-4456-99f8-d2978b1a7a23/files, not committed generated assets.
Earlier failures remain recorded above; no receipt or whole-suite pass implied.
Full publication gate blocked by no-az
direction; do not invoke runner that executes az. No push or live verification.
Screen-reader, voice-control and human approvals unclaimed.

## Amendments and divergences

No router. Critique PC-004's alleged /tmp prohibition rejected as unsupported;
user explicitly names /tmp/mv and canonical shared lock. Explicit worktree
PYTHONPATH used. Initial editable install completed successfully.
Related existing harness updates are current-state amendments, not scope
expansion: global script readiness and opt-in constructed privacy admission.
Fresh Web Interface Guidelines retrieved again before final review; repository
plain ASCII and sentence-case standard takes precedence over generic copy.

## Review handoff

Plan/details/changes reconciled. One independent post-implementation Review
assesses the full working candidate against origin/main baseline above, with
full-suite/SQL, publication, live and human acceptance explicitly unmet.

## PR #541 correction pass opening

Scope P04 only, explicit user-directed finite RPI pass. Research cycle 2
executed/Ready (C7-C9). One independent correction critique Complete/Revise;
CP-PC-001 rejected with parent-authority rationale in the plan. Original
critique and Review remain unchanged historical outcomes. Implement shared
metadata/submit denial disposal and focus, deterministic late-success tests,
and bounded redacted questions with core/HTTP regressions. Validation pending.
No push, az, shared-venv mutation or complete gate invocation.

### P04-T01/T03 implementation and targeted checks

Shared deny helper now removes the dialog, reports workspace guidance and
focuses #app for metadata/submit denials. Existing api() session-expiry path
still owns sign-in and current() prevents obsolete catches stealing focus.
Masked questions are bounded again before writing and prompt reuse.
Core regression covers three expanding masks across legacy/general/five
skills; HTTP regression covers the exact 8,000-character postcode example
across the same modes, stored mask and actual audit sequence. Both pass.
API chat/isolation/fixture/endpoint/workspace selectors: 83 tests pass.

Current-state amendment: the new typed core regression calls migrated untyped
Store/ChatIsolation/privacy boundaries. Initial mypy correctly reported five
no-untyped-call errors; add only test_chat_panel/tests.test_chat_panel to the
existing disallow_untyped_calls override, retaining strict body checking.
Core Ruff/format/mypy now pass (157 files). API Ruff/format/mypy pass (107 files);
an initial new browser undefined launcher reference was corrected.
Initial browser command lacked the documented shared test fixture PYTHONPATH
and failed import; retry will use the documented paths. No dependencies added.
Full core discovery admitted under the shared lock and running; browser awaits
that owned run's completion before nonblocking admission.

### P04-T02/T04 final validation

Browser regression requires the intercepted ask to arrive before navigation;
transport cancellation remains a separate check. One controlled-api helper
resolves successful metadata/thread/ask promises after close, navigation to a
replacement dialog or session expiry. It awaits the real consumer task, checks
promise fulfillment, prevents obsolete thread completion starting an ask, and
compares detached/current transcript, status, draft and active element.
All nine combinations and nine metadata/thread/ask 403/404/401 cases pass.

An initial browser run exposed a harness race: a role locator no longer matches
a closed dialog before its asynchronous close event actually removes it and
aborts the controller. An abort assertion failed once. Diagnostic runs passed
five times, but that did not resolve the race; final code now waits for zero
actual dialog.employee-chat DOM elements before taking the snapshot/resolving.
Final browser run after this correction passes. No failure was converted into
a skip or transport-abort substitute for successful completion.

Commands and results (installed distributions point to this worktree):

* From src/core: /tmp/mv/bin/ruff check .; ruff format --check .; mypy:
  pass, 157 files. No broad type-ignore added; only existing untyped-call
  boundary exemption extended to the new integration test owner.
* From src/api: same commands, pass, 107 typed files. JavaScript node --check
  for chat.js and git diff --check pass.
* From src/core: flock -n /tmp/ama-rpi-heavy.lock /tmp/mv/bin/python -m
  unittest discover -s tests -q: 1,470 tests in 310.671s, OK (190 skipped).
  Existing opt-in integration skips are not real SQL Server evidence.
* From src/api: PYTHONPATH=tests:../core/tests:../agents/tests /tmp/mv/bin/python
  -m unittest test_chat_panel test_chat_isolation test_chat_fixture_roles
  test_role_endpoint_inventory test_workspace_scripts -q: 83 tests, OK.
  Existing synthetic rule-check-unavailable diagnostics are expected, not failures.
* From src/api: same PYTHONPATH, flock -n /tmp/ama-rpi-heavy.lock
  /tmp/mv/bin/python -m checks.employee_chat_browser_check --axe <external
  pinned-file> --out <external browser-final>: pass; owned constructed-data
  loopback server health checked and terminated by its harness. Two axe states
  report zero violations; pinned 4.10.3 SHA-256 verified before execution.

External generated evidence: current session
285059ff-9e53-4387-9191-986e1300eb2f/files/pr541-checks under
/home/azureuser/.copilot/session-state (core-unittest.log, browser-final/
axe-results.json and verified axe input). No historical output deleted.
Whole API discovery, actual SQL Server, live provider/site, human approval and
complete publication receipt are not claimed. Full gate invokes forbidden az,
so it was not run. No push or az occurred.

### Correction Review handoff

P04 source/test/docs implementation and requested validation reconciled.
One independent Review will assess only this later correction diff against
starting HEAD 15252634, not reissue the original whole-feature Review.
Original PC/RV verdicts remain preserved. No additional feature discovery,
second correction Review or source changes are scheduled after that Review.

### Independent correction Review result

Execution Complete; outcome Conformant for P04; no new substantive findings.
The independent reviewer inspected the complete correction boundary, actual
core/axe output and fresh web guidelines, and ran JS syntax/diff checks.
Original Review Not accepted/RV-003 remains unchanged. Resolved correction
mechanisms are removed from current follow-ups without rewriting their
historical findings. Local implementation/evidence commit is the next action;
no source changes or second Review after this assessment.
