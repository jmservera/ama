<!-- markdownlint-disable-file -->

# Implementation Plan: rubric-gate-diff-base-tests

* Task ID: 2026-10-02-rubric-gate-diff-base-tests (child of 2026-10-02-rubric-gate-calibration-context)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-gate-calibration-context-review.md (RC-001, RC-002)

## Phase Checklist

<!-- P01 -->
### [x] P01 Tests

* [x] P01-T01 PR `diff_base` test advances `main` after branching so the merge base differs from the `main` tip (RC-001)
* [x] P01-T02 New push test: `diff_base` is the last commit that wrote latest.json (RC-002)

## Acceptance Criteria

* AC-1 Tests pass and would fail if `diff_base` used the `main` tip or HEAD.

## Critique Disposition

Critique not dispatched: test-only change restating review fixes; recorded skip.
