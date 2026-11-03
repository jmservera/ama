<!-- markdownlint-disable-file -->

# Changes: issue-99-exposure-limits

| File | Change |
| --- | --- |
| src/core/src/zava_forward/core/exposure_limits.py | New pure module: record_limits and assess |
| src/core/tests/test_exposure_limits.py | Six synthetic unit tests |
| docs/reference/log.md | Log entry |

## Validation

Run: `PYTHONPATH=src:tests python3 -m unittest test_exposure_limits` in src/core (6 tests OK); ruff check and format; mypy --cache-dir=/tmp/mypy-99 on the two files (clean).
Not run: the complete or focused rpi-checks gate, full suites, benchmarks, hosted CI.

## Divergences

None.
