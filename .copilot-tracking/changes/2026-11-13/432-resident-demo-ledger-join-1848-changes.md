---
title: Issue 432 resident demo ledger join changes
description: Implementation changes and validation
ms.date: 2026-11-13
---

* `aoai.py`: close the ledger reservation as `provider-unavailable` on credential/expiry exits; `configured_advisor(..., meters=None)` seam.
* `assistant.py`: close the reservation on empty credential and expiry exits.
* `test_resident_ledger_meter.py`: `call_join` and content-free canary tests (question, guidance, failure, credential failure, topic provider, configured seam).
* `test_ai_consumption_api.py`: `read-document` text join and canary test.
* `test_ai_call_site_inventory.py`: notes only; classifications unchanged because no host supplies a ledger, price or authority (owner decision on #432).

Validation: inventory, `test_ai_consumption*` (api 44 with inventory, core 43), `test_resident_*` api, resident showcase core, ruff, mypy core and api passed. Pre-existing failure: `test_resident_summary_ai_ui` (Playwright driver connection closed; fails on the unmodified baseline). Note: a test in the suite deletes `/tmp/venv-*`.
