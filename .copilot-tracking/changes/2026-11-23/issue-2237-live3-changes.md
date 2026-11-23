---
title: Changes issue 2237 live3
ms.date: 2026-11-23
---

## Changes

* Added: `test_retention_listing_recovers_with_200_on_the_request_after_a_busy_lock_503` in src/api/tests/test_error_logging.py.
* Added: docs/reference/research/issue-2237-live3-2026-11-23.md and its evidence folder.

## Validation

test_error_logging 13 tests OK; mypy (src/api) clean; ruff check and format clean. Tier: focused (test and docs only, no src code change).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history, not on demand | logged 500s; local deterministic test; no live drill |
| Find the cause in the demo container logs | Proven | cause note |
| Fix with a regression test | Proven | #2290 tests plus new retry test |
| Re-prove 200 live | Proven on 0000056 | 56 of 56 requests 200 |
