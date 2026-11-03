---
title: Plan for issue 619 automated accessibility slice
ms.date: 2026-11-03
---

* [x] Add `env_overrides` to `checks/design_system_browser_check.main`
* [x] Add `checks/production_config_a11y_browser_check.py`
* [x] Add `tests/test_production_config_a11y_check.py`
* [x] Update protocol, `src/api/README.md`, append `docs/reference/log.md`
* [x] Focused validation (unit tests, ruff, mypy, one browser run)

Stacked follow-up slices: resident site under its production image; re-run on the real production build; person-run rows.

Critique (single pass, executed): verdict proceed. Applied: only the existing axe pin is used; no password or secret in the header (synthetic GUIDs); do not claim conformance; Tab wrap to browser chrome is not treated as a failure. Not touching security code, infrastructure, SQL or deployment, so the focused tier applies.
