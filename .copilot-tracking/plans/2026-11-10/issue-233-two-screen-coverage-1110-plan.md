---
title: Issue 233 two-screen tension coverage plan
description: Plan for extending the existing tension browser check to the technical and quality per-home screens
ms.date: 2026-11-10
---

## Objective

Extend `src/api/checks/atlas_tensions_browser_check.py` so the same ZF-1 home is also checked on Technical queue and Quality queue (withheld panel, retained case, labelled regions, Tab reach, 1280 px and 320 px). Initial coverage only; correction authority UNKNOWN.

## Phases

* [ ] Phase 1: Fixture overlay and constants. Overlay `technical` and `quality` from `technical_quality_data()` onto ZF-1 in `tension_data()`; add screen titles and `WITHHELD_ITEMS` entries.
* [ ] Phase 2: Screen checks. Add `check_technical` and `check_quality`; open each through the existing `open_screen` navigation; loop both widths with `check_regions_and_keys` and the no-horizontal-scroll check; update docstring and COMPLETE message.
* [ ] Phase 3: Negative control tests. Add focused cases for `check_withheld` (missing item fails, complete lists pass) to the existing unit test file.
* [ ] Phase 4: Validation. Unit tests, scoped Chromium run under the heavy lock, pinned ruff and mypy on changed files.
* [ ] Phase 5: Related documentation. Update the atlas screen trace tension row, `src/api/README.md` paragraph, the reference index row and a log entry. No claim of WCAG, AT or user acceptance.

## Stop conditions

* Any new Chromium failure that is a product behaviour rather than a check expectation error: stop and return the diagnostic. No app, auth, panels.js, style.css, Core, schema or role-policy change.
* Assertions must be taken from installed behaviour already observed in the baseline inspection, not weakened to pass.

## Out of scope

Stage 1 destination, eight-stage walk, new fixtures, second role sign-in, recipe edits, full gate.
