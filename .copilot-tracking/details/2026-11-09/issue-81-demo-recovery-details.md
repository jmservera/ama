---
title: Issue 81 demo recovery phase details
description: Exact commands and boundaries for the demo-targeted recovery
ms.date: 2026-11-09
task_slug: issue-81-demo-recovery
---

## Phase 1 merge

`git merge origin/main --no-ff`; resolve `.github/rubric/scores/latest.json` to main, keep both sides of the two append-only documents with main first, accept the previously recorded resolutions for `employee_chat_browser_check.py` and `test_assistant_release.py` (result equals main). Verify `git diff --check` and no conflict markers.

## Phase 2 tests

Scratch install (out of tree, no bytecode, synthetic `ZF_DATA`): `src/core`, `src/agents`, `src/api` with `--no-deps` into a venv with ruff and mypy. Selectors from `src/core`: `python -m unittest test_gates test_resident_decisions test_quality_procurement test_hazard_referral test_handoff_lifecycle test_ranking_publication test_ranking_publication_runner`.

## Phase 3 SQL

Admission `flock -n /tmp/ama-rpi-heavy.lock`; owned container `mcr.microsoft.com/mssql/server:2022-latest` on loopback, unique name, removed after; per-test disposable database; `ZF_RESIDENT_MSSQL=1`. Remove only the exact owned container.

## Boundaries

No push, PR edit, issue tick, Azure, real model, role grant or credential read.
