---
title: Issue 217 metering wiring changes
date: 2026-11-04
---

* Added `usage_metering`; `summarize` now rejects stored usage that fails the closed metering schema. Stored audit shape is unchanged. No amendments or divergences.
* Validation run: unit tests `-k regulatory` in src/core (48 OK) and rule_engine tests (30 OK) from a temporary venv; ruff check, ruff format check, mypy (--cache-dir=/tmp/mypy-530) on the changed module.
* Not run: gate, benchmarks, full suites. Tier: focused. Temporary build files and cache removed; `git status --ignored` is clean.
