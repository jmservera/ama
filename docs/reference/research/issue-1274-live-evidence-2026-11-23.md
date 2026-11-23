---
title: Resilient verified official release downloads, live re-proof run 3 (#1274)
description: Fresh actionlint 1.7.7 checksum verification, regression runs and a per-criterion table for issue 1274 at main 342fad401d
ms.date: 2026-11-23
---

## Scope

Synthetic demo, desktop only. The issue concerns hosted CI release downloads, so the live Azure revisions 0000054 and 0000026 are not an input; no Azure resource was touched and no credential was read. No source file changed, so the focused tier applies. Head `342fad401d`. This note repeats [run 2](./issue-1274-live-evidence-2026-11-22-run2.md) with observations taken on 2026-11-23 around 00:5x UTC.

## Observations

* `python3 tools/install-actionlint.py <tmp>` with `GITHUB_TOKEN` unset: checksums and archive both `verified from github.com on attempt 1`; installed binary reports `1.7.7`.
* Independent `curl` plus `sha256sum -c`: checksums file 1119 bytes (SHA-256 prefix `ac22e6577b8d133c`), archive 2080472 bytes (prefix `023070a287cd8ccc`), `a.tgz: OK`.
* `python3 -m unittest discover -s tools -p test_install_actionlint.py`: 12 tests OK.
* `python3 -m unittest tools.test_rpi_checks`: 129 tests OK.
* Newest `Source projects CI` on main: run 42497999337, head `e2ecee256`, success, 2026-11-08. Job 128681102295 (#1271 AWF) log lines are dated 2026-11-08 and no later AWF installer failure was found; #1273 is merged and its failing logs are not retained.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| 1 Identify failing endpoints, logs and installers | Proven for actionlint (#1243, #1271) and the AWF `checksums.txt` endpoint (#1271), from [run 2](./issue-1274-live-evidence-2026-11-22-run2.md); unproven for #1273 | #1273 logs not retained |
| 2 Bounded fail-closed retrieval | Proven (ticked) | `tools/install-actionlint.py`, 12 tests OK |
| 3 Focused regressions, hashes, rpi-checks tests | Proven (ticked) | 12 and 129 tests OK |
| 4 Real checksum verification, ordered gates, hosted CI on reviewed exact head | Proven for actionlint 1.7.7 locally; unproven for AWF 0.28.23 (upstream installer, no repo hook) and for hosted CI on a new head (push forbidden; no source change) | Owner-gated |
| 5 Dependent PR resume route | Proven (ticked) | merged #1275 |

Whole-issue closure is not claimed; the commit uses `Refs #1274`.
