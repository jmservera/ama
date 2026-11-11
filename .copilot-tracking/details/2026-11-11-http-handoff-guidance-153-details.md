---
title: Issue 153 pending-handoff HTTP refusal and error guidance details
ms.date: 2026-11-11
task_id: 153-http-handoff-1111
---

## Status: prospective, NOT implemented

## Phase 0: resume gate (before any edit)

1. Coordinator confirms #1444 merged to main.
2. `git fetch origin`, then `git merge origin/main` in this worktree (ordinary merge; no rebase, no force). Resolve only genuine conflicts; if `app.js` conflicts inside `pendingHandoffs`, stop and record a blocker.
3. Re-verify: `pendingHandoffs` and `const HANDOFF_READ_ERROR` still sit before `let briefingBox`; #83's `handoffWaitingView` and constants sit after it; `git status` shows only the expected untracked or committed 2026-11-11 planning artifacts and no unrelated change.
4. Select worktree sources explicitly: from `src/api`, `PYTHONPATH=$PWD/src:$PWD/../core/src:$PWD/../agents/src:$PWD/tests:$PWD/../core/tests:$PWD/../agents/tests`, and assert `zava_forward.api.server.__file__` and `zava_forward.core.store.__file__` resolve under this worktree (host editable installs point at the primary checkout).

## Phase 1: source (`app.js`)

Add beside `HANDOFF_READ_ERROR`, after it and before the function:

`const HANDOFF_DENIED = "Your account cannot see the handoffs waiting for you, so we cannot tell whether any are waiting. Refreshing will not change this. Owner: your Retrofit Programme Manager or Programme Support Officer. Next action: ask them to check your role. Until then, ask the sender or open a case you already know, because the case list may not show every handoff waiting for you.";`

In `pendingHandoffs` (shape, not final code):

* helper `fail = (message) => { box.hidden = false; box.replaceChildren(h("p", { role: "alert" }, message)); }`
* `then`: `if (!Array.isArray(rows)) return fail(HANDOFF_READ_ERROR);` before the existing `!rows.length` test.
* `catch`: abort returns; `e.status === 401` keeps the existing `Could not load handoffs: ${e.message}`; `e.status === 403` uses `HANDOFF_DENIED`; otherwise `HANDOFF_READ_ERROR`.
* Keep the success markup, both download anchors and their text byte-identical. Do not edit lines outside this function and the constant.

Copy guard: ASCII only; no `gate`, `hold`, `provenance`, `trace` (word boundary, case-insensitive); no "no handoffs", "nothing waiting", "all clear".

## Phase 2: regression (`test_handoff_read_guidance.py`, existing file only)

Update (these pin the old behaviour and must change, recorded as intended contract changes):

* `test_abort_paints_nothing_and_http_paths_keep_their_text`: split. The `http` 500 case now expects fixed `HANDOFF_READ_ERROR` text and not `Handoff service said no`. The `ended` (401) case keeps `Could not load handoffs: Your session has ended. Sign in again.`
* `test_source_keeps_the_alert_element...`: `role: "alert"` count stays 1 (single paint helper); `HANDOFF_READ_ERROR` count updated to the actual occurrences; assert `HANDOFF_DENIED` defined once and before the function marker; assert no `e.message` interpolation other than the 401 branch; no `setTimeout`.

Add Node VM scenarios (real function source, stubbed `h`, `api`; one `api` call each, no mutation):

* 403 `Error("Your role does not include this.")`: alert, visible, refusal copy, owner roles named, "Refreshing will not change this", no "try again" advice, server text absent, no "Could not load handoffs".
* 500 with server text, 404, 429, and a `generic` read error: fixed load-failure copy, raw text absent, card visible.
* Malformed 200: `{}` and `0` (red before the change: currently hidden as empty); `"x"` and `null` are preservation checks only (they already reach the fixed error through the catch). Red-before evidence is required for 403, HTTP server-text, `{}` and `0` cases.
* Lexical guard over both constants (ASCII, banned words, no empty-queue claim).
* Existing transport, abort, 401, rows, empty cases stay and must pass unchanged.

Opt-in served browser (`ZF_BROWSER_TESTS=1`, existing `Served` helper; the existing `open()` navigates to the card before returning, so these cases need a variant that installs `page.route` BEFORE the first `/app#/` navigation and counts requests from that point; synthetic `test_mvp.DATA`, loopback only, non-served requests aborted), constructed states labelled as constructed:

* 403 via `page.route("**/api/handoffs", fulfill 403 JSON {"error": "CANARY refusal text"})`: visible `role=alert` with refusal copy, canary absent, `Pat Test` absent, exactly one GET to `/api/handoffs`, no POST except login, no further GET after a short wait (no automatic retry).
* 500 JSON `{"error": "CANARY server text"}`: fixed load-failure copy, canary absent, one GET.
* Malformed 200 (`text/plain` body "oops"): load-failure copy, card visible.
* Manual refresh: with the route failing, then `page.unroute` and `page.reload()`: rows appear from the actual backend projection; only the reload issued the second GET.
* Keep existing success/empty, session-ended and navigation-during-pending cases.

Do not add tests for constants, hierarchy or trivial accessors; do not duplicate cases into other files.

## Phase 3: focused validation (to run only at implementation; none run in this planning phase)

From `src/api` with the Phase 0 `PYTHONPATH`:

* `python3 -m unittest tests.test_handoff_read_guidance tests.test_unaccepted_handoff_download_ui tests.test_handoff_api tests.test_unaccepted_handoff_csv_api tests.test_case_journey tests.test_content_standard tests.test_ui_support tests.test_role_endpoint_inventory tests.test_role_screens tests.test_workbench -q`
* After main adoption also `tests.test_handoff_waiting_view` (#83) for screen, navigation, personal-card and CSV regression.
* Browser: the same selection with `ZF_BROWSER_TESTS=1` and own loopback servers. `test_unaccepted_handoff_download_ui` takes `/tmp/ama-rpi-heavy.lock` itself, so run it WITHOUT an outer `flock` (an outer lock would make its browser class skip). Run the new browser cases, which do not self-lock, under `flock -n /tmp/ama-rpi-heavy.lock`; busy means pause and record, not queue or retry. Confirm no skips.
* Red-before/green-after: run the new cases against base `app.js` (or with the edit stashed in a scratch copy, not in the tracked tree) to prove they fail without the change.
* `node --check src/zava_forward/api/web/app.js` (from `src/api`).
* Ruff check and format check and mypy for the changed Python test using the configured `src/api/pyproject.toml` (ruff 0.17.1, mypy 2.4.0 already installed; no installs).
* `git diff --check`; Markdown link review of changed docs.
* Web Interface Guidelines: re-fetch current rules, review the changed `app.js` hunk and report `file:line`; record that the typography `…` rule is superseded by the repository ASCII standard.
* Not run: full or `--changed` gate, SQL services, Docker, provider/model, real data, cloud, assistive-technology or human acceptance.

## Phase 4: evidence

Changes record (planned, deviations and divergences included), original author Review once with outcome and routing, state file, logs under `/tmp/zf-153-http-handoff-1111/` copied into `.copilot-tracking/`. Independent exact-head review and hosted CI are required before merge and are not claimed here.
