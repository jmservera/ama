# Changes: tenure verification and decision route (R2)

## Modified

* src/core/src/zava_forward/core/resident_decisions.py: `tenure_verify` action, `TENURE_ROUTES`.
* src/core/tests/test_resident_decisions.py, src/api/tests/test_resident_api.py: tests.
* src/core/README.md, src/api/README.md: contract.

## Validation (focused tier)

Run with PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH set to the worktree src folders.

* `test_resident_decisions -k tenure -k verification -k legal_position`: 23 run, pass, 8 skipped (MSSQL opt-in, not available).
* `src/api` `test_resident_api`: 18 run, pass, 1 skipped (a logged law-store ValueError is pre-existing noise).
* `ruff check --no-cache src/core src/api`: pass. `mypy --cache-dir=/tmp/mypy-131` on resident_decisions.py: pass.
* Not run: gate, benchmarks, full suites, MSSQL, browser tests.

## Divergences

None. No web screen added, so web-design guidance is not triggered.
