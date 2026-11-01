---
title: Issue 572 remaining criteria changes
ms.date: 2026-11-01
---

Documentation-only. Added these RPI artifacts. Validation: `python3 -m unittest tools.test_rpi_checks` Ran 55 tests, OK (about 32 s); mypy --strict tools/rpi-checks.py clean. `ruff check` and `ruff format --check` report pre-existing findings on untouched tool files under the unpinned local Ruff 0.17.3; the repository pins a different Ruff for the gate, so these are not treated as regressions. No source, skip allowlist or workflow changed.
