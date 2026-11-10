---
title: Issue 440 finance-parent verification changes
description: Actual commands, exits, counts and identities from the local observation of finance head 4642b55f
ms.date: 2026-11-10
---

Plan: [plan](../../plans/2026-11-10/issue-440-finance-parent-verification-plan.md). Critique: [critique](../../reviews/plans/2026-11-10/issue-440-finance-parent-verification-critique.md). No product, test, config or shared-document file changed. Raw logs are external under `/tmp/440fv-1110/` (SHA-256 below).

## Identities

* HEAD `4642b55fdbafec564b67803420439b91d7ea8ce1`, tree `e2628422d13ae87df3a6b7ecfdd12f24a4fc1052`, unchanged before and after; `git diff <pin> -- src docs infra tools .github skills-lock.json` empty; `git status --ignored` showed only this task's tracking records (no egg-info or caches).
* Main pin `ddeebd01694ddb46b456451d9ac6390347e51aaa`, tree `b917297ef34bc3e7e7948f9e46ffe6b7e66e6c88`, read only.
* Selected files equal the pin: `test_form_export.py` `e958edb7`, `test_form_staging_api.py` `f12fb157`, core `pyproject.toml` `ab7bf1f9`.

## Environment

* Interpreter `/tmp/440fv-1110/venv/bin/python`, Python 3.12.3. Ambient installs of core, api and agents point at the primary checkout and were NOT used.
* Network use: `pip install --require-hashes -r src/build-requirements.txt` (setuptools 84.2.1, packaging 26.3, wheel 0.48.0), then `--no-deps --no-build-isolation -e src/core -e src/agents -e src/api`. No other package acquired.
* Owned distributions: `zava-forward-{core,agents,api}` 0.1.0, editable, `direct_url` file URLs inside this worktree; `zava_forward.__path__` lists only this worktree's three `src/*/src/zava_forward`. Resolved `__file__`: core `forms`, `form_review`, `form_export`, `api.server`, and the five core test modules plus `dataset` under this worktree. API run also resolved `tests.test_form_staging_api` and `tests.test_mvp` in `src/api/tests` and `test_form_staging`, `dataset` in `src/core/tests`.
* Env: `PYTHONPYCACHEPREFIX` and `ZF_DATA` pointed at `/tmp/440fv-1110`; no private dataset read; no SQL Server, model, provider or browser.

## Observations

| Id | Working dir and path | Command | Exit | Result | Log SHA-256 |
| --- | --- | --- | --- | --- | --- |
| A | `src/core`, `PYTHONPATH=src:tests` | `unittest -v test_form_export.FormExport.test_export_carries_ordered_detached_review_history ...test_history_is_integrity_covered_and_legacy_copy_is_invalid` | 0 | ran 2, ok 2, skipped 0 | `99ab4ab5ec87...` |
| B | `src/core`, same | `unittest -v test_form_staging test_form_review test_form_review_pack test_form_export test_form_dependencies` | 0 | ran 67, ok 67, skipped 0, 23.3 s | `b49a010ef80f...` |
| C | `src/api`, `PYTHONPATH=../core/tests:../agents/tests` | `unittest -v tests.test_form_staging_api` | 0 | ran 7, ok 7, skipped 0, 6.5 s, loopback `127.0.0.1`, JSON plus SQLite temp store, inference patched to fail | `dac71fbeb7a2...` |

No failure occurred; nothing was rerun. No type or lint check selected. Counts are from these runs only.

## Cleanup

The editable install left no files in the worktree. The external directory `/tmp/440fv-1110/` remains as the evidence store and is not committed.

## Deviations

None from the details. Network use was limited to the pinned hashed build tools as critiqued.
