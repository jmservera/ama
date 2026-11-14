# Changes: rubric prepare PR diff scope (Refs #198)

Date: 2026-11-14.

* `.github/rubric/scripts/prepare.py`: filter `changed_artifacts` to artifacts touched by the PR diff on `pull_request`; move the reason line after the filter.
* `.github/rubric/scripts/test_prepare.py`: three tests for a lagging baseline (PR on `tools/foo.py` not scored, PR on solution code scored, push still scored).

Validation: `test_prepare.py` 75 passed, 1 pre-existing failure (same failure without the change). Full directory: 17 failures, identical to the pre-change run. `unittest discover` runs 0 tests (pytest-style suite). Ruff reports only the two pre-existing RUF100 findings.
