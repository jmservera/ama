---
title: "Details: issue 1362 extension E1 visible associated version"
description: Phase details for the checker-only visibility fix
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

## Phase 2: RED

Add `DesignVersionBrowserTests` to the existing test module, guarded by `unittest.skipUnless(os.environ.get("ZF_BROWSER_TESTS") == "1", ...)` as in `tests/test_chat_panel.py`. It launches Chromium, calls `page.set_content` with `<section><dl><dt>Current design version</dt><dd>1</dd></dl></section>`, applies one style change per case and calls the real `check_design_version` on `page.locator("section")`. Cases: valid passes; `dd` and `dt` `visibility:hidden` and `opacity:0` raise `AssertionError`; ancestor `section` `opacity:0` raises; wrong value `2` raises. Run against the pre-fix source to record that the four hidden cases (and the ancestor case) do not raise.

## Phase 3: fix

In `DESIGN_VERSION_FIELDS` replace `dt.checkVisibility() && dd.checkVisibility()` with a shared options constant `{visibilityProperty: true, opacityProperty: true}` applied to both. Keep `textContent.trim()`, the exact `str(expected)` comparison, the unique-label rule and the scroll-into-view. Do not enable `contentVisibilityAuto`.

## Phase 4: verification commands (from `src/api`, own venv, worktree PYTHONPATH)

* `python -m unittest tests.test_atlas_tensions_checker` (default) and with `ZF_BROWSER_TESTS=1` (real DOM, not skipped).
* `python -m unittest tests.test_atlas_tensions_checker tests.test_role_conformance` equivalents already used in the inherited task; atlas trace test as before.
* `ruff check`, `ruff format --check`, `mypy --strict` on the two files.
* `flock -n /tmp/ama-rpi-heavy.lock python -m checks.atlas_tensions_browser_check` (1280 and 320 inside).
* `flock -n ... python ROOT/.../diagnostic/visibility_d3.py 1280|320` (copied from the D3 record, unmodified) for the actual served-fixture negative pair.

## Rollback

Restore `DESIGN_VERSION_FIELDS` from `a6c8df61` if any check reveals the options break 320px rendering; preserve the failed log and stop (no retry).
