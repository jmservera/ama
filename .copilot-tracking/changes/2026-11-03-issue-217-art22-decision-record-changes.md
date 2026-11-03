---
title: Issue 217 changes
date: 2026-11-03
---

* Changed: regulatory_privacy.py, test_regulatory_privacy.py, src/core/README.md.
* Validation (focused tier): `test_regulatory_privacy.py` 14 tests OK; ruff check and format clean; mypy (cache /tmp/mypy-217) clean on the module.
* Not run: gate, benchmarks, full suites. No security, infrastructure, SQL or deployment change.
