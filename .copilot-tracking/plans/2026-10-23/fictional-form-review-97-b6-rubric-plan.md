<!-- markdownlint-disable-file -->

# Implementation Plan: fictional-form-review-97-b6-rubric

| Field | Value |
| --- | --- |
| Task ID | 97-b6 (additional cycle 1 of at most 4) |
| Date | 2026-10-23 |
| Research | .copilot-tracking/research/2026-10-23/fictional-form-review-97-b6-rubric-research.md |
| Details | .copilot-tracking/details/2026-10-23/fictional-form-review-97-b6-rubric-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-23/fictional-form-review-97-b6-rubric-plan-critique.md |
| Changes | .copilot-tracking/changes/2026-10-23/fictional-form-review-97-b6-rubric-changes.md |

## Executive Summary

Reviewer finding B6 is a mismatch inside the bot-generated rubric score. No supported local or deterministic fix exists, and hand editing generated output is forbidden. The plan rebases the clean branch onto fresh main, records the finding, root cause and options honestly, and hands a narrow blocker to the coordinator: a fresh automatic rescore after publication, or a coordinator-approved removal of the two bot commits. No source, score or fixture content changes. B6 is recorded as an unresolved generated-output blocker, not fixed. A rescore is supported but not guaranteed (model-nondeterministic, tracking-only pushes may be path-ignored, the paid run and push are outside this run). Readiness: Ready after the single critique disposition.

## User Decisions and Requirements

* Owner: up to 4 more cycles then ask; this is cycle 1 for #97 only, stop early on PASS, ask before a fifth.
* Do not hand-edit generated rubric output, spoof evidence or approval, weaken runtime validation, hide adverse review, or invent a deterministic fix. If unavailable tooling is needed, return evidence and a narrow blocker.
* Rebase the idle clean branch onto fresh origin/main preserving remote commits and append-only logs; do not touch the PR 441 worktree or session.
* No heavy gate, push, PR update or merge. Commit with privacy-safe noreply identity, Conventional Commit and Copilot trailer.
* Finance FD-01..FD-14, template authority, binding and OQ-015 stay unresolved; criterion 1 unmet, criterion 2 delivered by PR 377; issue stays open.

## Goals

* A clean rebased candidate with honest tracking of B6 and a scheduled complete-gate plan.

## Scope and Non-Goals

* In scope: rebase, tracking artifacts, focused read-only checks.
* Non-goals: latest.json content, README or fixture edits, runtime, rubric scripts, workflow, other worktrees, unrelated inherited failures (the 21 local rubric-script test failures are recorded only).

## Functional Requirements

* FR-1: Branch based on f1e2d830 with all prior issue and bot commits and log entries intact.
* FR-2: Changes and review records state B6 as unresolved, with cause, options and owner.

## Non-Functional Requirements

* ASCII, `*` bullets, no fabricated approval, evidence or gate claim.

## Acceptance Criteria

* AC-1: latest.json at HEAD is byte-identical to a74652aa (git diff a74652aa HEAD -- .github/rubric/scores/latest.json is empty), proving no hand edit; B6 recorded as unresolved.
* AC-2: git status --short --ignored is empty after commit; focused checks recorded with real commands and counts.
* AC-3: The complete-gate plan names the ordered commands: commit tracking, fetch main, python3 tools/rpi-checks.py --all --base <fresh origin/main> --out <new external dir> --lock-timeout 0, then --verify-receipt <receipt> --base <current origin/main>. Any later commit, base move or dirty input invalidates it; a lock timeout is a blocker.

## Phase Checklist

* [x] P01 Rebase onto fresh main and verify lineage
* [x] P02 Record findings, validate and commit (commit follows the Review, which is recorded in the review log)

## Follow-Up Items

* B6 resolution (coordinator or owner): rescore, drop the bot commits (force-with-lease), or accept as a recorded residual; also a gate.py follow-up issue so rationale and evidence mismatches are detected. 21 failing local rubric-script tests (unrelated, uninvestigated, not run by rpi-checks.py by text search).
* Publication method: the rebase rewrote published SHAs, so a push needs owner-authorized force-with-lease; alternative is reset to a74652aa and merge origin/main.

## Critique Disposition

Single critique executed before implementation; verdict Revise; none repeated.

| ID | Disposition |
| --- | --- |
| PC-001 | Accepted. Rebase and rubric pytest ran before this plan; disclosed in the changes record. |
| PC-002 | Accepted. Publication method recorded as coordinator or owner decision (force-with-lease or reset plus merge). |
| PC-003 | Accepted. Rescore reworded as supported but not guaranteed, with stop-and-escalate if B6 mismatches again. |
| PC-004 | Accepted. Exact command and counts recorded; gate coverage checked by text search; not fixed here. |
| PC-005 | Accepted. Options extended with caveats, accept-as-residual and gate.py follow-up. |
| PC-006 | Accepted. Gate sequence in AC-3. |
| PC-007 | Accepted. AC-1 and AC-2 rewritten to verify outcomes. |
