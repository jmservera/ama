---
title: Issue 203 live changes
ms.date: 2026-11-21
---

Refs #203. Documentation only; no src change, so the focused tier applies (checker run, checker tests, link review, diff review). No `rpi-checks.py --all`.

## Files

* `docs/reference/research/issue-203-live-20261121-2026-11-21.md` and its evidence folder (added)
* `docs/reference/README.md` index row (added), `docs/reference/log.md` entry (appended)

## Per-criterion table

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Search for `mvp/` and `prototype/` returns only intentional historical references naming the archive tag | Proven | Checker 0 violations, 8 tests pass |
| 2 | Relative links in the changed docs resolve | Already ticked | Not re-proven |
| 3 | Index updated and log entry appended | Already ticked | Index and log updated again for this run |
| 4 | Rubric comparison | Already ticked | Not re-proven |
| 5 | Deployed app and CI green from `src/` | Partly proven | Proven: apps and revisions healthy, `/healthz` 200, src-ci green on main dispatch 2026-11-08 and on recent PRs. Unproven: images built from `src/`; api logs `commit=unknown`, registry private, `src-deploy.yml` has 0 runs |
