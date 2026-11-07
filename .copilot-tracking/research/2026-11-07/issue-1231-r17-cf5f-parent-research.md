---
title: Issue 1231 r17 research, local alignment to parent79 cf5f57a00
description: Prospective research for one normal merge of local parent79 cf5f57a00 into the child
ms.date: 2026-11-07
---

Research disposition: executed (read-only git inspection). Written and committed before any merge. r15's admitted chronology deviation and the r16 records are preserved unchanged.

## Pinned identities (verified 2026-11-07)

| Item | Value |
| --- | --- |
| Child branch | fix/ranking-archive-concurrent-writer-metadata (PR1242 target stays feat/ranking-publication-runner-79) |
| Start head / tree | 5f904c290e81948463b651135e7ac2d9d1ba4176 / 6abbdc213b5a656ab8e6fb94dca733cb31789067, ignored-inclusive clean |
| Pinned LOCAL parent79 | cf5f57a0084bb3ade9b53c7d2884e0db8367c20c / tree dd20fdc71e7385c024c90e970fcc7d92fc1dd49b |
| Prior parent | 87c027a30ba5a1dd5e4f16b01052e7c32a09138c, ancestor of both; it is the merge-base |
| Main | origin/main 8af3aea6b042f5dfb3305e18334439717f7c5649, ancestor of the parent (not fetched or moved here) |
| Identity | repo-local 8036360+jmservera@users.noreply.github.com |

Remote parent181a and child f874 are expected older unpublished heads; the local cf5f is pinned, not the remote.

## Parent delta 87c027a30..cf5f57a00

* Commits: e2f593f43 plan, df9947c91 merge of main 8af3aea6 into the parent topic, cf5f57a00 record.
* 33 files, 989 insertions, 12 deletions. Non-record files: .github/rubric/scores/latest.json, docs/reference/README.md, docs/reference/log.md (additions only, 15 lines, 0 deletions), docs/reference/resources/ai-tokenomics.md, src/api/checks/case_journey_browser_check.py.
* The rest is .copilot-tracking records of issues 108, 1248 and 79 r19.
* The only src change is src/api/checks/case_journey_browser_check.py. No ranking publication, store, runner or their tests change.

## Child delta over 87c027a30

* Source and tests: ranking_publication.py, ranking_publication_runner.py, store.py, api server.py, the three test files and src/core/README.md, plus r16 records.

## Overlap

* The two sides touch disjoint source/doc files. The dry run `git merge-tree --write-tree HEAD cf5f57a00` was clean (tree 5a9f72d5a2d2a3a97e1d35664b5e27d16c0f32de, object only; includes the four r17 planning files only if committed first, so the real tree is recomputed after the planning commit).
* The child does not edit docs/reference/log.md, so append-only entries survive unchanged.

## Selectors derived from r16

* Core: `python -m unittest tests.test_ranking_publication tests.test_ranking_publication_runner` from src/core, r16 count 70, 0 skipped.
* API: `python -m unittest tests.test_ranking_publication_wiring` from src/api, r16 count 18.
* Static: Ruff 0.17.1 check and format check on src/core and src/api, mypy from src/core (268 files at r16; the parent change is in src/api/checks, record the actual count).
* The changed src/api/checks file is not run (browser check, no browser admitted); it is only statically checked.

## Risks

* Textual cleanliness is not proof of semantics: verify child 0600/stage_retained/winner metadata and parent hash/future/blocked guards still coexist by blob identity and the tests.
* The merge invalidates r14/g79 receipts; a NEW combined FULL, independent review and hosted checks remain required. #107 owns the heavy lane; none is admitted.

Planning Readiness: Ready.
