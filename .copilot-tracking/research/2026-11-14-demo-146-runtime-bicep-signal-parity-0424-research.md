---
title: Runtime to Bicep signal parity research
ms.date: 2026-11-14
---

Task: `demo-146-runtime-bicep-signal-parity-0424`. Refs #146. Parent branch `feat/demo-146-bicep-alert-runbook-coverage-0242` at `a94a43b4c4b2c0dd645807cc966710860811c99d`. Research disposition: executed. Planning Readiness: Ready.

## Queried signals (parent a94a43b4c)

* `infra/main.bicep`: `ContainerAppConsoleLogs` `Log has "LEDGER_DIGEST_ALERT"` and `"LEDGER_DIGEST_OK"`.
* `infra/modules/operationalMonitoring.bicep`: `Log has "AI_LIMIT_BREACH"`; `StorageQueueLogs` `PutMessage` on `agent-tasks-poison`; `Microsoft.App/jobs` `Executions` state `Failed`; IoT Hub `d2c.telemetry.*` platform metrics.

## Emitters

* `src/orchestrator/.../digest_blob.py`: `ALERT_MARKER`, `OK_MARKER` printed in `main`.
* `src/core/.../ai_consumption.py`: `LOG.warning("AI_LIMIT_BREACH reason=%s route=%s")` with reasons from `held =` and `reason =` sites.
* Job failure, poison queue and IoT metrics are platform signals; no source emitter exists (import-jobs-poison remains a documented gap).

## Findings

* Markers match with zero drift. Alert queries use no PII, reading or chat fields.
* Genuine drift: `request-depth-limit` and `duplicate-attempt` are emitted but absent from the `ai-limit-calls` runbook class. Fixed in `infra/monitoring-runbooks.md`.
