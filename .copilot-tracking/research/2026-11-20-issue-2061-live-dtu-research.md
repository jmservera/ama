# Research: issue 2061 live deploy with DTU SQL tier (2026-11-20)

Task: issue-2061-live-dtu (Refs #2061). Mode: automatic. Tier: FULL for infra, executed under owner decisions of 2026-11-20 (live deploy authorised, cap USD 700, no drills, no Key Vault rotation).

Research disposition: executed. Planning Readiness: Ready once the live inventory below is recorded.

## Owner decisions (authoritative)

1. SQL stays Standard S0 (10 DTU). Add optional `sqlTier='dtu'`; default unchanged; no serverless conversion.
2. Event Hubs: template creates its own `eh-<name>` namespace; IoT Hub route moves to it; delete `evhns-cutover-test-demo` only after telemetry flows end to end.
3. What-if parameters come from the runbook profile, not the stale deployment.
4. Stop if any Delete touches SQL data, storage, Key Vault, IoT Hub, `cae-cutover-test-demo` or its public IP.
5. After deploy: create-sql-users.py, move apps and jobs, Playwright sign-in, Key Vault 403 test, delete the runbook delete list by id, rollback on failure.

Prior artifacts of the earlier run (`2026-11-20-issue-2061-live-*`) are preserved; this loop uses the `-dtu` suffix.

## Findings

Recorded in the evidence section of the changes record as each step runs.
