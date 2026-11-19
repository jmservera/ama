---
title: Issue 1274 CI axe-core download hardening and retained 504 logs (Refs #1274)
description: Code change to verify and retry the axe-core CI download, plus retained-log evidence for the 1243, 1271 and 1273 release-download failures
ms.date: 2026-11-18
---

Refs #1274. Synthetic demo, desktop only; no Azure resource touched. Extends [the earlier audit](./issue-1274-release-downloads-audit-live-2026-11-18.md).

## Code change

The `Synthetic design-system browser checks` step in `.github/workflows/src-ci.yml` downloaded axe-core 4.10.3 from cdnjs with `curl --retry 2` and no digest check, although `tools/rpi-checks.py` already pins `AXE_SHA256`. The step now retries up to 5 times on any error (`--retry-all-errors`, 5 s delay), writes to a `.part` file, runs `sha256sum --check --strict` against the pinned digest and only then moves the file into place. A wrong or truncated file fails the step before the browser checks run. `WORKFLOW_HASHES["src-ci.yml"]` was updated and `test_src_ci_axe_download_is_bounded_and_verified_before_use` was added.

## Evidence

* Real download with the CI flags: exit 0, sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`, equal to `AXE_SHA256`.
* Negative check: `sha256sum --check --strict` on a wrong file printed `FAILED`, return code 1.
* `python3 -m unittest discover -s tools -p test_rpi_checks.py`: 110 tests OK. `test_install_actionlint.py`: 12 OK. ruff check and format check pass; mypy --strict on the installer files passes; actionlint 1.7.7 (installed by the verified installer) over the five native workflows exits 0.

## Retained failure logs (read with `gh api --allow-escape-sequences .../jobs/<id>/logs`)

| Head | Run, attempt, job | Step | Observed |
| --- | --- | --- | --- |
| 1243 `fb7231c788aa` | 42469282088, job 128696067639 | Native workflow actionlint | `curl: (22) ... 504`, exit 22 |
| 1271 `0639b6e3d` | 42464552756 attempt 2, job 128684597601 | Native workflow actionlint | `504`, exit 22 |
| 1271 | scorer 42464552761 attempts 1 and 2, jobs 128681102295, 128683494622 | Install AWF binary | five repeated `504` |
| 1273 `c1628cb50` | 42470092288 attempt 1, job 128698647692 | Native workflow actionlint | `504`, exit 22 |
| 1273 | scorer 42470092220 attempt 1, job 128698790743 | Install AWF binary | repeated `504` |

The `ModuleNotFoundError: No module named 'absent_rpi_package'` line in the actionlint jobs is expected output from a negative unit test, not the failure. Latest attempts for all three heads succeeded.

## Per-criterion status

| # | Status | Basis |
| --- | --- | --- |
| 1 | Proven for the demo | Table above separates fixture output from bootstrap 504s; 1243, 1271 and 1273 are merged |
| 2 | Proven for actionlint and axe; AWF not | Installer and the new axe check; AWF bootstrap is upstream gh-aw generated code |
| 3 | Proven for actionlint and axe | 12 installer regressions and the new workflow regression; WORKFLOW_HASHES updated; test_rpi_checks 110 OK |
| 4 | Partly proven | Real checksum verification of actionlint (earlier note) and axe (above); independent review and hosted CI of this head not run (no push permitted) |
| 5 | Already ticked | PR 1275 resume route |

## Limits

FOCUSED tier: no `src/` change. The edit changes a pinned download and a hashed workflow, so a conservative reading takes the FULL tier before publication; `rpi-checks.py --all` was not run by owner instruction, so the coordinator must decide. The AWF bootstrap stays open.
