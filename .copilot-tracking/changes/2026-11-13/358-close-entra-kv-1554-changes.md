---
title: Issue 358 close-out changes
ms.date: 2026-11-13
---

No source or test change: existing tests cover all three items. Added RPI evidence only. Validation: `test_setup_entra` plus `test_initialize_api_auth` 141 OK; mypy clean on `initialize-api-auth.py`; two guard mutations fail tests and were restored; live read-only inspect of `ca-cutover-test-api` returned no secrets (null). Full `infra/tests` discovery has pre-existing environmental failures (49 failures, 32 errors) on this host. Residual: populated live round-trip stays unmet (#358, #360).
