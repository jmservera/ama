# Changes: tenure Legal position reference (R1)

## Modified

* src/core/src/zava_forward/core/resident_decisions.py: `tenure_legal_position` action.
* src/core/tests/test_resident_decisions.py, src/api/tests/test_resident_api.py: tests.
* src/core/README.md, src/api/README.md: contract.

## Validation (focused tier)

Run with PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH set to the worktree src folders, because the installed distributions point at another worktree.

* `test_resident_decisions -k legal_position`: pass (JSON and SQLite); MSSQL variants skipped (opt-in loopback SQL Server not available).
* `test_resident_decisions -k tenure -k intake`: 36 run, pass, 13 skipped (MSSQL).
* `src/api` `test_resident_api`: 17 run, pass, 1 skipped (a logged law-store ValueError in output is pre-existing test noise).
* `ruff check` on src/core and src/api: pass. `mypy --cache-dir=/tmp/mypy-131` on resident_decisions.py: pass.
* Not run: gate, benchmarks, full suites, MSSQL, browser tests.

## Divergences

None. No web screen added, so web-design guidance is not triggered.
