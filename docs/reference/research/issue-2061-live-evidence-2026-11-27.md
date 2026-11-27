---
title: Issue 2061 live evidence pass 2026-11-27
description: Read-only re-verification of the single-environment demo and a Bicep fix for the resident sensor-consent wiring drift
ms.date: 2026-11-27
---

Refs #2061. Synthetic demo, desktop, resource group `ama`. This pass extends
[the 2026-11-23 pass](./issue-2061-live-evidence-2026-11-23.md). Evidence files sit outside the repository in
`/home/azureuser/.local/share/ama/phase-witness/2061-live-20261127T174601Z/live/`. No Azure change was made and no
throwaway resource was created.

## Findings

* Live shape: one environment `cae-cutover-test-demo` (`internal=false`); `ca-cutover-test-demo-api` (revision 0000149) and `ca-resident-demo` (revision 0000033) have external ingress; the agents app and seven jobs have none; one Event Hubs namespace, `eh-iot-cutover-test-rzsrg`.
* Role inventory for the four user-assigned identities is unchanged from 2026-11-23.
* Drift closed in code: `infra/resident-demo.bicep` now expresses the second identity and the `ZF_DEMO_SENSOR_CONSENT*` variables through opt-in parameters, default off. The live app was not redeployed.
* Not re-run today: Entra sign-in screenshots, import workbook, map, fresh what-if, negative identity probe, full gate receipt.

The per-criterion table is in the
[changes record](../../../.copilot-tracking/changes/2026-11-27/issue-2061-live-20261127T174601Z-changes.md).
