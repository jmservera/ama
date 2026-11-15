---
title: Issue 232 housing screen accessibility audit plan
ms.date: 2026-11-13
---

## Plan

* [ ] Phase 1: build `/tmp/venv-232-1905` with pip (editable core, agents, api, playwright 1.64.0).
* [ ] Phase 2: run `test_accessibility_baseline`, `test_role_screens`, `test_role_screens_conformance`, `test_specialist_keyboard_check` unit tests.
* [ ] Phase 3: run `role_screens_browser_check` (with `ZF_AXE_JS` pinned axe) and `specialist_keyboard_browser_check` under `flock /tmp/ama-rpi-heavy.lock`.
* [ ] Phase 4: record exact results, commands and the assistive-technology residual in the changes file; do not tick the criterion.
* [ ] Phase 5: independent `code-review`, remove venv, commit.

Details: [details](../../details/2026-11-13/232-housing-screen-a11y-audit-1905-details.md).
