---
title: Issue 432 resident demo ledger join review
description: Independent code-review outcome
ms.date: 2026-11-13
---

Execution: one independent code-review. Outcome: no high-confidence findings. The reviewer reported two subtest failures in `test_actual_chat_adapter_preserves_metering_without_proposal_eligibility` under a different PYTHONPATH; the full `test_ai_consumption_api` module passed (44 tests with the inventory) in the validation venv. Host wiring of the resident ledger join (ledger store, price, authority) remains an owner decision on #432; F1 is not claimed closed. Human approval and hosted CI are not satisfied.
