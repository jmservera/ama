---
title: Issue 86 integration of local parent ae54963 research
description: Prospective research for one normal merge of the pinned local parent into the child (Refs #86)
ms.date: 2026-11-07
---

Scope: Refs #86 only. Start ref `2eda76916daf642ea1b49a77d5cde04480fd49b4` (tree `e3c5b503…`), branch `feat/formal-complaints-adapter-86`, ignored-clean. PR 1243 target `feat/controlled-lifecycle-integration-81` is kept.

## Verified identities

* Local parent `/home/azureuser/source/ama-wt/parent-81`: `ae54963584181d1b5b4d5a788153f853ec0077b2`, tree `b0dd355f…`, ignored-clean. It contains main `8af3aea6…`, which is still `origin/main` after fetch. The remote parent and child are older, deliberately unpublished heads, so the difference is expected.
* Merge base of child and parent: `7d390e13…`. Parent is 12 commits ahead, child 11 ahead.

## Overlap

* Parent delta from the base: 45 paths. Source: `src/api/checks/case_journey_browser_check.py`, `src/core/.../appointments.py`, `src/core/tests/test_quality_procurement.py`; plus rubric score, reference index and log, ai-tokenomics, and other issues' tracking records.
* Child delta outside tracking: `src/core/README.md`, `complaints_route.py` (new), `resident_decisions.py`, `store.py`, `tests/test_resident_decisions.py`.
* Path intersection: none. `git merge-tree --write-tree` gives a clean tree `3ef76023…` with no conflicts.

## Limits

Per-store in-flight registry, point-in-time stale guard, no cross-process proof, no real receiver. The earlier RED 51/14/2, GREEN 308 with 110 skips and strict 267-file results are historical author evidence.
