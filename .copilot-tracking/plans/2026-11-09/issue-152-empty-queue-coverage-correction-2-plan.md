<!-- markdownlint-disable-file -->

# Implementation Plan: issue-152-empty-queue-coverage-correction-2

| Field | Value |
|---|---|
| Task ID | issue-152-empty-queue-coverage-correction-2 |
| Date | 2026-11-09 (prospective, written before source edits) |
| Parent | correction 1 and original task (preserved unchanged) |
| Research | .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-2-research.md |
| Details | .copilot-tracking/details/2026-11-09/issue-152-empty-queue-coverage-correction-2-phase-details.md |
| Critique | .copilot-tracking/challenges/2026-11-09/issue-152-empty-queue-coverage-correction-2-critique.md |
| Changes | .copilot-tracking/changes/2026-11-09/issue-152-empty-queue-coverage-correction-2-changes.md |
| Tier | focused |

## Executive Summary

Correction 1 added a two-line comment to `app.js` that contains the word "provenance", which the repository content audit bans in audited web files. The coordinator's focused gate recorded the resulting single API-suite failure. The fix removes that nonessential comment. Behaviour, the fail-closed unknown-coverage copy, the audit and all earlier evidence are untouched. The existing audit test is the check: it fails on the old comment (reproduced at the candidate head) and must pass afterwards. This is correction 2 of a partial slice (`Refs #152`); no AC-034/043, WCAG, accessibility, live or user claim is made. The failed receipt remains adverse evidence and no heavy or browser gate is run here.

## User Decisions and Requirements

* Correct only the demonstrated failure; prefer removing or rephrasing the nonessential comment.
* Preserve fail-closed unknown behaviour, semantics and accessible UI; do not weaken the audit, add a bypass, change executable behaviour, invent a metadata source or broaden scope.
* Run the exact audit plus lightweight queue/unit and syntax checks; record commands, versions, exits; show fail-before and pass-after without editing old evidence.
* Focused tier; stop for reassessment on any full-tier category.
* Web guidelines before edit and refreshed before review; report `file:line`.
* No `--changed`, full gates, browser, SQL, Docker. Commit scoped changes with repo-local privacy-safe identity, Conventional Commit, `Refs #152`, Copilot trailer. No push, PR, rebase.

## Goals

* Make the content audit pass for `app.js` without changing behaviour.

## Scope and Non-Goals

* In scope: delete the comment at `src/api/src/zava_forward/api/web/app.js` immediately above `queueEmptyExplanation`; correction 2 artifacts.
* Non-goals: audit, test files, README, producer, schema, SQL, other issues, heavy gates.

## Functional Requirements

* FR1: `queueEmptyExplanation` source and behaviour are byte-identical apart from the removed comment.

## Non-Functional Requirements

* No banned internal term is introduced; no UI, live-region, keyboard, motion or copy change.

## Acceptance Criteria

* AC1: `tests.test_content_standard.CopyAudit.test_no_internal_terms_in_web_copy` fails at the candidate head with the line 462 violation and passes after the change.
* AC2: `tests.test_queue_empty_state` and `tests.test_content_standard` (whole module) pass; `node --check` exits 0.
* AC3: `git diff` of source shows only the two removed comment lines.
* AC4: no old artifact, test or receipt is modified; verified with `git diff --numstat -- src` (only app.js, 0 insertions, 2 deletions) and `git show --stat --name-status HEAD` listing only app.js and correction 2 artifacts.

## Phase Checklist

<!-- P01 -->
### [x] P01: Remove the comment and validate

* [x] P01-T01 Delete the two comment lines above `queueEmptyExplanation`.
* [x] P01-T02 Run the audit before the edit (record command, head SHA, non-zero exit) and after (exit 0), queue test, content module, node check, diff check; record in changes.
* [x] P01-T03 Commit and report head and tree; refresh web guidelines in Review.

## Dependencies and Risks

* Risk: other audited-file violations unseen; mitigated by running the whole content-standard module. Heavy gates stay with the coordinator.

## Critique Disposition

Critique executed once, verdict Revise, 0 Critical/High, 1 Medium, 2 Low; all applied directly, no user decision, no second critique.

| ID | Severity | Disposition |
|---|---|---|
| PC-001 | Medium | Applied: P01-T02 now runs the audit before the edit and records command, head SHA and exit in the changes file, then after the edit. |
| PC-002 | Low | Applied: AC4 names `git diff --numstat -- src` and `git show --stat --name-status HEAD`. |
| PC-003 | Low | Applied: this table records the dispositions. |

## Follow-Up Items

* Coordinator: fresh exact-head changed gate, browser selector, independent review, hosted checks; preserve the adverse receipt.
* Owner decision on a trusted coverage producer (original F1).
