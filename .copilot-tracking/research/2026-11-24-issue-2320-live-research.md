# Research: issue 2320 GET /api/briefing 503 sql-write-lock-busy (2026-11-24)

Disposition: executed. Planning Readiness: Ready. Evidence note: `docs/reference/research/issue-2320-live-2026-11-24.md`.

## Findings

* `Store.briefing` serves a cached result only when `release_current(...)` accepts the cached release. A template result held by a release denial has `release=None`, so with AI configured the cache never hits.
* Each miss on SqlStore takes the SQL write lock three times: `release_block` audits `ai_release_denied`, `add_record` saves the comparison record, and `briefing` audits `ai_run`. `mssqlstore.BEGIN` waits 15 s per lock, matching the 17 to 43 s waits.
* Live 2026-11-24 09:26 to 09:30 UTC: other GETs (`/api/retention`, simulation quality, sensors) also returned 503 write-lock-busy, so contention is system-wide; briefing amplifies it by writing on every read.
* Fix scope: read-only denial predicate and a cache hit for a held template while the same denial holds.

## Follow-ups

1. Owner deploys and re-measures.
2. Audit other GETs that write on read (`/api/retention`, simulation quality).
