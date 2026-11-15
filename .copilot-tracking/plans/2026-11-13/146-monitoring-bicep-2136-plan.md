---
title: Issue 146 monitoring remaining criteria plan
description: Failing-first plan for poison, AI-limit alerts, workbook panels, runbooks and log redaction
ms.date: 2026-11-13
---

## Phases

1. Log redaction: add `zava_forward.core.diagnostic_logging` (redacting LogRecord factory: emails, JWTs, bearer tokens, IPs, URL query strings, payload-like key=value, exception text reduced to type, length cap) and call `install_diagnostic_redaction()` from API server, live simulator/receiver, resident demo, agents worker and importer entrypoints. Tests: core unit tests and a source-shape test for entrypoints.
2. AI signals: `ai_consumption` logs `AI_LIMIT_BREACH reason=` on alert events and `AI_USAGE capability= period= calls= tokens= outcome=` on completion. Tests with `assertLogs`, no owner, root or hashes in the lines.
3. Bicep: `operationalMonitoring.bicep` gains disabled poison-queue and AI-limit scheduled-query candidates, each with proposed owner and runbook link, enabled only via the existing approval guard. `main.bicep` passes the poison queue names.
4. Workbook: add cost-vs-budget and AI-usage-by-capability-and-period panels showing Azure cost record Unknown and unreconciled variance; breach panel.
5. Runbook and register: promote poison queues and `ai-limits` from gap to disabled candidate in `monitoring-runbooks.md` and `monitoring_coverage.py`; update matrices and privacy section.
6. Infra tests: every alert resource has owner and a runbook anchor that exists; workbook panels present; compiled template contains the new rules disabled by default.
7. Validate: `az bicep build` for all Bicep, unit tests (core, api, agents, infra), ruff check, ruff format --check, mypy.

## Non-goals

No web JS, no cutover evidence pack, no live activation, no billing feed, no push.
