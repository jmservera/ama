# Issue 189 changes

Status: implemented. Refs #189; criterion 3 (live owned run, time limit and budget alert) stays unproven, so the issue stays open.
Tier: FOCUSED (source-only; no Azure, SQL, infrastructure or deployment change).

## Files

* `src/api/src/zava_forward/api/live_control.py`: `parse` now validates owner and approval_reference with `sensor_stream.accountable_text` (still also refusing the local `PLACEHOLDERS`), so the control file, the admin API and the `live_control start` CLI share the rule used by `RunPlan` and `RunBudget`.
* `src/api/tests/test_live_control.py`: two regression tests (parse refusals for `nobody`, `<owner>`, 161 characters; CLI start with owner `nobody` exits 2 and writes nothing).

## Measurement

* Before: parse accepted owner/approval `nobody`, `<owner>` and a 5000-character string (reproduced on base eb51af5c9). Red run with the old `live_control.py`: 7 failures (6 subtests + CLI test).
* Note: the shell's editable installs point at the main checkout, so all runs set `PYTHONPATH` to this worktree's `src/*/src` (verified `live_control.__file__` resolves to the worktree).

## Validation (sequential, targeted)

| Command (from `src/api`, worktree PYTHONPATH) | Result |
| --- | --- |
| `python3 -m unittest tests.test_live_control test_simulator_admin tests.test_live_simulator tests.test_iot_stream` | 172 tests OK |
| `python3 -m unittest tests.test_run_plan tests.test_sensor_stream` (from `src/core`) | 42 tests OK |
| `ruff format --isolated --line-length 100 --check` on both files | already formatted |
| `mypy src/zava_forward/api/live_control.py` | no issues |

Not run: `rpi-checks.py --all` (heavy gate lock held, FULL tier not required), browser harness (no UI change), receiver SQL tests (no SQL touched).
