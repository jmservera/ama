<!-- markdownlint-disable-file -->
# Issue 189 current-main preparation plan (2026-11-09)

Research: [research](../../research/2026-11-09/current-main-prep-189-research.md). Details: [details](../../details/2026-11-09/current-main-prep-189-details.md). Critique: [critique](current-main-prep-189-critique.md). Parent: C1 (cycle 1 of five TOTAL spent, four remain; this ordinary source-preserving preparation does not reset or spend a cycle). Refs #189 only.

## Objective

Locally merge `origin/main` `9f9aacc8b` into `feat/demo-simulator-control-189-1109` with an ordinary merge commit, preserving every #189 and main intent, then confirm the directly impacted surface and record the exact remaining #1292 integration. Not final: Store/current-SQL integration and publication wait for #1292 on actual main.

## Phases

* [ ] P1 Commit this prospective research, plan, details, critique and state before any merge (frozen).
* [ ] P2 Verify merge preconditions (clean tree, head pinned to the frozen prospective-record commit whose parent is `8ab64519c`, repository-local committer email), run `git merge --no-ff origin/main` (no rebase, reset, force, stash, squash, sibling import). Resolve only genuine conflicts preserving both intents; if an intent conflict is unresolved, stop and report.
* [ ] P3 Pin actual post-merge source differences against pre-merge head (`git diff 8ab64519c HEAD -- src infra tools`) and prove #189 files are byte-identical to the pre-merge head (`git diff 8ab64519c HEAD -- <12 #189 src/api paths>` empty).
* [ ] P4 Selected checks, worktree-bound imports, each producer exit recorded without pipes, shared resources nonqueued (`flock -n` only for heavy work; none expected): default-deny read-only-admin mutation, Stop all readable writable states, manual/disabled paths through `test_simulator_admin`, `test_live_control`, `test_entra_authoritative`, `test_auth`, `test_content_standard`, `test_design_system`, `test_workspace_scripts`, browser 11-state check. If source differs unexpectedly, extend to the impacted tests only. Missing Chromium or pinned axe makes validation BLOCKED, not passed.
* [ ] P5 Changes record, one original Review (independent, source-level, over the merge delta), final state, local commit of evidence, coordinator handoff `handoff-189-current-main-preparation.md`.

## Success criteria

* Clean worktree, merge commit with parents the frozen prospective-record commit (a direct child of `8ab64519c`) and `9f9aacc8b`, no conflict-resolution edits to #189 or main content unless recorded.
* Historical records untouched: original review and adverse findings, C1 records, F3 cause UNKNOWN, capture 2105/365 producer 0.
* Remaining #1292 plan lists the exact files, selectors and re-run needs, without guessing SQL behaviour.

## Out of scope

Push, PR, board, issue changes, rebase, whole 2105-test API rerun (docs-only/non-impacting integration), full matrix, live SMB, cloud, model calls, budget alert acceptance, new source features, any C2 source fix.

## Stop rule

A real new blocking bug found by the selected checks stops the work for scoped authorization before any source expansion; it is recorded and not fixed here.
