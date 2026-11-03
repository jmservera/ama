# Changes: issue 124 slice 1

## Added

* `src/core/src/zava_forward/core/discovery_register.py`
* `src/core/tests/test_discovery_register.py`

## Modified

* `src/core/README.md` (discovery register section)
* `docs/reference/log.md` (appended entry)

## Validation

* Ran: 12 unit tests pass; ruff check clean on both files; mypy (cache `/tmp/mypy-124`) clean on both files.
* Not run: complete gate, benchmarks, full suites, browser checks (no web change).
* Tier: focused. No security, infrastructure, SQL or deployment change.

## Divergences

None. Evidence-gap and decision-rights checks were added after critique.
