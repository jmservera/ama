---
title: Issue 2202 live receipt for the demo rollout and owner checks
description: Dated live readbacks, replica hardening receipts and Playwright checks on the deployed synthetic demo, with a per-criterion proven or unproven table for issue 2202
author: AMA RPI agent
ms.date: 2026-11-21
ms.topic: reference
keywords:
  - issue 2202
  - live demo
  - container hardening
estimated_reading_time: 6
---

Refs #2202. Synthetic desktop demo, resource group `ama`, 2026-11-21 22:50 to 23:40 UTC, under the owner decisions of 2026-11-18. Sign-in values were read at run time from the owner files and appear in no retained output (each probe asserts this before writing). Probes: [probe_staff.py](./issue-2202-live-2026-11-21/probe_staff.py), [probe_staff_chat.py](./issue-2202-live-2026-11-21/probe_staff_chat.py) and [probe_resident.py](./issue-2202-live-2026-11-21/probe_resident.py), with JSON results and [screenshots](./issue-2202-live-2026-11-21/screens/) beside them.

## What was deployed before this run

* Images were built from main `62496349e8` and pushed in the registry window recorded in the [log](../log.md). Local tags `62496349e8` carry the digests now running: api, simulator and receiver `sha256:60b1d026...`, resident `sha256:12383ee4...`, agents `sha256:59ea12f4...`. Main has since changed only `src/README.md` under `src/` and `infra/`, so these images are the current source.
* Revisions: `ca-cutover-test-demo-api--0000043` (Healthy, 100 percent; the same digest as `0000042`, an environment-only revision made by another session at 22:58), `ca-resident-demo--0000019` (Healthy), `ca-cutover-test-demo-agents` (Healthy, queue scaled).
* `ZF_CONTAINER_HARDENING=enforced` on the api, agents, `job-live-simulator` and `job-live-receiver`. It was unset on `ca-resident-demo` and stays unset (the resident entrypoint honours it, but it was never applied).

## Changes made in this run

* `ca-resident-demo` revision `0000019` (rollback: revision `0000018`, or remove the five `ZF_DEMO_SENSOR_CONSENT*` variables): attached the existing `id-cutover-test-api` identity and set `ZF_DEMO_SENSOR_CONSENT=1` plus `ZF_DEMO_SENSOR_CONSENT_SQL_AUTH`, `_CLIENT_ID`, `_SERVER` and `_DATABASE`. Without it the page says "You cannot change this choice on this page right now" (checkbox absent). This is a demo exception: the design asks for a dedicated sensor-writing principal, and I reused the api identity because I cannot create SQL users (the SQL admin is `id-cutover-test-init`). The read-only showcase principal is untouched.
* `ca-cutover-test-demo-agents`: min replicas raised to 1 for a replica receipt (revision `0000002`), then set back to 0 (revision `0000003`, scales to zero after the queue cooldown).
* Source: the resident consent handler logged nothing when the write failed; it now prints the exception class and code (a test is added). Not deployed.
* No Azure resource was created, so nothing needed deleting.

## Replica receipts (`az containerapp exec`, `/proc/1/status`)

| App | Revision | Uid | CapInh, CapPrm, CapEff, CapAmb | NoNewPrivs | `ZF_CONTAINER_HARDENING` |
| --- | --- | --- | --- | --- | --- |
| api | `0000043` | 10001 | all 0 | 1 | enforced |
| agents (temporary replica) | `0000002` | 10001 | all 0 | 1 | enforced; console "standby, queue consumption is off" |
| resident | `0000019` | 10001 | CapInh `a80425fb`, others 0 | 1 | unset |

The agents app differs because it scales to zero on an empty queue, so a replica only exists while tasks are pending; a receipt needs a temporary replica. The resident replica is not under the guard, and its inheritable set is non-zero.

## Owner demo checks on the deployed hosts

| Check | Result |
| --- | --- |
| Sensor chart (#2193) | Home sensors tab for `ZF-2025-0031`: one SVG with two series and a second axis, plus the table ([screenshot](./issue-2202-live-2026-11-21/screens/home-sensor-chart.png)) |
| Map gauges (#2193) | Home card for `ZF-2025-0029` shows two `meter` gauges: 7.2 degC on 0 to 40 and 93.4 %RH on 0 to 100 ([screenshot](./issue-2202-live-2026-11-21/screens/map-gauges.png)) |
| Resident consent checkbox (#2192) | Absent on revision `0000018`. On `0000019` it renders with the label "Share my home sensor readings with Zava North Homes staff". A click withdrew consent (status "Staff cannot see your readings. New readings are not stored for your home.") and a second click restored it ("Staff can see your readings."). The final state is granted, as found. The first click failed with 503 after 18 s because the SQL write lock (15 s timeout) was held; the next two writes succeeded in about 3 s. Root cause of the long hold is not established ([granted](./issue-2202-live-2026-11-21/screens/resident-consent-granted.png), [declined](./issue-2202-live-2026-11-21/screens/resident-consent-declined.png)) |
| Chat routing (#2195), resident | "Which documents are missing" answered "Routed to the Documents helper"; a damp and mould question answered "Routed to the Safety route helper" ([screenshot](./issue-2202-live-2026-11-21/screens/resident-chat-routing.png)) |
| Chat routing (#2195), employee | A quality and sensor question showed "Routed to the Quality evidence agent. The question is about quality checks and inspection evidence." ([screenshot](./issue-2202-live-2026-11-21/screens/employee-chat-routing.png)) |
| Half of homes with readings (#2191) | `/api/map`: 443 homes, 10 fresh, 90 `no-readings`, 343 `not-loaded`; 2.3 percent have readings. Not met |

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| API, resident, simulator and receiver images rebuilt from main and rolled | Proven | Digests running match local images tagged `62496349e8`; no `src/` change on main since. Importer and orchestrator jobs (not in the criterion) are older |
| Revisions Running and Healthy | Proven | Revision list above |
| `ZF_CONTAINER_HARDENING` enforced with rollback noted; agents difference explained | Proven for api, agents, simulator, receiver; unproven for resident | Receipts above; rollback is to set the variable to `off` or return to the earlier revision; agents explained by scale to zero; resident unset |
| Owner demo checks: charts, gauges, consent checkbox, chat routing | Proven | Table above (the checkbox needed the writer configuration added in this run) |
| Owner demo check: half of homes with readings | Unproven | 10 of 443 (2.3 percent); the [2191 note](./issue-2191-live-coverage-2026-11-21.md) explains the per-device secret limit |
| Live receipt and `docs/reference/log.md` entry | Proven | This note and the log entry of 2026-11-21 |

## Not proven or open

* Half of homes with readings.
* Hardening on `ca-resident-demo`; setting it needs a deliberate rollout and a receipt.
* Why the SQL write lock `zavaforward_write` was held longer than 15 s at one point (the receiver and simulator share it); a repeat check after the first failure passed.
* The employee chat showed "Monitoring consent is unknown" for `ZF-2025-0031` while the sensors tab showed readings for the same case; I did not investigate.
