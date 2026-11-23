# Changes 2026-11-23 (issue 2187)

Planned: no `src/` or tools edit. Adds docs/reference/research/issue-2187-live-gate-lock-2026-11-23.md, an index row and a log entry. Tier: focused, documentation only; `rpi-checks.py --all` not run.

## Implemented

* docs/reference/research/issue-2187-live-gate-lock-2026-11-23.md, index row in docs/reference/README.md, log entry. No source edit; tools tests 129 OK.

## Per-criterion table (issue 2187)

| Criterion | Status | Evidence |
| --- | --- | --- |
| Lock only when a heavy group is selected | Proven | `needs_heavy_lock` and `nullcontext` branch (#2215); tests pass |
| Test added | Proven | `test_heavy_lock_only_for_docker_sql_or_browser_groups`, `test_main_skips_lock_without_heavy_group_and_takes_it_with_one` |
| Remainder after #2286 | None | #2286 did not touch lock selection |
| Live full-gate run with a worker proceeding under a held lock | Unproven | needs `--all`, forbidden here |
