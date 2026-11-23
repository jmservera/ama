---
title: Issue 2257 live changes
ms.date: 2026-11-23
---

Classification: FULL tier by rule (src change); coordinator owns the gate. Local focused checks recorded below once run.

## Changes

* `src/core/src/zava_forward/core/assistants.py`: `map_sensors` degrades to the `unavailable` sensor state when its transaction fails.
* `src/api/tests/test_map_sensors.py`: regression test.
* Research note `docs/reference/research/issue-2257-live-2026-11-23.md` and probe scripts/results.

Local checks: `test_map_sensors` 17 tests OK; mypy `src/api` clean; ruff check and format clean on changed files; `src/core` mypy shows 3 errors in untouched files (telemetry, device_provision), none in `assistants.py`.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Map recovers from a dropped connection without reload | Proven live on 0000054 | docs/reference/research/issue-2257-live-2026-11-23/recovery-proof-result.json |
| Map recovers from a server 500 | Unproven: hardening unit tested, not deployed | test_map_sensors |
| Cause found | Partly: server ProgrammingError, message and origin unknown | console log, research note |
| Fresh-session failures gone | Disproven: 1 of 8 failed on 0000054 | probe-result-014731.json |
| Billing, DPO/Legal, person-run AT | Not needed for the demo (owner decision 2026-11-18) | brief |
| Azure estate unchanged | Proven: read-only az queries and browser probes only | this record |
