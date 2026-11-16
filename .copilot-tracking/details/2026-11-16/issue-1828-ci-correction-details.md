---
title: Issue 1828 CI correction cycle 2 details
description: Phase details for the mypy patch target correction
ms.date: 2026-11-16
ms.topic: reference
---

## Phase 1: patch target

* File `src/api/tests/test_map_viewport_premise.py`, method `ViewportPremiseTests.run_check`.
* Replace `patch.object(check_module.time, "monotonic", monotonic)` with `patch("checks.map_fullscreen_browser_check.time.monotonic", monotonic)`. `check_module` remains used for `check_viewport_change_requests_map`.
* Success: mypy reports no error at line 97; the four premise tests still pass, including the three that reject a stale, old-width or unchanged read.

## Phase 2: verification

* From `src/api` with `/tmp/1828/venv/bin/python -m`: `mypy`, `unittest tests.test_map_viewport_premise tests.test_map_sensors tests.test_role_* tests.test_ui_support tests.test_browser_harness_scratch tests.test_employee_acceptance_check`, `ruff check`, `ruff format --check`.
* Optional mutation: restore the old patch line to confirm mypy fails (already reproduced in `mypy-failing-first.log`).

## Phase 3: browser

* From `src/api`: `flock -n /tmp/ama-rpi-heavy.lock` around `python -m checks.map_fullscreen_browser_check --axe /tmp/1828/axe.js --out <external dir>` after verifying `sha256sum /tmp/1828/axe.js` equals 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb. Expect 14 axe scans, 0 violations, zero unexplained skips. Second run only if the lock is still free.
