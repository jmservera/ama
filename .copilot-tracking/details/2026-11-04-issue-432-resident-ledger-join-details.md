---
title: "Details: #432 resident adapter ledger join"
ms.date: 2026-11-04
---

* `assistant.py`: new optional `record_call`; `_close` passes outcome, validated counts and the returned model name only (no content). The default behaviour with no hook is unchanged.
* `ledger_meter.py`: input bound is ASCII prompt bytes plus 32 framing tokens; output bound is the envelope maximum. Per-thread open reservation; `token()` calls `dispatch_check` after the credential and refuses the call if held.
* Tests use a constructed SQLite port, a fake transport and a fake credential; no network, no price or authority beyond constructed values, no resident text.
