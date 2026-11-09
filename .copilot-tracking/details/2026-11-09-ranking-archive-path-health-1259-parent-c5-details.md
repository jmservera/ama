---
title: Issue 1259 frozen parent c5 integration details
description: Exact commands and checks for the parent c5 merge and Blob path-health verification
ms.date: 2026-11-09
---

## Environment

Scratch directory `/home/azureuser/.local/share/ama/gates/g1259-parent-c5-int-1109` (external, uncommitted): venv with pip-installed dependencies from the pre-merge worktree plus `ruff==0.17.1` and `mypy==2.4.0` from `src/core/pyproject.toml`. Module origin is overridden by `PYTHONPATH` to this worktree: core `PYTHONPATH=<wt>/src/core/src:<wt>/src/core/tests`, API `PYTHONPATH=<wt>/src/api/src:<wt>/src/core/src:<wt>/src/core/tests:<wt>/src/agents/src:<wt>/src/api/tests` (the documented API layout). Synthetic `ZF_DATA` under scratch, no private data, no network beyond the earlier dependency download.

## Phase 3 merge

* `git merge --no-ff --no-commit 52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8`, resolve the two files, `git diff --check`, confirm only the two files were hand edited, then commit with Conventional Commit `merge: integrate frozen 1258 Blob parent 52f9b61bb` and the Copilot trailer. Author and committer are the repository-local noreply identity resolved from `gh api user`.
* Verify afterwards: `git rev-parse HEAD^2` equals the pinned parent; `git diff 52f9b61bb HEAD -- src` contains only the child path-health hunks and tests.

## Phase 4 probes

Add one test class to `src/core/tests/test_ranking_publication_runner.py` (Blob path-health matrix) and one direct test to `src/core/tests/test_ranking_archive_blob.py` (conditional create independent of listing), reusing `ranking_blob_fixture.FakeBlobContainer` (extend only if a needed fault is unmodelled, for example a transport raise on listing). Run them alone first and keep the raw output.

## Phase 6 commands

* Core: `python -m unittest test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents` from `src/core/tests` equivalent (discovery with `-s tests -p ...` from `src/core`).
* API: `python -m unittest discover -s tests -p 'test_ranking_publication_wiring.py'` plus `test_ranking_policy` and `test_ranking_scale` from `src/api` with the documented PYTHONPATH.
* Agents: `test_cohort_ranking_eval` only if a shared ranking module changed beyond the merge (it did not before; confirm after merge).
* `ruff check` and `ruff format --check` on changed files; `mypy` from `src/core` on `ranking_publication.py`, `ranking_publication_runner.py`, `ranking_archive_blob.py`.

## Acceptance of the plan

A phase is complete only with its exit code and count recorded. Pre-existing skips are reported as shown by the runner, not analysed beyond that.
