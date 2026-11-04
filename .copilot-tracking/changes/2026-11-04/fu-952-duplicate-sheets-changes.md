# Changes: issue 952

* Modified `src/agents/src/zava_forward/agents/review_effectiveness.py`: `pool_human_sessions` detects identical sheets by content fingerprint, flags them in `duplicate_sheets`, and leaves them out of all totals.
* Modified `src/agents/tests/test_review_effectiveness.py`: added duplicate regression test.
* Modified `docs/reference/log.md`: appended entry.

## Validation (focused tier)

* Run: `tests.test_review_effectiveness` (34 tests, OK); `ruff check`; `ruff format --check` on touched files; `mypy --cache-dir=/tmp/mypy-952 src` in `src/agents` (no issues).
* Not run: full suites, benchmarks, complete local gate (not required: no security, infrastructure, SQL or deployment change).
* No pyproject.toml edited.

## Divergences

None. Note: the pip-installed editable packages point at another worktree, so tests used an explicit `PYTHONPATH` to the local `src` folders.
