# Issue 125 changes (2026-11-14)

* Added `src/core/src/zava_forward/core/discovery_assistant_acceptance.py`.
* Added `src/core/tests/test_discovery_assistant_acceptance.py` (6 tests).
* Validation: ruff check and format passed; 38 of 39 focused tests passed. The one failure, `test_demo_runs_from_this_worktree_without_inputs`, spawns a subprocess and fails with `No module named 'zava_forward'` because the package is not pip-installed here; it is unrelated to this change.
* Not run: full local gate, hosted CI. Refs #125; no criterion is proven, so no closing keyword.
