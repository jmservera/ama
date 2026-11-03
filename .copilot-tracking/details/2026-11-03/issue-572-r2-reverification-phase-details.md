<!-- markdownlint-disable-file -->
# Phase details: issue 572 r2 re-verification

## Phase 1

* `tools/` `python3 -m unittest test_rpi_checks -q` with PYTHONDONTWRITEBYTECODE=1.
* `ruff check` and `mypy --cache-dir=/tmp/mypy-572` on `src/api/tests/test_chat_panel.py` from `src/api`.

## Phase 2

* Write changes and review evidence; remove `src/api/.ruff_cache`; confirm `git status --short --ignored` is empty after commit.
