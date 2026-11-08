---
title: Issue 86 prospective FULL admission preparation research
description: Tracking-only research for the next actual FULL of the issue 86 child candidate, including a later normal Main integration
ms.date: 2026-11-08
---

Scope: issue #86 only, `Refs #86`, local only. This is tracking-only preparation. It is not a FULL run, a Main integration or new feature authority. Nothing here is acceptance.

## Verified starting state (read-only)

* Child `feat/formal-complaints-adapter-86` HEAD `4da357c013e3b050a449dc8d19cfb121186a3f23`, tree `e1f48017872a6494797b2b34144743616a9acfe7`, ignored-inclusive clean.
* Fetched `origin/main` is `2e0c676ada9264b4322224a24bc98aa3367d4f4a` (rubric bot, after `4194c49ea`, the merged #1268 SQL-process test change, and `f548b65f`). `f548b65f` is an ancestor of it (explicit exit 0).
* Remote parent ref `feat/controlled-lifecycle-integration-81` is still `c5edb320ad10d3d73bb985bfb82b2d0bee94381a`. PR #1243 is OPEN with base `feat/controlled-lifecycle-integration-81`; its published head is `6ff492ad...`, so the local child head `4da357c0` is unpublished.
* Local parent `e888a499` and published parent `c5edb320` are both ancestors of the child (receiver reconciliation, merge `6a03b398`). Both remain distinct review deltas.

## Main delta since the child's base `f548b65f`

`git diff --name-only f548b65f origin/main` lists only inert tracking records for #107, `.github/rubric/scores/latest.json` (valid JSON, bot score) and two executable test files: `src/api/tests/assistant_process_worker.py` (new, 90 lines) and `src/api/tests/test_assistant_release.py` (+201 lines, with new `ProcessRaces` and `MssqlUnleasedRevocation` SQL process tests). No production `src` file, tool, infra or workflow byte changed. The child already carries earlier #107 test content from earlier merges; the later Main delta must be re-checked by blob at merge time, not assumed.

Open #1269 (native 530) is refreshing tracking-only evidence and holds the sole prospective focused window. Its old partial verifier is recorded as BLOCKED and its receipt is not reused. Its eventual merge is expected to add only inert RPI records, but that is an expectation, not a fact; Main may move again.

## Maintained runner facts (read from `tools/rpi-checks.py` and `src/README.md`, not executed)

* `--all` selects exactly 17 groups: `preflight`, five `project-*` (core, agents, api, orchestrator, importer), `namespace`, `static`, `infra`, `migration`, `browser`, `mssql`, four `image-*` (api, agents, orchestrator, importer) and `logo-0600`.
* `--jobs 1` gives a shard count of 1, so no API test shards. Full scope implies fresh image builds. Browser selections need a resolved `--out` of at most 58 bytes. The default `--lock-timeout` is 600; non-queued admission needs `--lock-timeout 0`.
* `SQL_SELECTORS` already includes `test_assistant_release.MssqlUnleasedRevocation`, `test_mssqlstore`, `test_lawstore.MssqlStoreTests`, five `test_assistants.Mssql*` classes (Contract, Review, Durability, Api, Ledger) and `test_resident_aoai_sql.AccountingSqlTests`. The new Main #107 SQL process tests therefore run only if the actual Main integration is in the candidate.
* README policy: run `--all`, then `--verify-receipt ... --base <current origin/main>`. Receipts bind exact head and base; any later commit, rebase, base or source change invalidates them. `--stack` exists for an ordered rebased stack, but this child is merged, not rebased, so it is not assumed.

## Inherited hunks absent from Main

The #1226 fail-closed quality gate, #1228 FR-008 provenance and #1229 capacity gate outcomes, plus the later sole-missing-capacity Unknown branch (`b205ed37`), live in `gates.py`, `procurement.py`, `quality.py`, `store.py`, `appointments.py` and their tests. They are not on Main and are in scope of the independent assessment.

## Open and unchanged

Original Medium findings, the adverse browser outcome, the #1238 stale-Pending supersession policy (separate, human-blocked), the per-store in-flight registry, the point-in-time stale guard, no cross-process proof of the adapter, no real receiver, and no human, resident, legal or professional approvals. LIGHT results (505 tests, 111 SQL/Azure opt-in skips, 269 mypy files, ruff) are not FULL.
