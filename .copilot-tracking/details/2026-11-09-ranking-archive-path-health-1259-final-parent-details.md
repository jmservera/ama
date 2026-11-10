---
title: Issue 1259 final parent integration details
description: Exact commands and checks for the final parent merge and targeted validation
ms.date: 2026-11-09
---

## Environment

Owned scratch directory `/tmp/ama1259-final.3W0oxn` (path also in `/tmp/ama1259-final.path`, uncommitted): venv with `ruff==0.17.1` and `mypy==2.4.0` (pins from `src/core/pyproject.toml`), plus the API and core runtime dependencies needed by tests. Module origin is forced to this worktree by `PYTHONPATH`; no editable install pointing elsewhere. Core `PYTHONPATH=tests` from `src/core` with `src` added; API `PYTHONPATH=tests:../core/tests:../agents/tests:src:../core/src:../agents/src` from `src/api`. All `ZF_*` and MSSQL variables unset; synthetic `ZF_DATA` under scratch. No credentials or Azurite fixtures read.

## Phase 3 merge

* `git merge --no-ff --no-commit 9b1e2567c2d0a2173b562103cd27508f75181526`, confirm no conflicts, `git diff --cached --check` (report inherited whitespace), commit `merge: integrate frozen 1258 SQL main parent 9b1e2567c` with the Copilot trailer, repository-local noreply identity for author and committer.
* Verify `HEAD^2` equals the pin, `HEAD^1` is the recorded pre-merge planning commit descending from `5ed86a6a7`, `git diff 5ed86a6a7 HEAD -- src` equals the parent's delta over c5 only, and `git diff 9b1e2567c HEAD -- src` equals the child's delta over c5 only.

## Phase 4 equivalence

* `git diff --stat 7fc680d0e HEAD -- src/core/src src/api/src` must be only the parent's SQL/store/server changes (no ranking adapter, publication or runner hunk).
* `git rev-parse HEAD:<path>` equals `7fc680d0e:<path>` (and the parent's for adapter/publication/runner) for `ranking_publication.py`, `ranking_publication_runner.py`, `ranking_archive_blob.py` and the ranking tests; if any differs, the earlier emulator claim is stated as invalidated.
* Compare adapter, publication, runner blobs with both child (`7fc680d0e`) and parent; ranking tests with the child.
* Behaviour: the wiring tests cover Store/API publish, status, error propagation and audit outcome; SQL-service behaviour is untested. The runner calls `verify`; the API does not call the runner.
* Grep that the parent Store/API callers of `ranking_publication` use signatures compatible with the child's `verify`.

## Phase 5 commands

* Core from `src/core`: `python -m unittest test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents`; and a second invocation `python -m unittest test_priority_order test_resident_decisions` (SQL Server opt-in skips recorded; in-process SQLite cases may run).
* API from `src/api`: `python -m unittest test_ranking_publication_wiring test_case_journey`; also the API-side ranking tests present in `tests/` (`test_ranking_policy`, `test_ranking_scale` if present).
* Lint and types under the CI configuration: from `src/core` `ruff check . && ruff format --check .` and `mypy`; from `src/api` `ruff check . && ruff format --check .` and `mypy`. Run `ruff check .` and `ruff format --check .` as separate commands and record each exit. Classify each lint diagnostic individually (rule, message, line content) against the parent's `test_ranking_publication_wiring.py` after mapping lines past the child's 11 added lines; an unmatched diagnostic is new.
* Agents `test_cohort_ranking_eval` only if shared ranking modules changed beyond the merge (expected not).

Each phase is complete only with exit code and count recorded; skips are reported as the runner shows them.
