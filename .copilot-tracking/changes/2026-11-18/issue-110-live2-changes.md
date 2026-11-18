---
title: Changes for issue 110 live2
ms.date: 2026-11-18
---

Refs #110. No `src/` change; tier FOCUSED (documentation plus live evidence).

## Log

* 13:53Z implement-start.
* 13:55Z temp roles (IoT Hub Registry Contributor on hub, Event Hubs Data Receiver on namespace) granted to `id-cutover-test-api`; job `job-110-live2` created (first creation attempts failed on CLI arg parsing, fixed via YAML command).
* 13:56Z job execution Succeeded: `homes=3 sent=6 failed=0 stored=6`, 21.6 s.
* 13:59Z job and both roles deleted; hub stats 0 devices; roles back to the 5 prior; hub public access Disabled.
* Added `docs/reference/research/issue-110-live2-iot-sql-evidence-2026-11-18.md`, index paragraph and log entry.
* Raw job output not retained in the repository; the figures below are the observed read-backs recorded in the note.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| C1 Distinct Hub identity with schema version and stable reading ID | Observed; raw output not retained | Earlier #1941 note (identities, schema, IDs) plus this run (3 devices, 6 sent, 6 stored in SQL) |
| C2 Idempotent append | Not re-proven (ticked) | Merged tests |
| C3 Bad-input handling visible | Not re-proven (ticked) | Merged tests |
| C4 No public unauthenticated endpoint | Consistent, not re-proven (ticked) | Hub public access Disabled |
| C5 No key in source or telemetry | Consistent, not re-proven (ticked) | No key in job output |

Unproven: row-level SQL read-back, production X.509, per-device detail in this run's own output.

## Validation

Documentation link and diff review only; no tests apply (no source change). `rpi-checks.py --all` not run.
