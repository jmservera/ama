# Changes: issue 1231 R12 alignment with parent 181a1c1bb

Date: 2026-11-06. Governing records: the R12 research, plan and critique in this folder set (committed in 1ce12ef78). Earlier R1 to R11 records and receipts are unchanged.

## Actions

* Normal no-ff merge of local parent 181a1c1bb5e83c2ce08a7663d0a2b9145e6fc85e into ae23c0d72. Preserved ref: backup/issue-1231-ae23-pre-r12-align. Conflicts in ranking_publication.py, store.py and tests/test_ranking_publication.py were resolved by hand.
* ranking_publication.py: adopted the parent's validated `_existing` and `_fsync_dir`; kept the child's O_EXCL unique stage, `_remove`, `ArchiveStorageError` and `stage_retained`. Order is write, flush, fsync, link, remove own stage, directory sync. An existing record is validated, and the directory is synced before it is returned. Dropped the merge's `tempfile` import. Updated the publish docstring.
* store.py: kept the child's OSError to ArchiveStorageError translation and stage_retained warning; added the parent's policy_signed in the audit detail and response body. The 503 wording changed from "Nothing was published" to "Publication could not be confirmed; a record already archived is reported as already published on retry".
* tests: kept the child's gated and spawn concurrent-writer tests; dropped the parent's duplicate race and fork tests; added tests for an unusable record at the final name, the sync-file/unlink-stage/sync-dir order, the existing-record directory sync and a post-commit directory-sync failure. Wiring test assertion updated to the new 503 wording.
* README: combined durability text.

## Critique dispositions applied

1. The edited-record test expects PublicationError and unchanged bytes. Applied.
2. Directory sync before returning an existing record. Applied.
3. Own stage removed before the final directory sync, stage_retained kept. Applied.
4. A post-link directory-sync failure is reported as "could not be confirmed"; no new state or audit path. Applied; the missing audit on that path is a residual.

## Checks (source-bound, PYTHONDONTWRITEBYTECODE=1, shared read-only /tmp/zf79venv, worktree src on PYTHONPATH; import origin printed from the worktree)

* core: `python -m unittest tests.test_ranking_publication tests.test_ranking_publication_runner` ran 63 tests, OK.
* api: `tests.test_ranking_publication_wiring` ran 17 tests, OK (logged tracebacks are expected negative probes).
* Ruff 0.17.1 check on changed files and all src/api: pass. Format check on three changed files: pass. store.py check: pass.
* mypy from src/core, external cache: no issues in 268 source files.
* git diff --check: clean. Ignored-inclusive status showed no ignored or untracked files.

## Not done

No FULL gate, SQL, browser, image, installed-package run, push, PR or retarget. Earlier receipts (r4, r7, r9, r11) are historical and do not cover this head.
