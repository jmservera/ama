---
title: Issue 215 research, regulatory alerts and home chat UX
date: 2026-11-17
---

# Research opened

Scope: measure current state of the unticked criteria (WCAG 2.2 AA human AT testing, staff comprehension) and
run the targeted tests on base eb51af5c. Research disposition: executed. Results appended below.

## Measurements (base eb51af5c, worktree-pinned PYTHONPATH, sequential)

* Note: the installed `zava-forward-*` editable packages resolve to the main checkout; tests were run with the worktree `src/*/src` first on PYTHONPATH so the worktree sources are measured.
* `python3 -m unittest test_regulatory_ux_check test_home_chat_regulatory_keyboard_provenance test_alert_chat_keyboard_provenance test_alert_chat_keyboard_live test_regulatory_ux_accessibility test_regulatory_chat_live_region_semantics -q` (cwd `src/api`): 73 tests OK.
* Earlier run of 86 related tests (ux check, a11y cues, role matrix, comprehension score, AT record, rule alerts, chat API) with default import resolution: OK.
* `python3 src/api/checks/regulatory_ux_check.py --out /tmp/ux215.json`: outcome passed, 21 browser states, axe skipped (not supplied), staff_comprehension "Not run; unmet".
* Unavailable states (503 alerts, chat errors) already carry owner, next action and a human route (`chat.js` unavailableNote and related lines).
* Issue comments (latest 2026-11-16): criterion 3 restored to unchecked pending human assistive-technology testing under #155; criterion 5 needs real staff sessions needing owner authorisation. Out of scope here: #1818/#1641 (core mssqlstore, chat grounding).

Planning readiness: Ready. No defect reproduced; the remaining criteria are human-only.
