---
title: Issue 217 metering record changes
date: 2026-11-03
---

* Added `metering_record` and tests. No amendments or divergences.
* Validation run: ruff check, ruff format, mypy strict (--cache-dir=/tmp/mypy-217) on regulatory_privacy.py, and `test_regulatory*.py` in src/core (46 tests, OK).
* Not run: gate, benchmarks, full suites. Tier: focused; no security, infra, SQL or deployment change.
