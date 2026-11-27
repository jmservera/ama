# Changes: issue 1204 live (2026-11-27)

Refs #1204. Tier FOCUSED: tools test and docs only; no src, workflow, Azure, or browser change. Classification basis: no permission, pin, package, secret, deployment or gate-semantics change.

## Changes

* tools/test_check_coordinator_handoff.py: six flaky wall-clock bounds (0.1 to 0.5 s) replaced by `LINEAR_TIME_BUDGET_S = 2.0`.
* docs/reference/research/issue-1204-extended-window-recheck-2026-11-27.md: evidence note.
* docs/reference/README.md index row and docs/reference/log.md entry.

## Validation

* Before: tools tests failed in 3 of 5 runs at load average 8 (25 tests).
* After: 25 tests OK in 5 of 5 runs; ruff check and ruff format --isolated --line-length 100 --check clean.
* Real 216-tick window: default 0 violations, `--require-extended` 216 violations (temporary copy deleted).
* Not run: hosted CI, independent exact-head review, rpi-checks (coordinator owns gates).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Fresh classification before idle or stop | Proven (ticked in issue) | Not re-audited |
| 2 Next action, bounded closure progress, approvals reconciled, no global stop | UNPROVEN at runtime; stays unticked | No local tick_log window (332 databases scanned) carries closure_batch, approval, reclassified or global_stop data; future ticks cannot be proven from a snapshot. Rules, strict mode and contract are in place |
| 3 One question, approved actions routed | Proven (ticked in issue) | Not re-audited |
| 4 Prompts active, obsolete schedules stopped | Proven (ticked in issue) | Not re-audited |
| 5 Handoffs and cleanup | Proven (ticked in issue) | Guard tests now deterministic under load |
| 6 Dated RPI artifacts and checks | Proven (ticked in issue) | These dated artifacts |
