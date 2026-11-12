<!-- markdownlint-disable-file -->
# Plan: accuracy follow-up for the post-153 checkpoint (2026-11-12)

* Task ID: `post153-integration-440-1112-accuracy`; parent `post153-integration-440-1112`; session `d351ddc0-f4e6-4e5f-ae56-db0937d3ad2b`; branch `docs/post153-integration-checkpoint-440-1112` from `8bfd52729048bc7c94b4d266188307f1d9bc213c`.
* Research: .copilot-tracking/research/2026-11-12/post153-integration-440-1112-accuracy-research.md (disposition `executed`, Planning Readiness `Ready`).
* Details: .copilot-tracking/details/2026-11-12/post153-integration-440-1112-accuracy-phase-details.md. Critique: .copilot-tracking/plans/2026-11-12/post153-integration-440-1112-accuracy-critique.md. Changes: .copilot-tracking/changes/2026-11-12/post153-integration-440-1112-accuracy-changes.md.

## Executive summary

Correct four factual statements in the new post-153 pack section by documentation edits only: the five-id search boundary (C1), the tracking-file counts (C2), the merge ordering of PR 1470 and 1475 against PR 1478 (C3) and the overbroad ARIA statement (C4). Add an append-only accuracy note, an index sentence only if the pointer changes materially, and a log entry. The original seven artifacts, original review, original adverse critique and raw evidence stay byte-identical, and no count, pin or conclusion changes. One independent critique runs once.

## User Decisions and Requirements

* Strictly bounded documentation-accuracy follow-up, additive RPI with `-accuracy` names; not the exhausted #440 coordinator/HVE/source campaign and not a new correction pool.
* No product, test, tool, workflow, instruction, approval or requirement edit; no issue creation, browser, SQL, cloud, model, live call, deployment or spending; do not fix the assistants.js accessibility concern.
* Preserve original artifacts byte-for-byte; do not reclassify the original review or erase its mistakes; record original errors and corrected interpretation.
* Correct exactly four claims (C1 to C4); the 145 executed, 92 skipped counts and the `4074b44f3` pin remain; no test rerun.
* Requirement-qualified positive coverage remains partial; no invented mapping or approval; proposed acceptance gates do not bar independent source work or constitute an owner decision.
* Check diff, links and exact original-artifact equality; one new clean local commit with resolved privacy-safe identity and Copilot trailer; no amend, rebase, push, PR or merge.
* Stop with the exact gap if broader scope is needed.

## Goals

* The pack section states only what the evidence supports for C1 to C4, and the corrections are visible as corrections.

## Scope and Non-Goals

* In scope: the new pack section, an append-only note in it, the log, the index only if material, the additive `-accuracy` artifacts.
* Non-goals: every item in the user decisions above; editing earlier pack sections or earlier log entries.

## Functional Requirements

* FR-1: the five-home paragraph states the actual boundary (runbook and web source read by the script; a tracked-file search finds one historical tracking record; not reproduced; no deployment claim).
* FR-2: the accuracy note gives the observed tracking-path counts (20 for PR 1470, 7 for PR 1475) and states that the original 16 and 19 were wrong and PC-007 was not fully applied.
* FR-3: the opening and the note state that PR 1470 (17:38:13Z) and 1475 (17:46:55Z) merged before PR 1478 (18:00:25Z), after the historical tested pin `bbb1d20cc`, and were excluded from the #1478 evidence.
* FR-4: F1 is narrowed to the specific `pre` and implicit-generic accessible-name concern, static and unverified, with no fetched standard, web review, conformance claim or confirmed defect.

## Non-Functional Requirements

* Plain ASCII, `*` lists, no em dashes, relative links, append-only log, no `.copilot-tracking` references in docs outside the evidence line already used by the log convention.

## Acceptance Criteria

* AC-1: `git status --short` and `git diff --stat 8bfd52729` list only the pack, the log, `docs/reference/README.md` (index sentence repeating C3, PC-002) and new `-accuracy` tracking files (untracked files included, PC-005).
* AC-2: the seven original tracking blobs equal `original-blobs-before.txt` (raw file in the external evidence folder).
* AC-3: `git diff` on the pack touches only the section opening, the five-home paragraph, F1, the original-evidence line that said all nine findings were applied (PC-001) and the appended note, and leaves counts and pin text unchanged.
* AC-4: relative links in changed docs resolve; the commit is the only new commit and the tree is clean.

## Phase Checklist

<!-- Marker: documentation edit phase -->
* [x] P01: Correct the pack section (dependency: critique disposition)
  * [x] P01-T01: Replace the "No other public tracked file" sentence with the actual boundary (FR-1)
  * [x] P01-T02: Qualify the section opening and add the append-only accuracy note covering C2, C3 and the original errors (FR-2, FR-3)
  * [x] P01-T03: Narrow F1 (FR-4)
* [x] P02: Log, index decision and verification
  * [x] P02-T01: Append the log entry; decide the index (the existing pointer still describes the section; add nothing unless the critique shows otherwise)
  * [x] P02-T02: Verify AC-1 to AC-4 and record the changes record
* [ ] P03: Review and commit
  * [x] P03-T01: One Review record
  * [ ] P03-T02: Commit locally with the resolved identity and trailer (marker left open until the commit exists; the commit hash is recorded in the state and final report)

## Follow-Up Items

* Owner decision on F1 and any independent source work remains with the existing owners (#153, #132, #134); not part of this plan.
* A runbook five-home test (F3) and the browser check (F2) remain open and unauthorised here.

## Critique Disposition

One critique ran (verdict Revise, six findings PC-001 to PC-006, all planner-applicable, no user decision). Critique file: .copilot-tracking/plans/2026-11-12/post153-integration-440-1112-accuracy-critique.md. No second critique.

* PC-001 (High): applied. The pack's process-limits line "all applied directly" is amended in place and AC-3 now allows it.
* PC-002 (High): applied. The index sentence repeating the C3 ordering error is corrected (README, two lines).
* PC-003 (Medium): applied. Earlier log entries stay unchanged; the new entry states that it corrects the entry above.
* PC-004 (Medium): applied the same way; the new entry narrows the role-less wording from the earlier entry.
* PC-005 (Medium): applied. AC-1 and the verification use `git status --short` so untracked files are seen.
* PC-006 (Low): applied. The C1 sentence names the commit and the areas not searched (untracked, ignored, `support/`).
