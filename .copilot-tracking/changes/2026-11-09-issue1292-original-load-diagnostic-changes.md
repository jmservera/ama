---
title: Issue 1292 original-load diagnostic changes
description: Implementation record for the second bounded unchanged-source diagnosis of the SQLite database-is-locked failure
ms.date: 2026-11-09
---

Refs #1292 only. No acceptance criterion is ticked. This is a focused diagnostic, not a release or full gate.

## Outcome

* Result: 0 of 2 paired selections reproduced the error. Cause stays UNKNOWN.
* No source, test, observer-behaviour or harness fix was made. No flake, necessary-load, sufficient-load or proposed-source-fix claim is made.
* Counters: 2 of 2 pairs used; 0 retries; 1 holder check (no holder); 1 nonqueued `flock -n /tmp/ama-rpi-heavy.lock` admission (granted, exit 0); E5 not spent.
* Source under test: tree equal to base `ef28d4da4` and to `8d6f029ca` for `src`; planning commit `4b8621f0dd6b7e85ae20dd48ae8e1c474d12b371`.

## Pairs (UTC, 2026-11-09)

| Pair | Mode | Process | Start | End | Exit | Ran | Skipped | Wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | plain | API (6 modules) | 16:56:16.948 | 16:58:18.704 | 0 | 263 | 58 | 120.4 s |
| P1 | plain | Core (4 modules) | 16:56:16.950 | 16:59:14.029 | 0 | 421 | 158 | 174.9 s |
| P2 | plain | API (6 modules) | 16:59:14.073 | 17:01:11.221 | 0 | 263 | 58 | 115.9 s |
| P2 | OBSERVER | Core (4 modules) | 16:59:14.075 | 17:01:41.583 | 0 | 421 | 158 | 145.6 s |

* Overlap: P1 about 121.8 s (API ran entirely inside Core); P2 about 117.1 s. Core outlasted API in both pairs.
* Neither process neared the 420 s cap; no exit 124. Counts match the original 421/158 and 263/58. All skips are the framework's opt-in owned loopback SQL Server skips; no skip was added or changed.
* The target `SqliteLegacyEdges.test_large_legacy_backfill_is_linear_and_survives_concurrent_openers` printed `ok` in both Core logs. No `database is locked` text appears in any log.
* The OBSERVER run (P2 Core) recorded 261 events (two opener threads, 24 enter/exit pairs), `raised=[]`, `harness_errors=[]`, `failures=[]`, `errors=[]`. Observer changes timing and failure semantics, so P2 does not show equivalence with a plain run. No exception was captured because none occurred.
* Plain and OBSERVER runs are reported separately. The wall time of Core was shorter than the original 224.3 s failing run in both pairs; the original load of about 5.4 was not reproduced (host load at start 2.29 and 3.90, load after 3.90 and 4.12).

## Runtime profile and deviations

* Profile A (system python plus PYTHONPATH) was rejected before any attempt: `~/.local` holds editable `.pth` files for another checkout that contaminate the `zava_forward` namespace (`provenance-1-profileA-contaminated.txt`, kept). Profile B (user site disabled) failed on missing `aiohttp` and `mssql_python` (`profile-b-probe.log`).
* Used an owned venv built with `pip install -q -e src/core -e src/agents -e src/api` (original command). Import origins all resolve inside this worktree `src`; no foreign path (`provenance.txt`). Package versions in `pip-freeze.txt` may differ from the lost original venv (not retained).
* Deviations, no equivalence claimed: cleared environment (`env -i`) with owned `ZF_DATA`, `TMPDIR` and pyc prefix; possibly different package versions; the original start offset and overlap were not retained; original host load differed.
* Provenance with SHA256 of `store.py`, `sqlstore.py`, `mssqlstore.py` and the selected test sources was recorded before the admission (`provenance.txt`). This corrects the prior FR1 gap prospectively only; it does not repair past import provenance.

## Additive qualification of prior records

* Prohibited prior amendment, disclosed: the unpublished commit `0e43484f652b774d9daeca5e9cab12899a05bf69` was amended into `72ca1c9aac6396e19174352a3503f9b5e4ee8643`. That was not authorised. Original `59accfa1c`, `8aea86f8b` and published owner history are unchanged. The earlier process is NOT fully conforming.
* First post-wait traces, stated precisely from the retained observer data: I2 `PRAGMA table_info(recommendations)` at 8.0001 s; I3, C2 and C3 `PRAGMA table_info(cases)` at 8.4058, 8.7021 and 8.4216 s. These are statement-start times; the COMMIT came later (about 0.0005 s after the statement start in the retained traces). No causality and no COMMIT duration is implied.
* The original 14 records, 29 raw members and Reviews are unchanged: `baseline-prior.sha256` re-checks with 0 failures and the raw `SHA256SUMS` verifies 29 of 29.

## Evidence and cleanup

* External log directory `/home/azureuser/source/ama-demo-wt/logs-1292-original-load-diagnostic/` (25 files); manifest `SHA256SUMS` sha256 `634ceca206c1a077e57cb8d421e2d5e9f63d30ad495cd2af8c7918e0f91566de`.
* Owned scratch, the venv, editable-install metadata and pycache directories were removed by exact path; `git status --short --ignored` is empty.
* Not performed: hosted CI reading, push, PR, issue, board, cloud, independent review.
