---
title: Issue 521 local container smoke changes
ms.date: 2026-11-13
---

Status: complete. Local-only pre-verification; no ACR push, no Azure or GitHub change. Only tracking artifacts were added.

## Source identity

* Tested commit: `e3e5f60e3a691fb96b505c97254b302bdc4d29a5` (equals `origin/main` after `git fetch` on 2026-11-13). Worktree clean apart from tracking artifacts.
* PR #1542 (`Closes #1530`) was OPEN at test time, so this result predates the redeploy-triggering merge. Re-run after that merge if main changes.
* Images: `zf-smoke-api:1921` = `sha256:51a863c93fbfcdd6c042b76cb30b65edd214ff2377e061da09544d759d7fa8a0`; `zf-smoke-agents:1921` = `sha256:f46772e6b0d88a18be2b047d944a9817fad483b8cf54046a75703d1ea4bfca6a`. Docker 29.9.0.

## Results

| Step | Command | Result | Time |
| --- | --- | --- | --- |
| Build api | `docker build -q -f src/api/Dockerfile -t zf-smoke-api:1921 src` | OK | 1m19s |
| Build agents | `docker build -q -f src/agents/Dockerfile -t zf-smoke-agents:1921 src` | OK | 25s |
| Api contract | `python3 src/check-container.py api zf-smoke-api:1921` | PASS (controls, negative probes, hardened and plain startup, logo) | 27s |
| Agents contract | `python3 src/check-container.py agents zf-smoke-agents:1921` | PASS (no mssql/azure modules) | 22s |
| Static contract | `python3 -m unittest infra.tests.test_container_contract -q` | 9 tests OK | 0.15s |
| Agents standby | hardened `docker run -d ... python -m zava_forward.agents serve`, then `docker exec ... python -m zava_forward.agents health` | uid 10001, standby log `queue consumption is off`, health exit 0 (also after api wait) | about 3s |
| Api health | hardened run with `ZF_AI=off`, read-only seed at `/data`, loopback port; poll `/healthz` and Docker health | uid 10001, `/healthz` 200, Docker health `healthy` | 28s |

Hardened flags for smoke runs: `--read-only --cap-drop=ALL --security-opt=no-new-privileges --tmpfs=/tmp --tmpfs=/state:rw,uid=10001,gid=10001`. Image config `User` is `10001:10001` for both.

## Cleanup

Containers `zf-smoke-agents-1921` and `zf-smoke-api-1921` removed by captured ID through a shell trap; the temporary seed directory was removed; `docker rmi zf-smoke-api:1921 zf-smoke-agents:1921` run; zero `zf-smoke` containers or images remain.

## Limits

* Local Docker only. Hosted Source CI for the exact head, Azure Container Apps behaviour, SQL connectivity, ACR push and the redeploy itself were not exercised.
* Agents queue consumption (route flag enabled) was not exercised; only standby and health.
