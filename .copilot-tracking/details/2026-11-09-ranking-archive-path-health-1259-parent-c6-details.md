---
title: Issue 1259 frozen parent C6 integration details
description: Exact commands for the C6 parent merge, profile checks and evidence binding
ms.date: 2026-11-09
---

## Environment

Owned scratch `/home/azureuser/.local/share/ama/gates/g1259-parent-c6-1109` (external, uncommitted, mktemp style names allowed). Python 3.12 venv inside it; `pip install -e` is not used for the child (editable installs would point elsewhere); instead install `ruff==0.17.1` and `mypy==2.4.0` plus the project dependencies non-editably from `git archive HEAD`, and run tests and mypy from the worktree with `PYTHONPATH` set to the worktree sources. The `blob` profile adds `azure-storage-blob==12.31.0` from `src/core/pyproject.toml` only when a module imports it. Synthetic `ZF_DATA` under the scratch directory; no private data, credential files or model calls.

Amended after critique: use separate scratch venvs `core-ci` (ruff, mypy, core only), `api-ci` (core, agents, API, dev tools) and `blob` (adds `azure-storage-blob==12.31.0`), and the same venv types on a parent export. Reuse hashes also cover `ranking.py`.

## Phase 3

* `git merge --no-ff --no-commit 99814198079c7c8fcd641497826986c706627b0f`, resolve the single conflict, `grep -rn '^<<<<<<<' src` is empty, commit as `merge: integrate frozen 1258 C6 parent 99814198`.
* Verify: `git rev-parse HEAD^2`; `git rev-parse HEAD:<path>` equals the qualified blob for the four paths; `git diff 99814198 HEAD -- src tools infra` lists only the own range paths.

## Phases 4 and 5

* Per project root `src/core` and `src/api`: `ruff check .`, `ruff format --check .`, `mypy` with the repository configuration; capture counts and the sorted diagnostics. Repeat in a clean `git archive 99814198` export for the parent baseline and diff the sorted diagnostics.
* Tests as in the plan, from `src/core` and `src/api` with the documented `PYTHONPATH`. Skips are reported as printed.

## Phase 6

`sha256sum` manifest of every log in a `SHA256SUMS` file beside them; for Azurite reuse, `git rev-parse HEAD:` for the four inputs compared with the recorded hashes and the emulator manifest check (`cd logs && sha256sum -c ../logs.sha256`).
