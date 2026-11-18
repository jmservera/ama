<!-- markdownlint-disable-file -->
# Plan: issue #126 prior retention-process qualification

* Task: `issue-126-process-qualification` (parent `issue-126-retention-correction`); date 2026-11-17; mode automatic
* Research: `.copilot-tracking/research/2026-11-17/issue-126-process-qualification-research.md` (Planning Readiness Ready)
* Phase details: `.copilot-tracking/details/2026-11-17/issue-126-process-qualification-phase-details.md`
* Critique: `.copilot-tracking/reviews/plans/2026-11-17/issue-126-process-qualification-plan-critique.md`
* Validation tier: focused. Basis: only `.copilot-tracking` Markdown/JSON; no behavior-bearing instruction or control change.

## Objective

Qualify the false opening-order sentence of the previous retention research and its status, without altering history, and recheck the retained-log facts.

## Boundary

* Writes: `.copilot-tracking/**` only; the existing table gains one dated section. Earlier research, critiques, Reviews and witness logs stay unchanged.
* No test, browser, SQL, Docker, scanner or gate run; no push, PR or retarget. Prose detector unavailable in confinement (disclosed).

## Phases

* [x] P01 Research (witness `research-open`, done first)
* [x] P02 (verdict Revise; PC-001, PC-002 applied directly) Plan, details, one critique (witness `plan-done`)
* [x] P03 Implement
  * [x] P03-T01 Write the changes record; witness `implement-start` before any table edit
  * [x] P03-T02 Add the dated section to the table
  * [x] P03-T03 Verify and record results; witness `implement-done`
* [x] P04 One original Review (witness `review-done`); local commit (witness `commit-complete`)
