---
title: Issue 1231 plan r6 (retained-stage wording accuracy)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written 2026-11-06 about 14:13Z, after the r6 Research file was completed and before any edit, test or check in this continuation. Task id `issue-1231-r6-stage-wording`. Research: `.copilot-tracking/research/2026-11-06/issue-1231-r6-stage-wording-research.md` (disposition `executed`, readiness `Ready`). Earlier records, including the R5 files and their qualifications, are unchanged.

## Executive summary

Two sentences claim a retained staging file is always a hard-link alias of the archived record. That is true only for the successful publisher. A concurrent loser's unlinked stage can hold a different `published_on`. The plan replaces both claims with conditional wording and changes nothing else.

## Identity

* Branch `fix/ranking-archive-concurrent-writer-metadata`, head `e5486018168b0cccb281e06be2fc156934a8bb2b`, tree `831f520a1bc1ebf24c26afaeab4fc51d9b756014`. Parent #79 local `43080ab42a96fada36b9d0bc523dfa16fe0c3cd5`. Target is that parent. Main provenance `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`.

## User Decisions and Requirements

* Make the wording conditional and conservative (for example "may share the archived record's bytes and inode, so do not edit it").
* Do not change outcomes, return keys, error handling, dates, audit or the storage contract. Add no abstraction or behavior. README only if directly necessary (Research: not necessary).
* Do not add tests of constant warning text. The existing loser regression already exercises the case.
* Light validation only. No FULL, SQL, browser, container, image, scanner or install. Existing shared venv and unpinned tools, if used, are attributed as such.

## Goals

* The two sites no longer assert a false alias for the loser.

## Scope and Non-Goals

* In scope: docstring line 13 of `src/core/src/zava_forward/core/ranking_publication.py`; warning text at `src/core/src/zava_forward/core/ranking_publication_runner.py:357-359`.
* Out of scope: helper logic, `store.py`, `server.py`, README, tests, other findings.

## Functional Requirements

* The warning keeps its code `stage_not_removed`, the stage name, the committed-record statement and the remove-by-hand action.

## Non-Functional Requirements

* ASCII only, no em dashes, line length within the Ruff limit, no `.copilot-tracking` references in source.

## Acceptance Criteria

* Neither site contains an unconditional "hard-link alias" claim.
* Existing cleanup, concurrent-loser, runner and Store/API error regressions pass unchanged.
* Ruff check, Ruff format check and mypy on the edited ranking files exit 0.
* Old tracking blobs are unchanged from the start state (blob hash comparison).

## Phase Checklist

* [ ] P01 Edit the two wording sites (details P01).
* [ ] P02 Run planned focused checks once, after both edits finish (details P02).

## Follow-Up Items

* Real unsupported-hard-link mount test (unchanged from R5).
* Final combined FULL, independent whole-feature review, hosted CI and publication stay with the coordinator.

## Critique Disposition

One independent critique ran (`.copilot-tracking/plans/2026-11-06/issue-1231-r6-stage-wording-critique.md`), verdict Pass.

* PC-001 no issue: wording covers both outcomes, scope surgical. Disposition: accepted, no plan change.

## Handoff

After the critique dispositions are applied the prospective Research, Plan, Details and critique are committed alone. Then P01 and P02, Changes, a separate author Review, state, and the closing commit follow.
