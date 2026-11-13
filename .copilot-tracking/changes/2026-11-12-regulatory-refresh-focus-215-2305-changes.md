---
title: Changes - restore keyboard focus after Refresh alerts (#215-R1)
description: Implementation record, failing-first evidence and validation for finding 215-R1
ms.date: 2026-11-12
ms.topic: reference
---

## Changes

* `src/api/src/zava_forward/api/web/chat.js`: `load()` in `regulatoryAlertsPanel` now records whether the Refresh button held focus, listens for focus or pointer presses elsewhere during the load, and in one `finally` re-enables the button and refocuses it only when it held focus, nothing else claimed focus and focus is on `body`. The previous body moved to `showAlerts()` unchanged except removal of its own enable/disable lines; awaiting it keeps the button disabled across the synchronous law-store branch so the click wrapper does not disable it again.
* `src/api/checks/regulatory_ux_check.py`: `check_refresh_focus` (keyboard Enter: API error, law-store-unavailable, held-response with focus moved to the toggle and with a pointer press on text, then success) plus an initial-load no-focus assertion in `open_home`. No new scan; still 21 states.
* `src/api/README.md`: one dated description paragraph that keeps "not WCAG conformance or staff comprehension evidence".

## Failing-first and validation (owned pip venv `/tmp/ama-215-own-venv-2305`, editable core/agents/api from this worktree, only test-helper paths, under `/tmp/ama-rpi-heavy.lock`)

* Canonical baseline before edits: 85 tests OK (1 skipped). The readiness 85-test and browser result used source-package `PYTHONPATH` and shared installs pointing at `/home/azureuser/source/ama/src`; it is disclosed and not reused as validation.
* Red: new harness on unchanged `chat.js` exits 1, `AssertionError: Locator expected to be focused` (actual `inactive`); logs `215-r1-red-2305.log`. A first red attempt with `flock -n` exited 1 without running because the lock was held; it was rerun waiting for the lock.
* A first green attempt hit a Playwright API misuse in the new test (`page.route` with a bound builtin); fixed with a lambda before the final run.
* Green: harness with pinned axe 4.10.3 (sha256 `880970c0...a68bb`) PASS, 21 browser states, zero violations; `215-r1-green-2305.log`.
* Five regulatory unit modules 85 OK (1 skipped); other chat.js-referencing modules (`test_case_journey`, `test_chat_widget_focus`, `test_content_standard`, `test_employee_live_responses`, `test_workspace_scripts`) 78 OK; `node --check chat.js`; ruff check and format on the harness; mypy 236 files clean.

## Web guidelines review (fetched in full 2026-11-12)

`chat.js` changed lines: no `autoFocus`, native `disabled` and `<button>` kept, existing `role=status` update kept, visible `:focus-visible` outline unchanged, no visual or Fluent 2 change. Pre-existing and not acted on: `chat.js` status "Loading role-scoped alerts." lacks an ellipsis (cosmetic). Harness and README: pass.

## Not done

No complete gate, hosted CI, push, PR, issue tick or screen-reader/staff work. No AC3 conformance and no AC5 claim; #215 stays open.
