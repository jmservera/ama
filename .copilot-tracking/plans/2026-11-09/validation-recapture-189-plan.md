<!-- markdownlint-disable-file -->
# Issue 189 validation recapture plan (2026-11-09)

Research: [research](../../research/2026-11-09/validation-recapture-189-research.md). Details: [details](../../details/2026-11-09/validation-recapture-189-details.md). Critique: [critique](validation-recapture-189-critique.md). Refs #189 only. Parent cycle count: C1 of five spent, four remain; none spent or reset.

## Objective

One fresh, relevant capture, unchanged source, of the same selections as the SQL/main integration, with genuine raw producer stdout, stderr and exit files and a hash manifest kept outside the repository, and concise durable records inside it. Implement phase is validation only.

## Phases

* [ ] P1 Commit this research, plan, details, critique (one) and initial state before any capture (frozen).
* [ ] P2 Preconditions: clean tree; HEAD is the frozen record commit whose source tree equals `d985f1495`; local noreply identity; fetch and re-pin `origin/main` (any `src`, `infra`, `tools` change since `8d6f029ca` stops the work); `ZF_*` unset; module paths print under this worktree.
* [ ] P3 Capture, each producer separate with stdout, stderr and exit files, no pipe, in an owned directory outside the repository:
  * `src/api`: `test_simulator_admin`, `test_live_control`, `test_entra_authoritative`, `test_auth`, `test_content_standard`, `test_design_system`, `test_workspace_scripts`, `test_case_journey` (verbose, so every skip and reason is captured).
  * `src/core`: `test_priority_order`, `test_resident_decisions` (verbose; actual-SQL cases skip and stay unverified).
  * Chromium plus pinned axe: `python -m checks.simulator_control_browser_check --axe <asset>` (correct flags only).
  * `node --check` of `app.js` and `simulator-control.js`.
* [ ] P4 Hash manifest of every raw file, kept beside the logs; concise changes record with commands, versions, source and tree, counts, exits, each skip and denial; one original Review; final state.
* [ ] P5 Evidence-only commit proving `git diff --name-only d985f1495 HEAD` is only under `.copilot-tracking/` and `src`, `infra`, `tools` and `.github` trees are identical to `d985f1495`. Local freeze and handoff `handoff-189-validation-recapture.md`.

## Success criteria

* Every selected producer exit is recorded from its own file; a nonzero exit is a recorded failure, not waived.
* Skips are reported as unverified, never passed; the loss of the earlier raw logs is disclosed.
* Raw logs and hash manifest are retained and never deleted.

## Out of scope

Full API suite, full local gate (`rpi-checks --all`), SQL Server, Azure, model calls, deployment, assistive-technology acceptance, web-guidelines acceptance, push, PR, board, issue ticks, rebase, reset, stash, force, source edits, new cycle.

## Stop rule

A failure or an environment prerequisite gap is recorded with its cause and stops that check; no source correction is made.
