---
title: Issue 80 round 4 research
description: Current-main preparation delta for the checklist CSV child
ms.date: 2026-11-05
---

Research disposition: reused (rounds 1 to 3) plus re-check of the current main delta. Planning readiness: Ready. Scope is current-main preparation only, not a new export slice.

## Identity (read 2026-11-05)

* Child `feat/checklist-list-export-80` at `ce5ba5728054d92a7fde8a710e089329bb0d45da` (tree `4d72f9216fa34e0ce6ad88744fc83506bab834cc`), clean including ignored inputs.
* Parent target `feat/case-workbench-integration-73` at `ead177ef90d24666557708ea344848a1be43bdf8`, checked out elsewhere and not moved. Parent acceptance is not assumed.
* Coordinator-fetched `origin/main` `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`; its merge-base with the child is `ead177ef9`.

## Issue state

Issue 80 is open: "Every list offers an Excel or CSV export" and "Owners set the staged transition thresholds" stay unticked. A checklist-only export proves neither.

## Main delta (`ead177ef9..bb3a3b03c`, 6 commits, 55 files)

* `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `tools/backlog-sync.py`, `tools/test_backlog_sync.py`, `.github/workflows/src-ci.yml`: gate and backlog tooling (#1209, #1210, #1217).
* `src/api/src/zava_forward/api/web/style.css`: one rule, `.top nav{row-gap:.125rem}` under the 600 px query (#1219, "restore the unchanged 320px case-summary contract").
* `src/README.md`, `docs/reference/log.md` (three appended 2026-11-05 entries), rubric score files, and 46 `.copilot-tracking` files for other issues.

## Overlap with the child

* The child changed `server.py`, `ops.js`, `projection.py`, `quality.py`, `README.md` (api) and five test files plus round 3 tracking files. The main delta touches none of them; no round 3 tracking path exists on main. A textual conflict is not expected.
* Semantic note: #1219 targets the same 320 px summary assertion that failed in the round 3 `case_journey_browser_check` with and without the child. Whether it now passes is unverified: no browser or heavy gate is permitted in this task, so the adverse round 3 result is preserved, not superseded.
* The #82 `quality.py` overlap remains an integration-review dependency; no server-gate semantics change here.

## Constraints

No push, no PR, no heavy or browser gate (the #96 runner holds the lock), no cleanup, no new exports, no application edits unless a merge defect forces a minimal fix.
