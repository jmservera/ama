---
title: Issue 2201 live9 review
ms.date: 2026-11-23
---

Review executed once. Outcome: conformant with routed open work.

* The change records only `type(error).__name__`; no message, connection detail or secret reaches stderr. Verified by an exact-stderr assertion and by the recorded attribute being the class name only.
* Raised error codes are unchanged; existing 109 tests pass; mypy and ruff clean.
* Routed open work: deploy the image and capture `receive_error_type` or `callback_error_type` from the next Failed receiver run (needs owner-authorised redeploy); the 23 Nov 09:30 to 11:30 cause stays unproven.
