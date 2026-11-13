---
title: Plan for demo AI readiness increments
description: Proposed initial increments for #107/#108/#159 verification and #891 decision hold
ms.date: 2026-11-13
---

## Objective

Convert IMPL-UNVERIFIED dispositions into observed local evidence without source changes, or record the precise decision still needed. Maximum two increments.

## Increment A (ready): exact-source local verification of three tokenomics/evaluation slices

* Existing criteria: #107 Tokenomics usage per accepted proposal; #108 Tokenomics cheaper-candidate failure and one-lever criteria; #159 Tokenomics per-turn receipt and limit fallback. None is ticked by this increment; it supplies evidence for a later owner tick decision.
* Smallest surface: no source file. Create a fresh virtualenv outside the repo and install `src/core`, `src/agents` and `src/api` from this exact worktree head into it without `-e` (non-editable, `--no-build-isolation` and `--no-index` with a local wheel cache). Stop and record a blocker if dependencies are unavailable offline; do not fall back to the network or to `PYTHONPATH=mvp`. Run from `src/agents` with the documented test-directory path only for fixtures: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest -q` on `test_candidate_comparison`, `test_chat_model` (provider-usage receipt path) and from `src/core` the modules `test_ai_consumption` and `test_chat_panel`. Record the observed module `__file__` origins, test counts and skips; zero discovered tests is a failure of the run, not a pass.
* Failing-first: before recording a pass, run and record `python3 -c "import zava_forward.core as c; print(c.__file__)"` in the new venv; the expectation (observed in this task only as the primary-checkout editable install listed by `pip list`) is that the original environment does not import this worktree, so the first assertion is that the new venv imports from the venv copy of this head. If any named test fails, the finding is a defect report on the exact main blob, not a fix.
* Dependencies: local Python only; no SQL, model, Azure or private data. Heavy-memory admission floor applies only if the runner is heavy; these are light unit tests.
* Authority and spent history: no model, spend or correction grant needed or used. Correction history for these slices is UNKNOWN, not zero; a failure would not authorize a repair cycle.
* Independently reviewable: yes, as one evidence file.

## Increment B (not ready): #891 AC2 failure-envelope attribution

* Existing criterion: #891 AC2. Gap: dispatched failure roots stay unjoined under the intentional #602/#432 rule.
* Not ready. Resume condition: a dated owner (jmservera) decision recorded as a comment on #891 on failure-envelope meter fields, fallback `eligible=False`, `chat_panel` ownership and a finite correction scope with stated spent history. Until then no failing-first test is authorized.

## Dispositions for the remaining issues

* #531 only live verification remains; #108 and #107 remaining criteria are HUMAN/CLOUD; #159 remaining is assistive-technology acceptance. No further slice proposed.

## Phases

1. Research: done. 2. Plan: this file. 3. Critique: one independent critique. 4. Implementation: documentary only (details, changes). 5. Review: one independent Review.
