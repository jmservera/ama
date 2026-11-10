# Plan: parent73 CLI component integration with current main

Task ID: `issue-73-cli-integration-1109`. Date 2026-11-09. Research: `.copilot-tracking/research/2026-11-09/cli-integration-73-1109-research.md` (disposition `executed`, readiness `Ready`). Details: `.copilot-tracking/details/2026-11-09/cli-integration-73-1109-phase-details.md`. Changes record: `.copilot-tracking/changes/2026-11-09/cli-integration-73-1109-changes.md`.

## Executive Summary

Merge current main (`3bc20719...`) into the owned parent branch (`a4317567...`) with an ordinary merge commit, then verify the combined source: importer suite, exact importer-project mypy, Ruff, and separate-process synthetic CLI scenarios. The research found disjoint deltas (parent: importer plus tracking; main: Core AI/sensor, API, docs), unchanged Core exception contracts and no API to importer edge, so a clean merge and no source change are expected. This is a partial CLI component integration only: #73 and whole #135 stay open, #80/#84/#122 dependencies stay retained, the register stays `NOT_CONNECTED`. Nothing is pushed or written to GitHub.

## User Decisions and Requirements

* Parent #73 partial CLI component integration only; no whole-epic or whole-#135 acceptance.
* Branch `feat/demo-exception-workflows-73-1109` from owned parent `a4317567...`; target main `3bc20719...`; work in this worktree only.
* Ordinary merge of current main after Plan and Implement activation; no rebase, force, reset, amend. Resolve only understood conflicts preserving both intents.
* No new feature/refactor, no budget/role/identity/schema change. Only README precision and a genuinely needed tiny importer compat fix after a red repro.
* Do not edit Core, API, shared hooks, exception_register, navigation, roles; do not hide `NOT_CONNECTED`. Ownership: #132 C5, #1238, #891, #153.
* Dependencies #80/#84/#122 are not waived or removed; whole/served holds retained. Stop precisely if a technical dependency or unrelated parent work appears.
* Verification: fresh venv with this worktree's Core+Importer; no `PYTHONPATH`; pip only actual missing deps; no SQL Server, browser, model, network, Azure or full gate. Local SQLite journal allowed.
* Prior child exact review (APPROVE, 0 findings) is not re-executed. Cycle: parent 0/5 to 1/5; child C2 of 5 is separate and not reset.
* Identity: GitHub noreply author/committer and Co-authored-by trailer on every commit including the merge. No issue/board/PR/push writes. PR (later, not now) `Refs #73`/`Refs #135` only.
* Handoff file: coordinator `files/handoff-73-cli-integration-1109.md`.

## Goals

* Combined parent+main tree whose importer CLI behaves as reviewed, with execution evidence.

## Scope and Non-Goals

* In: merge, verification, tracking artifacts, README precision if verification shows an overclaim.
* Out: Core/API/store/register/server changes, served queue, recovery, replay, correction, access control, SQL Server, hosted CI, publication.

## Functional Requirements

* FR1: ordinary merge commit with two parents `a4317567...` and `3bc20719...`.
* FR2: importer unchanged by the merge except understood conflicts; none expected.
* FR3: CLI scenarios (below) hold in separate processes.

## Non-Functional Requirements

* NFR1: all commits carry the resolved noreply identity and trailer.
* NFR2: evidence reports real commands, exits, skips and raw owner/SHAs.

## Acceptance Criteria

* AC1: `git merge-base --is-ancestor` holds for both pins against final head; no rebase/force.
* AC2: 71 importer tests pass (32 CLI/exception plus existing); affected Core exception feed/queue tests pass.
* AC3: importer-project mypy (`src` and `tests`) and Ruff format/check clean at pinned tool versions.
* AC4: scenarios pass: refusal persists across reopen; basename/replacement/hashless/unreadable identity; first-reason dedupe; DB open/write error exit 2 versus refusal exit 1; read-only viewer leaves DB and source hashes stable; missing steward shows Unassigned/Unknown.
* AC5: `git diff` for the merge touches no Core/API/hook/register/navigation/roles file beyond what main brought; register still reports `NOT_CONNECTED`; no API to importer dependency; no replay/correction.

## Phase Checklist

* [x] P01 Pre-merge qualification (identity, ownership, clean tree, venv)
* [x] P02 Merge current main into parent
* [x] P03 Verification of combined source
* [x] P04 Tracking, handoff and clean frozen state

## Critique Disposition

One critique executed (Complete, verdict Revise): `.copilot-tracking/reviews/plans/2026-11-09/cli-integration-73-1109-plan-critique.md`. All findings are direct planner corrections applied in the phase details; no user decision needed; no second critique.

| ID | Disposition |
| --- | --- |
| PC-001 | Accepted: P03-T03 now has a scenario table with construction, exit and oracle |
| PC-002 | Accepted in effect: venv, scratch script and data live in the session files directory (outside the repo), not in the index; the brief has no /tmp rule, so this is a hygiene choice |
| PC-003 | Accepted: literal commands, cwd, pass criteria, version and path proof; package index is the only network use, offline is a blocker |
| PC-004 | Accepted: merge by SHA with `-m` message and trailer, no fetch, identity post-check |
| PC-005 | Accepted: both path-set diffs with expected sets, concrete grep patterns, Core register tests |
| PC-006 | Accepted: precondition is no tracked modification plus the named untracked RPI artifacts; merge first, commit tracking in P04; collision check before merge |
| PC-007 | Accepted: research C2 corrected; focused-tier classification recorded |
| PC-008 | Accepted: absolute handoff path; red outside importer compat scope means stop and report, no history rewrite |

Validation tier classification: focused tier plus the planned local checks. This branch edits no workflow, dependency manifest, Dockerfile, infra, SQL or security control; main brings `.github/rubric/scores` and a mypy-override line in Core `pyproject.toml`, which this branch does not author. Hosted CI, independent exact-head review and human approvals remain required.

## Follow-Up Items

* Served queue, register hook, store transport, recovery and scoped operator access remain with #132 shared integration and whole #135.
