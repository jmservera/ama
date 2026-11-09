---
title: Issue 1292 current-main priority SQL regression validation changes
ms.date: 2026-11-09
task_id: 1292-current-main-sql-1109
---

## Change summary

* No source, test, fixture or harness change. Documentation and tracking only: this record, the review record, a dated subsection in the cut-over evidence pack, one index entry, one appended log entry, the updated state file.
* Planning records were committed first as `e208748cf134ddd2a9b11d7a7a0a6fe097d60242` (tree `bf4394dd270c2a7cd06f46faef884f0536845eee`) before any SQL execution. The runner verified `src` tree `86bc00e19a167e517ae2955ad88d6e2f7b4eac26` equals the pinned base `ba71894bb1a94d6a24aabf9828312668f88f3ff5` and that only `.copilot-tracking/` differs.

## Execution (one admission, no retry)

* Pre-admission recheck (18:14:29Z): `fuser` found no holder of `/tmp/ama-rpi-heavy.lock` (rc 1), `docker ps -a` empty, no flock, unittest or sqlservr process, memory 15983 MB with 10118 MB available, 134 GB free disk.
* One non-queued admission: `timeout -k 10 1190 flock -n /tmp/ama-rpi-heavy.lock bash sql-1292-current-main-v2.sh <outdir>`; flock rc 0; campaign 1794248073 to 1794248613 (540 s elapsed, limit 1200 s). External outputs are in `files/e1292-cm-sql-181429/` (not committed); `SHA256SUMS` (30 members, `sha256sum -c` zero failures) digest `b6cec06e5c4075e5271747f188078a30e49e169255a7810a350475fc57798bc0`.
* Container: one labelled `zf.task=1292-sql-disposable`, published on `127.0.0.1` only, memory 3g, three readiness probes (not a test retry). Image id `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718` (digest identical, `mcr.microsoft.com/mssql/server@sha256:cf8f...1718`, no pull). SQL Server 2022 (RTM-CU27-GDR, KB5126934) 16.0.4305.5. Python 3.12.3, `mssql-python` 1.15.0, `mssql-python-odbc` 18.6.2.1, Docker 29.9.0. Own environment `.venv` installed with `pip install -e src/core[sql] -e src/agents`.
* Import paths: `zava_forward.core.sqlstore` and `mssqlstore` resolved under this worktree's `src/core/src`; file sha256 `0b0caf62802def56aba8749aaea58dacfbf3f89f364384665b7773754876741a` and `1825dc5f2c6dd7b9b62870b47ea85be5dcd649169d2019ac06a0928514b7cce7` equal `git show HEAD:` blobs `89f409ee000b6ce97c25d0efb1d60732551da410` and `c712ad4a8a15f794f3a555de48bead66bb86eb39`.

## Outcomes (external verifier `verify-1292-cm.py`, exit 0)

| Process | Selection | Expected | Ran | Result | Exit | Seconds | Skips | SQL Server tests |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 12 `test_priority_order` classes (JSON, LegacyMetadata, LoopbackGuard, MssqlBeginRecovery, Sqlite x4, Mssql PriorityOrder, LegacyMetadata, LegacyEdges, LockTimeoutBegin) | 108 | 108 | OK | 0 | 309.366 | 0 | 31 |
| B | `MssqlC3Corrections`, `MssqlC4Corrections` | 34 | 34 | OK | 0 | 201.206 | 0 | 34 |
| C | the two original resident-control methods on `MssqlResidentControls`, plus parity on `SqlResidentDecisions` (SQLite) and `JsonResidentDecisions` (in-memory) | 6 | 6 | OK | 0 | 10.367 | 0 | 2 |

* Totals: 3 processes, 148 tests, 0 skips of any kind, 0 failures, 0 errors, 0 timeouts; A plus B equal the complete 142-test module (once each); 67 tests ran on the disposable SQL Server and 81 were SQLite, in-memory, fake-driver and guard tests. The six C lines include both original methods `test_challenge_source_exact_dependency_manifest_and_original_reviews` and `test_failed_priority_accept_edit_remove_disposition_and_audit` on `MssqlResidentControls`, each `ok`.
* Output SHA-256: `A.stderr.txt` `c2b6d2c2461b8742dfab9c5eaeef794b6e00000033e76e1b5c923b7bc6d27b27`, `B.stderr.txt` `e6fc70a6dbc910196e3029fc2772d855624e60daed4fa3488ac96fa107398707`, `C.stderr.txt` `a0c2d7c20d2e18800f404b5d4aaca17b953b08bc109a366958e5cd1b7a4928c9`, `imports.txt` `58930a36bf43307183f79d9e869e9baf803a4e627a615d43e6b6583f9772c463`, `meta.txt` `349c1e5ca1a725d877abff73b2c893e99dc2173440275a36902ea8765b59642f`; stdout files are empty. The stream redaction filter was active; a pattern scan of all 30 outputs found no password or connection-string marker.

## Cleanup

* The exact container (id `9d18437a720c4490e7646c3d14559518eebc2d984ffd49c2786f784bda34f78a`) was removed by id after label and name verification; `docker ps -a` shows zero containers. The leftover task-prefixed database query returned empty. The own manifest, `home` directory and `.venv` were removed by resolved path. Original image, other containers and caches were untouched; no prune.

## Plan variance

* The plan's two divergences are intentional and recorded: the 142-test module was split once by class into A and B to keep each process under 600 s (prior full runs 536.7 s and 558.0 s), and parity tests for the two resident methods were added. No selector, count or expectation changed after the run began.
* The first runner draft was never executed; `sql-1292-current-main-v2.sh`, `run-redacted.py` and `verify-1292-cm.py` are session files outside the repository.

## Not changed or claimed

* Not claimed: AC4 or AC5, the fails-against-old-behavior half of AC3, hosted CI, independent review, a complete local gate, whole-SQL acceptance, large-scale, lock-duration, Azure or live behavior, root cause or fix of the unknown historical startup failure, any resident or professional approval, or ticked or closed criteria. #1292, #81 and #440 are unchanged.
