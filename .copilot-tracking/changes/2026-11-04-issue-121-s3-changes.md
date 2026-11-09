---
title: Issue 121 s3 changes
date: 2026-11-04
---

* `src/core/src/zava_forward/core/data_protection.py`: `MODE_ENV`, `dispatch_hold`.
* `src/core/src/zava_forward/core/ai.py`: `DispatchDenied`; hold checks in `run`, `look_at`, `_request`.
* `src/core/tests/test_data_protection.py`: 6 behavioural tests (18 total).
* `src/core/README.md`, `docs/reference/log.md`: documented.

Validation run: test_data_protection (18 OK); core test_sensor_privacy, test_regulatory* and test_ai* (OK); api test_assistant_release and test_ai_* (OK); ruff check and format; mypy in src/core with --cache-dir=/tmp/mypy-121 (tests included, clean).
Not run: complete gate, benchmarks, full suites, hosted CI, mypy for src/api (untouched).
