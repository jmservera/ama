---
title: Changes for #185
ms.date: 2026-11-05
---

* `src/core/src/zava_forward/core/synthetic/device_provision.py`: new command.
* `src/core/tests/test_device_provision.py`: 7 tests.
* `src/core/README.md`: command section.
* Validation run: `unittest -p "test_device_*.py"` (45 OK), ruff check and format check, mypy strict over src and tests with `--cache-dir=/tmp/mypy-185`.
* Not run: gate, benchmarks, full suites. No knowledge-base file changed, so no log entry.
