---
title: Live-demo re-observation of unusable ranking archive paths (#1259), run 8
description: Red-before and green-after evidence for a real-filesystem permission-denied archive regression, with per-criterion status
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Local filesystem classification only. No credential was used and no Azure resource was created or changed; the ranking runner is an operator CLI with no deployed job, so live revisions cannot exercise it.

## Change

`UnusableArchivePathTests.test_real_permission_denied_parent_is_unknown_not_creatable` in `src/core/tests/test_ranking_publication_runner.py` places the archive below a mode-0 folder (no mock) and asserts verify and schedule report a problem with no latest or due value, publish is refused with `archive_unreadable`, and no path leaks. It is skipped for root. Runtime source is unchanged.

## Evidence

* Red-before: pre-fix `cd687abadd^` with the new test fails with `('due', True) != ('problem', None)`; the existing suite shows 7 failures there.
* Green-after: `PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q` gives `Ran 111 tests`, `OK`.
* `ruff check` and `ruff format --isolated --line-length 100 --check` pass. `python3 -m mypy` reports three errors in `telemetry.py` and `device_provision.py` (missing OpenTelemetry stubs, unused ignore), none in touched files.

## Per-criterion status

| Criterion | Status |
| --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (local tests, now including a real permission denial) |
| Unknown window and unreadable shape, no healthy-empty fallback | Proven (local tests) |
| Preserve absent first run and path-free diagnostics | Proven (local tests) |
| Regular-file and dangling-link regressions plus absent coverage; failure before fix | Proven: failures before, 111 pass after |
| Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven and process-gated: no `rpi-checks.py --all` run here, nothing pushed |
