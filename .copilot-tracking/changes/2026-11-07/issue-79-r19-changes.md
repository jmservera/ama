---
title: Issue 79 changes, r19 merge of main 8af3aea6
ms.date: 2026-11-07
---

Task `issue-79-r19-merge-main-8af3`. Planning commit `e2f593f43` preceded the merge; refs `preserve/issue-79-pre-8af3-merge` (start `87c027a3`) and `preserve/issue-79-r19-planning`.

## Chronology

* Start verified ignored-clean (`87c027a3`, tree `f391682d`); main fetched `8af3aea6`; overlap only `docs/reference/log.md`; `git merge-tree` dry run clean.
* Planning committed, main re-fetched unchanged, then `git merge --no-ff` produced merge commit `df9947c91` (tree `e5783ac67`), parents `e2f593f43` and `8af3aea6`. Auto-merge of `docs/reference/log.md` only; no conflict, no rebase, no rewrite.

## Proofs

* Every non-log path changed by main since `0f420dc9` has main's blob and mode in the merge; every non-log topic path has its pre-merge blob and mode; no mode changes against the start. The log has 11 additions and 0 deletions against the start and 23 additions and 0 deletions against main (before this task's own entry).
* Runner SHA-256 `5987f45dadedbbe2bb075517cb04930b2901af0a17461865f39e18fadc878a08` equals the r18 post-edit digest; helper `500e31e47d8d25a8149ea685073cecc43a95739a7063d9e93077af75c04df0c9`. Import origin is this worktree (`/mnt/ama-gates/g79-8af3-preparation-1107/origin.log`).

## Checks (scratch and logs in `/mnt/ama-gates/g79-8af3-preparation-1107/`, `PYTHONDONTWRITEBYTECODE=1`)

* Core `test_ranking_publication test_ranking_publication_runner`: exit 0, 53 tests OK, 0 skipped.
* API `test_ranking_publication_wiring.py`: exit 0, 15 tests OK, 0 skipped.
* Ruff 0.17.1 check on `src/core`: exit 0; format check on the five ranking files: exit 0; mypy 2.4.0 on `src tests`: exit 0, 268 files. Caches were external, so no ignored files were created.
* Not run: FULL, browser (incoming `case_journey_browser_check.py` is verified by blob identity only), SQL, scanners, images.

## Records

* This record, the Review, the state JSON and one appended `docs/reference/log.md` entry.

## Limits

* The tests use `/tmp/zf79venv` (installed from this worktree) and `/tmp/79-align-r13-1106/venv` for the pinned tools, both my own earlier environments, not rebuilt.
