---
title: Agentic workflow detection runs tracker (issue 1086) assessment
description: Read-only assessment on 2026-11-18 of the auto-managed "[aw] Detection Runs" issue, classifying its 113 warning comments, and what remains
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 1086
  - gh-aw
  - threat detection
  - rubric scorer
estimated_reading_time: 5
---

## Scope and method

Read-only `gh` queries on 2026-11-18 (this repository). No workflow, Azure or source change. The issue is a tracker created by GitHub Agentic Workflows (gh-aw), marked "Do not close this issue manually" and "No action to take". It has no acceptance-criteria checklist; its only checkbox is the ticked auto-expiry marker (`gh-aw-expires` 2026-12-04T15:59:12Z).

## Findings

* State: OPEN, created 2026-11-04, last comment 2026-11-18T07:00:31Z, 113 comments. All 113 are from one workflow, "Capstone Rubric Scorer" (`.github/workflows/rubric-score.lock.yml`), each with conclusion `warning` and reason `agent_failure`.
* Cause: classifying the runs behind all 113 comments gives 108 `cancelled` (80 push to `main`, 28 pull request), 3 `failure` (push to `main`) and 2 `success`. In the cancelled run inspected (44255138229) the `detection` job succeeded while `agent` and `activation` were cancelled. `rubric-score.md` sets `concurrency` with `cancel-in-progress: true`, so a newer push cancels the older run and the tracker records the missing agent result as a detection warning. This is a concurrency artefact, not a detected threat (no prompt-injection, secret-leak or malicious-patch reason appears in any comment).
* Activity: comments per day peaked on 2026-11-04 (40), 2026-11-13 (15) and 2026-11-14 (23), tracking bursts of merges. The last Rubric Scorer runs on `main` after 07:00Z 2026-11-18 produced no new comment.
* Related: the 3 genuine failures belong to the rubric recording gate tracked separately in #1397 (open, last updated 2026-11-10). The latest pull-request failure at 2026-11-18T07:15:30Z (`rubric/baseline-refresh`) is outside this tracker's comments.

## Still needed?

The tracker is working as designed and needs no action; it will expire on 2026-12-04 unless gh-aw refreshes it. It is useful only as noise evidence: it shows 108 of 113 warnings are cancellations. Do not close it manually.

## Remaining and follow-up

* Optional, owner decision, not done here: change `rubric-score.md` (and recompile the lock file) so cancelled agents do not raise detection warnings, or set `threat-detection` options. This is a workflow edit and was excluded from this task, and it would need the FULL validation tier.
* Keep #1397 as the owner of genuine scoring failures.
* Re-check after 2026-12-04 for expiry.

## Per-criterion record

| Criterion | Status | Evidence |
| --- | --- | --- |
| Expiry marker `[x]` (only checkbox) | Observed; raw output not retained | Issue body shows ticked `gh-aw-expires` 2026-12-04T15:59:12Z; auto-managed, not a deliverable |
| Any unticked acceptance criterion | None exist | Issue body has no acceptance list; demo-specific Azure, browser and sign-in proofs are not applicable (no UI or Azure behaviour involved, none used) |
