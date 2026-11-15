# Issue #99 research: envelope and tolerance controls

* Existing: `src/core/src/zava_forward/core/exposure_limits.py` (record_limits, assess, load_limits), `FinanceMixin.exposure_signal` in `finance.py`, API route covered by `src/api/tests/test_finance_exposure_api.py`.
* Gap 1: approval attribution used `approver`/`approved_on`; the criteria require `approved_by`/`approved_at`, never defaulted.
* Gap 2: signal was a string only; no structured `pause_signal` naming a human decision with `automatic_cut: False`.
* Planning readiness: Ready. No company figures are invented; limits stay file-supplied.
