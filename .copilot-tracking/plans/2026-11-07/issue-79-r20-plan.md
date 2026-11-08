---
title: Issue 79 plan, r20 merge of main 39506027
ms.date: 2026-11-07
---

Task `issue-79-r20-merge-main-1253`. Planning readiness: ready. Critique: one author-only prospective self-critique (not independent) below, before integration.

## Plan

* Phase 1: commit research, plan, details.
* Phase 2: re-fetch; stop on any drift from `39506027`; `git merge --no-ff origin/main` once.
* Phase 3: prove two parents, blob and mode parity for the whole incoming raw delta and for every topic path; then light checks, Changes, state, Review, log entry, commit.

## Acceptance

* Parents are the planning commit and `39506027`; no rewrite.
* Every path changed by main since `8af3aea6` has main's blob and mode; every topic path has its pre-merge blob and mode; the received `test_assistant_release.py` equals main's blob.
* Light checks with exits recorded, no tail masking, external scratch `/mnt/ama-gates/g79-main1253-preparation-1107`, `PYTHONDONTWRITEBYTECODE=1`.

## Commands

* Origin proof: `/tmp/zf79venv/bin/python` printing runner and helper `__file__` and SHA-256.
* Core: `cd src/core/tests && python -m unittest test_ranking_publication test_ranking_publication_runner` (53 expected).
* API: `cd src/api && PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_ranking_publication_wiring.py` (15 expected), then `-p test_assistant_release.py` for the received test if it runs without services.
* Static: pinned Ruff 0.17.1 `check src/core` and `format --check` on the five ranking files with `--cache-dir` in scratch; mypy 2.4.0 from `src/core` with `--cache-dir` in scratch.

## Self-critique

* Risk: main moves again; mitigated by re-fetch and stop on drift. Risk: the received test needs a service; then record as not run. No speculative fixes.

## Follow-up

* Coordinator aligns child 1231 to this frozen local parent; combined FULL, independent reviews, hosted gates; a child merge needs a NEW parent FULL before main.
