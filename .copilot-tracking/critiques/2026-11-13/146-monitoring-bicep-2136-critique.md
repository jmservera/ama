---
title: Issue 146 plan critique and dispositions
description: Single independent critique of the monitoring plan with direct dispositions
ms.date: 2026-11-13
---

## Execution

Executed once by an independent rubber-duck agent. Verdict: proceed with changes. No finding conflicts with a confirmed user decision; all were applied directly.

## Findings and dispositions

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Regex redaction can leak; `extra` added after the record factory | Applied: patch `Logger.makeRecord` so extras are dropped, string args pass only if short safe tokens, exceptions reduce to type name, redaction failure withholds the message; canary tests for paths, extras, exceptions, stack text |
| 2 | Existing approval guard would silently enable new rules | Applied: separate default-false gates `enablePoisonQueueAlerts` and `enableAiLimitAlerts`, ANDed with the existing guard |
| 3 | Queue signal unproven; default destination is `AzureDiagnostics`, no importer producer | Applied: queue diagnostics set to `Dedicated` destination, alert scoped to the storage account, only `agent-tasks-poison` becomes a candidate; `import-jobs-poison` stays a gap (no producer in source) |
| 4 | Usage markers can include rolled-back or missing events | Applied: markers emitted after the ledger scope closes, labelled non-authoritative console aggregate, duplicate completion emits nothing; ledger stays financial source |
| 5 | Marker delivery and level unspecified | Applied: installer ensures a console handler and INFO for the meter logger; tests format real handler output |
| 6 | Redaction may break `test_error_logging` contracts | Applied: safe int/token args preserved; run those tests with redaction installed |
| 7 | "Every alert" test exceeds change | Applied: module-scoped test plus existing register test for installed alerts |
