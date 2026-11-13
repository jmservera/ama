---
title: Issue 521 local container smoke research
ms.date: 2026-11-13
---

## Scope

Local-only pre-verification of the api and agents source images on `origin/main` e3e5f60e3 before the owner-authorized `ama` demo redeploy (`live_azure_demo_sync = redeploy_demo_and_sql_2028_after_merge`) after PR #1542 merges (it was OPEN at 2026-11-13). No ACR push, no Azure change, no GitHub edit.

## Evidence

* `src/api/Dockerfile` and `src/agents/Dockerfile`: build context `src/`, digest-pinned python:3.12-slim-bookworm, `USER 10001:10001`, no ENTRYPOINT.
* `src/check-container.py <project> <image>`: asserts user, Cmd, read-only/cap-drop/no-new-privileges probes with negative probes, agents has no mssql/azure modules, api `/healthz` and logo on both hardened and plain launches.
* `infra/tests/test_container_contract.py`: static contract tests (non-root, agents serve default, controls).
* `zava_forward.agents.worker.main`: `serve` without the route flag stays in standby and beats the heartbeat in `$ZF_STATE`; `health` exits 0 only with a fresh heartbeat.

## Approach

1. Build `zf-smoke-api:1921` and `zf-smoke-agents:1921` with timings.
2. Run `check-container.py` for both and the contract unit test.
3. Start an agents container in `serve`, run `health` via `docker exec`, then remove it.
4. Start an api container, check `/healthz` and Docker health status, then remove it.
5. Record timings and commands in the changes file; remove local smoke tags and containers.

## Planning Readiness

Ready. Research disposition: executed.
