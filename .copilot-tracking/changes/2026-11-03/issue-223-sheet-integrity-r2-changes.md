---
title: Issue 223 sheet integrity changes
date: 2026-11-03
---

* src/agents/src/zava_forward/agents/review_effectiveness.py: refuse stale or unversioned sheets and unknown proposal ids.
* src/agents/tests/test_review_effectiveness.py: 2 new tests, helper carries version (29 tests).
* src/agents/README.md: describes the refusal.

Validation (focused): unittest test_review_effectiveness 29 OK; ruff check and format --check; mypy --cache-dir=/tmp/mypy-223 clean. Not run: gate, benchmarks, full suites, any human session.
