---
title: Issue 222 golden-set cohort reporting changes
ms.date: 2026-11-03
---

## Changes

* `ai_eval.py`: `cohort_report()`; `cohorts` in the report and a text line.
* `test_ai_eval.py`: one new test.
* `README.md` (agents): note.

## Validation

Run: test_ai_eval, test_cohort_ranking_eval, test_cohort_manifest_draft (45 OK, PYTHONPATH to src), ruff check and format, mypy (cache /tmp/mypy-222).
Not run: gate, benchmarks, full suites, hosted CI. Pip install not used; PYTHONPATH avoided generated files.
