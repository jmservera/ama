# Issue 1258 SQL main integration plan (2026-11-09)

Refs #1258. Research: `.copilot-tracking/research/2026-11-09-ranking-archive-blob-1258-sql-main-research.md`. Details: `.copilot-tracking/details/2026-11-09-ranking-archive-blob-1258-sql-main-details.md`.

## Objective

Merge fetched `origin/main` `8d6f029cac004506953f36606862168bbe9d9412` (PR 1308 squash) into the topic branch with an ordinary local merge commit that preserves both intents (Blob ranking archive from #1258; priority order and committed-reload from #1292), then run the owner demo-targeted checks. No source edit by hand, no sixth cycle, no push.

## Phases

* [ ] Phase 1: commit this prospective research, plan, details and critique alone, before the merge and before any validation.
* [ ] Phase 2: re-fetch, require `origin/main` to equal the pinned SHA, `git merge --no-ff` that SHA. Any conflict stops the task: `git merge --abort`, report the exact conflicting paths and hunks.
* [ ] Phase 3: targeted validation in an owned `mktemp -d` venv with editable installs from this worktree.
* [ ] Phase 4: changes record, one original Review, state, local commit, handoff.

## Owner demo-targeted tier

No `rpi-checks --all`, no old receipt, no private database, no Azure or model call, no SQL Server (the Blob archive does not touch SQL; main's SQL evidence is #1292's own). Classification: executable `src` change by merge, demo-targeted tier.

Selectors, from `src/core` unless stated:

1. `python -m unittest test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents` (the c5 set, with the new main-side Store).
2. Changed Store, priority and resident regressions from main that run without SQL Server: `test_priority_order` (SQLite-backed classes; SQL Server classes skip without their opt-in) and `test_resident_decisions`.
3. From `src/api`: `test_ranking_publication_wiring` and `test_case_journey` with `PYTHONPATH=../core/tests:../agents/tests`.
4. `ruff check` on the changed Python files and `mypy` on the impacted core modules per `src/core/pyproject.toml`.

Skips are recorded literally and are not reported as passes. A failing selected test is not waivable and is reported without a fix.

## Stop conditions

Conflict; a merge delta outside the F1 12 source paths plus docs and tracking; a failing selected test needing a source change (no cycle available); missing prerequisite. Each is reported with the exact evidence; no repair.

## Boundaries carried

Refs #1258 only, no full AC claim. Unmet: Azure or real account run, WORM, role grant, Bicep env, deployment, folder-record migration decision, hosted CI on the final head, independent exact-head Functional closure on the final parent, Minor R-1 policy-name guard (no manual policy-name guard, retention or migration expansion). Emulator qualification is not Azure acceptance.

## Critique dispositions (one critique, not repeated)

Record: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-sql-main-critique.md`. PC-SM-1: selectors run with `PYTHONPATH=tests` (core) and `PYTHONPATH=tests:../core/tests:../agents/tests` (API). PC-SM-2: ruff findings in files unchanged by the merge are confirmed against `52f9b61b`, reported as pre-existing and not edited; findings in main-side files stop the task. PC-SM-3: unset all `ZF_RESIDENT_MSSQL`, `ZF_RESIDENT_AZURE_TEST`, `ZF_RANKING_ARCHIVE` and SQL connection variables for every validation command.

## Risks

* Textual cleanliness is not semantic proof; targeted tests and reading are the evidence.
* Selected tests do not exercise SQL Server for this change; #1292's own evidence is cited, not inferred.
