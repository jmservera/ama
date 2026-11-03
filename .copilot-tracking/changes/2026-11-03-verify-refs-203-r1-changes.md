---
title: Issue 203 round 1 changes
ms.date: 2026-11-03
---

* Added src/core/tests/test_live_doc_links.py.
* No knowledge-base file changed, so no index or log.md entry.

## Validation

Run: `python3 -m unittest tests.test_live_doc_links` in src/core (2 tests OK), `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-203` on the new file (all clean).

Not run: gate, full suites, benchmarks, rubric, Azure or deployment checks.
