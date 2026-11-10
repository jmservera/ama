---
title: Issue 133 aftercare C3 changes
description: Changes and table audit disposition for corrective cycle C3 (Refs #133)
ms.date: 2026-11-10
---

Refs #133. Counter: C3 of 5 used, 2 remain. No closure, push, PR, board write, rebase or reset.

## Table audit disposition

The aftercare evaluator table already had correct semantics (caption first, six `th scope="col"`, `th scope="row"` home cells, text `Unknown`). One small defect: no scroll region for six columns at narrow widths. Fixed by wrapping in the existing `table-scroll` region pattern (`role="region"`, `tabindex="0"`, `aria-label` equal to the caption). The inventory count is 12, justified by this audit and not a bare increment.

## Files

* `src/api/src/zava_forward/api/web/aftercare.js` (wrapper, caption constant)
* `src/api/tests/test_accessibility_baseline.py` (count 12)
* `src/api/tests/test_aftercare_screen.py` (DOM regression, red then green)
* `docs/reference/research/ux/wcag-conformance-baseline.md` (dated Tables row note), `docs/reference/log.md` (appended entry)

## Validation (logs in `/tmp/issue133-c3/logs/`)

* Red: baseline `12 != 11` on b1b0d6c; new DOM test failed before the wrapper.
* Green: baseline 12, screen 13, content standard, static assets (CI PYTHONPATH, discover), core 65, ruff, mypy 2.4.0 (204 and core), `node --check`, `git diff --check`.
* Whole api discovery: 2112 run, 380 skips, 7 modules failed to import `playwright` before `.[dev]` was installed; those 7 modules then passed (44 tests). 289 law-store `ValueError` lines are warnings in passing tests. CI reported 2560 run, so the 448 count gap is unexplained and not claimed as parity.

## Not run

SQL, browser, served DOM (not needed, no lock taken), full gate, model, network, hosted CI. No WCAG, assistive-technology or human acceptance claim.
