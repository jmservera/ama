---
title: 441 trace phase details
description: Details
ms.date: 2026-11-13
---

## Phase 1

Changes file lists the answers: PR #1059 (closed, unmerged, branch docs/accept-resident-portal-adr, commits 2cad28376 and 4f80b611b); ADR 0007 on main is 844346329/#1150; anchor broken by a75bbdffa (#558) with heading relocated to docs/capstone/history/storage-map-before-reorganization.md:223; correction cycles as a scoped inventory (at least five, not exhaustive), no cost figure.

## Phase 2

Re-run `git cat-file -e`, `git show -s`, `grep -n` for each citation; check PR states and timestamps with `gh pr view`; ancestry of both 2cad28376 and 4f80b611b vs origin/main; heading at a75bbdffa^ and at HEAD; stage new tracking files and run `git diff --cached --check`.

## Phase 3

Independent code-review of tracking diff; commit with Co-authored-by trailer.
