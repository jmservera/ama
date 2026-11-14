---
title: Issue 146 monitoring remaining criteria research
description: Source inventory and gaps for alerts, workbook, runbooks, diagnostic exclusion and AI-limit monitoring
ms.date: 2026-11-13
---

## Research disposition

Executed (source inspection of `origin/main` ee068a4b5). Planning Readiness: Ready.

## Existing on main

* `infra/modules/operationalMonitoring.bicep`: disabled job-failure and IoT metric alert candidates, shared workbook, `enableCandidateAlerts` plus `approvalReference` guard.
* `infra/main.bicep`: installed ledger digest scheduled-query alerts (ContainerAppConsoleLogs), budgets, action group.
* `infra/monitoring-workbook.json`: requests/errors/p95, availability, static cost and AI panels (all Unknown or Not connected).
* `infra/monitoring-runbooks.md`: entries for existing alerts and candidates; poison queues and AI limits are explicit gaps.
* `src/core/.../monitoring_coverage.py`: alert register (owner role, runbook anchor), indicator and AI-limit evaluators, allowlist sanitiser that is not wired to any logger.
* `src/core/.../ai_consumption.py`: append-only ledger with closed alert reasons (call/token/money budget, authority expiry) and per-capability usage; emits no aggregate console signal.
* Tests: `infra/tests/test_monitoring_workbook.py` (optional-table shape only), `src/core/tests/test_monitoring_coverage.py`, `test_bicep_policy.py`.

## Gaps against unticked criteria

| Criterion | Gap | Source-only closure |
| --- | --- | --- |
| Alerts incl. poison queue | no poison-queue alert | disabled scheduled-query candidates on `StorageQueueLogs` PutMessage to each poison queue |
| Alerts for AI limit breaches | no signal producer or alert | content-free `AI_LIMIT_BREACH` log marker plus disabled candidate with owner and runbook link |
| Workbook availability/errors/latency/cost vs budget | cost panel is static text only | cost-vs-budget table with budget value, Azure cost record Unknown, unreconciled variance |
| AI usage by capability and period beside Azure cost | none | `AI_USAGE` marker plus workbook panel by capability and month with cost record and variance columns |
| Each alert has runbook entry and owner | poison and AI limit entries say gap | promote to candidate entries with owner, response, recovery; test every Bicep alert |
| Diagnostic logs exclude PII, readings, chat | sanitiser unwired; about 60 `logging` calls incl. `.exception` tracebacks and request paths | process-wide redacting LogRecord factory installed at entrypoints |

## Constraints and limits

* No Azure access: queue log field shape (`ObjectKey`) and console markers are unverified against a deployed workspace; candidates stay disabled and the runbook says so.
* Azure cost is not in Log Analytics; variance stays Unknown/unreconciled, never zero.
* `print` markers (`LEDGER_DIGEST_*`) are not logging and stay untouched.
* Runbooks live in `infra/`, not `docs/reference/`, so the knowledge-base index and log are not changed.
