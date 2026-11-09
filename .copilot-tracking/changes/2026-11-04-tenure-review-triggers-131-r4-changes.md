# Changes: tenure review triggers (R4)

## Modified

* src/core/src/zava_forward/core/resident_decisions.py: two actions, `REVIEW_TRIGGERS`, `_open_triggers`, stale-pack and verify guards.
* src/core/tests/test_resident_decisions.py, src/api/tests/test_resident_api.py: tests.
* src/core/README.md, src/api/README.md, docs/reference/log.md.

## Validation (focused tier)

PYTHONDONTWRITEBYTECODE=1.

* core `test_resident_decisions -k trigger -k pack -k tenure -k verification -k legal`: 44 run, pass, 15 skipped (MSSQL opt-in).
* api `test_resident_api`: 20 run, pass, 1 skipped.
* core and api: `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-131` (strict, tests included, as src-ci.yml runs `mypy`): pass.
* Not run: gate, benchmarks, full suites, MSSQL, browser tests.

No web screen added. No divergences.
