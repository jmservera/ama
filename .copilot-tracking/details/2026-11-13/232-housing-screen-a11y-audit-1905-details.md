---
title: Issue 232 housing screen accessibility audit details
ms.date: 2026-11-13
---

## Commands (from `src/api`)

* `export PYTHONPATH=tests:../core/tests:../agents/tests ZF_BROWSER_TESTS=1 ZF_AXE_JS=/tmp/axepk/package/axe.min.js`
* `python -m unittest test_accessibility_baseline test_role_screens test_role_screens_conformance test_specialist_keyboard_check test_resident_choice_screen test_resident_service_screen -q`
* `flock -w 600 /tmp/ama-rpi-heavy.lock python -m checks.role_screens_browser_check 232` and the same with `232s`; record both outputs
* `flock -w 600 /tmp/ama-rpi-heavy.lock python -m checks.specialist_keyboard_browser_check`

## Success

* Every command exits zero; any skip, failure or incomplete axe result is recorded verbatim, never hidden. A failure is recorded as a finding, not fixed in this task (audit only).
* The changes file separates automated evidence from the residual: no screen reader, voice control, magnification, or human validation; axe incomplete items need human assessment.
* State that axe scans `main` of selected synthetic scenarios only, and that the keyboard fixture may declare a no-table gap for the service screen, which is a gap and not a pass.
* No source files change; the issue is not edited and the criterion is not ticked.
