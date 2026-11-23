# Issue 2257 r6 changes

Tier: FULL (src changed); only targeted tests and ruff run here, the coordinator runs gates.

## Files

* `src/api/src/zava_forward/api/web/app.js`: `api()` sets `error.gateway` for a non-JSON 500/502/503/504 read; the map's one automatic redraw now also runs for it.
* `src/api/tests/test_workspace_scripts.py`: extended map retry test.
* `docs/reference/research/issue-2257-live-r6-2026-11-23.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Cause logged (lock tag plus SQLSTATE) | Proven in code and test (r5); unproven live (not deployed) | r5 note |
| Map retries or recovers without reload | Proven live in r2 for dropped connections; gateway-failure redraw proven by unit test only, unproven live (not deployed) | r2 note, test_workspace_scripts |
| Fresh-session failures gone | Unproven (a sample cannot show a zero rate) | r2, r3 notes |
| Billing, DPO or Legal, assistive-technology testing | Not needed for the demo | owner decision 2026-11-18 |
