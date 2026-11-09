<!-- markdownlint-disable-file -->
# PR 1295 recovery phase details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/pr-1295-cxo-story-recovery-plan.md).

## Phase 2 checks

* Success: 7 Node source contracts and 9 navigation tests pass; deck source figures equal main; 54 slides and 54 PDF pages; cited source locators resolve.
* Missing prerequisite: `pwsh` for the PowerShell Build/Verify, cost-status and source-hash scripts. Record as not run; do not infer from `validation.json`.

## Phase 3 decision rule

Correct only a confirmed contradiction between a deck claim and current source that is directly coupled to the claim. `ama-mentor-deck` does not match this capstone deck scope. Any fix must use the existing builder and focused tests and keep every protected value.

## Phase 4

Write changes, review, state and a handoff. Commit with a Conventional Commit, the trailer and the repository-local noreply identity.
