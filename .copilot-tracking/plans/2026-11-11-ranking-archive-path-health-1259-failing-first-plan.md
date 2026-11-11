---
title: Issue 1259 failing-first verification plan
description: Prospective plan, written before any observation, for one source-unchanged focused replay
ms.date: 2026-11-11
---

## Objective

One source-unchanged verification and reconciliation increment: replay the existing main regression selectors against pinned old source and current source, in task-owned exports, and record raw results. No source correction, no new test, no FULL claim, no criterion tick.

## Prospective declarations (before any run)

* Current source blobs under `src/core/src/zava_forward/core/` at `077ad5ad2`: `ranking_publication.py` `ed2879856e4d1bacd4d1ef0e6cff1ebd236718f0`, `ranking_publication_runner.py` `0ea15181038aaff54e8153564187e84b42ff9a9c`, `store.py` `70d71de39a79670a75ee64ad18be3e5c472cd3da`, `ranking.py` `03cdc76a12449c19e10c8136d87f12d5b63c3d23`. Current runner test blob `687827a373960104628a774463262747bd0ede65`.
* Old candidate A `2be660e9d`: `ranking_publication.py` `96a180194c5977894bd265c1a3b4b22f44d6b13b`, `ranking_publication_runner.py` `d527696a892b2861e3e73f6bb40fdadcaa6682a5`, `store.py` `a941ad9f3868ab2f774d057cff56747a8487de9d`, `ranking.py` `052bc6b9ad85e1f23acc22f7a355786453cabdd0`.
* Old candidate B `6d793bc3a`: `ranking_publication.py` `7f2736283bacccac27d089f3f083a2a71d1fcc0e`, `ranking_publication_runner.py` `d009c0389f34015d559c2e4ee84a11792768a71a`, `store.py` `a99948569d64b3f0c2e0a34d409a5d810651dd06`, `ranking.py` `052bc6b9ad85e1f23acc22f7a355786453cabdd0`.
* Selectors (unittest, run from the export root `src/core`, module names under `tests`):
  1. `test_ranking_publication_runner.UnusableArchivePathTests` (regular file, dangling link, dangling ancestor, mocked stat failure across verify, schedule, publish and exercise; CLI exit codes; path-free fallback; absent-directory and link-to-real-folder controls; Store status).
  2. `test_ranking_publication_runner.StorageAndDuplicateFindingTests.test_unreadable_archive_is_a_problem_never_empty_or_healthy` and `...test_unreadable_archive_exits_nonzero_through_main` (existing archive-unreadable shape).
  3. Controls only: `UnusableArchivePathTests.test_absent_directory_stays_creatable_for_first_run` and `...test_absent_folder_below_a_link_to_a_real_folder_is_creatable`, run in verbose output as part of selector 1 and named separately in the report.
* Static checks, path behaviour only: `ruff check` and `ruff format --check` on the two current source files and the runner test file; `python3 -m py_compile` of the two source files; `git diff --check`.

## Method

1. Scratch `S=/home/azureuser/.local/share/ama/gates/g1259-ff-2122`. Exports by `git archive <rev> src/core` into `$S/cur`, `$S/oldA`, `$S/oldB`; the tests directory in each old export is replaced by the exact current-main tests (`git archive 077ad5ad2 src/core/tests`) so the same current tests run against old source. Record the byte-identity of each source file with its git blob.
2. Run with `python3 -S`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=<export>/src/core/src:<export>/src/core/tests`, temp dir and synthetic `ZF_DATA` under `$S`. Print `zava_forward.core.ranking_publication.__file__` as import-origin proof before each run. Never use the editable installs and never run inside the frozen checkout.
3. Run order: current export first (selectors 1 and 2, expected green), then candidate A, then candidate B only if A cannot load the tests or is otherwise inconclusive. Each at most once; no retry loop.
4. Classification: old-source failures are genuine only if the failing assertions match the defect (non-directory reported empty or healthy, wrong status, path leaked). Import or collection errors are environment or compatibility limitations, not red evidence.
5. Raw logs and a manifest (commands, exit codes, blobs, import origin, tool versions, scratch paths) are copied to `.copilot-tracking/evidence/2026-11-11-1259-failing-first/`.

## Stop conditions

* A faithful replay is impossible for both candidates: record the exact limitation, manufacture nothing.
* Current source fails a selector, or a result is surprising: record it and stop. This is not a grant to fix source or retry.
* Any need for credentials, network, containers or private data: stop.

## Boundaries

No change to `src/`, tests, tools, workflows, knowledge base or cutover files. Only original tracking records are added. No push, PR, issue or board edit, merge, closure or tick. FULL receipt (criterion 5) stays unmet. Independent exact-head review required.

## Checkpoints

* [x] Research and plan written before observation.
* [x] Replay executed and raw logs captured.
* [x] Changes record, single review and state written (handoff outside repo).
