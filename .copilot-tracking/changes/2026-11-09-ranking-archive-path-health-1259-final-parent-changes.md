---
title: Issue 1259 final parent integration changes
description: Actual merge, source equivalence and targeted validation for the frozen 1258 SQL main parent integration
ms.date: 2026-11-09
---

## Order

Research, plan, details and one critique committed first as `04cb315976a0e5392e835e562a7104d5178a6be1` (descends from frozen child `5ed86a6a7`). Merge, validation and these records followed.

## Merge

* Ordinary `git merge --no-ff` of exact `9b1e2567c2d0a2173b562103cd27508f75181526` (tree `b88cc90f4a4dd48a51b15e526b734e975fa036c5`) gives merge commit `13381ea25a24bd1b1ea72e2ed282d550009e1b5c` (tree `b83cc0f77343b40f70709950a3895f0dab086eca`). `HEAD^1` is `04cb3159`, `HEAD^2` is the parent. No conflict, no hand edit, no rebase, force, reset or parent source fix. Author and committer `8036360+jmservera@users.noreply.github.com`.
* `git diff --cached --check`: only trailing whitespace in main's committed `.copilot-tracking/changes/logs/1292-2026-11-08-sql/server-version.txt` (inherited via the parent, PR 1308 content).
* Parent ancestry verified: c5 `52f9b61bb` and main `8d6f029cac004506953f36606862168bbe9d9412` are ancestors. Newer `origin/main` `ef28d4da42d83b111d48f14df9b70e3c4932a477` is not imported.

## Source equivalence (git object comparison)

* `git diff 5ed86a6a7 HEAD -- src` and `git diff 52f9b61bb 9b1e2567c -- src` have the same stable patch-id `d1c835bcb334ae722831832b8ac79e5b249f5ab6`: the merge adds exactly the parent's source delta over c5 (12 files under `src/`, 8 of them non-test; none is a ranking file) and nothing else.
* `git diff 7fc680d0e HEAD -- src` contains no ranking file. Blobs of `ranking_publication.py`, `ranking_publication_runner.py`, `ranking_archive_blob.py`, `test_ranking_archive_blob.py`, `test_ranking_publication.py`, `test_ranking_publication_runner.py`, `test_ranking_publication_wiring.py` equal the frozen child's at `7fc680d0e`. `ranking_archive_blob.py` and `test_ranking_publication.py` also equal the parent's; the other five carry the child's path-health changes over the parent.
* Interface: the parent's `store.py` still calls `ranking_publication.verify(archive)`, `publish(snap, archive, today)`, `SCHEDULE` and the same error classes; the parent's only `store.py`/`server.py` hunks are priority-order (`_order_unresolved`, `CommittedReloadError`). The runner calls `verify`; the API does not call the runner.
* Consequence: the earlier Azurite observation (source `7fc680d0e`) concerned the unchanged adapter, publication and runner, which are byte-identical. No Azurite, transport or CA/SAS/credential fixture was re-run or read. The observation remains emulator evidence only, not Azure acceptance.

## Environment

Owned scratch `/tmp/ama1259-final.3W0oxn` (venv, `ruff==0.17.1`, `mypy==2.4.0`, `playwright==1.64.0`, API pins; editable `src/core`, `src/agents`, `src/api` of this worktree, `--no-deps`; logs). `ZF_DATA` and all `ZF_*`/MSSQL unset. No SQL Server, cloud, model, WORM, role, browser or `rpi-checks` action.

## Tests (owner demo-targeted tier; exit, count, skips)

| Command (cwd) | Exit | Result |
| --- | --- | --- |
| `PYTHONPATH=tests python -m unittest test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents` (`src/core`) | 0 | 146 OK, 0 skipped |
| `PYTHONPATH=tests python -m unittest test_priority_order test_resident_decisions` (`src/core`) | 0 | 398 OK, 158 skipped (SQL Server and Azure opt-in; not run) |
| `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_ranking_publication_wiring test_case_journey` (`src/api`) | 0 | 67 OK |
| same PYTHONPATH `test_ranking_policy test_ranking_scale` (`src/api`) | 0 | 31 OK |

A first core invocation without `PYTHONPATH=tests` errored on import (4 errors, my command omission, exit 1); it is not a product failure and is superseded by the rerun above.

## Lint and types (CI configuration: `ruff check .`, `ruff format --check .`, `mypy` in each project)

| Check | Exit | Result | Classification |
| --- | --- | --- | --- |
| core `ruff check .` | 0 | passed | clean |
| core `ruff format --check .` | 0 | 225 files formatted | clean |
| core `mypy` | 1 | 86 errors in 2 files (`tests/test_ranking_archive_blob.py` 77, `tests/ranking_blob_fixture.py` 9) | 84 inherited: parent `9b1e2567c` and c5 each show 84 under the same config. 2 are child-owned: the child's added test `test_conditional_create_never_lists...` (no `-> None`, untyped `requests` call), +2 vs parent; frozen child `5ed86a6a7` also 86 |
| api `ruff check .` | 1 | 10 errors (9 E501, 1 I001), all in `tests/test_ranking_publication_wiring.py` | all inherited: the same 10 diagnostics (rule, message, content) at the parent; the child's 11-line hunk at line 469 adds none. NOT cured, NOT waived |
| api `ruff format --check .` | 1 | `tests/test_ranking_publication_wiring.py` would be reformatted | inherited, identical at the parent. Not cured |
| api `mypy` | 1 | 13 errors in 5 files (9 in core `ranking_blob_fixture.py`, 4 elsewhere) | identical set to the parent (path-normalised; both runs resolve core through the editable worktree install) |

The CI chain `ruff check . && ruff format --check .` therefore fails for api (inherited) and core `mypy` fails (inherited plus two child-owned test-annotation errors). Both are red before this child.

## Not run

Full matrix, agents/orchestrator/importer tests, SQL Server, Azurite or any emulator/cloud, browser, model, WORM, role, scanners, `rpi-checks`, hosted CI.

## Budget

One of five review-correction cycles spent; none consumed here; four remain; no renewal.
