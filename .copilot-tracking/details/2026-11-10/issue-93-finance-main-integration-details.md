---
title: Issue 93 finance main integration details
description: Step-level commands and acceptance evidence for the bounded finance integration
ms.date: 2026-11-10
---

## Phase 2: merges

* `git merge --no-ff -m "merge: preserve finance-parent verification records (refs #93, #440)" test/demo-finance-parent-440-1110`, then `git merge --no-ff -m "merge: bring main 5318f738 into finance integration (refs #93)" 5318f738f6bc58a10a9d4df1ca18ae51c1547a79`. Both messages end with the Copilot co-author trailer.
* Expected: the first merge is a clean tracking-only addition; the second is predicted clean by `git merge-tree`. If a conflict arises, list `git diff --name-only --diff-filter=U`. Only `src/core/README.md` and `docs/reference/log.md` may be resolved, by keeping both sides in order. Any other path stops the loop with the exact conflict.
* Never cherry-pick, rebase, reset, amend or force.

## Phase 3: byte guards

* Product: `git rev-parse HEAD^1:<path>` blobs for the seven finance paths versus merged-tree blobs (README and log compared by content of the finance additions, since main also edited them).
* Main ownership: `git diff --stat 5318f738 HEAD -- . ':!.copilot-tracking' ':!docs/reference/log.md' ':!src/core/README.md'` lists only the five finance source and test paths; `server.py` and `test_form_staging_api.py` produce no diff.
* Verification records: `git diff ef63d180 HEAD -- <seven record paths>` empty.

## Phase 4: environment

* `python3 -m venv /tmp/issue93-finance-main-1110/venv`; install `src/build-requirements.txt` with `--require-hashes`; `pip install --no-deps --no-build-isolation -e src/core -e src/agents -e src/api`; install `ruff==0.17.1` and `mypy==2.4.0` from the project dev pins only. Further dependencies only after a recorded missing-dependency failure.
* Proof: each distribution's `direct_url.json` points at this worktree; `zava_forward.core.forms.__file__`, `form_review`, `form_export` and `zava_forward.api.server` resolve under the worktree; `git hash-object` of the selected test files equals the merged-tree blobs.

## Phase 5: observations

* A: from `src/core`, `python -m unittest -v` for the two history tests (names found with grep in `test_form_export.py`).
* B: from `src/core`, `python -m unittest tests.test_form_dependencies tests.test_form_review tests.test_form_review_pack tests.test_form_export tests.test_form_staging` (adjust to the project discovery form that resolves; record the invoked form).
* C: from `src/api`, `PYTHONPATH` unset, `python -m unittest tests.test_form_staging_api -v`, with the Core test helpers reaching it through the project's documented `../core/tests` path as the existing API guide states; record the exact working form.
* D: `python -m mypy` in `src/core` and in `src/api` with each project's own `pyproject.toml`. Raw adverse output is kept; failures are classified as caused by the parent delta, caused by main, or pre-existing before any action.
* E: `python -m ruff check` and `python -m ruff format --check` on the seven product paths from their project directories, honouring each project's excludes and ignores.
* Each unique test counts once; the overlap among A, B and C is declared when counts are summed.

## Phase 6: SQL

* Search the merged tree for MSSQL or SQL test modules touching form review, history or export and for `sqlguard` use with those names. If none, report absent. If one exists and the parent delta could alter its observed result, plan one nonqueued shared-heavy-resource admission with actual-holder inspection and an owned localhost disposable SQL service; never reuse another issue's database; no Azure fallback.

## Phase 7: evidence

* Changes record lists merge commit hashes, tree and blob inventory, command lines, exit codes, counts, skips, log SHA-256 values, environment identities and remaining limits. One Review assesses the exact head with the product path and blob inventory, ownership guards and unmet gates. Handoff goes to `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/handoff-93-finance-main-1110.md`.
