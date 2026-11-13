---
title: "#164 changes: wire gate into Run"
ms.date: 2026-11-13
---

* `chat_eval.py`: positive-bound validation, serialised dispatch, usage reconciliation with halt, `_gated` wiring in `Run`, `AuthorizedModel.expand`.
* `test_chat_eval.py`: zero bounds, Run wrapping and subclass bypass, usage breach and halt.
* `README.md`: behaviour and remaining open items (persisted ledger, owner evidence).
* Checks (`/tmp/venv-164w-1800`): 109 unittest OK; ruff check and format clean; mypy clean.
