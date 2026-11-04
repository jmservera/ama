---
title: Issue 223 session pool changes
date: 2026-11-03
---

* Added pool_human_sessions and multi-sheet `--score` (exit 1 if any session fails the gate).
* Added 4 unit tests (31 in file now); README sentence.
* Divergence: none. Gate logic untouched.
* Validation run: ruff check, ruff format, mypy (--cache-dir=/tmp/mypy-223), 31 tests in test_review_effectiveness (installed in a /tmp venv with ZF_REVIEW_GOLDEN set). Not run: gate, benchmarks, full suites, any human session.
