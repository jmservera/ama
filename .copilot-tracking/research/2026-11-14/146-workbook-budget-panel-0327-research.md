# Research: 146-workbook-budget-panel-0327 (Refs #146)

* Workbook is `infra/monitoring-workbook.json` (not under `infra/modules/`). It already has `ai-usage-by-capability`, `ai-variance-by-period`, `cost-vs-budget`, `ai-limit-breaches` and an `ai-usage-and-harm` table naming disabled task monitoring as Blocked.
* Gap: no single test pinning capability-level metered calls/tokens, disabled-task status, unreconciled variance and absence of raw prompt/PII projections. No workbook change needed.
* Planning readiness: Ready. Disposition: executed. Tier: focused (test-only).
