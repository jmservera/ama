<!-- markdownlint-disable-file -->
# Phase details: issue 572 r1 re-verification

## Phase 1

* `python3 -m unittest test_rpi_checks -q` from `tools/` (81 tests).
* `ruff check` and `mypy --cache-dir=/tmp/mypy-572` on `src/api/tests/test_chat_panel.py` under the api project config.
* Boundary: tools-only and test-only; no security, infrastructure, SQL or deployment change, so the focused tier applies. The gate is not run.

## Phase 2

* Write changes and review evidence, state record, and commit.
