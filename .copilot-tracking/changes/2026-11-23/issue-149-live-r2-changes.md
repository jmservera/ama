---
title: Changes, issue 149 live r2
ms.date: 2026-11-23
---

Tier: FULL classification (a web file under `src/api` changes). Targeted local checks only; the complete gate (`rpi-checks.py --all`) is the coordinator's and was not run.

## Files

* `src/api/src/zava_forward/api/web/style.css`: `.case-tab-panel pre` rule extended to `#law-out pre` (wrap long provision lines).
* `src/api/tests/test_law_viewer_reflow.py`: new regression test (fails without the rule, verified by reverting).
* `docs/reference/research/issue-149-law-viewer-reflow-2026-11-23.md`, `docs/reference/README.md` index row, `docs/reference/log.md` entry.
* Evidence: `.copilot-tracking/evidence/2026-11-23/issue-149-live-r2/before.png` and `after.png`.

## Validation

* Playwright, 320x640, stubbed APIs: `scrollWidth` 2772 before, 320 after.
* `unittest` for the new test plus baseline, content standard, landmarks, design system and static assets: 80 tests OK. `ruff check` and `ruff format --check` clean; `mypy` in `src/api` clean.
* Not done: web-design-guidelines source was not re-fetched for this one-rule CSS change; no live Azure render (law store returns 503 on the demo); no person-run AT testing (not needed for the demo).

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | #440 stabilization checkpoint | Unproven: owner-gated triage and decisions |
| 2 | Child features are accepted | Unproven: all sub-issues read CLOSED, but acceptance is an owner decision |
| 3 | Accessibility, content and usability evidence recorded | Proven locally (80 tests green, one new reflow measurement); already ticked |
| 4 | Design artefacts traceable | Not re-executed; already ticked |
