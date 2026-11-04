# Changes: issue 135 round 2

* `src/core/src/zava_forward/core/exception_feeds.py`: `feed_failed_imports`.
* `src/core/tests/test_exception_feeds.py`: two tests (source kept, rows not, dedupe; nothing raised for approved or staged).
* `src/core/README.md`: feed described; not-delivered list updated.
* `docs/reference/log.md`: entry.

Validation (focused tier): 22 exception tests pass (run with PYTHONPATH=src because the editable core install points at another worktree); ruff check and format clean; mypy (--cache-dir=/tmp/mypy-530) clean on the two files. Not run: gate, full suites, benchmarks.
