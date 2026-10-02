<!-- markdownlint-disable-file -->

# Changes: rubric-gate-diff-base-tests

* .github/rubric/scripts/test_prepare.py: PR `diff_base` test now commits to `main` after branching (RC-001); new `test_given_direct_push_when_context_written_then_diff_base_is_last_scores_commit` (RC-002)

## Validation

* 38 passed, 1 skipped (symlink), minimal pytest stub. Real pytest run (RS-002) still pending.
