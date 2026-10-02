<!-- markdownlint-disable-file -->

# Changes: rubric-gate-symlink-tests

* .github/rubric/scripts/prepare.py: `classify_changes` now treats every in-scope diff path that is not currently scorable as removed (covers symlink replacement, type change, delete, rename-out, oversize); artifact state no longer carries the redundant `oversize` list.
* .github/rubric/scripts/test_prepare.py: registry in the temp repo uses `max_file_bytes` 1000; new tests for rename within scope, type change, PR hiding by delete, rename-out, growth and symlink (self-skips if symlinks are unavailable), and push detection after `--no-ff` and `--squash` merges.

## Validation

* 36 test cases pass (minimal pytest stub; pytest download blocked on this host). The symlink case may self-skip on Windows without symlink privilege; it runs on Linux CI.

Correction (2026-10-02, follow-up rubric-gate-docs-accuracy): the symlink case did not run on this host (WinError 1314) and no CI workflow runs pytest, so the "runs on Linux CI" claim was wrong. The test now calls `pytest.skip` and reports as skipped.
* `get_errors`: no errors. Workflow unchanged, no recompile needed.
