<!-- markdownlint-disable-file -->

# Plan, Changes and Review: rubric-gate-push-test-head-parent

* Task ID: 2026-10-02-rubric-gate-push-test-head-parent (child of 2026-10-02-rubric-gate-diff-base-tests)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-gate-diff-base-tests-review.md (RT-001)

## Plan

* [x] P01-T01 Push `diff_base` test adds an unrelated commit after the delete so the expected base (last latest.json commit) differs from both HEAD and HEAD^.
* Critique: not dispatched (one-line test change restating RT-001's fix).

## Changes

* .github/rubric/scripts/test_prepare.py: `test_given_direct_push_when_context_written_then_diff_base_is_last_scores_commit` commits `docs/other.md` after the delete.

## Validation

* 38 passed, 1 skipped (symlink), minimal pytest stub.

## Review (one pass)

* Outcome: Conformant.
* RT-001 closed: the expected base is now HEAD~2. An implementation using HEAD gives an empty removed list and wrong base; one using HEAD^ gives the delete commit as base, whose diff to HEAD excludes the deletion, so both assertions fail.
* The optional second feature commit in the PR test was not added: the PR test already distinguishes the merge base from the `main` tip, which is the RC-001 risk; a HEAD^-based PR implementation is not a plausible variant because PR runs use the three-dot range.
* Open carry-over: RS-002 real pytest run.
