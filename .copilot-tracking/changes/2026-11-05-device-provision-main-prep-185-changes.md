---
title: Changes for #185 current-main preparation
ms.date: 2026-11-05
---

* Ordinary no-ff merge of pinned origin/main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` into the child; no conflicts, no source edits by this task. Merge result is the only code-path change; the provisioning command is unchanged.
* Light checks from `src/core` using `/tmp/v185` (Python 3.12.3, ruff 0.17.1, mypy 2.4.0): imports resolve to this worktree (`src/core/src/zava_forward/core/synthetic/device_provision.py` and `device_identity.py`); `unittest discover -p "test_device_*.py"` ran 45 tests, OK, no skips; `ruff check --no-cache .` passed; `ruff format --no-cache --check .` 215 files formatted; `mypy --cache-dir=/tmp/mypy-185-prep` (strict, src and tests) no issues in 268 files. Exit codes for the test, format and mypy lines were observed through a trailing `tail`, so the output text is the evidence.
* Not run: FULL gate, focused-refresh gate, heavy runner, browser, SQL, Docker, scans, Azure, provider calls, other suites, package installation.
* Missing: FULL evidence, independent exact-head review, hosted CI for the merged head, human approval. PR 1205 contexts predate this merge.
