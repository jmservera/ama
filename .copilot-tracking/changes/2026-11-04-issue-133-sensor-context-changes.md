---
title: Changes, issue 133 sensor context
ms.date: 2026-11-04
---
* Changed: aftercare.py, test_aftercare.py, src/core/README.md, docs/reference/log.md.
* Validation run: test_aftercare and test_retrofit_scenarios_production_consumers (21 OK, PYTHONPATH to this worktree src), ruff check and format check, mypy with --cache-dir=/tmp/mypy-133 as the src-ci workflow runs it (253 files incl. tests).
* Not run: gate, benchmarks, full suites, browser checks.
