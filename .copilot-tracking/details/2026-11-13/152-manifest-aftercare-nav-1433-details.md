# Details: #152 manifest aftercare navigation (1433)

## Phase 3 candidate (rejected by critique; evidence-only outcome applied, no guard added)

The failing assertion gives no hint that the imported `zava_forward` package is not the working tree. Candidate guard in `src/api/tests/test_workbench.py`: a test asserting `zava_forward.api.workbench.__file__` resolves under this checkout's `src/api/src`, so a stale editable install fails with an explicit message instead of four manifest diffs. Failing-first evidence is the reproduced 4-subtest failure in the stale environment; the guard was never implemented.

Alternative (default if critique rejects the guard): record evidence only, no source change.

## Validation

`test_workbench*`, `test_design_system*`, `test_accessibility_baseline*`, `test_aftercare*` (src/api); `test_scenario_manifest*`, `test_needs_inventory*` (src/core); `ruff check`, `ruff format --check`, strict `mypy` from `src/api`.
