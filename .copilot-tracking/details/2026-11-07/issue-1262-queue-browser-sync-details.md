---
title: Issue 1262 queue browser result synchronization phase details
ms.date: 2026-11-07
---

## Phase 1: Probes

* Probe A (unchanged code, scratch outside the checkout): a Chromium page that renders the app's status format and `.item` anchors, flips from `stale`/`ZF-1` to `overdue`/`ZF-4` through an in-page timer after a `select` change, and the old `wait_cases(page, 1)` followed by `ids(page)`. Record observed IDs and status. This is a harness probe, not the app.
* Probe B: the unchanged maintained browser journey, `python -m checks.design_system_browser_check`, run once under `flock -n /tmp/ama-rpi-heavy.lock` with an external `ZF_BROWSER_SCRATCH`, own pip environment, `PYTHONDONTWRITEBYTECODE=1`. Record holder, command, exit code and result honestly, whether or not the failure reproduces.

## Phase 2: Correction

File `src/api/checks/workbench_browser_check.py`:

* Add `wait_queue_result(page, queue, expected, *, timeout_ms=None)`. Predicate (in-page): status contains `Work queue: {queue}. ` and ` {n} case(s). `, the `.item` hrefs decode to a list exactly equal to `expected` in order. On Playwright `TimeoutError` raise `AssertionError` naming queue, expected IDs, observed IDs and observed status, chained from the timeout.
* In the queue loop replace `wait_cases(page, len(expected))` with `wait_queue_result(page, queue, expected)`; use it for the later `overdue` reselection too. Keep every `check(...)`.

File `src/api/tests/test_workbench_live_defaults.py` (existing): add a Chromium test class with a constructed page, skipping only when the Chromium executable is absent (pattern in `test_browser_asset_urls.py`):

* equal-count stale to overdue transition with delayed render: after the helper returns, IDs equal `["ZF-4"]` and the status names overdue.
* equal-count empty transition priority to unowned: after the helper returns the status names unowned and no rows.
* timeout diagnostics: a never-rendered expectation with a short `timeout_ms` raises `AssertionError` whose message holds expected and observed values.

Red proof: run the same tests with `wait_queue_result` replaced by the old `wait_cases(page, len(expected))` behavior, through an external wrapper (no source edit), and record the failure.

Critique amendment (see [critique](../../challenges/2026-11-07/issue-1262-queue-browser-sync-critique.md)): the predicate anchors on `Work queue: {queue}. Order:` and `. {n} case(s). Workflow stage:` with values passed as `arg`; one extra test asserts `app.js` still contains those two format tokens.

## Phase 3: Validation

From `src/api`, own virtualenv outside the checkout with src projects installed per README: `python -m unittest test_workbench_live_defaults -q`; `ruff check` and `ruff format --check` and `mypy` on the touched files with the repository configuration; the maintained browser journey; `python3 tools/rpi-checks.py --changed` only with same nonqueued admission. Record literal exit codes (no pipeline-masked zero) and skips.

## Phase 4

Changes, review, state; commit with the Co-authored-by trailer and a repo-local noreply author.
