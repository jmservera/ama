# Plan: authority rotation non-replenishment (Refs #107)

* [x] Phase 1: add `Assistants._pool`, which inherits the persisted ledger for an unseen authority digest; use it in `_reserve` and `disabled`.
* [x] Phase 2: failing-first tests in `src/api/tests/test_assistant_restart_non_replenishment.py` (calls, tokens, remaining-spend-once).
* [x] Phase 3: focused validation (ruff, mypy, core and api unittests) and review.

Critique: executed once, inline. Findings compatible; no conflict with confirmed decisions. Details: [details](../../details/2026-11-14/107-authority-refill-guard-0150-details.md).
