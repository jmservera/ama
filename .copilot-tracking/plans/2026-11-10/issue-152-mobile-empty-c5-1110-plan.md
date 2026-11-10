<!-- markdownlint-disable-file -->

# Implementation Plan: issue-152-mobile-empty-c5-1110

| Field | Value |
|---|---|
| Task ID | issue-152-mobile-empty-c5-1110 |
| Research | .copilot-tracking/research/2026-11-10/issue-152-mobile-empty-c5-1110-research.md |
| Details | .copilot-tracking/details/2026-11-10/issue-152-mobile-empty-c5-1110-phase-details.md |
| Critique | .copilot-tracking/challenges/2026-11-10/issue-152-mobile-empty-c5-1110-critique.md |
| Changes | .copilot-tracking/changes/2026-11-10/issue-152-mobile-empty-c5-1110-changes.md |
| Tier | targeted DEMO; Refs #152 and 149 only; C5 of 5 |

## Acceptance criteria

* AC1: `own_queue_empty_failures` rejects vertical clipping of `li.empty` (own and ancestor clip) with a distinct message, without requiring the page to fit one viewport.
* AC2: a constructed clipped-height negative (`height:12px; overflow:hidden`) fails for the clipping reason, the exact original inline style is restored in `finally`, and the helper then passes; the display:none negative remains.
* AC3: the served harness passes at 320, 390 and 1280 for all seven roles; all prior assertions remain.
* AC4: recipe SHA in scenario-manifest.json equals the harness bytes; Core manifest, needs-inventory and generator-coverage tests pass.
* AC5: affected API tests, strict mypy, Ruff check and project format pass.
* AC6: evidence wording states 15 empty-queue and 6 populated-queue observations; C4 records unchanged; no overclaim.

## Phases

* P01: implement the helper change, second negative, README qualification, recipe SHA, log entry (see details).
* P02: run the targeted checks and record raw outputs.
* P03: single Review; commit; witness; handoff.

## Critique Disposition

Critique executed once; compatible findings PC-001 to PC-003 applied directly (see critique artifact).
