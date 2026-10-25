# Changes: seed merge default database path correction (issue 360)

Date: 2026-10-25. Order followed: research, plan and details, independent critique (PASS), then edits. Origin: coordinator MEDIUM finding on 2799f236, which my own tests and review had missed because every CLI test set `ZF_SQLITE` and `ZF_STATE`.

* `factory.py`: new `sqlite_path(env)` (same resolution as before); `open_store` uses it.
* `seed_merge.py`: for the sqlite store, resolves the target with `sqlite_path` from the caller's environment and sets `ZF_SQLITE` before the empty `ZF_DATA` override. MSSQL settings, explicit `ZF_SQLITE`, `ZF_STATE` and `ZF_DIGEST_DIR` pass through unchanged.
* Tests (`test_seed_merge.py`): default-path merge updates the original database and creates no temporary database; state-only and explicit-path cases; `sqlite_path` resolution; MSSQL env receives no `ZF_SQLITE`. The default-path test errors on the 2799f236 `seed_merge.py` (verified by temporarily restoring it) and passes with the fix.
* Local result: `test_seed_merge` plus `test_sqlstore` 39 OK. 2799f236 gate result does not cover this head.
* `src/core/README.md`: one sentence stating the sqlite target resolution (added after review finding 1 below).

## Independent review (code-review agent, one record)
Verdict PASS-WITH-FINDINGS. Code meets the requirement and the reviewer ran 39 tests OK. One Medium finding: the planned README sentence was missing from the diff and the changes record. Fixed by adding the sentence and listing it above. The reviewer also reported an accidental stash that was restored with the same seven staged files; I rechecked status afterwards. The fix was not re-reviewed (one review per task).

## Gate cycle 1 failure and fix (recorded honestly; 5c06bc16 receipt is a failed receipt, retained)
Full gate on 5c06bc16 (`/tmp/ama-360-live/gate-seedcorr-5c06bc16`, runner PID 831300) blocked at project-core: ruff E501 (23 errors) and ruff format on `seed_merge.py` and `test_seed_merge.py`, plus strict mypy (115 errors). My earlier local runs used unittest only, so lint and type checks were first run by the gate. Everything else the gate ran passed, including the API container checks. Fix, with no behaviour change: formatted and wrapped lines, typed `seed_merge.py` and the test module (`SeedMergeBase` now a `TestCase` so mypy resolves `addCleanup`), and added the repo's existing `disallow_untyped_calls = false` mypy override entry for the two modules (the untyped legacy store boundary). Local: ruff check, ruff format check and mypy clean; 39 tests OK. This lint and type defect also applies to the parent 2799f236 candidate, whose gate would fail the same way.
