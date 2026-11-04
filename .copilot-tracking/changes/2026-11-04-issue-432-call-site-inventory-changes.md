---
title: "Changes: #432 provider call-site inventory"
ms.date: 2026-11-04
---

* Added `src/api/tests/test_ai_call_site_inventory.py` (3 tests). No other source change; no knowledge-base or log.md change.
* Validation (focused tier): the 3 new tests pass; ruff check and format and mypy (cache /tmp/mypy-432) clean on the file. Tests ran with PYTHONPATH pointing at this worktree's src because the shared pip environment installs another worktree. Not run: tools/rpi-checks.py gate, benchmarks, full suites, live Azure calls.
