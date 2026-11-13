---
title: Issue 521 local container smoke details
ms.date: 2026-11-13
---

## Commands

* P1: `docker build -f src/api/Dockerfile -t zf-smoke-api:1921 src`; `docker build -f src/agents/Dockerfile -t zf-smoke-agents:1921 src`.
* P2: `python3 src/check-container.py api zf-smoke-api:1921`; `python3 src/check-container.py agents zf-smoke-agents:1921`; `python3 -m unittest infra.tests.test_container_contract -q` (from the repo root; fall back to `python3 -m unittest discover -s infra/tests -p test_container_contract.py`).
* P3: `docker run -d --name zf-smoke-agents-1921 --read-only --cap-drop=ALL --security-opt=no-new-privileges --tmpfs=/tmp --tmpfs=/state:rw,uid=10001,gid=10001 zf-smoke-agents:1921 python -m zava_forward.agents serve`; wait; `docker exec ... python -m zava_forward.agents health` exit 0; `docker logs` shows standby; `docker rm -f`.
* P4: seed file in a temporary directory, run api with `ZF_AI=off`, loopback-published port, poll `/healthz`, read `docker inspect` health status, `docker exec id -u`; `docker rm -f`.
* P5: `docker rmi zf-smoke-api:1921 zf-smoke-agents:1921` (exact tags only); remove only the temporary seed directory.

## Success

All commands exit 0, uid 10001, standby log present, health OK, no leftover smoke containers, `git diff --check` clean.

## Critique amendments (PC-001 to PC-003)

* Pre-check that the `zf-smoke-*:1921` tags and `zf-smoke-*-1921` container names do not exist; cleanup removes only containers by captured ID and only these tags, via a shell trap.
* Api health: bounded poll of `/healthz` and `docker inspect` health until `healthy` (timeout 90 s), logs on failure; seed dataset directory mode 0755, file 0644, mounted read-only at `/data`, `/state` as tmpfs uid 10001.
* Record tested commit (`git rev-parse HEAD`), `git status --short` state and the resulting image IDs in the changes file.
