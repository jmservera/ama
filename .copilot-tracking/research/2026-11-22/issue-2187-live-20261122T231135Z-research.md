# Research: issue 2187 (run 20261122T231135Z)

Disposition: reused. Planning Readiness: Ready.

Evidence: docs/reference/research/2026-11-22-issue-2187-focused-lock-skip.md and a fresh read of `tools/rpi-checks.py` at HEAD 3219004e90.

* `needs_heavy_lock(groups)` is true only for `browser`, `mssql`, `logo-0600` and `image-*`.
* `main()` uses `heavy_lock(...)` only when `needs_heavy_lock(selected["groups"])`, else `nullcontext()`.
* Tests `test_heavy_lock_only_for_docker_sql_or_browser_groups` and `test_main_skips_lock_without_heavy_group_and_takes_it_with_one` exist.
* `python3 -m unittest discover -s tools -p test_rpi_checks.py -k lock -q`: 16 tests OK on this checkout.

Gap: the existing main() test patches `heavy_lock`, so it does not prove a real held lock is ignored. A focused test with a real flock held and `--lock-timeout 0` would. No source change needed; one test is added.
