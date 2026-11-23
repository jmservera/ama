---
title: Issue 184 live changes
ms.date: 2026-11-23
---

Tier: focused; no src change. Refs #184.

## Changes

* Added `docs/reference/research/issue-184-live-recheck-2026-11-23.md`.
* Added an index line in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.
* Evidence under `.copilot-tracking/evidence/2026-11-23/issue-184-live/`.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Proven (demo) | Sub-issues #185 to #189 all closed as completed |
| Simulator never connects to, discovers or represents installed real devices | Proven (demo); Hub identity registry not enumerated | Local rejection tests pass (170 tests, 2 skipped); live jobs succeed with `SYN-` ids only; CLI lacks data-plane access (401002) |
| No device key or connection string in source, logs or telemetry | Source and logs proven; live message bodies unproven | Repository scan test passes; 0 matches in 260,243 live log rows over 6 hours; Event Hubs bodies not read |

Validation: IoT suites run from `src/api`; link and diff review of the docs.
