# Issue 123 live plan details (2026-11-19)

## Phase 1

`GoldenFileError(FileNotFoundError)` with message `AI golden file not found at <path>; set ZF_AI_GOLDEN to its location`. `run_eval(golden=GOLDEN)` opens via `load_golden`, which catches `FileNotFoundError` and re-raises the named error. Other OSErrors pass through.

## Phase 2

Test with `run_eval(golden=Path(tmp)/"absent.json")` asserting the error type and `ZF_AI_GOLDEN` in the message; existing `test_golden_run...` covers the present path.
