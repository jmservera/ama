# Changes: issue 1204 tick_log checker (2026-11-19)

Refs #1204. Tier FOCUSED (tools only; no src, SQL, security or infrastructure). No Azure resource used or created.

## Files

* `tools/check-tick-log.py`: offline checker that validates an exported coordinator `tick_log` (action and evidence per tick, recovery after two no-progress ticks, closure batch of at most five without repeats, scoped approval reclassification, no global stop while work remains).
* `tools/test_check_tick_log.py`: 10 synthetic-fixture unit tests.

## Validation

* `python3 -m unittest discover -s tools -p test_check_tick_log.py -q`: 10 tests, OK.
* `python3 -m ruff check --isolated --line-length 100` and `ruff format --isolated --line-length 100 --check` on both files: pass.
* mypy: not applicable, `tools/` has no mypy project; no `src/<project>` modified. Complete gate not run, by owner brief.

## Per-criterion table

| Criterion of #1204 | Status | Basis |
| --- | --- | --- |
| Idle/stop needs fresh backlog classification | Proven (ticked) | Not re-audited; see 2026-11-18 note |
| Every tick has next action, bounded closure progress, approval reconciliation, no global stop | Partly proven | Instruction text proven on main (2026-11-18 note); the contract is now executable and tested on synthetic rows. Unproven: a real tick window, since the live `tick_log` lives in coordinator session SQL and is not exported for the demo. Box stays unticked |
| One-at-a-time questions, approved actions routed | Proven (ticked) | Not re-audited |
| Corrected prompts active, obsolete schedules stopped | Proven (ticked) | Not re-audited |
| Handoffs forbid premature publication; finite cleanup | Proven (ticked) | Not re-audited |
| Dated RPI artifacts, static review, scenarios, checks | Proven (ticked) | Not re-audited |

Unmet criterion: tick liveness over real ticks.
