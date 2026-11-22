---
title: Issue 2061 live changes
description: Changes record with per-criterion table
---

Refs #2061. Tier: focused (documentation and tracking only; no src, infra or workflow change). `rpi-checks.py --all` was not run.

## Files

* docs/reference/research/issue-2061-live-evidence-2026-11-22.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking research, critique, plan, details, changes, review and state for this task

## Estate effects

Throwaway job `job-tmp-probe-2061` created and deleted (verified absent). Nothing else changed. Evidence outside the repository: /home/azureuser/.local/share/ama/phase-witness/2061-live-20261122T233323Z/live/.

## Per-criterion proven/unproven table

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Decision record | Proven | docs/adrs/0008-single-external-demo-environment.md (Proposed), unchanged |
| 2 | One external environment, public ingress only on web and API | Proven live; fresh what-if not run | env list, app and job ingress read; 2026-11-20 what-if retained |
| 3 | Reviewed delete list, only those removed | Proven | 2026-11-20 delete ids; protected resources present; optional NSG, subnet, two alerts remain |
| 4 | Entra URI table; employee and resident sign-in | Proven for table and both sign-ins; stale URI removal unproven | URI table in the research note; screenshots; removal needs owner approval |
| 5 | Separate identities, role inventory, negative test | Partly proven | after inventory; negative probe 403/401 for id-resident-demo; no before inventory; resident app retains the API identity for sensor consent |
| 6 | Demo end to end | Mostly proven | simulator, hub route, receiver (receipts ~1030 per run), both sign-ins; import workbook flow and map interaction not re-exercised |
| 7 | Production build, infra tests, full gate receipt | Unproven here | no source change; coordinator owns the full gate |
| 8 | Rollback documented | Proven | infra/demo-single-environment-runbook.md rollback section |
