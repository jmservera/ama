# Changes: issue 146 workbook cost reconciliation

* `infra/monitoring-workbook.json`: cost panel query and note text.
* `infra/tests/test_monitoring_workbook_cost_reconciliation.py`: new tests.

Validation: JSON valid; `az bicep build` ok; infra tests 601 run, 1 error (`test_ledger_alert_queries_match_the_verifier_markers`, missing `zava_forward.orchestrator` package in env, unrelated); ruff clean on the new file (72 pre-existing ruff findings elsewhere in `infra/tests`). KQL was not executed against a live workspace.
