---
applyTo: '.copilot-tracking/changes/2026-11-18/issue-216-live3-changes.md'
---
# Plan: issue 216 live3

* [x] Phase 1: write authorization-live3.json (30 calls, 60,000 tokens, expiry 2026-11-19T00:00Z).
* [x] Phase 2: run the 20 non-refusal prompts in three throwaway-server batches (7, 7, 6) and the 10 refusal prompts in a fourth batch inside ca-cutover-test-demo-api; keep raw output.
* [x] Phase 3: rescore with scores_all (score_inner.py), rerun gate unit tests, write research note and per-criterion table.
* Tier FOCUSED; no src change; no rpi-checks --all.
Details: .copilot-tracking/details/2026-11-18/issue-216-live3-details.md
