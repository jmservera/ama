---
title: Issue 440 finance-parent verification details
description: Exact commands and acceptance evidence for each phase
ms.date: 2026-11-10
---

## Phase 2 environment

```text
python3 -m venv /tmp/440fv-1110/venv
/tmp/440fv-1110/venv/bin/python -m pip install --require-hashes -r src/build-requirements.txt
/tmp/440fv-1110/venv/bin/python -m pip install --no-deps --no-build-isolation -e src/core -e src/agents -e src/api
```

Evidence: `pip list`, each distribution's `direct_url.json` pointing at this worktree, `zava_forward.{core,agents,api}.__path__` and the `__file__` of `forms`, `form_review`, `form_export` and `api.server`. Editable-install metadata and egg-info written inside `src/*` must be checked against `git status` and, if untracked and ignored, recorded (not removed from tracked content).

## Phase 3 commands (from `src/core`, `PYTHONPATH=src:tests`, cache redirected with `PYTHONPYCACHEPREFIX`)

```text
python -m unittest -v test_form_export.FormExport.test_export_carries_ordered_detached_review_history test_form_export.FormExport.test_history_is_integrity_covered_and_legacy_copy_is_invalid
python -m unittest -v test_form_staging test_form_review test_form_review_pack test_form_export test_form_dependencies
```

The test class and method names are verified with a read-only `grep` before execution; a mismatch is reported, not edited.

## Phase 4 command (from `src/api`, `PYTHONPATH=../core/tests:../agents/tests`)

```text
python -m unittest -v tests.test_form_staging_api
```

Precondition: the module imports with no new third-party installs. Loopback address only, `ThreadingHTTPServer` on `127.0.0.1`, synthetic JSON and SQLite in a temporary directory, inference patched to fail.

## Acceptance

* Every command's exit status, ran/skipped/failed counts, interpreter version and path are recorded.
* Selected test files' blob hashes equal the finance pin's blobs.
* Final `git status --short` is empty (apart from tracking records), and `git diff <pin> -- src docs infra tools` is empty.
