# Plan: issue 350 live (2026-11-20)

Details: `.copilot-tracking/details/2026-11-20-issue-350-live-details.md`. Critique: `.copilot-tracking/plans/2026-11-20-issue-350-live-critique.md`.

* [x] Phase 1 Research and live evidence (done)
* [ ] Phase 2 Failing test in `src/core/tests/test_sqlreads.py`: body owner_code changed behind the columns, reopen store, `view=mine` page equals in-memory filter
* [ ] Phase 3 Fix `SqlStore._migrate`: repair rows whose stage/area/wave/owner_code/closed/contractor columns disagree with the body
* [ ] Phase 4 Evidence note, changes record with per-criterion table, review, commit

Tier: FULL (src/core change), local commit; no rpi-checks --all, no redeploy.
