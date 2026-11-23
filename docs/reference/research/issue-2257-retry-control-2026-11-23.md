---
title: Issue 2257 map retry control and live re-probe (2026-11-23)
ms.date: 2026-11-23
---

Evidence for #2257 on API revision 0000055 (Healthy, 100 percent traffic). Retrieved 2026-11-23, desktop demo, synthetic data.

## Findings

* The map draw showed "Map unavailable" with no control once the bounded read retries (2 for a dropped connection, 3 for a gateway failure) were spent; the panel stayed empty until a reload.
* Change: a visible "Try the map again" button and one bounded automatic redraw (4 s) for network failures. HTTP errors, including a JSON 500, are shown and not auto-retried. Test: `test_map_failure_offers_a_visible_retry_and_one_bounded_redraw` in `src/api/tests/test_workspace_scripts.py`.
* Live re-probe, 8 fresh sign-ins: 8 of 8 loaded 443 markers in 11.9 to 32.6 s ([probe-result-085002.json](./issue-2257-retry-control-2026-11-23/probe-result-085002.json), probe [live_probe.py](./issue-2257-retry-control-2026-11-23/live_probe.py)). No `ProgrammingError` lines in the last 300 console log lines.

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| The map retries or recovers without a reload | Dropped connection proven live on 0000054 earlier ([issue-2257-live-2026-11-23.md](./issue-2257-live-2026-11-23.md)); button and bounded redraw proven by unit test only, not deployed | unit test |
| The cause is found | Partly: dropped connection and overlay transaction 500 are evidenced; the live `ProgrammingError` message and origin are unproven | earlier note, console log |
| Fresh-session failures are gone | 8 of 8 loaded on 0000055; too small a sample to prove an intermittent fault gone | probe result |
| Billing, DPO or Legal, assistive-technology testing | Not needed for the demo (owner decision 2026-11-18) | owner decision |

The Azure estate was not changed.
