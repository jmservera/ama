---
title: Issue 184 live changes (run b)
ms.date: 2026-11-23
---

Tier: focused; no src change. Refs #184.

## Changes

* Add `docs/reference/research/issue-184-live-bodyread-2026-11-23.md`.
* Add an index line in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.
* Evidence under `.copilot-tracking/evidence/2026-11-23/issue-184-live-b/`.

## Azure actions

One role assignment (Azure Event Hubs Data Receiver, user principal, scope `sensor-readings`) was created and deleted; 0 user assignments remain. No other resource was created or changed.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Proven (demo), carried from the earlier run | Sub-issues #185 to #189 closed as completed; not re-run here |
| Simulator never connects to, discovers or represents installed real devices | Proven (demo), carried; registry not enumerated | Rejection tests and `SYN-` only live ids per the earlier note; simulator executions still Succeeded at 14:15 UTC |
| No device key or connection string in source, logs or telemetry | Source and logs proven (earlier note); live message bodies UNPROVEN | Body read attempted with a temporary data-receiver role; 0 events received because the namespace has public network access Disabled and local auth disabled, so the CLI host cannot connect. Opening the network would be a production change not authorised |

## Validation

* `test_iot_credential_hygiene` and `test_iot_stream`: 60 tests OK from `src/api`.
* Diff scanned for secret patterns: none. Relative links resolve.
