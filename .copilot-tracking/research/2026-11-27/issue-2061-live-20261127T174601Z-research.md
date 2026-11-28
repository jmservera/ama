---
title: Issue 2061 live research 2026-11-27
ms.date: 2026-11-27
---

Refs #2061. Opening record: re-verify the unticked criteria against live Azure (resource group `ama`) and the worktree,
building on `docs/reference/research/issue-2061-live-evidence-2026-11-23.md`. Findings are appended below.

Known candidate gap: `infra/resident-demo.bicep` does not carry the sensor-consent wiring that the live app holds.

## Findings

Evidence outside the repository: `/home/azureuser/.local/share/ama/phase-witness/2061-live-20261127T174601Z/live/`
(`live-2026-11-27.json`, `role-inventory-2026-11-27.txt`). Read-only `az` calls; no secrets printed.

* One environment `cae-cutover-test-demo` (`vnetConfiguration.internal=false`); apps `ca-cutover-test-demo-api` (rev 0000149) and `ca-resident-demo` (rev 0000033) external; `ca-cutover-test-demo-agents` and all seven jobs have no ingress; one Event Hubs namespace `eh-iot-cutover-test-rzsrg`. `GET` on the resident host returns 200.
* Role inventory is unchanged from the 2026-11-23 pass (public `id-resident-demo`: AcrPull, two named Key Vault secrets, OpenAI User).
* `ca-resident-demo` still holds `id-resident-demo` plus `id-cutover-test-api` and the opt-in env vars `ZF_DEMO_SENSOR_CONSENT*` read by `src/api/.../resident_demo/sensor_consent.py` (`port_from_env`, fails closed when unset).
* Real code gap: `infra/resident-demo.bicep` can express neither the second identity nor those variables, so a redeploy of committed Bicep silently drops sensor consent and the extra identity. Fix: opt-in parameters (default empty keeps the least-privilege single identity). No src change.

Planning Readiness: Ready. Research disposition: executed.
