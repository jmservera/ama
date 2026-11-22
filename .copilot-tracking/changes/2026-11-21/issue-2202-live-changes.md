---
title: Issue 2202 changes
ms.date: 2026-11-21
---

## Per-criterion result

| Criterion | Status | Basis |
| --- | --- | --- |
| Images rebuilt from main and rolled | Proven | Running digests match local images tagged `62496349e8` |
| Revisions Running and Healthy | Proven | Revision list in the receipt note |
| Hardening enforced, rollback noted, agents difference explained | Proven for api, agents, simulator, receiver; unproven for resident | Resident has `ZF_CONTAINER_HARDENING` unset |
| Charts, gauges, consent checkbox, chat routing | Proven | Playwright screenshots; checkbox needed writer config (revision 19) |
| Half of homes with readings | Unproven | 10 of 443 (2.3 percent); per-device secret limit |
| Receipt and log entry | Proven | Receipt note and `docs/reference/log.md` entry |

Tier: FULL (src change). Only targeted tests, mypy and ruff ran; the coordinator owns the full gate. The logging change is not deployed (the registry is private).

## Changes

* Azure (resource group ama): resident app config for the consent writer (revision 0000019, rollback 0000018); agents app temporarily min 1 then back to 0 (revisions 2 and 3).
* Source: log the sensor consent write failure code in the resident handler, with a test (full tier, local commit only).
* Docs: research note, index row, log entry.

Per-criterion table follows when complete.
