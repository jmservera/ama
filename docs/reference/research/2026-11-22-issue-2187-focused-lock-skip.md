---
title: Issue 2187 focused rpi-checks runs and the heavy lock
description: Evidence that rpi-checks.py already skips the heavy lock unless a heavy group is selected
ms.date: 2026-11-22
---

Issue #2187 asks that `rpi-checks.py --changed` take `/tmp/ama-rpi-heavy.lock` only when a Docker, SQL or browser group is selected, with a test.

## Finding

The behaviour was delivered earlier by commit 46c328182a ("fix(gate): take the heavy lock only for browser, SQL or image groups", #2215). On this branch (base dcaf271ad3):

* `tools/rpi-checks.py` defines `needs_heavy_lock(groups)`, true for `browser`, `mssql`, `logo-0600` and `image-*` groups.
* `main()` wraps the run in `heavy_lock(...)` only when `needs_heavy_lock(selected["groups"])`, otherwise `contextlib.nullcontext()`.
* `tools/test_rpi_checks.py` holds `test_heavy_lock_only_for_docker_sql_or_browser_groups` and `test_main_skips_lock_without_heavy_group_and_takes_it_with_one`.

## Evidence

* `python3 -m unittest discover -s tools -p test_rpi_checks.py -k lock -q`: 16 tests, OK.
* Live probe: with `flock -x /tmp/ama-rpi-heavy.lock` held, `rpi-checks.py --changed --base HEAD --lock-timeout 0` did not abort on the lock within 120 s (a heavy group would fail at once with the lock timeout); the probe was stopped by `timeout` and its output directory removed. This is supporting evidence only; the unit test is the proof.

## Scope

Documentation only, focused tier. No Azure, browser or credential use was needed: the issue concerns a local gate tool, so demo-environment criteria do not apply.
