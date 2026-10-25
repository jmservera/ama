# Changes: seed merge default database path correction (issue 360)

Date: 2026-10-25. Order followed: research, plan and details, independent critique (PASS), then edits. Origin: coordinator MEDIUM finding on 2799f236, which my own tests and review had missed because every CLI test set `ZF_SQLITE` and `ZF_STATE`.

* `factory.py`: new `sqlite_path(env)` (same resolution as before); `open_store` uses it.
* `seed_merge.py`: for the sqlite store, resolves the target with `sqlite_path` from the caller's environment and sets `ZF_SQLITE` before the empty `ZF_DATA` override. MSSQL settings, explicit `ZF_SQLITE`, `ZF_STATE` and `ZF_DIGEST_DIR` pass through unchanged.
* Tests (`test_seed_merge.py`): default-path merge updates the original database and creates no temporary database; state-only and explicit-path cases; `sqlite_path` resolution; MSSQL env receives no `ZF_SQLITE`. The default-path test errors on the 2799f236 `seed_merge.py` (verified by temporarily restoring it) and passes with the fix.
* Local result: `test_seed_merge` plus `test_sqlstore` 39 OK. 2799f236 gate result does not cover this head.
* `src/core/README.md`: one sentence stating the sqlite target resolution (added after review finding 1 below).

## Independent review (code-review agent, one record)
Verdict PASS-WITH-FINDINGS. Code meets the requirement and the reviewer ran 39 tests OK. One Medium finding: the planned README sentence was missing from the diff and the changes record. Fixed by adding the sentence and listing it above. The reviewer also reported an accidental stash that was restored with the same seven staged files; I rechecked status afterwards. The fix was not re-reviewed (one review per task).
