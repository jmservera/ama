<!-- markdownlint-disable-file -->
# Changes: issue 946

* `src/core/src/zava_forward/core/workflows.py`: `_hazard_receiver` splits the released and not-referred conditions with separate messages.
* `src/core/tests/test_hazard_referral.py`: new `test_receiver_error_names_the_failing_condition`.
* `docs/reference/log.md`: log entry.

## Validation

* Run: `test_hazard_referral.py` (37 tests, 1 skipped, OK; JSON and SQL variants); ruff check passed; mypy on the two touched files passed with `--cache-dir=/tmp/mypy-946`.
* Not run: gate, benchmarks, full suites, CI. The installed editable packages pointed at another worktree, so tests ran with `PYTHONPATH` set to this worktree's `src/*/src`.
* `ruff format --check` reports pre-existing formatting drift in `workflows.py` (not touched by this change).
* No `pyproject.toml` edited.
