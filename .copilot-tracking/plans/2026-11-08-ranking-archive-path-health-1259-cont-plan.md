---
title: Issue 1259 parent 6d793bc propagation plan and details
description: Plan for one normal merge of the new 1258 parent and LIGHT proof tests
ms.date: 2026-11-08
---

## Plan

* [ ] 1 Commit this prospective research and plan.
* [ ] 2 One normal merge (--no-ff) of local fix/ranking-archive-ancestor-durability 6d793bc3 into the child.
* [ ] 3 New scratch /home/azureuser/.local/share/ama/gates/g1259-parent6d-light-1108: fresh venv, non-editable install of git-tracked export, prove module origins, synthetic ZF_DATA, external caches.
* [ ] 4 Run test_ranking_publication*.py (core), API test_ranking_policy, test_ranking_publication_wiring, test_ranking_scale with the documented tests PYTHONPATH. Failures block the freeze; no speculative production edits.
* [ ] 5 Changes, one author Review (not independent), state update, commit.

## Boundaries

No critique repeat (original Revise PC-001..007 stands; propagation only). No gate, SQL, browser, Docker or benchmark. No push, PR or issue change. FULL, receipt, independent assessment and hosted checks stay unperformed. Refs only.
