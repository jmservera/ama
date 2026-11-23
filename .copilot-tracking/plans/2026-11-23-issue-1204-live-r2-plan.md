# Plan: issue 1204 live r2 (2026-11-23)

Refs #1204. Tier FOCUSED (non-gate tooling in `tools/`, no `src/` change).

1. Add rule `closure-progress` to `tools/check-tick-log.py`: a row that carries `closure_batch` (extended schema) with `unassessed > 0`, `running < 8` and an empty batch is flagged.
2. Make `load_sqlite` read optional `closure_batch`, `approvals_granted`, `approvals_expired`, `reclassified`, `global_stop` columns (JSON text) when present.
3. Add focused tests; run `python3 -m unittest test_check_tick_log` in `tools/` and ruff.
4. Evidence note and per-criterion table.

## Critique (executed once)

* Legacy rows lack `closure_batch`; enforcing the rule on them would flag the 216 real ticks. Decision: enforce only when the key is present. Accepted.
* Optional columns must not break legacy databases. Decision: inspect `PRAGMA table_info`. Accepted.
* Verdict: proceed, no open decision.
