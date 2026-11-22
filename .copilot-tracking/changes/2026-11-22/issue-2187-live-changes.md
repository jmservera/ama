# Changes: issue 2187

Tier: focused (documentation and tracking only; no src change). Classification basis: no source, workflow or gate-tool edit.

Files: docs/reference/research/2026-11-22-issue-2187-focused-lock-skip.md and .copilot-tracking records.

Validation: `python3 -m unittest discover -s tools -p test_rpi_checks.py -k lock -q` gave 16 tests, OK. Hosted CI not observed (no push).

| Criterion | Status | Evidence |
| --- | --- | --- |
| Lock only when a heavy group is selected | Proven (code and test, delivered by #2215) | needs_heavy_lock in tools/rpi-checks.py; research note |
| Test | Proven | test_heavy_lock_only_for_docker_sql_or_browser_groups, test_main_skips_lock_without_heavy_group_and_takes_it_with_one pass |
| Live probe under held lock | Unproven (supporting only) | probe ran 120 s without lock abort, stopped by timeout; no receipt produced |
