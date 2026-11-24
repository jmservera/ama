---
title: Issue 2304 live details (2026-11-24)
ms.date: 2026-11-24
---

# Details

* Cache key: (lower email, role, oid, tid, period). Value: (monotonic time, result). A hit inside the TTL is returned as a deep copy without SQL.
* Job: daemon thread running `_forecast_compute` with its own connection; result or exception stored on a small job object guarded by a lock; one job per key at a time; waiters use `Event.wait(remaining)`.
* Errors: `ForecastTimeout` after the client wait; job exceptions re-raised to the waiting request once (PermissionError, ValueError and ForecastTimeout keep their API mapping); a failed job is never cached.
* Limit: a staff change (revocation) takes effect within the TTL for a repeat read of a precomputed counts-only forecast. Recorded in the evidence note.
* Tests in `src/api/tests/test_assistants.py::ForecastStatements`.
