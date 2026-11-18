---
title: Plan for issue 110 live IoT Hub to SQL rerun
ms.date: 2026-11-18
---

Refs #110. Tier: FOCUSED (documentation and live evidence only; no `src/` change).

* [x] P1 Probe: throwaway job `job-110-live2` with the demo API image, check `zava_forward.api.live_demo` exists.
* [x] P2 Grant temporary roles (IoT Hub Registry Contributor on the hub, Event Hubs Data Receiver on the namespace) to `id-cutover-test-api`.
* [x] P3 Run the bounded send: homes ZF-2025-0029 to 0031, 2 slots, 6 messages, seed 110, cleanup on. Retain raw output outside the repo.
* [x] P4 Independent read-back: hub device count 0 afterwards, roles and job removed, public access still Disabled.
* [x] P5 Write the evidence note `docs/reference/research/issue-110-live2-iot-sql-evidence-2026-11-18.md`, index and log entries.
* [x] P6 Commit locally with trailers; no push.

Stop rules: any need to change source, SQL schema or the hub network setting stops the run and reports FULL tier. Cost: 6 messages against a 200 message demo cap and a minutes-long job; no measurable spend.
