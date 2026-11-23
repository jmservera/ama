---
title: Issue 2257 live changes (run 084412Z)
ms.date: 2026-11-23
---

Classification: FULL tier by rule (src change); the coordinator owns the gate. No `rpi-checks.py --all` was run here.

## Changes

* `src/api/src/zava_forward/api/web/app.js`: the map panel shows a native "Try the map again" button after a failed draw (hidden otherwise) and schedules one automatic redraw (4 s) for network failures with no HTTP status; the timer is cleared on dispose and on every new draw; HTTP errors are never auto-retried. The failure notice names the control.
* `src/api/tests/test_workspace_scripts.py`: `test_map_failure_offers_a_visible_retry_and_one_bounded_redraw` (fails on the previous `app.js`, passes now).
* `docs/reference/research/issue-2257-retry-control-2026-11-23/`: live probe and its result (8 fresh sign-ins on revision 0000055).

## Local checks

* `test_workspace_scripts`, `test_accessibility_baseline`, `test_content_standard`, `test_app_js_notices_content`: 67 tests OK.
* `python3 -m mypy` in `src/api`: no issues; ruff check and format clean on the changed test; `node --check app.js` OK.
* Not run: browser check of the new button against a running server; hosted CI; the full gate.

## Process note

An early `app.js` edit was made before the implement-start witness; it was reverted, the artifacts were written, and the same patch was re-applied after the witness. The witness recorded a qualification about this.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Map recovers from a dropped connection without a reload | Proven live earlier on 0000054 (`issue-2257-live-2026-11-23/recovery-proof-result.json`); the bounded redraw is unit tested only | test above, earlier note |
| Visible retry control exists | Proven in source and unit test; unproven live (not deployed, no estate change) | test above |
| Bounded retry | Proven by test: 2 read retries, one 4 s redraw, none for HTTP errors | test above, `test_map_read_recovers_from_a_dropped_connection` |
| Cause found | Partly: dropped connection and overlay transaction 500 evidenced; the live `ProgrammingError` message and origin are unproven | research note |
| Fresh-session failures gone | Weakly supported: 8 of 8 loaded on 0000055, 0 error log lines; not proof for an intermittent fault | `probe-result-085002.json` |
| Billing, DPO or Legal, person-run assistive-technology testing | Not needed for the demo (owner decision 2026-11-18) | brief |
| Azure estate unchanged | Proven: read-only `az` queries and browser probes only | this record |
