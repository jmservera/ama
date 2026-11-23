# Changes: live smoke 0000055 / 0000027 (issue 2237)

Refs #2237. Tier focused: no `src/` change, `rpi-checks.py --all` not run. Planned: probes, results and screenshots under `docs/reference/research/issue-2237-smoke-0055-live-2026-11-23/`, evidence note, README index row, log entry. The per-criterion table is added at implement-done.

## Changes

* New note `docs/reference/research/issue-2237-smoke-0055-live-2026-11-23.md` and folder of probes, JSON results, revision snapshots, system-log summary and screenshots; README index row; log entry. No `src/` change, no Azure change.

## Per-criterion table (issue 2237, plus 2257 and 2244 as named in the goal)

| Criterion | Status | Evidence |
| --- | --- | --- |
| 2237 re-prove 200 live | Proven on 0000055 (16 of 16 calls 200) | note, `probe-employee-result.json` |
| 2237 reproduce, cause, fix with regression test | Unproven in this run (not repeated; earlier note holds it; fix is local only) | `issue-2237-live-cause-and-fix-2026-11-23.md` |
| 2237 chat thread POST | Proven 200 (a request-API 403 was a probe artefact) | note |
| 2257 map loads with sensor overlay | Proven for one session (443 markers); intermittent failure not reproduced or explained | `employee-map.png` |
| Resident chart loads | Proven (stale data, no forecast, as designed) | `resident-sensors-chart.png` |
| 2244 start-up healthy | Partly: Healthy and `/healthz` 200, but readiness probe timeouts 03:54 to 03:57 UTC; fix itself unproven | `system-log-summary.txt` |

Validation: documentation and diff review only; no tests apply. Nothing ticked on any issue.
