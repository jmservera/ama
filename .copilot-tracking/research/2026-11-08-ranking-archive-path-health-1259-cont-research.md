---
title: Issue 1259 parent 6d793bc propagation research
description: Prospective research of the new 1258 parent delta before a normal merge into the 1259 child
ms.date: 2026-11-08
---

## Evidence

* Child fix/ranking-archive-path-health 683ec271 (tree ecd094c1), ignored-clean. Old parent 26b4ea39.
* New local parent fix/ranking-archive-ancestor-durability 6d793bc3ad3fd8427f745530a633bb1e553ec0ef, tree b614f008, single parent 26b4ea39, ignored-clean. Main f548b65f4 unchanged.
* Delta 26b4..6d793: test-only changes in src/api/tests/test_ranking_publication_wiring.py (+40) and src/core/tests/test_ranking_publication.py (+22), plus 1258 continuation records. No production source change, so none of my _names/_require_creatable hunks overlap.
* git merge-tree dry run: conflict-free (tree 718462fa).
* Parent residuals (R1 real crash, R4 extra-sync visibility, FULL, independent, hosted, approvals) are retained, not resolved here.

## Disposition

Planning Readiness: Ready for one normal merge, no rebase, reset, amend or parent write. LIGHT tests only.
