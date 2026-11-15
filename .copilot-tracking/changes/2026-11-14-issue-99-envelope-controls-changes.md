# Issue #99 changes

* exposure_limits.py: approved_by/approved_at attribution, `pause_signal`, public `held()`.
* finance.py: Held results use `el.held()` so they carry `pause_signal`.
* test_exposure_limits.py: attribution and pause-signal tests.
* Validation: test_exposure_limits (18 OK), test_finance_exposure_api (4 OK), ruff, mypy clean. Run with PYTHONPATH set to this worktree because the editable install points at another checkout. unittest discover not run.
