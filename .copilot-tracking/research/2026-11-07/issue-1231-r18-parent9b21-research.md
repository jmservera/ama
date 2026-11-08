---
title: Issue 1231 r18 research, local alignment to parent79 9b21a6a0
description: Prospective research for one normal merge of local parent79 9b21a6a0 into the child
ms.date: 2026-11-07
---

Research disposition: executed (read-only). Written and committed before any merge. r15 chronology deviation, r16 and r17 records are preserved unchanged.

## Pinned identities (verified 2026-11-07)

| Item | Value |
| --- | --- |
| Child | fix/ranking-archive-concurrent-writer-metadata, start 201f2612e7277cd1b4a403c07905b60436de2223 / tree 81f0ee1eb335ded40591bea5a654470456313e95, ignored-inclusive clean |
| PR1242 | OPEN, base feat/ranking-publication-runner-79, remote head f87416add (older, unpublished local heads are expected); target kept |
| Local parent79 | /home/azureuser/source/ama-wt/issue-79-publisher, 9b21a6a0d2bc0646076cd2da03f7fc4d088af06e / tree 5d571a4a0215aac35638509a5672638bee0fa98c, ignored-inclusive clean |
| Prior parent | cf5f57a0084bb3ade9b53c7d2884e0db8367c20c, ancestor of both; merge-base |
| Main | origin/main 3950602754437c21d20e91c49ddc1589426e7d1b, ancestor of the parent; not fetched or moved. Main may move (hosted correction 1252 pending); not assumed to be the eventual FULL base |
| Identity | gh api user: jmservera, id 8036360; repo-local 8036360+jmservera@users.noreply.github.com |

## Incoming delta cf5f57a00..9b21a6a0d

* Commits: 482904dbd plan, a9a7e1e42 merge of main 39506027, 9b21a6a0d record.
* Outside .copilot-tracking three paths: .github/rubric/scores/latest.json, docs/reference/log.md (append-only), src/api/tests/test_assistant_release.py. Remaining changes are tracking records.
* No ranking publication, runner, store, server or ranking test file changes.

## Overlap

Child owns ranking_publication*.py, store.py, api server.py, three ranking test files, src/core/README.md. None overlaps. Child does not edit log.md. Dry run `git merge-tree --write-tree HEAD 9b21a6a0` was clean (before planning files, tree b524462b; final tree recomputed after the planning commit).

## Selectors (from r17)

Core from src/core: `-m unittest tests.test_ranking_publication tests.test_ranking_publication_runner` (70). API from src/api: `tests.test_ranking_publication_wiring` (18). Ruff check and format check on src/core and src/api, mypy from src/core. test_assistant_release.py is an incoming parent-side test: run only if it needs no service, otherwise static only.

## Risks

Textual cleanliness is not semantics; verify by raw delta and blob identity. Merge invalidates all receipts. No FULL, SQL, browser, scanners, images or lock is admitted.
