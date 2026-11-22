---
title: Issue 2201 live changes, 2026-11-22
---

Status: complete. Tier: focused (no src change; no gate run). Files: `docs/reference/research/issue-2201-live-three-runs-2026-11-22.md`, `docs/reference/README.md`, `docs/reference/log.md`, tracking artifacts and `.copilot-tracking/evidence/2026-11-22/issue-2201-live3/`. No Azure change, no Bicep, ACR read back Disabled, no throwaway resource.

Executions: job-live-receiver-29922000 (04:00), -29922030 (04:30), -29922060 (05:00, ended 05:25:44) all Succeeded on digest sha256:295164ca...4f72.

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence | Partly proven | Defect and captured SENSOR_SQL_UNAVAILABLE; exit code and older logs unavailable |
| Fix merged and deployed | Proven | #2231 on main; job image equals API revision digest |
| Three consecutive scheduled runs Succeeded | Proven | 29922000, 29922030, 29922060 |
| Readings in store and employee map with timestamps | Proven for demo | map 200/443 items; ZF-2025-0030 fresh, latest 2026-11-22T05:10:00Z; hub-to-store hop inferred |
