---
title: "Plan: issue 1362 extension E1 visible associated version"
description: Checker-only plan to reject CSS-hidden or transparent associated Current design version fields
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

## Objective

Make the exact associated `Current design version` `dt`/`dd` assertion require genuinely visible text, rejecting `visibility:hidden` and `opacity:0` on the label or the value, without weakening any D1 control or changing the product.

## Scope

* `src/api/checks/atlas_tensions_browser_check.py`: `DESIGN_VERSION_FIELDS` only.
* `src/api/tests/test_atlas_tensions_checker.py`: one opt-in real-Chromium regression class.
* No app, panel, CSS, fixture, schema, role, permission or identity change. No manifest change (recipe is `workbench_browser_check.py`).

## Phases

* [ ] Phase 1: baseline. Unit baseline 17 OK on merged head (done in Research). Browser baseline is the reproduced D3 record; no repeat diagnosis.
* [ ] Phase 2: RED. Add the real-DOM regression; run it with `ZF_BROWSER_TESTS=1` against the old extraction and capture that the four hidden cases fail to raise.
* [ ] Phase 3: fix. Pass `{visibilityProperty: true, opacityProperty: true}` to both `checkVisibility` calls.
* [ ] Phase 4: GREEN and candidate checks. Unit (default and opt-in), role conformance and atlas trace tests, Ruff lint and format, strict mypy on the two files, one full Atlas browser run at 1280 and 320, one actual-DOM negative pair (the D3 script) at both widths.
* [ ] Phase 5: Review, commit locally, handoff.

## Budget and stop rules

* Heavy runs: one full browser run, one D3-style pair. Non-queued `flock -n /tmp/ama-rpi-heavy.lock`; busy returns HOLD. No retry until green; a failure is preserved and stops the correction. Own venv `/tmp/ama-1362-env` at declared pins only.
* No full gate, SQL, Docker, cloud or private data. Commit only the two source files and the RPI records, with the noreply identity and Copilot trailer. Debit: E1 used, four left.

## Success

Positive control passes at both widths; `dd`/`dt` `visibility:hidden` and `opacity:0` and all D1 negatives reject at the new assertion; full Atlas browser exit 0 at 1280 and 320.
