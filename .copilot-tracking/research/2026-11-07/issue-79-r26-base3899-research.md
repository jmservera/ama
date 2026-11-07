---
title: Issue 79 r26 research, base reconciliation to main 38990b19
description: Delta and dependency research before rebasing the root onto current main
ms.date: 2026-11-07
---

Research disposition: executed. Planning Readiness: Ready.

## Identities

* Root start: `bb7e044c33d7f3670ad293ae9e3ff0cae2a801fc`, tree `430c07c72607f6d8cb91bb5c245067724c45feaa`, ignored-inclusive clean, branch `feat/ranking-publication-runner-79`, 41 commits ahead of main (5 are merges of earlier main heads).
* Fetched `origin/main` equals the admitted `38990b19122bfa59a292d3bbaedecfec43580db5`, tree `d58afd30855096029866022dcc2f5753670ccd00`. No newer base. Previous base `23b26a7f`.
* PR 1239 is open to main; its remote head is the stale `181a1c1b` and is not touched.
* Preservation ref: `preserve/issue-79-pre-base3899` = `bb7e044c`.

## Delta 23b26a7f to 38990b19 (22 paths)

* Source: `src/api/src/zava_forward/api/web/role-screens.js` (exception register screen, overview signature), `src/api/tests/test_data_operator_screen.py`, new `src/api/tests/test_exception_register_screen.py`.
* Docs: `docs/architecture/cutover-evidence-pack.md`.
* Tracking: 18 new RPI files for issues 135 and 73. No log.md, core, server.py or workflow change.

## Dependency

* The incoming paths are disjoint from every path this root changes (comm of both path sets is empty), and `git merge-tree` of the two heads is clean. Root changes are core ranking publication, Store, runner, API server route and wiring tests; the incoming change is front-end screen code and its tests, with no import of the ranking publication.
* Relevant light checks after rebase: ranking publication core and API wiring, the new exception register screen and data operator screen tests, Config, ruff, mypy.

## Gaps

* Rebase drops the five main-merge commits (their content is in main) and rewrites 36 commit ids; the old chain stays reachable by the preserve ref. Hosted, FULL and independent gates stay absent.
