# Research: issue 146 workbook cost reconciliation

Planning Readiness: Ready. Disposition: executed.

* Panel `cost-vs-budget` in `infra/monitoring-workbook.json` was a static `print`.
* Existing tests (`test_monitoring_workbook.py`, `_sla_budget.py`, `test_ai_observability_workbook_budget.py`) require the literals `ConfiguredMonthlyBudget=__MONTHLY_BUDGET__`, `AzureActualCost='Unknown'`, `AzureForecast='Unknown'`, `VarianceAgainstBudget='Unreconciled'`.
* No currency placeholder exists; the query assumes `ExpectedCurrency='USD'` (assumption to confirm).
* Boundary: do not touch `infra/main.bicep` or `infra/monitoring-runbooks.md` (PR #1625).
