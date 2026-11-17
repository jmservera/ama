# #176 Cycle 1 correction research (2026-11-14)

Refs #176. Source: independent review of `8d0c3396d` (request_changes).

* `resident_preview_fixture.build()` read the wall clock (`date.today`, `datetime.now`, `uuid4`) through the store, wrote none of seed, version or generator_revision to `dataset.json`.
* `sensor_backfill.write(..., fault_rates=...)` wrote `truth/manifest.json` without `generator_revision`.
* The store's capacity review must be within 7 days of the real clock, so a pinned fixture date goes stale for a live preview. Live callers must pass `as_of` explicitly.
* Planning readiness: Ready. Research disposition: executed.
