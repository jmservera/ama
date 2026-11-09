---
title: Issue 1259 final parent integration research
description: Prospective research for merging the frozen 1258 SQL main-integrated parent into the 1259 path-health child
ms.date: 2026-11-09
---

## Disposition

Research executed 2026-11-09 (rpi-agent, Sonnet 5.5) before this task's plan, details, critique, merge or any source edit. Planning Readiness: Ready. Order for this task: Research, Plan and Details, one Critique (all committed), then merge, validation, changes, one Review, state.

## Pinned identities

* Child worktree `/home/azureuser/source/ama-demo-wt/issue-1259-recovery`, branch `fix/ranking-archive-path-health`, clean, frozen HEAD `5ed86a6a7f799aa7c2bc574f8f101a56fb30fdda` (source `7fc680d0e`, Azurite record commit on top).
* Exact frozen parent `9b1e2567c2d0a2173b562103cd27508f75181526`, tree `b88cc90f4a4dd48a51b15e526b734e975fa036c5`, branch `fix/ranking-archive-ancestor-durability` (clean in worktree `issue-1258-blob`). Parent is the local main-8d integration: it contains c5 `52f9b61bb` and fetched main `8d6f029cac004506953f36606862168bbe9d9412` (both verified ancestors). Handoff read: `handoff-1258-sql-main-integration.md` (coordinator session files). The merge uses the SHA, never the branch name.
* Fetched `origin/main` is now `ef28d4da42d83b111d48f14df9b70e3c4932a477`, newer than the parent's main-8d. Main reconciliation beyond the parent is not in scope and is not imported here.
* Declared PR target is the parent topic `fix/ranking-archive-ancestor-durability`, not main. Nothing is pushed.

## Budget

One of five review-correction cycles is spent on 1259 (the parent c5 integration, source `7fc680d0e`); four remain. No renewal or reset. This integration is expected to be a pure merge. A source edit is made only for a probed, concrete failure and would consume cycle 2.

## Merge relationship (read-only)

* Merge base of child and parent is c5 `52f9b61bb`. Child ahead 14 commits, parent 11.
* Child source delta over c5: `ranking_publication.py`, `ranking_publication_runner.py`, `test_ranking_archive_blob.py`, `test_ranking_publication_runner.py`, `src/api/tests/test_ranking_publication_wiring.py` (plus tracking records).
* Parent delta over c5 in `src/`: `server.py`, `app.js`, `test_case_journey.py`, `continuity.py`, `mssqlstore.py`, `sqlstore.py`, `store.py`, `sqlguard.py`, `test_priority_order.py`, `test_resident_decisions.py`, `core/README.md`, `core/pyproject.toml`, plus KB and unrelated docs. Ranking adapter, publication, runner and their tests are byte-identical to c5 in the parent (the parent handoff states this).
* File-level overlap of the two deltas is empty. `git merge-tree --write-tree HEAD <parent>` exits 0 with no conflict (tree `5676dd95b65f1d982e94cee3734d3870cf0b5583`).
* Intent: the parent adds SQL order-unresolved handling and committed-reload 409s in priority routes, orthogonal to the child's path-free Blob listing errors and runner visibility. Both are expected to survive.

## Inherited facts (not ours to cure)

* Parent C5 budget is zero. Parent handoff: API `ruff` fails with 10 errors (9 E501, 1 I001) in `src/api/tests/test_ranking_publication_wiring.py`, byte-identical to c5. This child edits the same file (11 added lines), so lint of that file will show these inherited errors plus possibly none new; the added lines must be checked not to add errors. No cure and no waiver.
* The parent's trailing whitespace in main's committed `server-version.txt` is inherited.
* Duplicate `NextMarker` concern was independently classified speculative. No owner blocker is raised without new concrete counterevidence.

## Evidence boundaries

* Earlier Azurite validation of the child at source `7fc680d0e` is recorded in `...-emulator-*` records and is not repeated. This merge changes no ranking adapter/transport source, so no equivalence is claimed beyond verified byte identity of those files, and any change to them invalidates that claim.
* No SQL service, cloud, model, WORM, role grant, full matrix or `rpi-checks` run. SQL-dependent tests are opt-in skips and are reported as such.
