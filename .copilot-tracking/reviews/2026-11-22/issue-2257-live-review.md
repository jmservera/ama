---
title: Issue 2257 review
ms.date: 2026-11-22
---

Review executed once. Outcome: conformant with open items routed as follow-ups.

* Retry is bounded, GET-only, abort-aware; mutations untouched; status restored in `finally`.
* Tests updated for the deliberate behaviour change; web guideline suites pass.
* Open (later work): deploy the client; consider min replicas 1 and probe timeouts; request-level cause remains unproven.
