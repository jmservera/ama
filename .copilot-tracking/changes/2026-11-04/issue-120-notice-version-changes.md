<!-- markdownlint-disable-file -->
# Changes: issue 120 slice 1

## Modified

* src/api/src/zava_forward/api/timecapture.py: notice approval counts only when `ZF_TIME_NOTICE_VERSION` equals `NOTICE_VERSION`.
* src/api/tests/test_timecapture.py: fixtures set the version; new version test; bump test updated.
* src/api/README.md: documents `ZF_TIME_NOTICE_VERSION`.

## Added

* .copilot-tracking research, plan, details, changes, review and state files for `issue-120-notice-version`.

## Validation (focused tier)

* Run: `python -m unittest test_timecapture` (24 tests, OK) with PYTHONPATH pointing at this worktree's `src/` (the installed editable packages point at another worktree); `ruff check` and `ruff format --check` in `src/api` (pass); `mypy --cache-dir=/tmp/mypy-120` in `src/api` as CI runs it, tests included (no issues, 175 files).
* Not run: complete gate, benchmarks, full suites, browser or screen reader checks.

## Divergences

None from plan.
