# Changes: Phase 0 baseline and wait analysis (Refs #124)

* Added `src/core/src/zava_forward/core/discovery_flow.py` and `src/core/tests/test_discovery_flow.py`.
* Updated `src/core/README.md` and appended `docs/reference/log.md`.

Validation run: `python -m unittest discover -s tests -p 'test_discovery_*.py'` from src/core with PYTHONPATH=src (30 tests OK; the installed package points at another worktree); ruff check and format; mypy --cache-dir=/tmp/mypy-530 on the new module (clean).
Not run: gate, benchmarks, full suites, hosted CI.
