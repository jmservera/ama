---
title: Issue 2061 live changes
description: Changes record with per-criterion table
---

Refs #2061. Tier: focused (documentation and tracking only; no src, infra or workflow change). `rpi-checks.py --all` was not run. Live: revisions 0000054 and 0000026.

## Files

* docs/reference/research/issue-2061-live-evidence-2026-11-23.md (new)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking research, critique, plan, details, changes, review and state for this task

## Estate effects

None. No throwaway resource was created. Evidence outside the repository: /home/azureuser/.local/share/ama/phase-witness/2061-live-20261123T005026Z/live/.

## Per-criterion proven/unproven table

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Decision record | Proven | ADR 0008 (Proposed), unchanged |
| 2 | One external environment, public ingress only on web and API | Proven live; fresh what-if unproven | env and app reads; 2026-11-20 what-if retained |
| 3 | Reviewed delete list, only those removed | Proven; optional leftovers owner-gated | NSG, `snet-aca`, two alerts remain |
| 4 | Entra URI table, both sign-ins | Proven; stale URI removal owner-gated | URI table, Playwright employee and resident sign-in |
| 5 | Separate identities, role inventory, negative test | Partly proven | after inventory 2026-11-23; negative probe 2026-11-22; no before inventory; resident app holds the API identity and its sensor-consent env vars are absent from Bicep (drift, owner decision) |
| 6 | Demo end to end | Proven except blob-triggered load job | import workbook check, map with 59 fresh readings (314 s old), sign-ins |
| 7 | Production build, infra tests, full gate receipt | Build and 759 infra tests proven; receipt unproven here | coordinator owns the gate |
| 8 | Rollback documented | Proven | infra/demo-single-environment-runbook.md |
