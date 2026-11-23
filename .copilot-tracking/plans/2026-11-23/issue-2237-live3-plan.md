---
title: Plan issue 2237 live3
ms.date: 2026-11-23
---

Plan: add one API regression test, record a live re-proof note, finish with per-criterion table.

* [ ] Phase 1: add `test_retention_listing_recovers_on_retry_after_busy_lock_503` to src/api/tests/test_error_logging.py.
* [ ] Phase 2: write docs/reference/research/issue-2237-live3-2026-11-23.md with live evidence.
* [ ] Phase 3: run the test file, mypy and ruff for src/api; commit.

Tier: focused (test and docs only, no src code change). Details: [details](../../details/2026-11-23/issue-2237-live3-details.md).

## Critique (executed once)

Verdict: proceed. The test must fail if the 503 path left state behind, so it patches `store.audit` to raise once then restores it, and asserts 503 then 200 with a `records` key. Compatible finding applied: also assert the 503 body carries no secret. No conflict with confirmed owner decisions.
