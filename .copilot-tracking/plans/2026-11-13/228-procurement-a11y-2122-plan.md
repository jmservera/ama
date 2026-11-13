---
title: Issue 228 criterion 5 plan (2026-11-13)
ms.date: 2026-11-13
---

## Plan

* [x] Phase 1: repair the stale browser check (read panels that use `content-visibility: auto`).
* [x] Phase 2: extend to four states per role (Issued from the real store; Completed and corrected, Withdrawn, Empty by rewriting real GET responses with a test route).
* [x] Phase 3: keyboard-only entry by Tab and Enter, Tab order over every table, visible and uncovered focus indicator, one Shift+Tab step, at 1280 and 320 px.
* [x] Phase 4: text assertions (no empty cell, status region, captions, row values), axe 4.10.3 at 1280 and 320 px with `ZF_AXE_REQUIRED=1`.
* [x] Phase 5: README wording, ruff, mypy, focused tests, commit without push.

## Decisions

* No product change: no genuine WCAG, focus, label, caption or status defect was found, so there is no failing-first product test. The failing-first evidence is the baseline run failing on unchanged `main`.
* Do not edit `workbench-browser-check.mjs`; no manifest recipe change.
* Tier: focused (non-gate, check tooling and README only).
