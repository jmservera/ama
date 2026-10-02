<!-- markdownlint-disable-file -->

# Implementation Plan: rubric-gate-docs-accuracy

* Task ID: 2026-10-02-rubric-gate-docs-accuracy (child of 2026-10-02-rubric-gate-symlink-tests)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-gate-change-detection-review.md (RG-003 to RG-007); .copilot-tracking/reviews/2026-10-02/rubric-gate-symlink-tests-review.md (RS-001)

## Executive Summary

Make calibration runs blind to the baseline in context and prompt (RG-003), give each forced dispatch its own concurrency slot (RG-004), correct README statements on live criteria and issue creation (RG-005, RG-006), expose a usable `diff_base` for reading deleted files (RG-007), and make the symlink test report as skipped with a corrected change log (RS-001).

## Phase Checklist

<!-- P01 -->
### [x] P01 Context, workflow, prompt, README and test

* [x] P01-T01 prepare.py: force mode withholds the whole baseline; context adds `diff_base` (merge base for PRs, scores commit otherwise)
* [x] P01-T02 Workflow: per-run concurrency group for dispatch; prompt uses `diff_base` and forbids reading the scores file in calibration; recompile
* [x] P01-T03 README: live-criteria instrument exception, issue wording, calibration blindness and concurrency
* [x] P01-T04 test_prepare.py: `pytest.skip` for unavailable symlinks; change-log correction

## Acceptance Criteria

* AC-1 Tests pass with the symlink case reported as skipped on this host. AC-2 Compile has 0 warnings. AC-3 Force-mode context has empty baseline and a `diff_base`.

## Critique Disposition

Critique not dispatched: each task restates a reviewed finding's stated fix; recorded skip.
