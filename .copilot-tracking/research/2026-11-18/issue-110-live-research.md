---
title: Research for issue 110 live IoT Hub identity proof
ms.date: 2026-11-18
---

Refs #110. Scope: synthetic desktop demo, hub `iot-cutover-test-rzsrg` (B1, private only), route `route-demo-sensor` to Event Hub `sensor-readings`, namespace `evhns-cutover-test-demo`. Hub-generated symmetric keys (owner decision, #185).

Unticked criteria: C1 only ("Each simulated device is a distinct IoT Hub identity with schema version and stable reading ID"). C2 to C5 are ticked on the issue and are not re-proven.

Disposition: executed. Plan: throwaway Container Apps job creates N SAS devices, sends generator readings (`schema_version`, `reading_id`, `message_id = reading_id`), reads them back from Event Hub with the hub-stamped device id, checks distinctness, deletes devices and job. Prior art: #185 and #188 notes. No source changes.
