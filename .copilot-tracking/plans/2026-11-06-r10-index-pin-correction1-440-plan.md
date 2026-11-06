---
title: R10 index pin correction 1 plan
description: Plan for correcting one wrong short pin in the R10 index paragraph and appending a focused log entry
ms.date: 2026-11-06
---

## Task

Task ID `440-r10-index-pin-correction1`, slug `r10-index-pin-correction1-440`, parent `440-r10-design-checkpoint`. First correction of the new R10 checkpoint batch. Local only, documentation only. Research: `.copilot-tracking/research/2026-11-06-r10-index-pin-correction1-440-research.md` (disposition executed, readiness Ready). Details: `.copilot-tracking/details/2026-11-06-r10-index-pin-correction1-440-details.md`. Critique: `.copilot-tracking/plans/2026-11-06-r10-index-pin-correction1-440-critique.md`. Changes (written by implementation): `.copilot-tracking/changes/2026-11-06-r10-index-pin-correction1-440-changes.md`.

## Executive summary

`docs/reference/README.md` line 460 prints `1e199209` for the R10 design commit whose exact id is `1e19209985d93e053dd449e873e792f214dd110c`; the correct short pin is `1e192099`. The plan changes that one token, appends one focused log entry, and records an additive qualification of old R10 state and plan pending metadata in the new Changes record. No pack, source, requirement, ADR or design edit, no renumbering, and no rewrite of any existing record.

## User Decisions and Requirements

* Correct only the one index pin; pack and log exact pins are already correct (root assessment r68).
* Append a focused log entry noting the correction; no new checkpoint, renumbering or broad canonical repair.
* Preserve byte-identical all 38 existing batch tracking records (31 prior plus 7 R10), original and adverse RPI, and prior log text.
* Qualify old R10 state and plan pending metadata additively; do not rewrite originals.
* Local only: no push, PR, merge, issue, board, tick, deletion, rebase or retarget. Eventual 136 published topology stays unresolved and is not an owner question.
* The Review runs after the focused checks and Changes in a later completed turn; state is written after Review in one atomic sequential edit.
* Do not claim the new records are original prior passes; this cycle corrects a current frozen pin and does not backfill phases.

## Goals

* The README R10 pin equals the first eight characters of the exact R10 commit id.
* The correction is traceable in the append-only log.

## Scope and Non-Goals

Scope: one README token; one log entry; new RPI records. Non-goals: the older unresolved log anchor, source, tests, requirements, ADRs, design, pack, state or plan rewrites.

## Functional Requirements

* FR1 Replace `1e199209` with `1e192099` in `docs/reference/README.md`, once.
* FR2 Append one log entry stating the old pin, the new pin, the exact commit id and that nothing else changed.

## Non-Functional Requirements

* NFR1 ASCII, `*` lists, no em dashes; new Markdown has frontmatter and no H1.
* NFR2 Append-only log; pack and earlier README text unchanged.
* NFR3 Commit identity is the repository-local noreply address for author and committer, Conventional message with the Copilot trailer, no amend.

## Acceptance Criteria

* AC1 `1e199209` is absent from the README and appears in `docs/` only inside the one new log entry that quotes it as the corrected old token; `1e192099` matches the first eight characters of the exact commit id; every other hash token in the corrected README paragraph (`bb3a3b03`) matches the pins.
* AC2 `git diff --check` exits 0; README diff is one line; log diff is additions only; pack diff is empty.
* AC3 All 38 existing batch tracking records are byte-identical to the start head.
* AC4 New records pass frontmatter, ASCII and JSON parse checks; fresh main and governance pins recorded; ignored-inclusive status clean at freeze.

## Phase Checklist

* [ ] P1 Correct the index pin and append the log entry
* [ ] P2 Run focused checks
* [ ] P3 Record Changes, run the later author Review, finalize state and commit

## P1 Correct the index pin and append the log entry

* [ ] P1-T1 Edit the README token (FR1).
* [ ] P1-T2 Append the log entry (FR2).

## P2 Run focused checks

* [ ] P2-T1 Run the checks in AC1 to AC4 and capture exact commands and exits; limit them to documentation and Git checks, with no test, SQL, browser, container, model or provider execution.

## P3 Record Changes, Review, state and commit

* [ ] P3-T1 Write Changes after the checks, with the additive qualification of old R10 state and plan pending metadata.
* [ ] P3-T2 Write the author Review in a later completed turn after the checks and Changes.
* [ ] P3-T3 Write the state JSON once after Review, then commit and verify ignored-inclusive clean status.

## Follow-Up Items

* Eventual published topology for `feat/infra-hosting-integration-136` is unresolved before code publication; not in scope.
* Older unresolved log anchor `eighth-stabilization-checkpoint-finance-parent-held...` is unrelated and untouched.
* The earlier R10 critic's full critique-skill load is unverified and is not invented here.

## Critique Disposition

One independent critique ran (verdict Revise, 0 Critical or High, 1 Medium, 2 Low). Skill files actually read by the critic: SKILL.md and the critique template. All findings are applied directly; no user decision is needed and no second critique runs.

* PC-001 Medium, applied: AC1 restated (above) so the old token is permitted only inside the new log entry; details P2-T1 grep step follows it.
* PC-002 Low, applied: AC1 now also checks the other hash tokens in the corrected paragraph.
* PC-003 Low, applied: one commit carries the README edit, the log entry and the new task records (planning records are already committed earlier in a separate planning commit before the canonical edit).
