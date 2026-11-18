# Issue 223 comparison slice plan (2026-11-14)

* Add `comparison()` to `review_effectiveness.py`; include it in the report and CLI output.
* Add one unit test covering detection rate, gate result and effort delta versus workflow-only.
* Validate: ruff check and format (line length 100) on `src/agents`; `tests.test_review_effectiveness`.
* Critique: one pass; compatible, additive change only, no gate semantics changed.
