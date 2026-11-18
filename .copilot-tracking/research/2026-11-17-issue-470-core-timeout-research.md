---
title: Issue 470 core suite timeout research
ms.date: 2026-11-17
---

* Task: raise or shard the project-core unit suite timeout in `tools/rpi-checks.py` (issue #470, Refs).
* Disposition: executed (code read only; no heavy runs, shared gate holds /tmp/ama-rpi-heavy.lock).
* Evidence: `tools/rpi-checks.py` hardcodes `timeout=1800` for project unit suites in `required_checks` (planned contract) and in the runner (`tests` unsharded path, `sharded_tests`). `SHARDED_PROJECTS = {"api": 3}` only. Issue reports core at 1535 s sequential on the PR 1641 candidate (4059 tests), 1085 s on main (3529 tests), under shared load; a 1800 s ceiling leaves little margin.
* Receipt verification compares `timeout_seconds` from the trusted contract against the executed row, so planned and runner values must change together.
* Measurement: not reproducible locally without a heavy run; recorded issue figures are the baseline. The timeout is a ceiling, not a check.
* Decision: smallest fix is a per-project suite timeout constant (core 3600 s, others 1800 s) used at all three sites, plus a regression test and README note. Sharding core is larger and changes receipt shapes; deferred.
* Planning readiness: Ready.
