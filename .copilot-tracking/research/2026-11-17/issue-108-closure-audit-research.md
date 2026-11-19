---
title: Issue 108 closure audit research
description: Evidence audit of issue 108 acceptance criteria against main eb51af5c9
ms.date: 2026-11-17
---

## Scope

Audit issue #108 ticks against `origin/main` eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4. Docs plus one focused test. Offline, desktop-only. Out of scope: #1818, #1641 (core mssqlstore, chat grounding).

Research disposition: executed. Planning Readiness: Ready.

## Measurements (main, before any change)

* `git merge-base --is-ancestor 08c36e4dc origin/main` is false; #1771 sits only on `origin/feat/demo-164-chat-grounding-provenance-0900` and other feature branches.
* `ai_eval.task_coverage` on main reports the five assistants (stock-prioritisation, assessment-preparation, funding-evidence, works-resident-coordination, quality-evidence) as NOT_EVALUATED; pinned by `TaskCoverageTests` in `src/agents/tests/test_ai_eval.py`.
* `ai_eval.evidence_gate` states calibration "not applicable", benefit "not permitted", actual-model and human effectiveness not evaluated.
* No `subgroup` accounting exists in `src/agents/src` on main; cohorts appear only in `heldout_freeze` (freeze check) and `cohort_*_eval` (priority only).
* `candidate_comparison.LEVERS` enforces exactly one lever with same-case baseline on main (`tests/test_candidate_comparison.py`, 19 tests OK).
* Baseline targeted runs OK: `test_ai_eval` 20, `test_candidate_comparison` 19, `test_heldout_freeze` 13, `test_heldout_batch` 40.
* Issue body still ticks RAI rows 2 ("all five assistants ... legacy family") and 3 ("subgroup results") although the 2026-11-17 closure-correction comment says affected criteria were restored; main does not prove them.

## Findings

* F1: RAI row 2 tick is unsupported on main (assistants not evaluated).
* F2: RAI row 3 tick is only partly supported (critical misses, calibration not applicable yes; subgroup results no).
* F3: No existing knowledge-base page records a per-criterion closure matrix against main.

## Open (unchanged)

Regional model/quota, held-out labelled split, human participants, effort comparison, actual-call authorization, real AI/SQL/Azure proof, routing/caching option actually evaluated.
