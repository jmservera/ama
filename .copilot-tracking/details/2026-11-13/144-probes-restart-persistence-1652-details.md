---
title: "144 probes and restart persistence details"
ms.date: 2026-11-13
---

## Phase 1

`infra/tests/test_container_contract.py`: slice the `agents` resource text; assert `probes` absent, `activeRevisionsMode: 'Single'`, `type: 'azure-queue'`, `minReplicas: 0`, `maxReplicas: 5`; assert the api resource has Startup, Readiness and Liveness probes with a `/healthz` HTTP path. Comment: Container Apps probes are HTTP or TCP only and the worker has no listener.

## Phase 2 (revised after critique PC-001)

`test_worker.py`: with an empty queue `serve` pulses once per loop and waits `IDLE_SECONDS`; assert the pulse count grows with the idle wait and that `IDLE_SECONDS * 10 < HEARTBEAT_MAX_AGE_SECONDS`. Assert `healthy()` boundary with fixed `now` (age equal to max healthy, just over unhealthy). Assert the 40 s provider timeout bound plus backoff and idle fit inside the max age, labelled as the provider-call margin only. No worst-case guarantee is claimed: queue, token, post and ack calls are not bounded by this test. README says the heartbeat is a local/container diagnostic, not a hosted probe.

## Phase 3 (revised after critique PC-002)

`test_worker.py` with a `Crash(BaseException)` that `serve` does not catch. Case A, crash before post: provider raises Crash; no result, no ack, message leased. Simulated visibility expiry (`release`) then a fresh `serve` with a new worker handles it exactly once. Case B, crash after post and before ack: queue `ack` raises Crash after the sink recorded the result; after expiry a replacement worker posts again; assert two posts carry the identical task id (at-least-once, dedupe belongs to the receiver) and final ack happens once. Stop `serve` via a sink/queue hook setting the stop event after ack.

## Phase 4 (revised after PC-003, PC-004)

Infra README: label `test_restart_audit.py` as SQL store reopen evidence, not an API replica restart; hosted single-replica restart receipt and executable revision rollback test remain Unmet. Document the agents no-probe platform boundary.
