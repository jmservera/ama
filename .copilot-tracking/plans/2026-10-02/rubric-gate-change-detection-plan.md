<!-- markdownlint-disable-file -->

# Implementation Plan: rubric-gate-change-detection

* Task ID: 2026-10-02-rubric-gate-change-detection (child of 2026-10-02-rubric-score-gate)
* Evidence: .copilot-tracking/reviews/2026-10-02/rubric-score-gate-review.md (RV-001, RV-003, RV-004, RV-012)

## Executive Summary

Make deletions, renames out of scope and oversize files count as artifact changes so the score can drop (RV-001). Add a `force` input to manual dispatch for calibration runs that rescore every criterion from scratch, report only, and never open issues; restrict regression issues to `refs/heads/main` (RV-004). Correct the README on instrument changes, live criteria, AI credit caps, the setup PR run and the doubly pinned model (RV-003, RV-012).

## User Decisions and Requirements

* Owner selected follow-up 1: RV-001, RV-004 and README corrections from RV-003 and RV-012.
* Parent decisions OD-1 to OD-3 still apply.

## Goals

* G1 A PR that removes or hides scored evidence can lower the score.
* G2 Manual calibration runs are possible without side effects.
* G3 README matches behaviour.

## Scope and Non-Goals

* In scope: prepare.py, gate.py, test files, workflow source and recompiled lock, README.
* Non-goals: RV-002 context artifact, RV-005 to RV-011 hardening, instrument fingerprint redesign from RV-003 (README correction only).

## Functional Requirements

* FR-1 `prepare.py` parses `git diff --name-status -M` (PR: `base...HEAD`; other events: baseline commit to HEAD when resolvable) and adds every touched path matching an active artifact's include globs (including deleted and rename-source paths) plus oversize skipped files to that artifact's changed files and to `removed_files`.
* FR-2 Glob matching for diff paths treats `**/` as zero or more directories.
* FR-3 Agent context exposes `removed_files`; `changes.diff` covers removed paths; prompt tells the agent removed evidence is a change it may cite.
* FR-4 `workflow_dispatch` boolean input `force`; `prepare.py` and `gate.py` accept `--force`; forced runs score all criteria from scratch, skip comparison and carry-forward, are labelled calibration, and never open issues.
* FR-5 Issues for regressions or failures are opened only for `refs/heads/main` non-forced runs.

## Non-Functional Requirements

* NFR-1 Standard library only. NFR-2 Existing tests keep passing.

## Acceptance Criteria

* AC-1 New gate test: drop citing a removed path is accepted and fails the gate.
* AC-2 New prepare tests: name-status parsing (modify, delete, rename) and `**/` glob matching.
* AC-3 `gh aw compile` succeeds; lock contains the `force` input.
* AC-4 README states instrument-change behaviour, live criteria behaviour, separate detection credit cap, setup PR bootstrap run, and model pinned in two places.

## Phase Checklist

<!-- P01 -->
### [x] P01 Change detection and force mode

* [x] P01-T01 prepare.py: `glob_match`, `parse_name_status`, diff-based changed and removed files, oversize tracking, `force`
* [x] P01-T02 gate.py: `--force`, calibration label
* [x] P01-T03 Tests: gate deletion test; new test_prepare.py

<!-- P02 -->
### [x] P02 Workflow, prompt and README

* [x] P02-T01 Workflow: dispatch input, `--force` plumbing, main-only issues, prompt note on removed files; recompile
* [x] P02-T02 README corrections

## Follow-Up Items

* RV-002, RV-005 to RV-011 (carried from parent).
* RV-003 instrument fingerprint in latest.json.

## Critique Disposition

Critique: .copilot-tracking/reviews/plans/2026-10-02/rubric-gate-change-detection-plan-critique.md (Pass with changes, 11 findings, all applied directly).

| Finding | Applied change |
|---------|----------------|
| CC-001 | Non-PR diff base is the last commit that wrote latest.json on the trusted ref; unresolvable outside bootstrap fails closed |
| CC-002 | Removed paths unioned after the artifact-file intersection; fully removed artifacts stay changed |
| CC-003 | One regex `glob_match` used for both tracked files (`git ls-files`) and diff paths; exclude honoured; D/R rows classified |
| CC-004 | Oversize files count only when they appear in the diff |
| CC-005 | test_prepare.py builds temporary git repos and runs compute_state through evaluate for PR and push deletions |
| CC-006 | Force runs never write latest.json, are labelled calibration, publish returns early; force read through env; concurrency group includes event name |
| CC-007 | Three call sites updated; force context omits baseline scores; prompt calibration line |
| CC-008 | `--name-status -M -z` parsing |
| CC-009 | Diff uses `-D`; prompt points to `git show <base>:<path>` |
| CC-010 | Removed paths justify decreases only |
| CC-011 | AC-4 extended; README notes fix applies after merge |
