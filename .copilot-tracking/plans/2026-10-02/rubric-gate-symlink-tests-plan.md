<!-- markdownlint-disable-file -->

# Implementation Plan: rubric-gate-symlink-tests

* Task ID: 2026-10-02-rubric-gate-symlink-tests (child of 2026-10-02-rubric-gate-change-detection)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-gate-change-detection-review.md (RG-001, RG-008)

## Executive Summary

Generalise change classification so any in-scope path touched by the diff that is not currently scorable (deleted, renamed away, symlink, oversize, type change) counts as removed (RG-001), and add tests for rename within and out of scope, type change, oversize growth, symlink replacement, and push detection after merge-commit and squash merges (RG-008).

## User Decisions and Requirements

* Owner selected follow-up 1: RG-001 and RG-008.

## Goals, Scope and Requirements

* FR-1 `classify_changes(entries, include, exclude, files)` returns (in-scope touched paths in `files`, in-scope touched paths not in `files`).
* FR-2 Tests listed above; symlink case self-skips where the host cannot create symlinks.
* Non-goals: RG-002 to RG-007, RG-009, RG-010.
* AC-1 All tests pass; AC-2 no workflow change required.

## Phase Checklist

<!-- P01 -->
### [x] P01 Classification and tests

* [x] P01-T01 Generalise `classify_changes`; drop the unused oversize bookkeeping from artifact state
* [x] P01-T02 Add classification, hiding and merge-style tests

## Follow-Up Items

* RG-002 to RG-007, RG-009, RG-010, RV-002, RV-005, RV-006, RV-009, RV-010.

## Critique Disposition

Critique not dispatched: two-task change fully specified by RG-001's stated fix and RG-008's listed gaps; recorded as a deliberate skip under the one-pass rule (zero critiques, not a second one).
