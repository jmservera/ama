<!-- markdownlint-disable-file -->
# Plan: issue #126 historical batch A/B log retention correction

* Task: `issue-126-retention-correction` (parent `issue-126-restart-followup`); date 2026-11-17; mode automatic
* Research: `.copilot-tracking/research/2026-11-17/issue-126-retention-correction-research.md` (Planning Readiness Ready)
* Phase details: `.copilot-tracking/details/2026-11-17/issue-126-retention-correction-phase-details.md`
* Critique: `.copilot-tracking/reviews/plans/2026-11-17/issue-126-retention-correction-plan-critique.md`
* Validation tier: focused. Basis: only `.copilot-tracking` Markdown/JSON changes; no application, test, gate, prompt, agent, skill, dependency or control file; no behavior-bearing instruction changes.

## Objective

Remove the false claim that parent batch A/B logs were lost, record the verified copies and results with exact source qualification, and keep every other limitation.

## Boundary

* Writes: `.copilot-tracking/**` only (the existing table in place, plus new dated artifacts). Earlier Reviews, research, plans and changes records stay unchanged.
* Historical logs are not new execution. No test, browser, SQL, Docker, scanner or gate run. No push, PR or retarget.

## Phases

* [x] P01 Research (witness `research-open`)
* [x] P02 (verdict Revise; PC-001, PC-002 applied directly) Plan, details, one critique (witness `plan-done`)
* [x] P03 Implement
  * [x] P03-T01 Write the changes record (witness `implement-start` before any table edit)
  * [x] P03-T02 Edit table line 332 in place and add a dated provenance clarification distinguishing inaccessible-to-worker from missing; name the superseded claim
  * [x] P03-T03 Verify hashes/results, links, diff scope; record results (witness `implement-done`)
* [x] P04 One original Review (witness `review-done`); commit locally (witness `commit-complete`)
