---
title: Issue 1259 frozen parent C6 integration research
description: Prospective research for merging the implemented 1258 C6 parent into the 1259 child with hash-qualified reuse of earlier evidence
ms.date: 2026-11-09
---

## Disposition

Research executed 2026-11-09 (qualified rpi-agent, Sonnet 5.5, session b9ebef9f) before this task's plan, details, critique, merge or any edit. Planning Readiness: Ready for an integration-only plan. No source edit is expected; none is planned.

## Pinned identities (read from refs and objects)

* Child worktree `/home/azureuser/source/ama-demo-wt/issue-1259-recovery`, branch `fix/ranking-archive-path-health`, clean at start, HEAD `c0c0a199204d3cea5c41ae114ca298c2fdf01d29`, tree `6f72b22ea53ca1eaab68e4bb1d10ca19495ae018`.
* Parent (implemented C6, frozen): exact `99814198079c7c8fcd641497826986c706627b0f`, tree `0658fe7f883c5efa09ca286cb026be5cde16ada9`, based on main `5c3b8b4bed4bef82b53b15274fdbbb27d9eaba74`. Parent independent Functional review `362c0bec-b992-4f6f-bb93-4a6c5506c8a6` is still running: the parent is not publication-approved. A local merge of the pinned commit is permitted; the parent is never mutated; no push, PR or publication. If the parent moves, record that revalidation is needed.
* Current fetched `origin/main` `1a84b3b0054990262a0df0625d95e3f545d2739a` (the parent base `5c3b8b4be` is its ancestor; one docs commit `#1322` ahead). Recorded only; main is not merged here and the declared child target remains the parent topic `fix/ranking-archive-ancestor-durability`, not main.
* Merge-base of child and parent: `9b1e2567c2d0a2173b562103cd27508f75181526` (the previously integrated frozen SQL main parent). No unmerged sibling (#136) is imported.

## Own range versus parent

* Own source range over the merge-base (`git diff 9b1e2567c HEAD -- src`): 5 paths, +291/-3: `ranking_publication.py` (local-folder path health, `verify` docstring), `ranking_publication_runner.py` (fixed Blob error text), tests `test_ranking_publication_runner.py`, `test_ranking_archive_blob.py` (one added, C2-typed conditional-create test), API `test_ranking_publication_wiring.py` (one added route test).
* Parent range over the merge-base: 37 `src`, `tools` paths, +3361/-132 (runtime, 1308 SQL, 1313 controls, 1315 photo, 1320 receipts, simulator admin, typing of the Blob test fixture and tests). Parent diff over the merge-base on `ranking_archive_blob.py`, `ranking_publication.py` and `ranking_publication_runner.py`: 0 lines.
* Dry run `git merge-tree --write-tree HEAD 99814198`: exactly one conflict, `src/core/tests/test_ranking_archive_blob.py`. Parent annotates `-> None` on the existing `test_repeat_is_idempotent...`; the child inserts its own test directly above that method. `test_ranking_publication_wiring.py` auto-merges (parent reformats the file, child adds one test). Mechanical; both intents are retained by keeping the child's typed test and the parent's annotated neighbour.

## Source and protocol qualification inputs

* Adapter blob `ranking_archive_blob.py` is `346784573abfcdcf2886be3b99c32df7e5cb0b85` at `7fc680d0e` (the emulator-qualified source), at the parent and at child HEAD. Transport module `documents.py` is identical at `7fc680d0e` and the parent. `ranking_publication.py` (`ed2879856e4d...`) and `ranking_publication_runner.py` (`0ea15181038a...`) at child HEAD equal their `7fc680d0e` blobs; the parent holds its own older versions that the ordinary merge must leave as the child's (verified after the merge).
* `src/core/pyproject.toml` differs only by two mypy override module names (`test_priority_order`); the `blob` extra stays `azure-storage-blob==12.31.0`. The adapter uses the urllib transport (no SDK import).
* Earlier local Azurite 3.37.0 evidence (`handoff-1259-emulator-validation.md`, scratch `g1259-emulator-1109.P6T1sb`, 29-log manifest verified: all 29 sha256 OK) was produced against exactly these inputs. After the merge it may be cited only if the four blob hashes still match; otherwise it is not reused. No new emulator run is planned and none is admitted. No real Azure.

## Budget and limits

* Child review-correction cycles: C1 and C2 spent; three of five remain by default. This integration and evidence task consumes none. A source fix would require a prospective plan and critique and would then be C3; none is planned, and no renewal is self-granted.
* Parent type baselines (mypy core 84 and API 9; all inherited) and the parent's Any/profile questions belong to the parent review. The child does not fix or paper over them. Child-owned diagnostics must be zero.
* Tier: owner-selected demo-targeted. No SQL, browser, full gate, deploy, credential file, private data or model call. Owned scratch venv only, no global install.

## Risks to check

* Child-added tests under the parent's stricter lint, format and types (parent reformatted the API wiring file and typed the fixture and blob tests).
* The merge brings 1308 SQL, 1313 controls, 1315 photo and 1320 receipt code unchanged; none of it may be edited by the child.
