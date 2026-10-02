<!-- markdownlint-disable-file -->

# Implementation Plan: rubric-gate-calibration-context

* Task ID: 2026-10-02-rubric-gate-calibration-context (child of 2026-10-02-rubric-gate-docs-accuracy)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-gate-docs-accuracy-review.md (RD-001, RD-002)

## Executive Summary

Qualify the two prompt lines that assumed a baseline in calibration runs (RD-002) and add automated tests for the calibration context and `diff_base` (RD-001).

## Phase Checklist

<!-- P01 -->
### [x] P01 Prompt and tests

* [x] P01-T01 Prompt Inputs step 1 notes the baseline is empty in calibration; live-criteria rule covers bootstrap and calibration; recompile
* [x] P01-T02 test_prepare.py: force context withholds baseline; PR context `diff_base` equals merge base and lists removed files

## Acceptance Criteria

* AC-1 Tests pass. AC-2 Compile has 0 warnings.

## Critique Disposition

Critique not dispatched: two stated fixes from a review; recorded skip.
