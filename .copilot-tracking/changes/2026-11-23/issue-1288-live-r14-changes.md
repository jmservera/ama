---
title: Issue 1288 r14 changes
date: 2026-11-23
---

Refs #1288. Status: complete. Tier FULL (src change); the change only downgrades a flag, no gate, permission, release or security semantics changed. `rpi-checks.py --all` not run (coordinator owns the gate); no push; Azure not touched, nothing to delete.

## Changes

* `src/core/src/zava_forward/core/assistants.py`: `review_flag` reports `implausible-readings` when a cited reading is impossible in the current successful capture.
* `src/api/tests/test_quality_sensor_grounding.py`: `test_cited_reading_corrected_to_impossible_after_capture_downgrades_the_flag` (failed first).
* `docs/reference/research/issue-1288-live-r14-quality-sensor-evidence-2026-11-23.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* The malformed r13 session state file (duplicate keys) was rewritten for r14. One premature source edit was reverted before the implement-start witness and reapplied after it.

## Validation

* `test_quality_sensor_grounding`, `test_quality_sensors_correlation`, `test_quality_sensors`: 229 run, OK, 94 skipped (SQL Server, browser). core assistants tests OK.
* ruff check clean; mypy src/api clean; src/core mypy 3 errors identical to base. `ruff format --check` flags `assistants.py` on base (existing).
* Not run: hosted CI, browser/SQL-gated cases, live probe.

## Per-criterion table (issue 1288, unticked)

| Criterion | Status | Basis |
| --- | --- | --- |
| 3 identical IDs and values consumed | Proven locally (mock provider); unproven live | Correlation tests; no live model request |
| 4 release-admitted proactive flag | Unproven | No approved release record, owner not appointed (OQ-017); human approval, not code |
| 5 finding, IDs, time, model, unapproved status visible | Proven locally; unproven live | Flag tests; no live model output |
| 6 explicit unavailable states and human route | Proven locally, now including post-capture impossible readings; live per r12 | New test |
| 7 focused tests correlate UI and snapshot | Proven as local engineering evidence | 229 tests OK; SQL/browser cases skipped |
| 8 finite live walkthrough with real model | Unproven | Blocked by criterion 4; no mock or fabricated release |

No tick or closure is claimed. Independent review and hosted CI outstanding.
