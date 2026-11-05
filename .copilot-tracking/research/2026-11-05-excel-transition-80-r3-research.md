---
title: Issue 80 round 3 research
description: Delivery status and slice choice for the checklist list CSV export
ms.date: 2026-11-05
---

Research disposition: reused (rounds 1 and 2 research) plus re-check of the current issue and code. Planning readiness: Ready.

## Identity

* Branch `feat/checklist-list-export-80`, stacked under parent topic `feat/case-workbench-integration-73` (issue #73).
* Parent SHA pinned at `ead177ef90d24666557708ea344848a1be43bdf8`; it equals local `origin/main` and this branch's start.

## Issue state (read 2026-11-05)

* Met: import preview and no source change; export retains history independent of the AI provider.
* Open: "Every list offers an Excel or CSV export; Excel stays one-way read-only" and owner staged thresholds (ADR 0001, a separate owner decision).
* Delivered exports: PR 303 (importer library, history and preview), PR 1019 (CSV for cases, packages, work orders, handoffs, visits, funding, with formula-safe cells), PR 1176 (finance and stock queues).

## Gap and slice choice

* `/api/checklists` (quality checklists per measure) has no export. Governance, resident, chat and form lists are also missing and stay out of this slice.
* Slice 3: `GET /api/checklists.csv`, one row per check (`measure`, `version`, `step`, `check`), from the same constant as the JSON route, so rows match what the signed-in staff role already sees.
* The data is fixed reference text: no case, resident, user or service data, no free-text cells, no query selectors.
* Existing exports do not write audit events (read-only, row data equals the JSON list); this slice follows that convention. Nothing involves an AI provider.
* No `.xlsx`: the literal criterion allows CSV, the API must not import the importer, and no dependency is added.

## Overlap with concurrent work

* #82 (`feat/remaining-gate-outcomes-82`, worktree `issue-82-gates`) edits `src/core/src/zava_forward/core/quality.py`: import line, new functions after `checklist_for`, and `handover_blockers`. This slice adds `checklist_rows` before `checklist_for` and one `typing` import. Hunks are separate; a textual merge is checked after commit. No interface dependency: `checklist_rows` reads only `CHECKLISTS`.
* #79 (`feat/ranking-publication-runner-79`) touches `src/core/pyproject.toml` and new ranking runner files only; no overlap.
* Heavy lane: held by the #188 full gate (pid 1148896, `/tmp/rpi188-full-20261105T0740`).

## Not in scope

Owner thresholds, governance and resident and chat and form exports, XLSX, workbook-history proof for other routes.
