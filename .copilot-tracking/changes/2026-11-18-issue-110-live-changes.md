---
title: Changes for issue 110 live proof
ms.date: 2026-11-18
---

Refs #110. Source changes: none. Tier: focused (docs/evidence only; no src, SQL, infra or deployment change). Added `docs/reference/research/issue-110-live-iot-identity-evidence-2026-11-18.md`, the KB index entry and a log entry. Live resources created and removed (job, two role assignments, three devices); verified afterwards.

| Criterion | Status | Evidence |
| --- | --- | --- |
| C1 Distinct IoT Hub identity per device with schema version and stable reading ID | Proven for the demo (SAS over HTTPS, Event Hub read-back); production X.509 receiver unproven | docs/reference/research/issue-110-live-iot-identity-evidence-2026-11-18.md |
| C2 Idempotent append on sensor ID plus reading ID | Already ticked; not re-proven | Issue |
| C3 DQ handling visible | Already ticked; not re-proven | Issue |
| C4 No public unauthenticated ingestion endpoint | Already ticked; hub public access Disabled observed | Issue |
| C5 No key in source or telemetry | Already ticked; probe output leak check clean | Issue |

Checks run: document diff and link review; no unit tests apply. `rpi-checks.py --all` not run.
