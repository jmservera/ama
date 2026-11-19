---
title: Issue 146 live monitoring research (2026-11-18)
---

# Research: issue 146 monitoring coverage (demo, live)

* Research disposition: executed. Planning Readiness: Ready.
* Scope: docs/evidence only; resource group `ama`; no drills, rotations or production changes.
* Unticked criteria: C1 alerts (jobs, poison, digest, IoT); C2 dashboard/workbook; C3 runbook owners; T2 tokenomics dashboard with variance.
* Prior evidence: docs/reference/research/issue-146-live-monitoring-evidence-2026-11-18.md (earlier run). This run re-observes live state and extends it.
* Findings are appended below as they are gathered.

## Findings (live, 2026-11-18T10:05Z)

* Installed alerts unchanged: four metric alerts (Foundry throttle, SQL CPU, API 5xx, API restarts) plus `alert-109-probe-connectivity` (fired Sev3 08:38Z, from #109); four scheduled-query alerts (Key Vault expiry, denied access, ledger digest mismatch, ledger verify missing); one action group `ag-cutover-test-ops` (one email receiver).
* No workbook, no job-failure, poison-queue or IoT alert installed. Source monitoring.bicep defines the job and IoT candidates disabled, pending named-human approval.
* The ledger digest mismatch alert (fired 08:18Z) was provoked by the #115 forced-mismatch copy test, which explains the earlier "adverse finding": it is not a real tamper signal.
* Budget listing now returns RBACAccessDenied for this login; budget values come from the earlier run.
* Job `job-cutover-test-ledger-verify` Failed executions: 5 at 07:05Z, 6 at 08:05Z (metric `Executions`, dimension `state`), usable as a real signal for a job-failure rule.
* Gap decision: poison queue and workbook rendering stay unprovable without changing security controls (storage diagnostics, query public access).
