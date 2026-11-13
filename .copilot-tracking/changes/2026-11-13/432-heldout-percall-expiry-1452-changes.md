---
title: Issue 432 per-call expiry changes
ms.date: 2026-11-13
---

* `heldout_batch.py`: `clock` replaces `now` on `run_batch`; `_drift` re-checks authorization and freeze identity before every dispatch; dry-run always uses `dry_run_call`; non-object proposals are refused; gate exceptions become refusals.
* `test_heldout_batch.py`: tests pass `clock`; new tests for expiry, drift, replacement manifest, clock failure, dry-run and non-object proposals.
* Divergence: the plan-done and implement-start witness records were written after the first code edits (critique had already run); the first implement-start was refused for the missing changes artifact and retried.
* Validation: test_heldout_batch and full src/agents (376 tests) OK; ruff check, ruff format --check and mypy clean.
