# Details: issue 952

## Phase 1

* File: `src/agents/src/zava_forward/agents/review_effectiveness.py`.
* SHA-256 of canonical JSON (sorted keys, compact separators) per sheet; first occurrence kept, later identical sheets recorded as `{position, duplicate_of, reviewer_code, fingerprint}` (12 hex chars).
* Totals, by-defect-class, effort and `session_count` use unique sheets only. CLI exit code logic unchanged.

## Phase 2

* File: `src/agents/tests/test_review_effectiveness.py`, `test_pool_flags_a_duplicate_sheet_and_does_not_double_count_it`: two identical sheets give one session, one flagged duplicate, effort and detection equal to the single-sheet pool; a single sheet reports no duplicates.

## Phase 3

* `python3 -m unittest tests.test_review_effectiveness` (with local PYTHONPATH), `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-952 src`.
