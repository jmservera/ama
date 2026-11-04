# Changes: gate workflow matrix drift (2026-11-04)

* `tools/rpi-checks.py`: `src-ci.yml` pin updated to `99a20cf0...`.
* `tools/test_rpi_checks.py`: `test_real_src_ci_jobs_are_pinned_and_every_step_classified`.
* `docs/reference/log.md`: entry added.
* Validation: 82 gate tests pass, ruff and mypy --strict clean.
* Also updated `infra/tests/test_pipeline.py` for the final #979 mssql `if:` condition (same stale-after-last-commit cause).
