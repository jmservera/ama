# Changes: assistant release integrity regression (#107)

Plan: [plan](../plans/2026-11-07-assistant-release-integrity-107-plan.md). Base add72cc9013ab84a36a240e635cc4417dae714d3.

## Files

* `src/api/tests/test_assistant_release.py`: imports `threading` and `Assistants`; new `Release.test_racing_workers_and_restart_after_revocation_keep_allowance_and_make_no_call`.
* RPI artifacts under `.copilot-tracking/` (research, plan, details, critique, this file, review, state).

No production code, schema, workflow, dependency or documentation change. Divergences from plan: none. Amendments: none.

## Validation (all from `src/api`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=tests:../core/tests:../agents/tests`)

| Command | Result |
| --- | --- |
| `python3 -m unittest test_assistant_release -q` | Before: 45 OK. After: 46 OK, exit 0 |
| `python3 -m unittest test_assistant_release test_assistants test_continuity -q` | 188 tests OK, 58 skipped (disposable SQL Server classes need `ZF_SQL_SERVER`; browser), exit 0 |
| `python3 -m mypy` (src/api) | no issues in 188 files |
| `python3 -m ruff check src/api src/core` | all checks passed |
| `ruff format --check` on the test file | would reformat, and the base file already does; not enforced, left as is |

Note: the PYTHONPATH shown is the component's documented test path plus `tests`; the bare README form could not import the module by name from `src/api`.

## Not run

FULL gate (`tools/rpi-checks.py --all`), disposable SQL Server tests, hosted CI, independent review. FULL PUBLICATION NOT READY until the coordinator admits the gate.
