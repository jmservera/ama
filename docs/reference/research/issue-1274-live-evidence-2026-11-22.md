---
title: Resilient verified official release downloads, live re-proof (#1274)
description: Re-reads the retained failing job logs, repeats the real exact-version actionlint checksum verification and the local regression tests, and restates what stays unproven
ms.date: 2026-11-22
---

## Scope

Synthetic demo, desktop only. No Azure resource was touched, no credential was read and no source file changed, so the focused tier applies. Head is `dcaf271ad3`. This note repeats the proof in [issue-1274-live-evidence-2026-11-21.md](./issue-1274-live-evidence-2026-11-21.md) with fresh observations. Issue 1274 has two unticked boxes, criteria 1 and 4.

## Criterion 1: failing endpoints

Job logs re-read with `gh api repos/jmservera/ama/actions/jobs/<id>/logs` on 2026-11-22 (still retained):

| Job | Head | Result |
| --- | --- | --- |
| 128696067639 (#1243, run 42469282088) | `fb7231c78` | `failure`, job `src-namespace`; step runs `curl -fsSL` on `https://github.com/rhysd/actionlint/releases/download/v$version/actionlint_${version}_linux_amd64.tar.gz` and the matching `_checksums.txt` |
| 128680975934 (#1271, run 42464552756) | `0639b6e3d` | Same two actionlint URLs, same inline `curl` |
| 128681102295 (#1271, run 42464552761, agent) | `0639b6e3d` | `https://github.com/github/gh-aw-firewall/releases/download/v0.28.23/checksums.txt`, `curl: (22) ... 504` at 08:51:00Z |

The failures sit in bootstrap steps, while the unit and ruff stages in the same runs passed, so they are not unit fixture failures. The #1273 failures are not retained at its final head (see the 2026-11-21 note). The two maintained installers are `tools/install-actionlint.py` (repo-owned, bounded, fail-closed, called at `.github/workflows/src-ci.yml` line 278) and the upstream AWF installer shipped by the pinned `gh-aw-actions/setup` action.

## Criterion 4: real exact-version verification

* `python3 tools/install-actionlint.py <dir>` with `GITHUB_TOKEN` unset: both assets `verified from github.com on attempt 1`, installed binary reports `1.7.7`.
* Independent plain `curl` plus `sha256sum -c`: checksums file 1119 bytes, SHA-256 `ac22e657...f351e0`; archive 2080472 bytes, SHA-256 `023070a2...e0757`, `a.tgz: OK` against the official checksums file. Both equal the pins in the installer.
* `python3 -m unittest discover -s tools -p test_install_actionlint.py`: 12 tests OK (504 recovery, truncation, wrong checksum, exhaustion).
* `python3 -m unittest tools.test_rpi_checks`: 123 tests OK.
* Hosted observation: run 42497999337 on main (head `e2ecee256`, 2026-11-08) is the latest `Source projects CI` run on main and is `success`; the earlier note records its `verified from github.com on attempt 1` log lines.

## Verdict

| Criterion | Verdict |
| --- | --- |
| 1 | Proven for actionlint (#1243, #1271) and AWF endpoint (#1271); #1273 not retained |
| 4 | Proven for actionlint 1.7.7 locally and on main. Not proven for AWF 0.28.23 (upstream installer, no repo-owned hook). A hosted run on a newly reviewed exact head was not made because nothing changed and nothing was pushed |

Whole-issue closure is not claimed; accepting the actionlint scope for criterion 4 is an owner decision.
