# Research: simulator run owner, time limit and budget alert (#189)

Date: 2026-11-14. Planning Readiness: Ready. Disposition: executed.

* Issue #189 has one unticked criterion: "Run has an owner, a time limit and a budget alert".
* `src/core/src/zava_forward/core/synthetic/run_plan.py` already enforces an owner, a bounded `max_seconds` and a USD alert threshold fraction, but exposes no GBP alert amount and no runtime event; `sensor_stream.RunBudget` has only an `alert_reference` label.
* `sensor_stream.accountable_text` rejects blank and placeholder owners and is reused.
* Gap: no deterministic budget-alert event when projected or accumulated cost reaches the threshold, and no halt before the cap.
* Decision: add a separate `run_governance.py` (`RunGovernance`, `RunMeter`) with GBP Decimal amounts so existing USD estimate contracts stay unchanged.
