---
title: Issue 2202 live research
ms.date: 2026-11-21
---

## Status

Research disposition: executed (2026-11-21). Planning Readiness: Ready.

## Evidence

* Estate read-back at 23:0x UTC: api revision 43 (same digest as 42, env-only revision by another worker), resident 18 then 19, agents 1 (ScaledToZero), simulator and receiver jobs on the api digest `60b1d026...`, all matching local images tagged `62496349e8`. Main has only src/README.md changed since `62496349e8`.
* API, simulator, receiver, agents: `ZF_CONTAINER_HARDENING=enforced`; resident unset (the resident entrypoint honours it, the setting was never applied).
* Replica receipts via `az containerapp exec`: api and a temporary agents replica run as uid 10001, CapInh/Prm/Eff/Amb 0, NoNewPrivs 1, hardening enforced; resident uid 10001, caps empty, NoNewPrivs 1, hardening None.
* Resident checkbox (#2192): absent on rev 18 and on rev 19 until `ZF_DEMO_SENSOR_CONSENT` plus a writer identity were configured; then rendered. First POST failed 503 after 18 s because the Azure SQL write lock `zavaforward_write` (15 s timeout) was held; a repeat attempt succeeded and the state was restored. The handler swallows the exception with no log line.
* Chat routing: resident chat routed "Documents helper" and "Safety route helper"; employee chat showed "Routed to the Quality evidence agent".
* Charts/gauges: sensors tab SVG chart with two series and axes, map home card with two `meter` gauges (7.2 degC, 93.4 %RH).
* Cohort: 10 of 443 homes fresh (2.3 percent); 20-home cohort.

## Follow-ups

* Log the consent write failure class (defect found, fix planned).
* Half of homes with readings stays unproven (per-device secrets).
