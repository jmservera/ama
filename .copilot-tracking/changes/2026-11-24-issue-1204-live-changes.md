# Changes: issue 1204 live (2026-11-24)

Tier: FOCUSED (tools only, no src, no Azure).

* `tools/check-tick-log.py`: `check_ticks(rows, require_extended=False)` and CLI `--require-extended`; rows missing closure_batch, approvals_granted, approvals_expired, reclassified or global_stop yield a `schema` violation.
* `tools/test_check_tick_log.py`: one test (legacy row rejected only in strict mode; full row accepted).
* `docs/reference/research/issue-1204-require-extended-live-2026-11-24.md`: evidence note.

Validation: 25 tests OK; ruff check/format clean; real 216-tick window: default 0 violations, strict 216 violations (expected, legacy schema). No divergences.

## Per-criterion table (issue 1204)

| Criterion | Status |
| --- | --- |
| 1 Fresh classification before idle or stop | Proven (ticked, not re-audited) |
| 2 Next action, bounded closure progress, approvals, no global stop | Unproven at runtime: rules and tests proven; next-action proven on 216 legacy ticks; no real window with extended fields; future liveness not provable for the demo |
| 3 One question, approved actions routed | Proven (ticked) |
| 4 Prompts active, obsolete schedules stopped | Proven (ticked) |
| 5 Handoffs and cleanup | Proven (ticked) |
| 6 Dated RPI artifacts and checks | Proven (ticked) |
