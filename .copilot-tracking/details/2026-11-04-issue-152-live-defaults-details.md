---
title: Phase details, issue 152 live default queue check
ms.date: 2026-11-04
---

## Phase 1

For each manifest profile with a default, log in as its identity and compare `items` ids, `total` and order from `/api/cases?view=mine&sort=urgent` with the declared default; compare all-cases scope for staff with `all_case_ids`; open declared `#/case/` endpoints.

## Phase 2

Add three sentences to the manifest paragraph in `src/api/README.md`.

## Phase 3

Run with `PYTHONPATH=../core/tests:../agents/tests:../core/src:../agents/src:src:.` from `src/api` (installed packages pointed at another worktree).
