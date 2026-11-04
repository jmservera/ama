<!-- markdownlint-disable-file -->

# Changes: issue-99-s2-signal-read

| File | Change |
| --- | --- |
| src/core/src/zava_forward/core/exposure_limits.py | load_limits, committed_exposure |
| src/core/src/zava_forward/core/finance.py | read-only exposure_signal |
| src/core/tests/test_exposure_limits.py | five synthetic tests |
| docs/reference/log.md | log entry |

Validation: 11 unit tests in test_exposure_limits and 29 in test_finance_signoffs pass; ruff check/format and mypy (cache /tmp/mypy-530) clean on the two changed files. Not run: gate, full suites, benchmarks, CI.
