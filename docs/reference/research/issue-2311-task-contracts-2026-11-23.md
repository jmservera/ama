---
title: Issue 2311 per-task data contracts evidence
ms.date: 2026-11-23
---

## Scope

Evidence for #2311 (Refs #121, #107), synthetic demo, no live Azure action needed because every criterion is code or test.

## Result

* `task_contracts.CONTRACTS` declares purpose, audience, permitted fields with type and length, prohibited content and a minimum-necessary rationale for all 13 registered tasks; `ai_registry.data_contract` exposes it.
* `ai_prompts.render` calls `task_contracts.enforce` before any retained prompt is built. Undeclared fields, wrong types, over-length values and prohibited content (email, UK phone, National Insurance number, bank details, card number) raise `ContractRefusal` without echoing the value.
* `enforce(..., user_permission=True)` is ignored by design; tests show permission does not widen a contract.
* Evidence command, from `src/core`: `PYTHONPATH=src:tests python3 -m unittest tests/test_task_contracts.py -q` gives 8 tests, OK.

## Limits

* Assistant, chat and concern-pack contracts are declared and callable through `enforce`, but their prompt builders are not yet routed through it (follow-up).
* Regex patterns catch identifiers only, not free-text special-category data.
* DPO and Legal approval is not claimed; it stays under #121.
