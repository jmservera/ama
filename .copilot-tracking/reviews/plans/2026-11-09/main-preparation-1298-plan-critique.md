<!-- markdownlint-disable-file -->
# Plan Critique: main-preparation-1298

* Critique run: single final-candidate critique, 2026-11-09, by the planning agent (not independent)
* Execution status: Complete
* Verdict: Approve with direct corrections
* Severity summary: High 0, Medium 1, Low 2

## Inputs

* Plan, details and research for main-preparation-1298; git facts C1 to C8; the approved independent Functional metadata (base-relative only).

## Findings

* PC-001 Medium: the proof must not rely on the unexecuted ancestry claims of the earlier review. Applied: Phase 3 runs ancestry and blob comparisons directly.
* PC-002 Low: the targeted regression name must come from the existing changes record, not memory. Applied in Phase 4.
* PC-003 Low: caches must stay out of the repository. Applied: cache directories point at the owned log directory.

## Verified

* Tools, workflows, README and `chatthreads.py` are untouched on main; trial merge-tree is clean; the selector premise still holds on main; pinned tool versions exist in an owned venv, so no installation is planned.

## Open

* Independent exact-head and current-base review, hosted CI and the full gate remain outside this lane.
