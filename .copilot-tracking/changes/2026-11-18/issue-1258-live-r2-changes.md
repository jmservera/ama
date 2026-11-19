---
title: Changes for issue 1258 (live demo run 2)
ms.date: 2026-11-18
---

No `src` file changed; tier FOCUSED. `rpi-checks.py --all` not run.

Files added or changed: `docs/reference/research/issue-1258-live-closure-r2-2026-11-18.md`, folder `docs/reference/research/issue-1258-live-r2-2026-11-18/` (strace logs, inject result, two throwaway scripts as `.txt`), `docs/reference/README.md`, `docs/reference/log.md`, and this run's `.copilot-tracking` records.

## Per-criterion status (issue 1258)

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Sync new ancestors before confirming | Proven (real ext4 syscall order) | strace-raw.txt |
| 2 Post-link sync failure keeps record, committed_unconfirmed | Proven (real fsync EIO via strace injection) | inject-result.txt |
| 3 Syscall-order regression, red before fix | Proven offline; pre-fix raw output not retained | 110 tests pass |
| 4 Retry, stage, audit, path-free, original date | Proven offline | 110 tests pass; API 409/503 not re-run here |
| 5 Original RPI, FULL receipt, exact-head review, hosted checks | Unproven; not provable for the demo | No src change so no FULL; independent review and hosted CI on a publishing head are human/CI gates; no check-run for main head b285d6039 |

Production-only (unproven): power-loss crash proof, real deployed volume durability, Blob variant durability. FULL-tier source needs: none from this lane.

## Validation

* `PYTHONPATH=tests python3 -m unittest test_ranking_publication test_ranking_publication_runner` (src/core): 110 tests OK.
* `python3 -m mypy` (src/core): no issues in 396 files. ruff format and check on `ranking_publication.py`: clean.
* Docs: link review by reading; `git diff --check`.
