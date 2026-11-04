---
title: Issue 951 changes
ms.date: 2026-11-04
---

* `src/core/src/zava_forward/core/challenges.py`, `src/core/tests/test_challenges.py`, `src/core/README.md`, `docs/reference/log.md`.
* Breaking note: callers of `hazard_referrals_overdue` must now pass `max_days`; the only caller in the repository is the test.
* Validation run: `test_challenges` (OK), ruff check and format, mypy strict with `--cache-dir=/tmp/mypy-949` on both Python files.
* Not run: gate, benchmarks, full suites, other projects.
