---
title: Issue 521 local container smoke plan
ms.date: 2026-11-13
---

## Plan

* [x] P1 Build `zf-smoke-api:1921` and `zf-smoke-agents:1921` from `src/` with `time`.
* [x] P2 Run `python3 src/check-container.py api|agents <image>` and `python3 -m unittest infra.tests.test_container_contract` with timings.
* [x] P3 Agents: run `serve` standby under hardened flags, `docker exec ... health`, confirm standby log, remove container.
* [x] P4 Api: run with seed dataset, `/healthz` 200, Docker health status, non-root user, remove container.
* [x] P5 Record commands and timings in the changes file; remove only the two local smoke tags and containers.
* [ ] P6 Independent review, clean commit with trailer. No push.

Details: see `.copilot-tracking/details/2026-11-13/521-local-container-smoke-1921-details.md`.

Boundaries: no ACR push, no Azure, no GitHub writes; the only repository writes are tracking artifacts. Tier: Focused.
