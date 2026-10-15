---
title: PR 286 review fixes changes
description: Changes made for the five PR 286 review findings
ms.date: 2026-10-15
---

* `mvp/zavaforward_mvp/chat_isolation.py`: memory_for uses prompt_memory; masked question prompted; replies redacted before storage; out-of-scope case raises ChatNotFound.
* `mvp/zavaforward_mvp/server.py`: memory lifecycle endpoints; ChatNotFound and LookupError return 404.
* `mvp/tests/test_chat_isolation.py`: opt-in helper, lifecycle gating, masking and redaction, 404 tests.
* `mvp/README.md`: endpoint list and behaviour.

Validation: `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` (result in review).
