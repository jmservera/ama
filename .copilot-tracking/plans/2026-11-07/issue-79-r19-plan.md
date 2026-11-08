---
title: Issue 79 plan, r19 merge of main 8af3aea6
ms.date: 2026-11-07
---

Task `issue-79-r19-merge-main-8af3`. Planning readiness: ready. Critique: one prospective self-critique below, before integration.

## Executive summary

Merge exact `origin/main` `8af3aea6` into the topic with one normal merge commit, prove parents and blob parity, run light no-service checks, record Changes and one author Review, commit.

## User decisions and requirements

* One normal merge; no rebase, force or rewrite; stop on drift or unclear conflict; keep append-only log entries.
* Commit prospective records before the merge. No new behavior, no unrelated formatting.
* No FULL, SQL, browser, scanner, images, provider, Azure, push, PR update, retarget, ticks or approvals. Child untouched.

## Phases

* Phase 1: research, plan, details committed (this commit).
* Phase 2: re-fetch and confirm main is still `8af3aea6`; `git merge --no-ff origin/main` with a Conventional message.
* Phase 3: proofs, then light checks, then Changes, state, Review, log entry, commit.

## Acceptance criteria

* Merge commit has exactly two parents: the planning commit and `8af3aea6`.
* Every non-log path from main has main's blob and mode; every topic-changed path keeps its pre-merge blob (including the runner, its test and README at the r18 digests).
* log.md has all main entries and all topic entries, no deletions against either side.
* Light checks pass or failures are recorded as found; ignored-inclusive clean.

## Validation commands (all with `PYTHONDONTWRITEBYTECODE=1`, scratch `/mnt/ama-gates/g79-8af3-preparation-1107`, logs captured with `> file 2>&1; echo $?`, no tail pipelines)

* Import origin: `/tmp/zf79venv/bin/python -c` printing `__file__` of the runner and helper; SHA-256 of both.
* Core (53 tests): from `src/core/tests`, `/tmp/zf79venv/bin/python -m unittest test_ranking_publication test_ranking_publication_runner`.
* API (15 tests): from `src/api`, `PYTHONPATH=../core/tests:../agents/tests /tmp/zf79venv/bin/python -m unittest discover -s tests -p test_ranking_publication_wiring.py`.
* Ruff: pinned `ruff==0.17.1` from `/tmp/79-align-r13-1106/venv/bin` with `--cache-dir` under the scratch dir, `check src/core` and `format --check` on the ranking files only (no broad formatter; `src/check-container.py` is known pre-existing).
* mypy: pinned `mypy==2.4.0`, from `src/core`, `mypy --cache-dir <scratch>/mypy src tests`.

## Self-critique

* Risk: main's incoming browser check could interact with nothing here; mitigated by blob parity and no run.
* Risk: main moves again before the merge; mitigated by re-fetch and stop on drift.
* Risk: a score-only bot commit may land after the freeze; reported, not chased.
* Rejected: rebase (rewrites hashes already stacked on), merging main into the child.

## Follow-up items

* Coordinator: align child 1231 to the frozen parent, combined FULL, independent reviews, hosted checks; a child merge invalidates the parent, so a NEW parent FULL is required before main.
