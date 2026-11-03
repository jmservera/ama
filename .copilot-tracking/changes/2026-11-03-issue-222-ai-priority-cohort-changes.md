---
title: Issue 222 AI priority cohort changes
ms.date: 2026-11-03
---

## Changes

* New `src/agents/src/zava_forward/agents/cohort_ai_eval.py` and `tests/test_cohort_ai_eval.py`.
* `src/agents/README.md`: usage and limits.

## Validation

Run: `test_cohort_ai_eval`, `test_ai_eval`, `test_cohort_ranking_eval` (re-run before commit), ruff check and format, mypy strict (cache /tmp/mypy-222) on touched sources.

Not run: gate, benchmarks, full suites, hosted CI. No divergences.
