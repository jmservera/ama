---
title: Ranking archive ancestor durability 1258 changes
description: Implementation record for issue 1258 plan phases 1 to 3 (LIGHT source preparation, not FULL validation)
ms.date: 2026-11-08
---

## Boundary

Approved planning head `3712f107227d69cd8da51d34e610d767d4f626a5` (tree `5019e9e3507c1d09aec95b9c9feb66a147ab5529`), base `f548b65f4aa31eb92a2cc9cb801130e422daed7f`; ignored-inclusive status was clean at start. Plan phases 1 to 3 only. No `--all` or `--changed` runner, SQL, browser, Docker, scanner, model or Azure work. No push, PR or issue write. Scratch: `/home/azureuser/.local/share/ama/gates/g1258-source-light-1108` (venv, non-editable out-of-tree install from a copy of `src`, pip and mypy caches, synthetic `ZF_DATA` under scratch, `HOME` under scratch). Import origin proven under the venv `site-packages` (not `src/`).

## Changes

* `src/core/src/zava_forward/core/ranking_publication.py`: new private `_ancestors()` (plan D3 and D4: realpath, writable run of parents nearest first, stop after a mount point or root, stop before a non-writable parent); `_confirmed()` syncs the archive folder then each ancestor, any `OSError` becomes `DurabilityUnconfirmedError` (record kept, no rollback). Exception message and docstrings say "archive folder or a parent folder".
* `src/core/src/zava_forward/core/ranking_publication_runner.py`: uncertainty message wording only (PC-005).
* `src/core/tests/test_ranking_publication.py`: new `AncestorDurabilityTests` (7 tests); `test_publish_syncs_file_then_removes_stage_then_syncs_directory` deliberately relaxed from an exact event list to file, unlink-stage then at least two directory syncs (plan 1.9).
* `src/core/tests/test_ranking_publication_runner.py`: one parent-folder failure test.

## Red evidence (unfixed source, before any source edit)

Command: `cd src/core; PYTHONPATH=tests python -m unittest tests.test_ranking_publication.AncestorDurabilityTests tests.test_ranking_publication_runner -q` exit 1, `Ran 47 tests`, `FAILED (failures=7)`:

* nested order: `['file','link','archive'] != ['file','link','archive','b','a','root']`
* ancestor failure after link: `DurabilityUnconfirmedError not raised`
* retry with all directories present: `DurabilityUnconfirmedError not raised`
* partial creation: `DurabilityUnconfirmedError not raised`
* symlinked parent: `[] != ['x','real']`
* mount stop: `['file','link','archive'] != ['archive','b','a']`
* runner: `(0,'published') != (2,'committed_unconfirmed')`

The steady-state prefix test passes before and after (it guards unchanged first-run order). Raw log retained in scratch `red.log`.

## Green evidence

* Core: `python -m unittest discover -s tests -p "test_ranking_publication*.py" -q`, exit 0, 84 tests OK. The first green run failed only the exact-order test (`[..., 'sync-dir','sync-dir','sync-dir']`), the expected plan 1.9 update; both logs kept in scratch.
* API: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p "test_ranking_*.py" -q`, exit 0, OK (existing archive-directory fault test and path-free 409 unchanged).
* `ruff check` and `ruff format --check` on the four files pass after one format fix and one E501 fix. System `mypy` was broken (`No module named 'mypy'`, preserved); mypy installed into the scratch venv, `mypy -p` on the two modules: no issues (resolved to the installed copy of the same source).

## Divergences and open items

* DV-1 Existing exact event-order assertion relaxed as planned (1.9).
* DV-2 No API wiring test added: the runner test covers the ancestor-targeted `committed_unconfirmed` mapping and path-free message; `server.py` maps by exception type, unchanged. A reviewer may want an API-level ancestor case in FULL.
* DV-3 Plan 1.7 non-writable-ancestor behavior is exercised only by the mount-stop mock; the writability branch is not directly tested (root-skip and host-layout dependence).
* D5 effect confirmed: steady-state publication issues extra directory syncs (up to the first mount point or non-writable parent). Permissions do not prove durability.
* Mocked syscall order is not real crash or filesystem durability proof.
