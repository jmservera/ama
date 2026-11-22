---
title: Issue 2201 live6 details
ms.date: 2026-11-22
---

## Phase 1

`az containerapp job execution list -g ama -n <job>`; `az monitor log-analytics query` on `ContainerAppConsoleLogs` (column `ContainerGroupName`).

## Phase 2

`issue-2201-live6/probe_readings.py` (copy of the live3 probe) against `/api/map` and five case sensor endpoints.

## Phase 3

New note `docs/reference/research/issue-2201-live-receiver-streak-2026-11-22.md`; one index paragraph in `docs/reference/README.md`; one entry appended to `docs/reference/log.md`.
