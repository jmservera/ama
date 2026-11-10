---
title: Issue 149 process D1 details (2026-11-10)
ms.date: 2026-11-10
---

## P1 content

* Old chain: path, sha256 `14de2fc4610d07d8fa07f84a5ee9aa3db857026e1e8d6d2d7951e4621ff0efde`, 7 records, actual verify exit 1 QUALIFIED at implement-start, literal reason preserved, notes preserved.
* Exact sequence: launch (clean local `736561ba0`, 09:13:51Z), authorized normal fast-forward to reviewed input `ae4b20007`, research-open, plan-done, implement-start (09:21:00Z), normal merge `0e5758da2` (09:21:05Z), implement-done, review-done, commit-complete at `26a40c7df`.
* Distinguish: reviewed input adoption (not authored by this task), own prospective main integration, own plan/implement/review events, instrument limitation.
* Identities: input parent, main `d52f20a51`, merge and tree, final `26a40c7df` and tree, source tree `6502cdfe1d18`.
* Carried-forward local checks by source identity to `0e5758da` only: dates, pins (ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0, Chromium 156.0.8078.4, Python 3.12.3), commands and exits from the old pack; M4a exit 1 command fault then M4a2 exit 0; skips (4 opt-in browser, 7 SQL); axe only in role-screens stories.
* Limits and one D1 debit, no D2 or D3, no budget reset, #1362, #156 M1, PR 1371 and #1373 untouched.

## P2 commands

`sha256sum -c` over the baseline snapshot, `git diff --name-status 26a40c7df HEAD`, `git rev-parse HEAD:src 0e5758da:src`, `git diff --check`.

## Out of scope

Any rerun of checks, source, docs, index, log, pack, old tracking edit, push, merge or rebase.
