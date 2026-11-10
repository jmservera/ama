---
title: "Recovery plan and details: issue 233 rendered tension checker"
description: Forward recovery plan with one critique, written before the recovery validation
author: Copilot
ms.date: 2026-11-05
ms.topic: reference
---

Written after the recovery Research and before any recovery validation, commit or edit. It plans validation of the already existing code. It does not claim the checker was planned before it was written.

Research: `../research/2026-11-05-issue-233-rendered-tensions-recovery-research.md`. Tier FOCUSED (checker, tests and process documentation only). LIGHT only; no heavy lock, browser, gate or build.

## Plan

* [ ] Phase 1: retain the existing checker, tests and documentation unchanged unless a validation step shows a confirmed in-scope defect, in which case stop and report instead of expanding.
* [ ] Phase 2: read the complete checker, test and documentation diff against main and confirm the source identity (HEAD, tree, blobs, clean tracked status).
* [ ] Phase 3: run, with `PYTHONDONTWRITEBYTECODE=1` and external caches in a new `mktemp -d` directory:
  * `tests.test_atlas_tensions_checker` and `tests.test_role_screens_conformance` (expected 19 tests, 0 skips) from `src/api` with explicit source imports resolved to this worktree.
  * `tests.test_atlas_screen_trace` (expected 17 tests) and the trace CLI from `src/core`.
  * Ruff `check --no-cache --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, `format --no-cache --check --line-length 100`, and `mypy --strict` with an external cache on the checker and its test.
* [ ] Phase 4: write recovery Changes and Review, then commit only the four recovery records.
* [ ] Phase 5: pending separate admission: focused partial gate, Chromium checker and DOM controls for the new head.

## Details

* Use the maintained venv `/tmp/r233i/venvs/api` read only for tooling, with `PYTHONPATH` set to this worktree's `src/*`; no install or mutation. Prove imports by naming concrete modules, not namespace `__file__`.
* Capture each command's own exit code, never a trailing pipe.
* Do not claim prior test runs as newly executed.

## Critique (single pass, self-applied)

* Risk: producing a diff to look like recovery. Disposition: no source edit is planned; only new records are added.
* Risk: treating light results as validation of the new head. Disposition: the Review states the old receipt and 194-PASS run are historical and the new head needs fresh admitted evidence.
* Risk: backdating or excusing the original failure. Disposition: the records state it remains uncured.
* No conflict with confirmed owner decisions found.
