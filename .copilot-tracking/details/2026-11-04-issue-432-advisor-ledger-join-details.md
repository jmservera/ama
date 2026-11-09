---
title: "Details: #432 resident advisor ledger join"
ms.date: 2026-11-04
---

* `ledger_meter.py`: `capability` and `case_type` keyword arguments (defaults `resident-topic`, `resident-chat`); `advisor_meters(consumption, model, configuration, prompts)` requires a prompt version per kind.
* `aoai.py`: `_request(payload, resident, kind)`. Order is payload checks, SQL reserve, ledger reserve, credential (wrapped for the dispatch recheck), transport, ledger close, then the existing validation and SQL complete. Transport errors close the ledger as `timeout` or `provider-unavailable` and re-raise unchanged. Ledger close failures are logged and never change the resident outcome.
* Pre-dispatch failures after the ledger reservation (credential error) stay open and become unknown liability after 40 seconds, matching the topic adapter and the never-refund rule.
* Input bound for the ledger is the ASCII payload byte length plus 32 framing tokens (bytes upper-bound tokens).
