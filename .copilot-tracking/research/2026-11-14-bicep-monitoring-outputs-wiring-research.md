# Bicep monitoring outputs wiring research (Refs #146)

* Date: 2026-11-14; branch `test/demo-146-bicep-outputs-0952`, parent `985b19bcb` (PR #1625).
* Disposition: executed. Planning readiness: Ready.
* Sources inspected: issue 146, `infra/main.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/modules/monitoring.bicep`, `infra/monitoring-workbook.json`, `infra/monitoring-runbooks.md`, `infra/README.md`.

## Findings

* `main.bicep` supplies all required module params; none are unknown.
* `workspaceId`, `appInsightsId`, `actionGroupId` come from `monitoring.outputs.*`, which exist.
* `budgetName: budget.name` and `monthlyBudget` feed the workbook placeholders; all four placeholders (`__WORKSPACE_ID__`, `__APP_INSIGHTS_ID__`, `__MONTHLY_BUDGET__`, `__BUDGET_NAME__`) are replaced by the module.
* Candidate gates forward from main and default to false/empty.
* `workbookId` output flows to `operationsWorkbookId`; documented in runbooks and README.
* Every alert resource targets `actionGroupId`.
* Gap: no wiring gap in source. The contract had no dedicated test. No Bicep change needed.
* Not proved (unchanged): deployment, portal rendering, owners, thresholds.
