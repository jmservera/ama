---
title: Issue 146 live2 monitoring research (2026-11-18)
---

# Research: issue 146 monitoring coverage, second live pass

* Research disposition: executed.
* Scope: demo resource group `ama`, read-only Azure queries, raw output retained under docs/reference/research/issue-146-live2-evidence-2026-11-18/.
* Planning Readiness: Ready.

## Findings (read-only, 2026-11-18 ~12:35Z)

* Eight alerts installed and enabled: four metric (Foundry throttle, SQL CPU, API 5xx, API restarts), four scheduled-query (Key Vault expiry, Key Vault denied access, ledger digest mismatch, ledger verify missing). No permanent job-failure, poison-queue or IoT alert. No workbook. No `tmp146*` resources remain.
* Alerts Management (7d): ledger digest mismatch Sev1 fired 08:18Z and resolved; `tmp146c-job-failed` (a deleted throwaway rule from the earlier run) fired Sev3 at 10:17Z on `job-cutover-test-ledger-verify`, which proves a job-failure metric rule fires on a real Failed execution.
* Job metric `Executions` by state over 12h: Failed 11, Running 6, Succeeded 6.
* IoT Hub exposes `d2c.telemetry.ingress.sendThrottle`.
* Log Analytics and Application Insights have public query access Disabled, so workbook queries cannot render from this host. Storage has no queue log category, so poison messages cannot be observed.
* Offline tests: infra alert tests (28) and named runbook, workbook and privacy modules (24) pass.
* Raw output: docs/reference/research/issue-146-live2-evidence-2026-11-18/.
