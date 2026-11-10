---
title: Issue 153 pending-handoff read-failure guidance details
ms.date: 2026-11-10
task_id: 153-handoff-read-guidance-1110
---

## Phase 1: source (`app.js`)

Constant, ASCII, existing vocabulary from `GENERIC_READ_ERROR`:

`The handoffs waiting for you could not load, so we cannot tell whether any are waiting. Owner: application support. Next action: refresh to try again, then contact application support if it continues.`

Catch behaviour:

* `e.name === "AbortError"`: return (navigation or sign-out already replaced the view; the detached card is not painted).
* `e.status` truthy: unchanged `Could not load handoffs: ${e.message}` (HTTP error, `GENERIC_READ_ERROR` and 401 paths).
* otherwise (transport rejection or any non-HTTP failure): `HANDOFF_READ_ERROR`.

The card stays visible (`hidden = false`), single `p[role=alert]`.

## Phase 2: regression (`test_handoff_read_guidance.py`)

Node VM: slice the source between `function pendingHandoffs` and `let briefingBox`, plus the constant; stub `h`, `api`, `me`. Assert the slice markers exist so a refactor fails loudly rather than skipping.

Opt-in browser (`ZF_BROWSER_TESTS=1`), loopback `Store` from `test_mvp.DATA`, actual `/api/handoffs` projection for success and empty. The rejection is explicitly constructed by a page `fetch` wrapper on `GET /api/handoffs`; it is labelled as such. Assertions: visible alert text, no canary, request count, no POST, card visible. Navigation case: hold the GET, navigate to another view, release; alert must not appear in the new view.

## Phase 3: commands

* `python3 -m unittest tests.test_handoff_read_guidance tests.test_handoff_api tests.test_content_standard tests.test_ui_support tests.test_case_journey -q` from `src/api` with explicit `PYTHONPATH` to this worktree and asserted module origins.
* Browser: `ZF_BROWSER_TESTS=1 flock -n /tmp/ama-rpi-heavy.lock timeout 300 ...`; busy means pause, not queue.
* `node --check app.js`, Ruff check/format and mypy on the new test file, `git diff --check`.

## Phase 4: evidence

Changes stub is persisted and recorded in state before `implement-start`. Raw logs stay in `/tmp/zf-153-handoff-1110/logs/` and are copied to the Root evidence directory.
