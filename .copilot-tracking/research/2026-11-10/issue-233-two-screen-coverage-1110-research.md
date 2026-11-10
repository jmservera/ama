---
title: Issue 233 two-screen tension coverage research
description: Prospective research for the initial technical and quality per-home tension coverage increment
ms.date: 2026-11-10
---

## Status

Research executed after the research-open witness record (seq 2). The file was opened as a minimal stub before that record and rewritten with these findings afterwards. Planning Readiness: Ready.

## Scope

* Task: issue 233 (parent 149), initial two-screen engineering coverage for the technical and quality per-home withheld panels in `src/api/checks/atlas_tensions_browser_check.py`.
* Base: main 736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd. Correction authority: UNKNOWN. No product, app, auth or backend fix authorized; a reproduced defect stops the task.
* Research disposition: executed.

## Evidence

* Existing checker (530 lines) signs in once as `pam@example.test` (Retrofit Programme Manager) and walks programme-queue, resident-choice and procurement-packages for ZF-1 at 1280 px and 320 px using `panels`, `precedes`, `check_withheld`, `check_regions_and_keys` (identity-aware: index-based Tab reach, labelled caption regions) and `check_readonly`. Its fixture `tension_data()` builds on `role_screens_fixtures.synthetic_data()`, which sets `quality = []` and carries no `technical` record.
* `role_screens_fixtures.technical_quality_data()` already supplies the same synthetic home with returned, stale and missing technical evidence and two open quality defects. It can be reused unchanged by overlaying its `technical` and `quality` onto ZF-1 in `tension_data()`; no fixture edit is needed.
* `role-screens.js` registers `technical-queue` (roles include Programme Manager, Quality Inspector) and `quality-queue` (Quality Inspector, Programme Manager, Programme Support Officer), each with a `screenWithheld` panel and read-only boundary text. Stage links 2 and 6 of programme-queue point to them and keep the case.
* Unit tests `src/api/tests/test_atlas_tensions_checker.py` (8 tests) cover empty, whitespace, absent, no-region labels and duplicate-name reach for `check_regions_and_keys`.
* Scenario manifest: only `workbench_browser_check.py` is registered as a recipe source; neither `atlas_tensions_browser_check.py` nor `role_screens_fixtures.py` is a registered source, so no recipe SHA applies (N/A; no edit to `workbench_browser_check.py`).
* Tool pins: ruff 0.17.1 and mypy 2.4.0 are in `~/.venvs/zf123-pinned`; the global ruff 0.17.3 and mypy 2.4.1 are not canonical. A pinned venv with playwright exists in another worktree and is used read-only with this worktree's sources first on PYTHONPATH (verified `zava_forward.core.store` resolves here).
* Web guidance fetched (Web Interface Guidelines command.md, first 3000 characters): rules target UI code; the changed files are a Python check, so they apply only as the engineering checks (labelled regions, keyboard reach, reflow) that the checker asserts.

## Baseline (unchanged), under /tmp/ama-rpi-heavy.lock (no holder, nonblocking)

* Unit tests: 8 of 8 pass, exit 0.
* Existing checker in Chromium 156.0.8078.4: exit 0, 194 PASS, no FAIL, no page errors.
* External inspection of both target screens with `pam@example.test` and `quality@example.test`, ZF-1, 1280 and 320 px: both screens render for both roles, headings and "Not shown for this role" panel present, 4 (technical) and 2 (quality) labelled table regions, no horizontal scroll, no defect reproduced. Role-specific omission observed: the Quality Inspector sees "Held for roles with a recorded need" for the technical latest change note, the Programme Manager sees the note. Panels use content-visibility, so text must be read after scrolling each section into view (the existing `panels` helper does this).
* Logs retained outside the repository (witness evidence directory `runs/`).

## Decision

Baseline passes and no defect is reproduced, so the coverage increment is supported. Programme Manager only in the checker (existing identity; no second sign-in); the Quality Inspector observation stays as external evidence.

## Planning Readiness

Ready.
