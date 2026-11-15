# Changes: Issue #146 monitoring coverage (Refs #146)

Task `146-monitoring-bicep-2136`, branch `feat/demo-146-bicep-monitoring-runbooks-2136`.
Plan: `.copilot-tracking/plans/2026-11-13/146-monitoring-bicep-2136-plan.md`.
Critique (single, all 7 findings applied directly): `.copilot-tracking/critiques/2026-11-13/146-monitoring-bicep-2136-critique.md`.

## Added

* `src/core/src/zava_forward/core/diagnostic_logging.py`: process-wide fail-closed log redaction (drops extras, stack and exception text; withholds non-token args; redacts email, JWT, bearer, IP, URL queries and payload keys).
* `src/core/tests/test_diagnostic_logging.py`: canary tests for PII, raw readings and chat content.
* `infra/tests/test_monitoring_alerts.py`: owner and runbook link per new alert, separate default-false gates, Dedicated queue diagnostics, compiled disabled state, workbook panels.

## Modified

* `src/core/.../ai_consumption.py`: content-free `AI_LIMIT_BREACH` and `AI_USAGE` console markers (non-authoritative).
* Entrypoints (`api` server, live_simulator, live_receiver, resident_demo, `agents` worker, `importer`) install the redaction.
* `src/core/.../monitoring_coverage.py` and its test: `agent-tasks-poison` and `ai-limits` become disabled candidates; `import-jobs-poison` (no producer) and `rai-harm` remain gaps.
* `infra/modules/storage.bicep`: queue diagnostics use the Dedicated destination (StorageQueueLogs).
* `infra/main.bicep`, `infra/modules/operationalMonitoring.bicep`: two scheduled-query alert candidates with separate gates, owners and runbook links.
* `infra/monitoring-workbook.json`: cost-vs-budget, ai-usage-by-capability and ai-limit-breaches panels; Unknown and Unreconciled, never zero.
* `infra/monitoring-runbooks.md`: runbook entries, privacy boundary and evidence matrix updated.

## Not done / divergences

* No criterion is ticked; no deployment, appointment, signal drill or DPO approval exists.
* Queue-log field shape and console markers are unverified against a deployed workspace.
* `src/api` mypy reports pre-existing errors (missing playwright stubs); none in files changed here.
* `docs/reference/` untouched, so the index and log are unchanged.

## Validation

* `az bicep build` of every `infra/*.bicep` and `infra/modules/*.bicep`: pass.
* Infra monitoring tests: 9 pass. Core targeted tests (diagnostic logging, AI consumption, coverage): 75 pass.
* `ruff check`, `ruff format --check`: pass in core, api, agents, importer. `mypy`: core, agents, importer clean.
* Affected and targeted suites per review artifact; full core/api suites not completed locally.
