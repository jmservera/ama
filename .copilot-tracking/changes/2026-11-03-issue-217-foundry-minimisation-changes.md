---
title: Issue 217 changes
date: 2026-11-03
---

* Added `minimise_query` and field allowlists to `src/core/src/zava_forward/core/regulatory_privacy.py`.
* Added three tests to `src/core/tests/test_regulatory_privacy.py`.
* Documented in `src/core/README.md` (#217 section).
* Validation run: 40 regulatory tests (installed in a /tmp venv), ruff check, ruff format --check, mypy (--cache-dir=/tmp/mypy-217). Not run: gate, benchmarks, full suites, hosted CI.
* No divergences from the plan.
