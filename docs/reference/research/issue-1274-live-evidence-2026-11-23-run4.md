---
title: Resilient verified official release downloads, live re-proof run 4 (#1274)
description: Retained job-log proof of the actionlint 504, fresh checksum verification and regression runs, and a per-criterion table for issue 1274 at main 5c08bedd8f
ms.date: 2026-11-23
---

## Scope

Synthetic demo, desktop only. The issue concerns hosted CI release downloads, so no Azure resource was touched and no credential was read. No source file changed, so the focused tier applies. Head `5c08bedd8f`. This note extends [run 3](./issue-1274-live-evidence-2026-11-23.md) with the exact retained log lines for the failing endpoint.

## Observations

* Retained log of job 128696067639 (run 42469282088 attempt 1, head `fb7231c788`, 2026-11-08T10:01:37Z): line 1382 requests `https://github.com/rhysd/actionlint/releases/download/v1.7.7/actionlint_1.7.7_linux_amd64.tar.gz`, line 1383 the `actionlint_1.7.7_checksums.txt` file, line 1397 `curl: (22) The requested URL returned error: 504`, line 1398 `Process completed with exit code 22`. This is an actual bootstrap failure, not a unit fixture failure.
* Attempt 2 of the same run failed only in job `src-namespace` (a test job); the download jobs passed, so that failure is not a release-download failure.
* `python3 tools/install-actionlint.py <tmp>` with `GITHUB_TOKEN` and `GH_TOKEN` unset: checksums and archive both `verified from github.com on attempt 1`; installed binary reports `1.7.7`.
* Independent `curl` plus `sha256sum -c`: checksums file 1119 bytes (SHA-256 prefix `ac22e6577b8d133c`), archive 2080472 bytes (prefix `023070a287cd8ccc`), `a.tgz: OK`.
* `python3 -m unittest discover -s tools -p test_install_actionlint.py`: 12 tests OK. `python3 -m unittest tools.test_rpi_checks`: 129 tests OK.
* Newest `Source projects CI` on main: run 42497999337, head `e2ecee256`, success, 2026-11-08. PR #1275 (the fix) merged 2026-11-08T10:51:51Z, merge commit `4bc1e3f336`.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| 1 Identify failing endpoints, logs and installers | Proven for actionlint (#1243, line-level above) and the AWF `checksums.txt` endpoint (#1271, [run 2](./issue-1274-live-evidence-2026-11-22-run2.md)); unproven for #1273 | #1273 logs not retained |
| 2 Bounded fail-closed retrieval | Proven (ticked) | 12 tests OK |
| 3 Focused regressions, hashes, rpi-checks tests | Proven (ticked) | 12 and 129 tests OK |
| 4 Real checksum verification, ordered gates, hosted CI on reviewed exact head | Proven for actionlint 1.7.7 locally; unproven for AWF 0.28.23 (upstream installer, no repo hook) and for hosted CI on a new head (push forbidden, no source change) | Owner-gated |
| 5 Dependent PR resume route | Proven (ticked) | merged #1275 |

Whole-issue closure is not claimed; the commit uses `Refs #1274`.
