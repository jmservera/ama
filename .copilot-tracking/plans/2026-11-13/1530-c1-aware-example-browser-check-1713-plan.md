---
title: Issue 1530 C1 fix plan
description: Add aware-hint example and committed populated safety panel browser check
ms.date: 2026-11-13
---

* [ ] Phase 1: `app.js` `hz-aware-hint` gains `Example: Resident phoned the repairs desk at 09:15 on 13 Nov 2026.`; `test_safety_panel_ux.py` asserts `Example:` on `hz-note-hint`, `hz-source-hint` and `hz-aware-hint`.
* [ ] Phase 2: `case_view_ux_browser_check.py` gains `populated_safety_panel` (route fixture injects one referred open hazard and one legacy hazard on ZF-1) scanning `#case-safety` at 1280, 390, 320 px and 200% root font scale with pinned axe (0 violations) and no horizontal overflow; called from `run_browser` when not baseline.
* [ ] Phase 3: manifest digest: `scenario-manifest.json` binds only `workbench_browser_check.py`; update only if that file or a bound file changes (verify with `test_scenario_manifest`).
* [ ] Phase 4: run listed tests, browser check, ruff, mypy in `/tmp/venv-1530c1-1713`; remove venv; commit.
