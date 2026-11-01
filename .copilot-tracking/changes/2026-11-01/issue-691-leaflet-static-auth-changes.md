---
title: Issue 691 follow-up changes
date: 2026-11-01
---

* `src/api/src/zava_forward/api/server.py`: static non-HTML assets authenticate with the provider only; `index.html` keeps identity binding.
* `src/api/tests/test_employee_live_responses.py`: `test_vendor_asset_does_not_depend_on_the_identity_store` (fails without the fix, passes with it).

Validation: test_employee_live_responses (7), test_static_assets (5), test_employee_identity_check (7), test_auth (40) pass; ruff check and format pass; mypy on server.py clean.
Live re-check after next deploy: pending.
