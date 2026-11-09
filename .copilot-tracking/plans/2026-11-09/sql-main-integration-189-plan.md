<!-- markdownlint-disable-file -->
# Issue 189 SQL/main integration plan (2026-11-09)

Research: [research](../../research/2026-11-09/sql-main-integration-189-research.md). Details: [details](../../details/2026-11-09/sql-main-integration-189-details.md). Critique: [critique](sql-main-integration-189-critique.md). Parent: C1 (cycle 1 of five TOTAL spent, four remain; an integration without a real fix neither resets nor consumes a cycle). Refs #189 only.

## Objective

Merge actual `origin/main` `8d6f029ca` (#1308, all 19 hosted checks green on its squash) into `feat/demo-simulator-control-189-1109` with an ordinary `--no-ff` merge preserving both intents, finalize App/Store/admin composition using the existing controls (read-only administrators default-deny every mutation; Stop in every readable and writable state; manual and unavailable routes), and verify the impacted surface. No new feature.

## Phases

* [ ] P1 Commit this prospective research, plan, details and critique (one) before any merge, merge edit or check (frozen).
* [ ] P2 Preconditions: clean tree, HEAD is the frozen record commit (child of `0972a40cb`), repository-local noreply identity, fresh `git fetch` and re-pin of `origin/main`. Run `git merge --no-ff origin/main`. No rebase, reset, stash, force or sibling import. Resolve only genuine conflicts keeping both intents; an unresolved intent conflict stops the work and is reported.
* [ ] P3 Pin actual differences: `git diff 0972a40cb HEAD -- src infra tools` and prove the 13 #189 `src/api` paths are byte-identical to pre-merge except the files main also changed (`server.py`, `app.js`, `test_case_journey.py`, which are compared to each side by `git diff` against both parents).
* [ ] P4 Composition check (read-only first): `do_POST` order CSRF, view-only gate, simulator hook, ordinary routes keeps #1308 `CommittedReloadError` handlers after the gates; `do_GET` simulator prelude and `#/simulator` route do not touch `priorityPanel`.
* [ ] P5 Selected checks (owner demo-targeted tier), nonqueued, producer exit recorded without pipes, worktree-bound imports in an owned `mktemp -d` directory:
  * `src/api`: `test_simulator_admin`, `test_live_control`, `test_entra_authoritative`, `test_auth`, `test_content_standard`, `test_design_system`, `test_workspace_scripts`, `test_case_journey` (carries #1308 priority route and app.js DOM harness).
  * `src/core`: `test_priority_order`, `test_resident_decisions` (SQLite/JSON; actual-SQL cases skip and stay unverified).
  * Browser: Chromium plus pinned axe 4.10.3 `simulator_control_browser_check --axe <verified asset>` 11 states (view-only default-deny, Stop in expired, invalid, already-stopped, stale and permitted, manual and unavailable paths). Missing Chromium or axe makes validation BLOCKED.
  * Web guidelines: `app.js` changed upstream; refetch `web-design-guidelines` source and review the merged web files only if the integrated `app.js` or `simulator-control.js` region differs from reviewed content (records the fetch or its failure).
  * Inherited SQL/Azure test variables are unset before each run. If `origin/main` has moved from `8d6f029ca`, stop and report. Whole API suite only if a selected failure or the composition check shows actual integration risk; not a docs-only rerun. No ruff/mypy unless source needs a change.
* [ ] P6 Changes record, one original Review over the integration delta, final state, local evidence commit, coordinator handoff `handoff-189-sql-main-integration.md`.

## Success criteria

* Clean worktree; merge commit parents are the frozen record commit and `8d6f029ca`; no resolution edits unless recorded.
* All selected checks have producer exit 0, or each failure is recorded as a blocker with its cause and not waived.
* Historical records untouched (adverse reviews, C1, approve 0 on `8ab64519c`, F3 cause UNKNOWN, capture 2105/365 producer 0).
* Known SQL skips reported as unverified, never passed.

## Out of scope

Push, PR, board, issue tick, rebase, owned SQL Server (no #189 SQL path), matrix, SMB, cloud, model calls, budget alert, release, new source feature.

## Stop rule

A confirmed new defect records its scope and the cycle count before any fix, and stops for authorization if the fix expands scope.
