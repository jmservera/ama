---
title: Issue 1259 final parent integration plan
description: Prospective plan to merge exact frozen parent 9b1e2567 into the path-health child and verify source equivalence and targeted tests
ms.date: 2026-11-09
---

## Objective and boundary

Locally merge exact `9b1e2567c2d0a2173b562103cd27508f75181526` into `fix/ranking-archive-path-health` (ordinary `--no-ff`, no rebase, reset, force, amend, push, PR, issue or board change). No parent source fix. Do not cure the parent's API wiring-test lint errors or waive them. Refs #1259 only; nothing closes.

## Ordering

This plan, details, research and the single critique are committed before the merge or any edit. The merge, validation, changes record, one Review and state follow.

## Tier

Owner demo-targeted tier: relevant child Core, API, runner and Blob contract tests, plus Ruff and mypy under the maintained CI configuration (`src-ci.yml`: `ruff check .`, `ruff format --check .`, `mypy` per project), bound to this worktree with `PYTHONPATH`. Actual failures and skips are kept. No full matrix, SQL Server or Azure SQL service, emulator rerun, cloud, model, WORM or role action. Hosted CI, independent exact-head review and human approval remain.

## Critique dispositions applied (one critique, Revise, six findings)

* PC-001 applied: pre-merge SHA recorded; ancestry of `5ed86a6a7` verified instead of `HEAD^1` equality.
* PC-002 applied: lint classified by individual diagnostic (rule, message, mapped line content) versus the parent's blob, not by file identity; the ten inherited errors are retained, not cured or waived.
* PC-003 applied: `ruff check .` and `ruff format --check .` run and recorded independently; the CI chain failure is also reported.
* PC-004 applied: the no-SQL boundary means no SQL Server or Azure SQL service, no `ZF_*`/MSSQL variables. In-process SQLite store tests inside the selected suites may run and are reported as run, never as SQL Server evidence.
* PC-005 applied: phase 4 adds behaviour checks of the Store/API publish, status and error paths and audit outcome through the selected wiring tests; SQL-service behaviour is stated as untested. The runner calls `verify`; the API does not call the runner.
* PC-006 applied: separate executable `python -m unittest` invocations with working directories in the details; changed ranking tests are compared with the frozen child, adapter/publication/runner blobs with both child and parent.

## Cycle budget

One of five spent, four remain, no renewal. This task is a merge; it consumes no cycle unless a concrete failing probe justifies one scoped source edit (stop and record instead if it needs a parent change).

## Phases

* [ ] 1. Research (done, `...-final-parent-research.md`).
* [ ] 2. Plan, details, one critique, committed.
* [ ] 3. Merge exact parent. Record the post-planning pre-merge SHA (PC-001: the planning commit descends from `5ed86a6a7`, so `HEAD^1` is that planning commit, verified with `merge-base --is-ancestor 5ed86a6a7`). Verify `HEAD^2` equals the pin, no conflict, no hand edit, whitespace check on the merge.
* [ ] 4. Source equivalence: tree/blob comparison of the ranking adapter, publication, runner and their tests against the frozen child and the parent; interface check that the parent's Store/API wiring still calls the child's `verify`/runner signatures.
* [ ] 5. Targeted tests, Ruff and mypy; classify each failure as inherited (identical in the parent) or new.
* [ ] 6. Changes record, one Review, state, commit LOCAL freeze, handoff.

## Stop rules

A new failure in a selected test caused by the merge stops productive work and is recorded; a fix is attempted only if it is a child-owned source defect within cycle 2. Any failure that needs a parent source change is reported, not fixed. A failing selected test is not waived.

## Remaining criteria (unmet here)

Real Azurite-or-account acceptance on this head, Blob container, WORM, role grant, Bicep, deployment, folder-record migration decision, hosted CI, independent exact-head review, human approval, parent C5 budget and API wiring-test lint authority. All #1259 criteria stay literal and unticked.
