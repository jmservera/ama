<!-- markdownlint-disable-file -->
# Plan: issue-1294-validation-policy-correction-c3

* Task ID: issue-1294-validation-policy-correction-c3 (bounded correction C3, parent: issue-1294-validation-policy-correction-c2)
* Base: HEAD bd63b22c0b5405ae00f7cbe4d511db30446ab556, tree e2e237d18922d13addd15df735bdff69b22713da; origin/main fa7ae0c9770e890f82482456bfcb8e97f1e05429
* Research: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c3-research.md
* Details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c3-phase-details.md
* Changes record (implementation owns): .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-correction-c3-changes.md

## Executive Summary

Three confirmed findings from the independent review of bd63b22: (1) the behavior loop stopped at Revise with untested post-grade edits, (2) the C2 log entry overstates the tested revision, (3) the direct employee acceptance command omits its runner PYTHONPATH. Plan: fix 3 in src/README.md, append (not rewrite) a log correction for 2, then run a fresh full independently designed, simulated and graded behavior test on the resulting wording; if grading finds confirmed contract defects, correct them in one batch and run one more fresh full test, with at most two post-fix attempts, otherwise report the exact blocker. Focused tier; proxy profile (host cannot bind subagent models); no hosted CI claim.

## User Decisions and Requirements

* Fix only confirmed requirement or evidence defects, not cosmetic preferences; confine grading to the issue contract and label cosmetic observations nonblocking.
* Direct acceptance command gets its required PYTHONPATH from src/api and its three-test, zero-skip contract; verify discovery read-only with and without the path; no browser claim.
* Append a correction to docs/reference/log.md identifying the earlier tested state and the actual result; never rewrite earlier entries.
* Fresh full hve-builder-tester run (independent design, simulation, grading) on actual candidate wording, retain-sandbox on every attempt, proxy label, no Pass fabrication; Deferred/blocker if a stage is unavailable or bounded attempts fail.
* Preserve all prior evidence, sandboxes 2 and 3, reports 1-3 and tools/__pycache__; delete nothing; no push, PR, rebase or cleanup.

## Goals

* Make the guide's direct employee acceptance command executable as written and equal to the runner contract.
* Make the knowledge-base log truthful about which revision was behavior-tested.
* Reach a genuine, honestly labeled behavior verdict on the frozen wording.

## Scope and Non-Goals

* In scope: src/README.md, docs/reference/log.md (append), C3 tracking evidence, sandbox 4+ and report 4+.
* Non-goals: workflow, tool, source, SQL, infra, Docker, installs, branch protection, cosmetic rewrites, reuse of report 3 grades.

## Functional Requirements

* FR1 Direct acceptance bullet uses PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests (runner and CI path) and states three tests, zero skips.
* FR2 Appended log entry names tested state (HEAD 7260826 plus pre-grade C2 diff, report 3) versus post-grade edits not re-simulated, and the actual result (Revise).
* FR3 Full behavior run(s) per hve-builder-tester with fresh designer, executor and grader.

## Non-Functional Requirements

* Read-only Python probes with PYTHONDONTWRITEBYTECODE=1; ASCII; workspace-only outputs; no filesystem-root search.

## Acceptance Criteria

* AC1 README acceptance command line carries the path and contract; probe outputs recorded with exits.
* AC2 Log has an appended C3 correction and a later outcome entry; git diff shows no changes to earlier lines.
* AC3 Report 4 (and 5 if needed) exist with actual verdict; no Pass unless an independent grader returns Pass on the frozen wording with no post-grade edit.
* AC4 diff-check, link, ASCII, stale-phrase checks exit 0.
* AC5 Prior artifacts, sandboxes and pycache intact; tier recorded focused.

## Phase Checklist

<!-- rpi:phase P01 -->
* [x] P01 Guide and log corrections
  * [x] P01-T01 README acceptance command (FR1)
  * [x] P01-T02 Append log correction (FR2)
<!-- rpi:phase P02 -->
* [x] P02 Validation and behavior loop
  * [x] P02-T01 Focused checks, command-discovery probes
  * [x] P02-T02 Behavior attempt(s) (FR3)
<!-- rpi:phase P03 -->
* [x] P03 Reconcile, Review, commit
  * [x] P03-T01 Changes record, Review, commit

## Critique Disposition

| ID | Severity | Disposition |
|---|---|---|
| PC-001 | High | Applied: freeze and terminal rule, cap two attempts, defect criterion (details P02-T02). |
| PC-002 | Medium | Applied: log correction now states C2 facts only; C3 outcome appended after the verdict. |
| PC-003 | Low | Applied: probe loads the three test IDs. |

## Follow-Up Items

* Host model binding for subagents (proxy limitation) remains a residual limitation.
