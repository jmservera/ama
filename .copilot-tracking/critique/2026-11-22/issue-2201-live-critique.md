---
title: Issue 2201 live critique, 2026-11-22
---

Verdict: approve with direct dispositions. Executed once.

* Risk: Running execution 05:00 may fail. Disposition: record the real outcome; do not claim three successes unless 04:00, 04:30 and 05:00 are all Succeeded. If it fails, capture the replica stream or execution detail and diagnose.
* Risk: claiming the hub-to-map hop without a fresh reading. Disposition: re-read /api/map with Playwright or the staff API at runtime, credentials never printed.
* Risk: "scheduled" runs. All three are cron-named executions (29922000, 29922030, 29922060), not manual starts.
* No source change planned, so the Tier is focused; no gate run.
