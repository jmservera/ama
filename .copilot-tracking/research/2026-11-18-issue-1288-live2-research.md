# Research: issue 1288 live demo re-verification, run 2 (2026-11-18)

Refs #1288. Demo, desktop only, docs and evidence only (no src change, FOCUSED tier). Research disposition: reused plus delta. Planning Readiness: Ready.

## Prior work reused

* Merged PR 1971 (`docs/reference/research/issue-1288-live-quality-sensor-evidence-2026-11-18.md`) already holds the per-criterion record, local tests (497 OK), browser check (33 passed) and SQL runs. Merged source PRs 1331, 1642, 1696, 1745 delivered the feature. Open worktree `issue-1288-20261117T1805` holds only older tracking files.
* Not reopened: criteria 1, 2 and 9 (ticked). Open: 3 to 8.

## Delta to research live

* Whether the retained readings are now fresh (an earlier run saw stale) and whether the release gate has changed. Both read-only.

## Live findings (probe `.copilot-tracking/evidence/2026-11-18/issue-1288-live2/live_probe.json`, 13:08Z)

* Revision `ca-cutover-test-demo-api--0000031`, same image digest as run 1. Role `Retrofit Programme Manager`; only ZF-2025-0031 is in scope (11 others 403).
* `/sensors`: `retained-reading-view-v2`, 12 readings, newest `LIVE-S7XBQ3HG3P5-20261118T1300Z` at 13:00Z, `freshness: fresh` (age 498 s), `calibrated: false`, retrofit context unavailable with an explicit text. Another demo worker's job (`job-demo-live7`, tagged issue 1818) is writing retained readings; it is not a #1288 admitted run.
* Release gate unchanged: `/api/assistants/forecast` `proactive: false`, `call_allowance: 0`; invoke returns 202, `envelope: null`, `release: null`, reason "Operator authority, finite allowance and expiry are required." RAI metrics `invocation` 6 to 7, `tokens` 0.
* Probe note: the script invokes whenever a case is in scope, so it wrote one more retained denial proposal (an unintended second write, same effect as run 1).
* The `live-case-*.png` screenshots show the case header, not the sensor panel (tab query not honoured by the route).
