---
title: Issue 1231 r10 details (normal local merge of the named parent)
ms.date: 2026-11-06
---

## Phase 2 merge details

* Pre-check (critique fixes 1 and 2): `git status --short --ignored` is empty; HEAD is the Phase 1 prospective commit, a descendant of `29d1669e6`; `git rev-parse feat/ranking-publication-runner-79` still equals `d654634fc…`. Recompute the expected tree with `git merge-tree --write-tree HEAD d654634fcbe5c82a362e9a3d948d09d0c2993d6d` (the earlier `5d21b1d…` excluded the Phase 1 records and is only the research prediction).
* Command: `git merge --no-ff --no-commit d654634fcbe5c82a362e9a3d948d09d0c2993d6d`, merging the SHA itself.
* Success criterion: exit 0, no unmerged paths, and `git write-tree` equals the recomputed tree.
* Failure: `git merge --abort`, record the output, stop with the smallest missing decision.
* Commit: `merge: align ranking archive child with local parent d654634fc` with `Refs #1231` and the Copilot trailer, using the freshly resolved repository-local privacy-safe identity.

## Phase 3 proofs

* `git merge-base --is-ancestor` for each of `43080ab42`, `d654634fc`, `56eec7369`, `29d1669e6`.
* `git diff --quiet 29d1669e6 HEAD -- src infra tools .github/workflows`.
* `git diff --name-status 29d1669e6 HEAD` outside `.copilot-tracking` must list only the coordinator agent file.
* Blob equality of `ranking_publication.py`, `ranking_publication_runner.py`, `store.py`, `server.py`, the three core and API test files and `src/core/README.md` between `29d1669e6` and HEAD.

## Phase 4 checks

* Venv: own external venv `/mnt/ama-gates/restart-1106-1231-align/venv` only if the existing read-only `/tmp/zf79venv` lacks a tool; otherwise source-bound use with `PYTHONPATH` set to this worktree and printed `__file__` origins. The result is source-bound, not an installed-distribution proof, and is recorded as such.
* Tests: `test_ranking_publication`, `test_ranking_publication_runner` (core) and `test_ranking_publication_wiring` (API), with skips recorded.
* Lint: Ruff check and format on `src/api` and the core ranking files with the project's pinned settings, mypy from `src/core`.
* Caches (critique fix 4): `PYTHONDONTWRITEBYTECODE=1`, Ruff `--no-cache`, mypy `--cache-dir` and pytest/unittest outputs under the external scratch directory; confirm ignored-inclusive status stays empty.
* Documents (critique fix 3): `git diff --check` on explicit ranges (`29d1669e6..HEAD` for the child side, and the Phase 1 commit to the merge commit); whitespace findings inherited from parent tracking records are classified as inherited, not edited. `python -m json.tool` on r10 state files, relative links in r10 records.
* Logs: only under `/mnt/ama-gates/restart-1106-1231-align/`.
