---
title: Issue 79 plan, r21 merge of main a1d26534
ms.date: 2026-11-07
---

Task `issue-79-r21-merge-main-1252`. Planning readiness: ready. Critique: one author-only prospective self-critique (not independent) below, before integration.

## Plan

* Phase 1: commit research, plan, details.
* Phase 2: re-fetch; stop on drift from `a1d265340` unless the new head is a descendant changing only `.github/rubric/scores/latest.json` (parsed JSON); `git merge --no-ff` once.
* Phase 3: prove two parents, blob and mode parity for the whole incoming raw delta and every topic path; light checks, Changes, state, Review, log entry, commit.

## Acceptance

* Parents are the planning commit and `a1d265340`; no rewrite.
* All 15 paths changed by main since `395060275` carry main's blobs and modes; every topic path keeps its pre-merge blob and mode; helper blob of `tools/backlog-sync.py` is `43338cb8f`.
* Light checks with exits recorded, no tail masking, scratch `/mnt/ama-gates/g79-main1252-preparation-1107`, `PYTHONDONTWRITEBYTECODE=1`.

## Commands

* Origin proof: `/tmp/zf79venv/bin/python` printing runner and helper `__file__` and SHA-256.
* Core: `cd src/core/tests && python -m unittest test_ranking_publication test_ranking_publication_runner` (53 expected).
* API: `cd src/api && PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_ranking_publication_wiring.py` (15), then `-p test_assistant_release.py` (46).
* Received tools test: `python -m unittest tools/test_backlog_sync.py` style run from the repository root if service-free.
* Static: pinned Ruff 0.17.1 `check` and `format --check` on the five ranking files plus the two tools files, and mypy 2.4.0 from `src/core`, caches in scratch.

## Self-critique

* Risk: main moves again; mitigated by re-fetch and stop on drift. Risk: the tools test needs gh or network; then record as not run. No speculative fixes.

## Follow-up

* Coordinator aligns child 1231 to this frozen local parent; combined FULL, independent reviews, hosted gates; a child merge needs a NEW parent FULL before main.
