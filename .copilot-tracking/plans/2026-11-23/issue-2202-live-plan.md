# Plan: issue 2202 readings coverage tool (2026-11-23)

* [x] Phase 1: add `tools/demo_readings_coverage.py` (pure `coverage`, CLI over saved `/api/map?sensors=1` snapshots, bbox tile merge, dedupe by home id) and `tools/test_demo_readings_coverage.py`.
* [x] Phase 2: live run: tile the live map with `sensors=1`, merge, record the share of homes with readings and the consent checkbox on the current resident revision.
* [x] Phase 3: research note, README index, log entry, changes record with per-criterion table, review.

Tier: src is untouched (tools only); focused tier; no rpi-checks --all. Details: [details](../../details/2026-11-23/issue-2202-live-details.md).
