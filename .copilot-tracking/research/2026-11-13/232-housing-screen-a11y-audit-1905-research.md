---
title: Issue 232 housing screen accessibility audit research
ms.date: 2026-11-13
---

## Scope

Audit the one unchecked criterion of #232: "Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation". Tier: Focused (read-only audit plus a changes record; no source change planned).

## Disposition

Research disposition: executed. Planning Readiness: Ready.

## Evidence found

* `src/api/tests/test_accessibility_baseline.py` (`Wcag22Baseline`): static WCAG 2.2 baseline checks (language, zoom, contrast, focus, 24px targets, status regions, table captions).
* `src/api/checks/role_screens_browser_check.py`: constructed stories `232` (resident choice/pause/update commitment queue) and `232s` (service issue, contact needs, safe route); asserts text state meaning (`check_readonly_accessibility`), Tab reachability per table, design-system use and, with `ZF_AXE_JS`, an axe-core 4.10.3 scan of `main` (SHA-256 pinned in the check).
* `src/api/checks/specialist_keyboard_browser_check.py` with `tests/test_specialist_keyboard_check.py`: Tab/Shift+Tab/Enter walk of specialist screens with focus visibility and status-region text.
* `src/api/tests/test_role_screens.py`, `test_role_screens_conformance.py`: unit coverage for the role screens.
* A pinned axe 4.10.3 file is available locally at `/tmp/axepk/package/axe.min.js`; its SHA-256 matches `AXE_SHA256` in the check.
* Chromium for Playwright is installed in `~/.cache/ms-playwright`.

## Limits

* The checks are synthetic engineering evidence. The checks' own documentation states DOM status text is not assistive-technology output and axe incomplete results need human assessment.
* No screen-reader, voice-control, magnification or human-validation evidence exists in these checks; that stays an honest residual (#155 owns validation).

## Determination

Run the listed existing checks in a throwaway pip venv `/tmp/venv-232-1905`, record exact results and the residual in the changes file, and do not tick the criterion: only the issue owner can do that on reviewed evidence.
