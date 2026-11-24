# Plan: issue 2320 briefing without write lock on repeat reads

Tier FULL (src change); the coordinator runs the gate, not this worker. Details: `.copilot-tracking/details/2026-11-24/issue-2320-live-details.md`.

* [x] 1. Add `release_denial` (pure read) to `Store` and `SqlStore`; `release_block` uses it and still audits.
* [x] 2. Add `_briefing_denial_unchanged` and use it in the `briefing` cache hit.
* [x] 3. Extend the existing denied-briefing test to assert zero `BEGIN IMMEDIATE` and no audit on the repeat GET.
* [ ] 4. Run targeted tests, ruff, mypy.
* [ ] 5. Evidence note with per-criterion table; commit.
