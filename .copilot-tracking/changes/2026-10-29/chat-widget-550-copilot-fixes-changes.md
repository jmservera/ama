---
title: Chat widget 550 Copilot findings changes
description: Per-finding implementation and local validation evidence
ms.date: 2026-10-29
---

Task 550-copilot-fixes; parent 550-rebase. Full plan in scope.
Research executed / Ready; one independent critique Complete / Pass.
P01/P02 complete. No blockers, no material divergence. P03 Review complete.

## Intake

Initial worktree clean; branch feat/chat-widget-550. First shell command:
git status --short && git branch --show-current && git pull --rebase.
Exit 0, Already up to date. PR 556 OPEN, head feat/chat-widget-550, base main.
Initial HEAD 1d7710b6. Historical RPI artifacts unchanged.
No push, az invocation or rubric edit permitted.

## P01 Implementation

Four corrections implemented: CSS tier 1100, explicit soft/brand Close hover,
pre-append bottom/focus guard, and !widget-only employee opener/decorator.
Two Node regression methods and four browser helpers added to existing files.
README updated. Tests removed: none. New test files: none.

Local implementation judgment: same-context route rendering calls show(),
which intentionally focuses the page and hides the nonmodal popup. Browser
refresh assertions preserve that focus-dismiss behavior; they require retained
widget identity/draft/icon/toggle and consistent aria-expanded, then prove
both launcher reopen and close after refresh. No app-wide focus change.

## P02 Validation

External evidence root:
/home/azureuser/.copilot/session-state/ad8b0385-46d2-4a6b-b6f4-8f9df1363f23/files/widget-fixes.

Initial static.log: PASS, API Ruff, 59 formatted files, isolated browser
Ruff/format, configured mypy 112 files, three JS syntax checks.
chat-units.log: PASS, 139 tests, no skips, including enabled chat-panel
browser unit and four widget focus methods. Expected law-store fixture errors
are recorded, not suppressed or treated as failures.
negative-units.log: both new regression methods correctly fail against
original HEAD JS copied into a temporary directory, removed after execution.

Initial browser attempts are preserved, not represented as full passes:

* attempt1 reached Close hover PASS (6.54:1), then Sources.last dynamically
  selected the newly appended disclosure instead of the original focused one.
  Corrected assertion to retain original element identity.
* attempt2 required waiting for delayed loading feedback before measuring
  bottom state; otherwise the pending timer could shrink the log after the
  test positioned it. Explicitly await visible loading before positioning.
* attempt3 passed employee scroll/layout/focus/axe and real map hit tests;
  coordinator default cutoff inherited the harness's synthetic 2030 clock.
  Use the fixture-compatible explicit past cutoff 2026-01-01.
* attempt4 passed those same boundaries, then exposed intended show() focus
  dismissal. Corrected refresh assertion as described in P01, retaining all
  identity/ARIA/reopen/close requirements. No product workaround added.

browser-attempt5.log and browser-attempt5/results.json: PASS, Chromium
156.0.8078.4, both actual synthetic loopback applications. All existing
loading/consent/denial/stale-operation/focus/axe/reflow assertions retained.
static-final.log: PASS, all requested checks after the final harness edits.
negative-css-browser.log: original CSS fails hover at 1.45:1 and actual map
stacking hit tests. Both regressions catch the original bugs.

### Per-finding regression matrix

| Finding | Implementation | Executed regression evidence |
| --- | --- | --- |
| 1: map obscures chat | Both shared selectors use 1100, strictly between map 1000/account 1200 | employee_stacking: eight real overlap hit tests, popup/launcher above map/control/card, below account; employee-stacking.json all true. Original CSS rejected. |
| 2: Close hover contrast | Scoped hover soft background and brand text | close_hover computed employee 6.54:1, resident 7.52:1, each >=4.5:1. Original employee CSS 1.45:1 rejected. |
| 3: reply jumps history | Capture pre-append bottom within 1px and exclude active focus anywhere in log | reply_scroll both sites: older reader, older Sources, Sources at bottom, log focus at bottom preserve position within 1px and focused element/hit visibility; unfocused bottom reader follows within 2px. Node test adds subpixel tolerance and original JS fails. |
| 4: install replaces toggle | Assign opener and decorate only inside !widget guard | employee_refresh actual coordinator form/query updates from open and closed widget states: same DOM/icon/toggle, draft and consistent ARIA; launcher opens then closes. Node repeated-install guard; original JS fails. |

### Command record

All commands below ran from src/api with the same environment:

```bash
export PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
/tmp/mv/bin/ruff check .
/tmp/mv/bin/ruff format --check .
/tmp/mv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 checks/chat_widget_browser_check.py
/tmp/mv/bin/ruff format --isolated --line-length 100 --check checks/chat_widget_browser_check.py
/tmp/mv/bin/mypy
node --check src/zava_forward/api/web/chat-widget.js
node --check src/zava_forward/api/web/chat.js
node --check src/zava_forward/api/resident_demo/web/assistant.js
ZF_BROWSER_TESTS=1 /tmp/mv/bin/python -m unittest test_chat_widget_focus test_chat_panel test_chat_isolation test_chat_fixture_roles test_resident_chat_api test_resident_chat_agenda test_resident_assistant_api test_case_journey -q
# E is the external evidence root above; axe is hash-verified by the checker.
/tmp/mv/bin/python -u -m checks.chat_widget_browser_check \
  --axe "$E/axe-4.10.3.min.js" --out "$E/browser-attempt5"
```

Every listed final command exited 0. Ruff: 59 formatted project files plus
the separately checked harness; mypy: 112 source files. Units: 139 in 61.769s,
no skips. Axe bytes retrieved from cdnjs 4.10.3 with curl; integrity validated
by the existing checker before browser startup. No dependencies installed.
Browser harness verified owned server responsiveness and cleaned up its
applications; external requests blocked except the explicit axe retrieval.
Negative controls: original HEAD JS loaded via a temporary directory, removed
on exit; original HEAD CSS intercepted only inside an isolated browser context.
No tracked source mutation for negative testing.

### Review readiness reconciliation

P01/P02 plan checkboxes and details reflect completion and actual intended
route-focus behavior. No scope/architecture or user-decision divergence.
Two unit methods/four browser helpers/zero new test files and zero removals.
All four fixes have executed semantic assertions and original-code negative
controls. Current web guidelines re-fetched before Review on 2026-10-29.
No required check unavailable. No human assistive-technology, live model,
hosted CI, full API discovery or complete publication gate claimed.
The latter checks remain outside this expressly local-only correction.

## P03 Review and Persistence

Exactly one independent Review by widget-fixes-independent-review: execution
Complete / outcome Conformant. No source defects, material evidence gaps or
unaccepted decisions. Reviewer independently passed four focus-unit methods,
three JS syntax checks and test-budget/diff hygiene, assessing broader logs
without claiming independent re-execution.
Review artifact:
.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-copilot-fixes-review.md.
RV-001 is Low non-blocking residual future publication/acceptance work, not
an implementation correction. No post-Review source edits or repeat Review.
Publication gate, hosted CI and human/live acceptance remain separate.

Pre-commit git diff --check and unchanged rubric diff pass. gh api user
resolved id 8036360/login jmservera, yielding repository-local author/committer
email 8036360+jmservera@users.noreply.github.com. No global git config change.
The containing commit is the local persistence receipt for P03-T02.

```bash
# Repository root; only six scoped files plus seven dated RPI artifacts staged.
git diff --cached --check
GIT_AUTHOR_EMAIL="$(git config --local user.email)" \
GIT_COMMITTER_EMAIL="$(git config --local user.email)" \
git commit -m "fix(chat): resolve popup layering, scrolling and toggle findings (Refs #550)" \
  -m "Add executed unit and two-site browser regressions for all four findings and retain the single RPI critique/review evidence." \
  -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git status --short
git log -1 --format=fuller
git diff --exit-code HEAD^ HEAD -- .github/rubric/scores/latest.json
```

Final task status is complete only with the successful containing commit and
those post-commit verifications. No source changes after independent Review.
No push, az, dependency install, rubric edit or issue-acceptance change.
