# Changes: issue 135 round 7

* `src/core/src/zava_forward/core/exception_queue.py`: optional `ref` on `raise_conflict`.
* `src/core/src/zava_forward/core/exception_feeds.py`: `feed_stock_conflicts`.
* `src/core/tests/test_exception_feeds.py`: one test (both values with source, date and version; owner; open/closed/reconciled filtering; dedupe; operator scope excluded).
* `src/core/README.md`: feed described; not-delivered list updated.
* `docs/reference/log.md`: entry.

Validation (focused tier): 23 exception tests pass (PYTHONPATH=src); ruff check and format clean; mypy (--cache-dir=/tmp/mypy-530) clean on the two source files. Not run: gate, full suites, benchmarks, test_stock_reconciliation (needs a dataset module path outside this slice).
