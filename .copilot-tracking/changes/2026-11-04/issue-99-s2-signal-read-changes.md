<!-- markdownlint-disable-file -->

# Changes: issue-99-s2-signal-read

| File | Change |
| --- | --- |
| src/core/src/zava_forward/core/exposure_limits.py | load_limits, committed_exposure |
| src/core/src/zava_forward/core/finance.py | read-only exposure_signal |
| src/core/tests/test_exposure_limits.py | five synthetic tests |
| docs/reference/log.md | log entry |

Validation: 11 unit tests in test_exposure_limits and 29 in test_finance_signoffs pass; ruff check/format and mypy (cache /tmp/mypy-530) clean on the two changed files. Not run: gate, full suites, benchmarks, CI.

## Review fixes (PR 1028)

* `exposure_limits.py`: added `MAX_AGE_DAYS` (366) and `stale_reason`; `assess` returns Held for limits older than that or dated in the future. `load_limits` converts non-UTF-8 and other read errors to `LimitsError`. `committed_exposure` raises `LimitsError` for non-numeric, boolean or non-finite amounts.
* `finance.py`: `exposure_signal` catches these and returns Held, never raising.
* Tests: stale or future file, non-UTF-8 file, non-numeric commitment amount. The 366-day horizon is an engineering default pending owner confirmation. Gate not run, as directed.
