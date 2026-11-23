# Research: issue 1204 live r2 (2026-11-23)

Refs #1204. Tier FOCUSED. Research disposition: executed. Planning Readiness: Ready.

Only unticked criterion: next action, bounded closure-review progress when capacity is free, approval reconciliation, no global stop.

Gap found in `tools/check-tick-log.py` on main d8f1aa5f6d:

* No rule enforces "bounded closure-review progress when capacity is free": a tick with unassessed items, free capacity and an empty `closure_batch` passes.
* `load_sqlite` reads only the legacy columns, so a session `tick_log` carrying `closure_batch`, approval, reclassification or stop columns is never checked for those rules.

Evidence note: docs/reference/research/issue-1204-live-r2-2026-11-23.md.
