---
title: Issue 1401 cycle 2 requalification details
ms.date: 2026-11-11
task_id: 1401-c2-qualification-1111
---

## Phase 2 commands

Evidence directory: `/tmp/zf1401-c2-1111-<UTC timestamp>` created with `mkdir` (no `-p`, fails if it exists). Each command writes `NAME.out`, `NAME.err` and `NAME.exit` using `set -C` (noclobber); the exit file records `$?` of the direct tool before anything else runs. No pipeline hides a status.

* Environment for core: `cd src/core && PYTHONPATH=tests:src:../agents/src:../api/src` (same as C1 verification). For API: `cd src/api && PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests`.
* Provenance (same environment, separate attempt): print `__file__` and SHA256 of `aftercare`, `aftercare_intake`, `aftercare_store`, `store`, `sqlstore`, `mssqlstore` (import only, no connection), the API `server` and `workbench` modules, and the three core test files plus the two API test files; every path must be under this worktree. A path under the primary checkout stops the cycle.
* Core: `python3 -m unittest -v tests.test_aftercare tests.test_aftercare_intake tests.test_aftercare_store`.
* API: `python3 -m unittest -v tests.test_aftercare_served tests.test_aftercare_screen`.
* Static: from `src`, `ruff check` and `ruff format --check` on `core/src/zava_forward/core/aftercare.py`, `core/tests/test_aftercare.py`, `core/tests/test_aftercare_store.py`; from `src/core`, `mypy` on the same files as C1 ran it.
* Target compatibility (nonmutating): `git merge-tree --write-tree HEAD origin/main` and `git diff --name-status <base> origin/main` filtered for source paths, plus blob identities of the three changed source and test files in HEAD and in origin/main.
* Source unchanged check: `git diff --exit-code 678c458 -- src` before and after, and `git status --short` empty before the records are written.

## Phase 3 to 5

Write one changes record, the process-deviation record and capture limits, the critique record, the Review record and a state file under new dated `2026-11-11-issue1401-c2-qualification-1111-*` names, then commit with the repository-local noreply identity for author and committer.
