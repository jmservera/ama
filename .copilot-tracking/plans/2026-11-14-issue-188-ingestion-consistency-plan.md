# Issue #188 plan

* Add `src/core/src/zava_forward/core/sensor_ingest.py`: `ingest_window`, `home_series`, `handover_continuity` (exact Decimal, inclusive thresholds, required declared `Tolerance`).
* Add `src/core/tests/test_sensor_ingest.py`: window re-run idempotence, changed-slot conflict, combined per-home ordered query, pass within tolerance, fail beyond it, one-sided and invalid configuration refusal.
* Validation: focused sensor tests, `ruff check` and `ruff format --line-length 100 --check` on `src/core`.
* Tier: focused (new helper and tests only; no workflow, dependency, SQL schema or security-control change).
* Critique: executed once inline; compatible finding applied (use Decimal so inclusive tolerances are exact).
