---
title: Issue 1274 release-download resilience criteria proof
description: Per-criterion evidence for the verified official release download fix delivered by #1275, run 2026-11-19 for the synthetic demo
ms.date: 2026-11-19
ms.topic: reference
---

Refs #1274. Synthetic demo, desktop only. No source change: criteria 2 and 3 are already delivered by merged #1275 and no unmet criterion is code-addressable locally. No Azure action was taken.

## Evidence

* Failing endpoint, #1243 head `fb7231c788aa49d5dbcd7e30bd81c4806fea3cbf`: run 42469282088 job 128696067639 (`src-namespace`), step "Native workflow actionlint". The retained log (fetched 2026-11-19 via the Actions jobs logs API) shows the old inline `curl -fsSL https://github.com/rhysd/actionlint/releases/download/v1.7.7/actionlint_1.7.7_linux_amd64.tar.gz` followed at 2026-11-08T10:01:37Z by `curl: (22) The requested URL returned error: 504` and `Process completed with exit code 22`. The same job passed its tool, unit and ruff stages (`All checks passed!`), so this is a bootstrap failure, not a unit fixture failure.
* Maintained installer and workflow: `tools/install-actionlint.py` (tried browser URL, then release asset API 221573254; 3 attempts per source; pinned size and SHA-256) invoked from the "Native workflow actionlint" step of `.github/workflows/src-ci.yml`.
* Real exact-version verification (2026-11-19, downloads only, nothing executed from the download before the pinned digest matched): `curl` of the official v1.7.7 assets gave archive SHA-256 `023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757` (2080472 bytes) and checksums file SHA-256 `ac22e6577b8d133c7cd779682e65712ef722e719a297633699a4da05e9f351e0` (1119 bytes); `sha256sum` matched the listed `actionlint_1.7.7_linux_amd64.tar.gz` line and both pins in the installer. `python3 tools/install-actionlint.py /tmp/v1274/bin` printed both "verified from github.com on attempt 1" lines and installed the binary.
* `python3 -m unittest discover -s tools -p test_install_actionlint.py`: 12 tests, OK (covers 504 recovery, truncated, wrong checksum, exhausted retrieval per the existing suite).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Identify failing endpoints, logs and workflows | Proven for #1243 only | Job log above. Runs for #1271 and #1273 heads (`0639b6e3d`, `c1628cb50`) are not retrievable by head SHA or PR association (merged, runs absent from the API); the AWF 0.28.23 bootstrap failure is therefore not independently re-observed. |
| 2 Bounded, fail-closed retrieval | Proven for actionlint | `tools/install-actionlint.py` code review plus live run above; AWF bootstrap is upstream and has no repo-owned hook (owner comment 2026-11-12). |
| 3 Focused regressions and hashes | Proven for actionlint | 12 installer tests pass; `WORKFLOW_HASHES` unchanged because no native workflow changed. |
| 4 Real checksum verification, then review, hosted CI, merge | Partly proven | Checksum and artifact verification proven above; independent exact-head review and hosted CI on a reviewed head cannot happen without a push, which this run is forbidden to do. |
| 5 Dependent PR resume route | Ticked in issue | Already recorded by #1275. |

Unproven: AWF 0.28.23 bootstrap recovery, hosted CI on a reviewed head, merge.
