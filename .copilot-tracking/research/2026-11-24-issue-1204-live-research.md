# Research: issue 1204 tick criterion (2026-11-24)

Disposition: executed (reuse of 2026-11-18/19/23 notes plus fresh checks). Planning Readiness: Ready.

* Criterion 2 (next action, bounded closure progress, approvals, no global stop) is unticked.
* Main already has `tools/check-tick-log.py` with no-progress, recovery, closure-batch, closure-repeat, closure-progress, approval and global-stop rules, and `load_sqlite` reads the extended columns (13 tests OK).
* Fresh scan of local `~/.copilot/session-state/*/session.db`: three `tick_log` tables (216, 17, 4 rows), none with extended columns.
* Gap: the checker silently passes a window that lacks the extended columns, so a legacy window could be mistaken for proof of the closure and approval sub-claims. Missing check: a `--require-extended` mode that fails when a sqlite window lacks them, or a JSON window rows lack `closure_batch`.
* Runtime liveness over future ticks is not provable for the demo. No Azure surface; no browser proof applicable.
