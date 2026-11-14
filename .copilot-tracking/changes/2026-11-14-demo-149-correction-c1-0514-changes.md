# C1 changes

* Two test files edited as in the details; no web assets changed.
* Validation: 68 tests OK across all `test_epic149_*` and `test_accessibility_baseline` (run from the repository root with the src/*/src and tests paths on PYTHONPATH); heading-hierarchy file green on 3 consecutive runs; `ruff check` and `ruff format --check` clean on the 4 changed Python files; `python3 -m mypy` from `src/api`: 0 issues in 254 files.
* Not run: hosted CI, the complete local gate. Focused tier, test-only change.
