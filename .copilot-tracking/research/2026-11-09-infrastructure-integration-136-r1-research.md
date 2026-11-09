---
title: Infrastructure integration 136 recovery R1 research
description: Prospective 2026-11-09 recovery research for the adopted planning-only parent PR 1272 and the next Bicep demo increments
ms.date: 2026-11-09
---

## Execution and boundary

Research executed 2026-11-09 (demo recovery). Original 2026-11-08 research, critiques, reviews and C1 are preserved unchanged. Seed: PR 1272 head `f16a398d400538b918eb965baf461cb2997a0c27`, base `main`, state OPEN. Fetched `origin/main` = `b46a9ad9a9619db535368d1b2cbbddec8110e122`; merge base `0f05e9aae`, 21 commits behind.

## Findings

* R1 Candidate disposal: `git diff origin/main...HEAD` is 16 files, 815 insertions, all under `.copilot-tracking/`. No Bicep or source change. Focused pure-doc review applies; no local gate (owner demo tier).
* R2 Main drift since the merge base touches `infra/` only in `infra/README.md` (actionlint retrieval note, 4 lines, #1275). The candidate does not edit it; a local merge is conflict-free by path and not required for a tracking-only PR.
* R3 Identity and ordering: `0bd489d3` is a Copilot session UUID, not a Git object (C1 amendment F1). Gate order is local validation, independent assessment, authorized push/PR, hosted checks. The authenticated commit identity resolves to `8036360+jmservera@users.noreply.github.com`, already set locally.
* R4 Actual inventory in `infra/main.bicep` and `infra/modules/`: identity, network, monitoring, keyvault, storage, registry, sql, foundry, containerapps, iothub (module wired at `main.bicep:347`, B1, one unit, routing off), edge, guards, envDns. Standalone: `resident-demo.bicep`, `live-simulator-job.bicep`, `iot-hub-live.bicep`, `public-edge-existing.bicep`, `resident-assistant.bicep`.
* R5 IoT Hub is already present (module and live templates); do not create another module.
* R6 Demo ingress versus edge: `containerapps.bicep` has `demoDirectIngress` (external environment, tag `zava-forward-ingress=direct`) for the demo API; production Front Door/WAF stays deferred in #143 (custom domain, production-profile evidence unmet).
* R7 Workload images and queue: Container Apps declares agent KEDA `agent-tasks` and import `import-jobs` azure-queue rules with `QUEUE_ENDPOINT`. Source gap: `zava_forward.agents.worker serve` still refuses (no queue adapter or API post-back on main) and the orchestrator `__main__` prints a version only. Open PR #1141 (base main, Refs #144) adds `queue_azure.py` and README/log changes; it is unmerged and not integrated here.
* R8 Simulator: `live-simulator-job.bicep` (issue 184 stage 2) is authored and compiled, not deployed; needs IoT live approval, device registration, certificate storage, SQL read grant, AcrPull and digest image. Parameter contract requires `approvalReference`, digest `image`.
* R9 Native children (live 2026-11-09): #137 open (region/quota checks unticked), #138 open (all six AC unticked), #139 closed, #140 open (one AC: device provisioning owner), #141 closed, #142 open, #143 open, #144 open (five AC unticked, one ticked), #145 open, #146 open, #147 closed, #148 open (dry-run/disposable test unticked).

## Ranked smallest existing children

* 1 #144 queue/worker completeness, after #1141 merges: images real and queue binding. Smallest because the Bicep scale rules already exist; the gap is source.
* 2 #140 last AC: decide device provisioning approach and credential owner (decision, not Bicep).
* 3 #137 region/quota check parameters (what-if evidence, owner values).
* 4 #138 what-if on PR and digest release (largest, deferrable beyond 16 November).
* Deferred, AC retained: #143 Front Door/WAF, #147 Defender decision, #145/#148 from-empty and live proofs, #146, #142.

## Planning readiness

Ready for a docs-only parent assessment. No Bicep implementation is in scope.
