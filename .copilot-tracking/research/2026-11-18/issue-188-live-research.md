---
title: Issue 188 live research (opening)
ms.date: 2026-11-18
---

Opening note. Goal: prove live+backfill series queryable together per home, no discontinuity, idempotent re-run on live Azure SQL (demo, desktop). Disposition: executed. Evidence is recorded in docs/reference/research/ once gathered.

## Findings (2026-11-18)

* Disposition: executed. Planning Readiness: Ready.
* Topology: private SQL `sql-cutover-test-rzsrg`; IoT Hub `iot-cutover-test-rzsrg` routed to Event Hub `sensor-readings` on Basic namespace `evhns-cutover-test-demo` (only `$Default`).
* The production receiver needs X.509, `api-consumer` and a Standard namespace, so the demo uses SAS devices and a `$Default` reader (precedent commit `b92745b87`, Refs #1818).
* The indoor backfill in SQL belongs to a home with no live stream and a different schema; the verifier refuses mixed schemas. Use a same-schema weather backfill.
* Ledger table: throwaway synthetic rows cannot be deleted.
* Outcome evidence: [docs/reference/research/issue-188-live-backfill-evidence-2026-11-18.md](../../../docs/reference/research/issue-188-live-backfill-evidence-2026-11-18.md).
