---
title: Resilient verified official release downloads, live re-proof run 2 (#1274)
description: Fresh retained-log reads, real exact-version actionlint checksum verification and regression runs for issue 1274 criteria 1 and 4
ms.date: 2026-11-22
---

## Scope

Synthetic demo, desktop only. No Azure resource touched, no credential read, no source file changed, so the focused tier applies. Head `3219004e90` equals `origin/main` at start. Issue 1274 has two unticked boxes (criteria 1 and 4). This note repeats [issue-1274-live-evidence-2026-11-22.md](./issue-1274-live-evidence-2026-11-22.md) with new observations taken at 2026-11-22T23:2x UTC.

## Criterion 1: failing endpoints (logs re-read with `gh api --allow-escape-sequences .../jobs/<id>/logs`)

| Job | Head | Conclusion | Failing endpoint and line |
| --- | --- | --- | --- |
| 128696067639 (#1243, run 42469282088) | `fb7231c78` | failure | inline `curl -fsSL` on `https://github.com/rhysd/actionlint/releases/download/v$version/actionlint_${version}_linux_amd64.tar.gz`; `curl: (22) ... 504`, `exit code 22` at 10:01:37Z |
| 128680975934 (#1271, run 42464552756) | `0639b6e3d` | failure | same actionlint URLs; `curl: (22) ... 504`, `exit code 22` at 08:55:53Z |
| 128681102295 (#1271, run 42464552761, job agent) | `0639b6e3d` | failure | `https://github.com/github/gh-aw-firewall/releases/download/v0.28.23/checksums.txt`; three `curl: (22) ... 504` at 08:51:00Z, 08:51:10Z, 08:51:20Z |

The failing steps are bootstrap steps (the `src-namespace` and `agent` jobs), not unit fixtures; the unit and ruff stages of the same runs passed. The #1273 failures are not retained at its final head, so they cannot be re-read. Maintained installers: `tools/install-actionlint.py` (repo-owned, bounded, fail-closed, called from `.github/workflows/src-ci.yml`) and the upstream AWF installer shipped by the pinned `gh-aw-actions/setup` action, which already retries three times but has no repo-owned hook.

## Criterion 4: real exact-version verification

* `python3 tools/install-actionlint.py <tmp>` with `GITHUB_TOKEN` unset: checksums and archive both `verified from github.com on attempt 1`; installed binary reports `1.7.7`.
* Independent `curl` plus `sha256sum -c`: checksums file 1119 bytes (SHA-256 prefix `ac22e6577b8d133c`), archive 2080472 bytes (prefix `023070a287cd8ccc`), `a.tgz: OK` against the official checksums file.
* `python3 -m unittest discover -s tools -p test_install_actionlint.py`: 12 tests OK (504 recovery, truncation, wrong checksum, exhaustion).
* `python3 -m unittest tools.test_rpi_checks`: 127 tests OK.
* Hosted: latest `Source projects CI` on main is run 42497999337, head `e2ecee256`, `success` (2026-11-08). No newer hosted run on a newly reviewed exact head exists because nothing changed and nothing was pushed.

## Verdict

| Criterion | Verdict |
| --- | --- |
| 1 | Proven for actionlint (#1243, #1271) and AWF endpoint (#1271). Unproven for #1273 (logs not retained). |
| 4 | Proven for actionlint 1.7.7 locally and on main. Unproven for AWF 0.28.23 (upstream installer) and for a hosted run on a new reviewed head (no push permitted). |

Whole-issue closure is not claimed; the commit uses `Refs #1274`.
