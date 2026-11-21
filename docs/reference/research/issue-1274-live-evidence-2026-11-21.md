---
title: Resilient verified official release downloads, live evidence (#1274)
description: Identifies the exact failing release endpoints from retained run logs, records a real exact-version actionlint checksum verification and a hosted observation, and states what stays unproven
ms.date: 2026-11-21
---

## Scope

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Issue 1274 has two unticked boxes: criterion 1 (identify the failing official release endpoints) and criterion 4 (real exact-version checksum and artifact verification, then reviewed hosted CI). No Azure resource was touched, no credential was read, and no source file changed. Head is d2585a4c9. Run logs were read through `gh api` and are public repository evidence.

## Criterion 1: failing endpoints, by run and job

| Dependent PR and head | Run, job | Step | Endpoint and result | Class |
| --- | --- | --- | --- | --- |
| #1243 `fb7231c78` | 42469282088 attempt 1, job 128696067639 | Native workflow actionlint | `curl: (22) ... 504`, exit 22, 2026-11-08 10:01Z | Bootstrap |
| #1243 `fb7231c78` | 42469282088 attempt 2, job 128703802032 | Native workflow actionlint | `curl: (22) ... 503`, exit 22, 10:36Z | Bootstrap |
| #1271 `0639b6e3d` | 42464552756 attempts 1 and 2, jobs 128680975934 and 128684597601 | Native workflow actionlint | `curl: (22) ... 504`, exit 22 | Bootstrap |
| #1271 `0639b6e3d` | 42464552761 attempts 1 and 2, jobs 128681102295 and 128683494622 (agent) plus 128681464470 and 128683922558 (detection) | Install AWF binary | `https://github.com/github/gh-aw-firewall/releases/download/v0.28.23/checksums.txt`, six `curl` 504 responses 10 seconds apart, exit 22 | Bootstrap |
| #1273 `c1628cb50` | none retained as failed at this head; both workflows on the head are `success` (runs 42470092288, 42470092220) | | The 1273 failures cited in the issue are not retained at its final head | Not reproducible from retained logs |

Findings:

* The actionlint failures are the old inline `curl -fsSL` of `https://github.com/rhysd/actionlint/releases/download/v1.7.7/actionlint_1.7.7_linux_amd64.tar.gz` (and the checksums file) in `.github/workflows/src-ci.yml`, job `src-namespace`. Neighbouring jobs (`src-core`, `src-api` and the others) passed in the same run, so these are bootstrap failures, not unit fixture failures.
* The AWF failure is the upstream `install_awf_binary.sh v0.28.23 --rootless` from the pinned `github/gh-aw-actions/setup` action. It already retries six times and checks SHA-256, then exits 22 when GitHub returns 504 on every attempt.
* The same AWF endpoint recovered on a later run: run 42473216720 (merge commit of #1275, 4bc1e3f33) downloaded the checksums, logged `Verifying SHA256 checksum for awf-bundle.js` and `Installed awf bundle`, after a 72 second download, and all eight jobs passed. That is one observed recovery, not a guarantee.
* Both maintained installers are now identified: `tools/install-actionlint.py` (repo-owned, bounded, fail-closed) and the upstream AWF installer (no repo-owned hook; the gh-aw compiler pin and any mirror are separate owner decisions already recorded in the issue comment of 2026-11-12).

## Criterion 4: real exact-version verification

* Ran `tools/install-actionlint.py` into a throwaway directory with `GITHUB_TOKEN` unset. Output: both assets `verified from github.com on attempt 1`, exit 0, installed binary reports `1.7.7`.
* Independent check with plain `curl` and `sha256sum -c`: archive `actionlint_1.7.7_linux_amd64.tar.gz` (2080472 bytes) `OK` against the official checksums file (1119 bytes, SHA-256 `ac22e657...f351e0`, equal to the pin in the installer). The archive digest equals the pinned `023070a2...e0757`.
* `python3 -m unittest discover -s tools -p test_install_actionlint.py`: 12 tests, OK (504 recovery, truncation, wrong checksum, exhaustion).
* Hosted observation on a reviewed head: run 42497999337 (main, 2026-11-08), job `src-namespace` logged `actionlint_1.7.7_checksums.txt: verified from github.com on attempt 1` and the archive line, then passed the `1.7.7` version assertion.

## Verdict per criterion

| Criterion | Verdict | Basis |
| --- | --- | --- |
| 1. Identify failing endpoints, logs and affected installers, separate unit from bootstrap failures | Proven for actionlint (#1243, #1271) and AWF (#1271); #1273 failure not retained | Table above, job logs |
| 2. Bounded, fail-closed retrieval | Ticked, reconfirmed | 12 tests OK |
| 3. Focused regressions | Ticked, reconfirmed | Same tests |
| 4. Real exact-version verification, then reviewed hosted CI | Proven for actionlint 1.7.7 (local real download plus hosted run on main). Not proven for AWF 0.28.23: no repo-owned installer to verify, and the issue's "independent review, hosted CI on a reviewed exact head" order is satisfied only historically by #1275 | Section above |
| 5. Dependent PR resume route | Ticked, unchanged | Issue comment of 2026-11-11 |

Recommendation for the owner: criterion 1 can be ticked for the actionlint scope and the AWF endpoint identification. Criterion 4 needs an owner decision to accept the actionlint scope, since the AWF installer is upstream. Whole-issue closure is not claimed.

## Unproven and why

* AWF bootstrap resilience: the installer ships in the pinned upstream action and no repo-owned change is admitted; a retry, mirror or compiler upgrade is an owner decision.
* #1273 failure causes: not retained at the final head.
* A fresh hosted run on a new reviewed head was not made; no source changed and nothing was pushed.
