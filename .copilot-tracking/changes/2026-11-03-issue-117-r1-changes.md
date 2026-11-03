---
title: Issue 117 round 1 changes
ms.date: 2026-11-03
---

## Changed

* src/core/src/zava_forward/core/doc_controls.py
* src/api/tests/test_document_controls.py
* src/api/README.md

## Validation

Run: `python3 -m unittest discover -s tests -p test_document_controls.py` from src/api (15 OK); core `tests.test_document_rescan` (38 OK, 19 skipped: MSSQL variants); ruff on changed files (pass); mypy with --cache-dir=/tmp/mypy-117 (2 pre-existing errors: the `tags` monkeypatch at doc_controls.py:123 and signoffs.py:42, neither touched).

Not run: gate, benchmarks, full suites, MSSQL, hosted CI, any real Defender account.

Tier: focused; security-adjacent, so the complete gate is for the coordinator.
