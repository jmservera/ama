---
title: Issue 232 resident engagement screens accessibility changes
ms.date: 2026-11-13
---

## Outcome

Implementation commit `8c8c7503c` on `feat/demo-232-resident-screens-a11y-2220` (base `36a2a5733`). The #232 criterion 4 is not ticked: automated synthetic evidence does not establish WCAG 2.2 conformance or assistive-technology acceptance, and only the issue owner can tick it. Not pushed; no PR.

## Files changed

| File | Change |
| --- | --- |
| `src/api/src/zava_forward/api/web/role-screens.js` | Opt-in `rowHeader` for `screenTable`, `screenRecordTable` wrapper for seven resident tables; choice screen service request table shows "State and meaning" |
| `src/api/tests/test_resident_choice_screen.py`, `test_resident_service_screen.py` | Table caption, column header and row header structure; state meaning text |
| `src/api/checks/role_screens_browser_check.py` | `check_table_headers`, extracted `run_axe`, queue-state axe, 320 px Tab reach for stories 232 and 232s |
| `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/log.md` | Dated status section and log entry |

No `aria-invalid` site, scenario recipe, `infra/`, #215 module or ranking file changed, so the counted guard and `scenario-manifest.json` SHA needed no update.

## Validation (Focused tier)

Environment: pip venv `/tmp/venv-232-2220` (editable `src/core`, `src/agents`, `src/api`, `playwright==1.64.0`, ruff, mypy; no uv), Chromium 156 from the Playwright cache, pinned axe 4.10.3 at `/tmp/axepk/package/axe.min.js` (SHA-256 asserted by the check). Venv removed after the work.

| Check | Result |
| --- | --- |
| Unit: `test_accessibility_baseline test_content_standard test_design_system test_role_screens test_role_screens_conformance test_resident_choice_screen test_resident_service_screen test_specialist_keyboard_check test_workspace_scripts` | 105 tests OK |
| Core: `test_scenario_manifest test_needs_inventory test_atlas_screen_trace` | 36 tests OK |
| `role_screens_browser_check 232` | exit 0, 48 PASS, axe no violations in queue and selected states, incomplete empty |
| `role_screens_browser_check 232s` | exit 0, 47 PASS, same axe result |
| `specialist_keyboard_browser_check` | exit 0, 805 PASS |
| `ruff check .`, `ruff format --check`, `mypy .` (from `src/api`) | clean; 154 files formatted; 239 source files no issues |
| Negative proof | With the JS change stashed, the 232 check fails on "no row header" |

## Automated versus human evidence

Automated: axe, DOM structure, Tab reach and static tests on constructed data in Chromium. Not evidenced: screen-reader or voice-control output, human review of wording, cross-browser, hosted CI (not pushed), reflow beyond the checked widths. #155 owns validation.
