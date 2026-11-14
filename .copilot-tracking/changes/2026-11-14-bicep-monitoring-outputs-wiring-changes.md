# Changes: monitoring outputs wiring (Refs #146)

* Added `infra/tests/test_bicep_monitoring_outputs_wiring.py`: required/unknown param match, output sourcing, budget and placeholder flow, default-false gate forwarding, `operationsWorkbookId` exposure, action-group wiring for all alerts.
* No Bicep, workbook or runbook edits (no gap found).
* Validation: 7 tests OK; ruff check and format check pass.
