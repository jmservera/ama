# Issue 1258 main preparation re-pin addendum (2026-11-09)

Refs #1258. Additive prospective addendum to `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-main-prep-plan.md`. Written and committed before any merge. It is not a second critique and not a correction cycle.

## Trigger

The pre-merge re-fetch required by PC-MP-1 found `origin/main` moved from the pinned `9f9aacc8be6a1b0e9a10efd367d1ea8bd7520939` to `ba5cc74b8b717957b046fd1d28804a989a7f3dd7`. The plan's stop rule fired and no merge was made at that point (the guarded merge command did not run; HEAD stayed `c292024138d2f57ef5b2615d6e2775dcc958335a`).

## Evidence

* `git log 9f9aacc8b..origin/main`: one commit, `ba5cc74b8 chore(rubric): record score 78/100`.
* Delta: one modified path, `.github/rubric/scores/latest.json` (+45/-56). It is a generated score record (data), not a workflow, permission, action pin, image, package, secret, deployment or gate-semantics file. Classification by actual impact: data record, no executable behavior.
* PR 1308 still OPEN, `mergedAt` null; #1292 remains excluded.

## Decision (planner-owned, ordinary preparation)

* New immutable pin: `ba5cc74b8b717957b046fd1d28804a989a7f3dd7`. Same re-fetch equality guard applies; if main moves again before the merge, stop and report.
* Expected merge delta against the pre-merge HEAD is now the 36 pinned paths plus `.github/rubric/scores/latest.json` (37 paths, ours-vs-main path overlap none).
* Equivalence claim narrows to `src`, `infra`, `tools` trees (identical object IDs) and to `.github` except `.github/rubric/scores/latest.json`; verified by listing `git diff --name-only <approved-HEAD> <merge>` over `.github` and requiring only that one path.
* All other plan stop conditions, tier, unique output paths and unmet criteria are unchanged.
