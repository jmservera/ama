---
title: Issue 1262 queue browser result synchronization research
ms.date: 2026-11-07
---

* Task: `issue-1262-queue-browser-sync`; branch `test/queue-browser-result-sync-1262`; base main `f0afa8d76d7be13ec4278321e09e16e23eaeb37c`. Research disposition: `executed`, static reading only. No probe or edit had been run when this was written.
* Tier: FOCUSED, test-only. Selected scope: `src/api/checks/workbench_browser_check.py` and existing tests under `src/api/tests/`.

## Evidence read

* Checker blob `7b32d7ce4aa2a1608f8fbfd67be565043f915ab7` (matches the value the coordinator verified for main and the C18 checker).
* `wait_cases(page, count)` (lines 69-74) waits only for `.item` count equal to `count` and `#workspace-status` containing `"{count} case"`. It carries no queue identity or ID list. It has 28 call sites in `workbench_browser_check.py` and one in `employee_briefing_browser_check.py`.
* The queue loop (lines 487-501) selects `new` (`["ZF-1"]`), `stale` (`["ZF-1"]`), `overdue` (`["ZF-4"]`), `priority` (`[]`) and `unowned` (`[]`). It enters `page.expect_response(...)` around `select_option`, then `wait_cases(page, len(expected))`, then asserts `ids(page) == expected`.
* `expect_response` completes when the response arrives, not when `app.js` has parsed the JSON and called `render()` (`load()` in `src/api/src/zava_forward/api/web/app.js` lines 803-822: `await api(...)`, then `rows = d.items`, `render()`).
* Rendered status text (app.js line 784) contains `Work queue: {queue}.` and `{total} case(s)`. Rows are `.item` links with `href` ending in the case ID. A stale response is discarded in `load()` by `seq` and `signal`, so the rendered queue label is a reliable identity of the completed render.
* Transition `stale` to `overdue` is equal-count (1 to 1) with different IDs. `new` to `stale` is equal-count and equal-ID, so it cannot expose the race. `overdue` to `priority` and `unowned` are 1 to 0 and 0 to 0; the last is an equal-count empty transition with no row change at all.
* Existing helper patterns: `check(name, passed)` raises `AssertionError(name)`; `ids(page)` reads `.item` hrefs; browser unit tests (`tests/test_browser_asset_urls.py`) launch Chromium via `sync_playwright` and call `skipTest("Chromium is installed by the later browser-check step")` only when the executable is absent. The checker module imports Playwright at top level, so a test importing it already needs Playwright installed.
* Actual failure (from the issue, not re-observed): `AssertionError: overdue queue exact expected IDs` at line 501 on 2026-11-07, preceding checks green. The original logs are on `/mnt/ama-gates/...`; not read or modified here.

## Hypothesis (to be tested, not asserted)

The wait can be satisfied by the previous render (stale row `ZF-1`, count 1) before the overdue render replaces it, so `ids(page)` is read too early. This is a test-harness synchronization defect candidate. The actual observed IDs in the failed R31 run are not available in the issue and must not be invented. Whether the maintained browser run reproduces it on this VM is unknown and must be recorded as observed.

## Boundaries

* No change to API, UI, ranking, policy, auth, SQL, infra or expected IDs. Not a product defect claim; no web file is changed, so web-design-guidelines review has no changed web scope (disclosed).
* No private data, Azure, model calls or support/cohort material.

## Planning Readiness

Ready.
