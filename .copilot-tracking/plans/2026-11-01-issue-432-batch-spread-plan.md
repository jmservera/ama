# Plan: #432 batch spread slice

1. Add `batch_spread` to `ai_consumption.py`; `report(batch=...)` adds median and population standard deviation only when a closed-shape spend authority with held_out true and a finite max_proposals covers the measured count; otherwise Unknown and the unauthorised label.
2. Tests in `test_ai_consumption_demo.py`.
3. Validate: core consumption tests, ruff check, ruff format --check, mypy.
4. Critique (single pass): authority is recorded not verified; label says so; no spend assumed. Accepted.
5. Commit, push, PR with Refs #432.

## Correction cycle 1

* `batch_spread` takes the full root count and validates both references as bounded nonempty strings, returning Unknown otherwise; regression cases added.
