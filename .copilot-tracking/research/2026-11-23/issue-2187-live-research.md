# Research 2026-11-23 (issue 2187)

Planning Readiness: Ready. Research disposition: executed.

Question: does `rpi-checks.py` take `/tmp/ama-rpi-heavy.lock` only when a Docker, SQL or browser group is selected, and what remains of #2187 after #2286?

Findings:

* `needs_heavy_lock(groups)` in tools/rpi-checks.py returns true only for `browser`, `mssql`, `logo-0600` and `image-*`; `main` wraps `heavy_lock` in `contextlib.nullcontext()` otherwise. It came from commit 46c328182a (#2215), not #2286.
* #2286 (merged 2026-11-23T01:41:01Z, Refs #2186 #2188) touched tools/rpi-checks.py for receipt-inert paths and concurrent image builds; it did not change the lock selection.
* tools/test_rpi_checks.py already holds `test_heavy_lock_only_for_docker_sql_or_browser_groups` and `test_main_skips_lock_without_heavy_group_and_takes_it_with_one`.
* `python3 -m unittest test_rpi_checks -q` from tools/: 129 tests OK at this head.
* Group inventory (`required_groups`): preflight, project-*, namespace, static, infra, migration, browser, mssql, image-*, logo-0600, extra-*. Only the heavy set uses Docker capacity in the Runner dispatch.

Gap check: no source remainder found. Live Azure and browser proof do not apply to a local gate tool.
