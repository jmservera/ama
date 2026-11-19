---
title: Live-demo closure of issue 1258 ranking archive ancestor durability, run 2
description: Real-filesystem syscall order and kernel fault-injection evidence on current main, with per-criterion proven/unproven status for issue 1258
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, `src/core` ranking publication. Base `origin/main` b285d6039 (2026-11-18). No `src` file changed, so the tier is FOCUSED and `rpi-checks.py --all` was not run. Builds on [run 1](issue-1258-archive-ancestor-durability-2026-11-18.md), whose gap was that the order was shown only with mocked `os.fsync`. Raw files are in [issue-1258-live-r2-2026-11-18/](issue-1258-live-r2-2026-11-18/).

## Method and results

* Local tests on main: `PYTHONPATH=tests python3 -m unittest test_ranking_publication test_ranking_publication_runner` in `src/core`: 110 tests, OK. `python3 -m mypy`: no issues in 396 files. `ruff format --isolated --line-length 100 --check` and `ruff check` on `ranking_publication.py`: clean.
* Real syscall order: `strace -f -y` on `publish()` first publication into a missing `a/b/archive` on a real ext4 volume (`/var/tmp`). Raw: [strace-raw.txt](issue-1258-live-r2-2026-11-18/strace-raw.txt), script [publish-first-run.py.txt](issue-1258-live-r2-2026-11-18/publish-first-run.py.txt). The three `mkdir` calls come first, then:

```text
fsync(<archive>/.ranking-...tmp)   staged file
linkat(archive, .tmp -> ranking-1.0.0-2026-10-09-7502f1822e79.json)
fsync(<archive>)  fsync(<archive>/a/b)  fsync(<archive>/a)  fsync(<root>)  fsync(/var/tmp)  fsync(/var)  fsync(/)
```

* Real kernel fault: `strace -e inject=fsync:error=EIO:when=4` made the fsync of ancestor `a` (after link) return EIO from the syscall layer. Raw: [strace-inject-raw.txt](issue-1258-live-r2-2026-11-18/strace-inject-raw.txt), [inject-result.txt](issue-1258-live-r2-2026-11-18/inject-result.txt), script [publish-ancestor-sync-fault.py.txt](issue-1258-live-r2-2026-11-18/publish-ancestor-sync-fault.py.txt). Result: `DurabilityUnconfirmedError` errno 5, `written True`, message path-free, the record present after the failure, no staged file left. That is the `committed_unconfirmed` contract, without a mocked `os.fsync`.
* Hosted checks: `Source projects CI` does not run on pushes to main; the last main run is a `workflow_dispatch` on `e2ecee256` (success). The check-runs for the merge commit `cd687abad` (PR #1328) are 6 success and 2 cancelled. No check-run exists for the current main head `b285d6039` or for this local branch.
* Azure (resource group `ama`, read-only): `ca-cutover-test-demo-api` revision `0000032` is configured with `ZF_BLOB_ACCOUNT_URL`, container `evidence`, and no local ranking archive path variable. The deployed demo persists through Blob (owner decision 2026-11-08), so the local-filesystem ancestor sync is not the deployed demo path. No resource was created, so none was deleted. No browser proof applies: there is no web surface in this issue.

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Sync new archive ancestors before confirming; keep first-run behaviour | Proven (real ext4 syscall order, also ticked) | strace shows link, then archive, `b`, `a`, root and above, then confirmation; first run created the nested folders |
| 2 Post-link sync failure keeps record, `committed_unconfirmed` | Proven (real fsync EIO injected via strace) | inject-result: errno 5, record kept, no false rollback or success |
| 3 Syscall-order regression, nested ancestors and post-link failure, red before fix | Proven offline (tests) | 110 tests pass; run 1 recorded the pre-fix (`cd687abad^`) failures; raw pre-fix output still not retained |
| 4 Retry, private stage, audit, path-free 409/503, original date intact | Proven offline | 110 passing tests in the two modules; API 409/503 tests not re-run in this lane |
| 5 Original RPI, current FULL receipt, independent exact-head review, hosted checks | Unproven; not provable for the demo | See below |

## Unproven and needs

* Production-only: real power-loss or crash proof (a fault injected into the syscall result is not a lost write after power failure); durability of a real deployed volume or Azure Files; Blob durability of the deployed variant. None is claimed.
* FULL-tier source needs: none in this lane. A FULL receipt (`--all` at an exact head), an independent exact-head review and hosted CI on a publishing head are required only when `src` changes; they are human or CI gates and are not waived by the demo decisions.
* Open and not resolved here: the mount-topology precondition (PC-002), and extra steady-state sync overhead. The strace run walks to `/`, so on this volume the mount-id bound did not stop the walk below the filesystem boundary because all directories share one mount.
