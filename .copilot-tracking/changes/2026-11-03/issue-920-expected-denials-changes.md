---
title: Issue 920 changes
description: Files changed for the expected-denial slice
ms.date: 2026-11-03
---

## Changes

* `src/api/src/zava_forward/api/server.py`: `/api/me` adds `services`.
* `src/api/src/zava_forward/api/web/app.js`, `chat.js`: skip predictable denials, plain wording.
* `src/api/tests/test_expected_denials.py`: new unit test.
* `src/api/checks/expected_denials_browser_check.py`: new Chromium check, asserts no console errors.

## Validation run

* unittest (api): test_expected_denials, test_employee_live_responses, test_auth, test_error_logging, test_rule_alerts, test_regulatory_chat_api: 71 OK.
* Chromium check: all PASS, console errors empty.
* ruff check and format, mypy `--cache-dir=/tmp/mypy-920` on new files: clean.
* `node --check` on both JS files: OK.

## Not run

* Gate (`rpi-checks.py`), full suites, benchmarks, axe/keyboard evidence, live deployment.
