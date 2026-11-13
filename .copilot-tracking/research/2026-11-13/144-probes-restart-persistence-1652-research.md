---
title: "Issue 144 probes, heartbeat and restart persistence research"
description: "Local software-provable audit of issue 144 criteria C2 and C5"
ms.date: 2026-11-13
---

## Scope and disposition

Research disposition: executed. Planning Readiness: Ready. Tier: Focused. No push, no issue edit, no live Azure.

## Findings

* `agents` Container App (`infra/modules/containerapps.bicep`, `resource agents`) has Single revision mode, 0.5 vCPU/1 GiB, an azure-queue scale rule (0 to 5, queueLength 5) and no `probes` block. `api` has Startup, Readiness and Liveness HTTP probes on `/healthz:8088`.
* Container Apps probes are HTTP or TCP only (no exec). The worker has no listener, so `python -m zava_forward.agents health` (heartbeat file at `$ZF_STATE/worker-heartbeat`) cannot be wired as a hosted probe. Adding an HTTP/TCP probe would fail and restart a healthy worker, so the absence is a deliberate, documented boundary that is currently untested.
* Heartbeat (O1 from the standalone worker review): `pulse()` runs once per `serve` loop iteration. Idle cadence is `IDLE_SECONDS` = 2 s; a loop iteration can block in `run_once` for a task (provider timeout bounded at 1..40 s by `TaskMessage`) plus `ERROR_BACKOFF_SECONDS` = 5 s on faults. `HEARTBEAT_MAX_AGE_SECONDS` = 120 s. The margin holds but no test ties the constants together, so a later change to either could make `health` report a live worker unhealthy.
* Restart evidence: `src/api/tests/test_restart_audit.py` covers SQL ledger persistence across a store restart (entries, chain, digest). `src/agents/tests/test_worker.py` covers post-failure redelivery but not a worker replacement that abandons a leased task (crash/revision swap) and is then redelivered to a fresh worker without loss or duplicate ack.
* API single replica: `enablePublicSimulationLane` forces `maxReplicas` 1 and is tested in `test_bicep_policy.py` (lines ~2288-2298).
* Rollback: `activeRevisionsMode: Single` asserted for api and agents; the rollback procedure is a reviewed revert plus release (infra README, hosting completeness status).

## Gap decisions

1. Add a contract test that the `agents` app defines no HTTP/TCP probe (platform limit) and that the worker health constants leave a margin over the worst-case loop block. Document the boundary in the infra README.
2. Add a deterministic agents restart test: a first worker is stopped mid-task without ack, a fresh worker on the same queue handles the redelivered message exactly once.
3. Extend the API restart audit test to cover a restart after the heartbeat-independent audit append continuing the digest chain is already covered; add no duplicate.

## Out of scope

Live rollout, hosted hardening, declared-scale load run, hosted restart receipt. These stay unmet and are not claimed.
