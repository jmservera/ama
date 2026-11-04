# Changes: tenure question pack (R3)

## Modified

* src/core/src/zava_forward/core/resident_decisions.py: two actions, helpers `_tenure_report`, `_pack_is_current`.
* src/core/tests/test_resident_decisions.py, src/api/tests/test_resident_api.py: tests.
* src/core/README.md, src/api/README.md, docs/reference/log.md.

## Validation (focused tier)

PYTHONDONTWRITEBYTECODE=1, PYTHONPATH to worktree src folders.

* core `test_resident_decisions -k pack -k tenure -k verification -k legal_position`: 35 run, pass, 12 skipped (MSSQL opt-in).
* api `test_resident_api`: 19 run, pass, 1 skipped.
* `ruff check --no-cache src/core src/api`: pass. mypy --cache-dir=/tmp/mypy-530 on resident_decisions.py: pass.
* Not run: gate, benchmarks, full suites, MSSQL, browser tests.

No web screen added; web guidance not triggered. No divergences.
