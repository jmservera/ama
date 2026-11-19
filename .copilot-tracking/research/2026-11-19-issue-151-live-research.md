---
title: Issue 151 live research 2026-11-19
---

## Scope

Issue #151, one unticked criterion: "Manual screen-reader and keyboard checks are recorded for each role workflow". Research disposition: executed (repository inspection only).

## Evidence

* `docs/reference/research/ux/wcag-conformance-baseline.md` "Manual check record" lists eight role workflows, every cell `Not run`; the template requires a named tester, tool and browser versions, per screen reader per OS.
* Automated keyboard walks already exist (`src/api/checks/specialist_keyboard_browser_check.py`, `src/api/tests/test_specialist_keyboard_check.py`, `test_safety_screen_wcag_keyboard.py`, `test_assistant_panel_a11y_159.py`); the baseline states these are browser DOM evidence, not assistive-technology output.
* Owner decision 2026-11-18: person-run assistive-technology testing is not needed for the demo.

## Classification

The criterion needs a human running a real screen reader (NVDA, VoiceOver). No code or test can prove it, and a synthetic substitute would be a fabricated record. Planning Readiness: Ready (stop, no source change).
