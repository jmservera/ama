# Research: issue 1204, run r3 (2026-11-19)

Task: issue-1204-live-r3. Disposition: executed. Tier FOCUSED, synthetic demo, no push.

## Opening findings

* Five of six criteria are ticked; the unticked one is tick liveness (next action, bounded closure review, approval reconciliation, no global stop).
* `tools/check-tick-log.py` is on main. The r2 note said no real `tick_log` existed locally. A fresh read-only scan of `~/.copilot/session-state/*/session.db` finds three coordinator databases with `tick_log` (216, 17 and 4 rows). This contradicts r2 and is preserved here as a correction.
* Plan: export a bounded window read-only to `/tmp`, map columns to the checker schema, run the checker, and record what the schema can and cannot prove. Add an exporter tool with tests only if it is small.

## Evidence

* Window: coordinator session `74bd1fe9` `tick_log`, 216 ticks, 2026-11-16 08:29:52 to 2026-11-17 11:34:37 (read-only export, kept in /tmp, deleted afterwards; no secrets).
* Mapping: `ready_count`, `running_count`, `unknown_count` (as `unassessed`), `human_blocked_count`, `dep_blocked_count`; `action_taken` and `evidence` unchanged.
* `python3 tools/check-tick-log.py <export>` printed `216 ticks, 0 violations`, exit 0.
* Raw facts: 0 ticks with an empty action or evidence; 175 ticks had ready or unassessed work; 37 ticks had none; 36 action texts mention closure review; 3 mention approvals.
* Limits: this schema has no `closure_batch`, `approvals_granted/expired`, `reclassified` or `global_stop` columns, so the checker could not test batch size, repeats, approval reclassification or global-stop flags. Only no-progress and recovery rules were exercised. The other two databases (17 and 4 rows) store classifications as one text column and were not mapped.

Planning readiness: Ready. No source change needed; the checker exists and a code exporter for private, schema-varying session DBs is not justified.
