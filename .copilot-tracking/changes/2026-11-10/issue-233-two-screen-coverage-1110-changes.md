---
title: Issue 233 two-screen tension coverage changes
description: Change record for the technical and quality screen coverage increment
ms.date: 2026-11-10
---

## Changes

* `src/api/checks/atlas_tensions_browser_check.py`: `tension_data()` overlays the existing `technical_quality_data()` technical and quality evidence onto ZF-1 at design version 1; new `TECHNICAL`, `QUALITY` constants and withheld item lists; new `check_technical` and `check_quality`; the run opens both screens through the existing `open_screen` navigation at 1280 px and 320 px with `check_regions_and_keys` and the no-horizontal-scroll check; docstring and COMPLETE message updated. Existing three-screen code unchanged.
* `src/api/tests/test_atlas_tensions_checker.py`: three `check_withheld` cases (complete lists pass, missing item fails, missing authorisation statement fails). The eight original control tests are unchanged.
* Docs: atlas screen trace tension row and `ms.date`, `src/api/README.md` paragraph, reference index row, log entry.
* `role_screens_fixtures.py` not modified. No product, Core, schema, role-policy or backend file touched. Scenario manifest: neither changed check file is a registered source (N/A).

## Divergences and amendments

* First candidate run failed a fixture precondition (`fixture supplies a paused choice...`): overlaying design version 2 made the paused resident choice read "Not recorded" (choice bound to design version 1). This was a fixture overlay error in the new code, not a product defect. Overlay now keeps design version 1 and the assessment sign-off version 1. Raw adverse log retained externally as `candidate-run-1-adverse-overlay-design-version-2.log`. This is an implementation-phase fix before review, not a post-review repair.
* One edit was made with a python rewrite rather than the edit tool; content was verified in the diff.
* `ruff format` was applied to the two changed files (checks are excluded from format by project config; the original check file was already formatter-clean, so it was kept so).

## Validation

* Unit tests: 11 of 11 pass (8 original, 3 new).
* Chromium 156.0.8078.4, synthetic loopback, heavy lock held, no holder: baseline 194 PASS; candidate 362 PASS, 0 FAIL, all 194 baseline check names still present; 4 of 4 and 2 of 2 table regions reached by Tab at both widths on the technical and quality screens.
* Pinned ruff 0.17.1 check and mypy 2.4.0 on the two changed files: clean. Core scenario-manifest and needs-inventory tests: 19 pass.
* Not run: full or `--changed` gate, hosted CI, axe, assistive technology.
