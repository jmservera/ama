---
title: Issue 146 research, live (2026-11-26)
---

Refs #146. Research disposition: executed. Builds on live8 and live9 notes (2026-11-25).

## Findings so far

* Source already uses Total aggregation for job-failure rules; live8 shows only ledger digest enabled.
* `job-live-simulator` has no failure alert and no runbook entry; `job-live-receiver` has both (opt-in via `failureAlertActionGroupId`).
* Planning Readiness: Ready for one source gap (simulator rule + runbook entry + test) plus a fresh read-only live inventory.

## Live inventory (2026-11-26, read-only, resource group ama)

* Enabled metric alerts: Foundry throttle, SQL CPU, API 5xx and restarts (legacy and demo). Disabled: demo audit/orch/load job failure (Total), four IoT rules.
* Scheduled-query: Key Vault expiry/denied, ledger digest and verify (legacy and demo) enabled; AI limits and agent-tasks poison disabled.
* Jobs: load, audit, orch, live-simulator, live-receiver, 184-bodyscan. No failure rule for live-simulator, live-receiver or 184-bodyscan.
* Workbook modified 2026-11-21 (stale vs source per live8). No `tmp146` resource.
* Same state as live8/live9; no drill, no estate change.

## Decision

Add the opt-in failure rule to `infra/live-simulator-job.bicep` (mirrors receiver), a runbook entry with owner, and test coverage. 184-bodyscan is a separate legacy job outside this module set.
