# Plan: quality sensor risk explanation

* [x] Add `quality_sensor_risk.py`: `explain_inspection_risk`, `rank_homes`; factors sustained_high_humidity and inspection_age; `advisory_only=True`, `requires_inspector_signoff=True`, `signoff_state=pending_human_inspector`; insufficient telemetry falls back to inspection age.
* [x] Add `tests/test_quality_sensor_risk_explanation.py` (5 cases).
* [x] Validate with unittest, ruff check and ruff format --check.
* Critique (single pass, self-run): no conflicts with decisions; scope stays bounded, no chat_eval.py, no UI or task wiring.
