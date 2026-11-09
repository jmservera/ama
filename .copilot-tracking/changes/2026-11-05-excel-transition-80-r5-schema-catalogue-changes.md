---
title: Issue 80 round 5 changes
description: Changes and light validation
ms.date: 2026-11-05
---

Changed: server route and whitelist, three test files, API README. No core, web, quality.py or dependency change; no divergence from the plan.

## Light validation (not FULL)

Tools: ruff 0.17.3, mypy 2.4.1, Python 3.12.3; bytecode off; `RUFF_CACHE_DIR` and mypy caches under `/tmp/r5-80-*`. Installed distributions resolve to another checkout, so worktree `src/*/src` and test paths were put on `PYTHONPATH` (no `mvp`); `server.py` and `forms.py` printed paths are under this worktree. Real exit codes captured.

* Test before fix: with `server.py` from HEAD (`git archive` copy in `/tmp/r5-80-base`) the new tests ran 24, failed 5 and errored 1 (rc 1), including the registry test.
* First after-fix run: one test error, a mistake in my test (`store.cases` is a dict); corrected, not hidden.
* After: 50 tests OK (`test_form_staging_api`, `test_list_export_api`, `test_role_endpoint_inventory`, `test_loading_feedback`), rc 0.
* `ruff check` rc 0. First `ruff format --check` rc 1 on my new test code; formatted; recheck rc 0. `mypy` (tests included) rc 0, 186 files.

## Preserved adverse records

Round 3 viewport failure (unverified after #1219), failed gate admission and author-only reviews are unchanged. Not run: FULL gate (the #96 runner owns the lock), browser, SQL server, Docker, hosted CI.
