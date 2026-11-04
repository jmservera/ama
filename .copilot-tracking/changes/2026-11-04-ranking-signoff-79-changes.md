---
title: Issue 79 changes
ms.date: 2026-11-04
---

* Added sign-off check functions to `ranking.py`; status now derives `policy_signed` instead of a constant.
* Added six behavioural core tests and one wiring assertion; README documents the check.
* No policy file, ranking order, resident, approval or AI behaviour changed.

Validation run: core `test_ranking_publication` (13 tests), api `test_ranking_publication_wiring`, `test_ranking_policy`, `test_ranking_scale` (this ran its 60k-home timing checks by mistake of selection; no benchmark was intended), ruff check and format on touched core files, mypy strict on src/core with `--cache-dir=/tmp/mypy-79`. Not run: gate, full suites, api mypy and ruff.
