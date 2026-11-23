---
title: Changes issue 2237 live4
ms.date: 2026-11-23
---

## Changes

* Modified: `retention_due` in src/core/src/zava_forward/core/doc_controls.py. An unreadable `retention_trigger` or `stage_since` date now yields a row `needs review: trigger date unreadable` (or the legal-hold status) instead of a `ValueError` that failed the whole listing with 500. The sort key is None-safe.
* Added: `test_unreadable_trigger_date_is_listed_for_review_not_a_failure` in src/api/tests/test_document_controls.py (runs on the memory and SQL stores). It errors without the fix and passes with it.

## Validation

test_document_controls 21 tests OK; ruff check clean; mypy src/api clean; mypy src/core shows 3 pre-existing errors (missing opentelemetry stubs, one unused ignore) identical with the change stashed. Tier: FULL applies (src change); the coordinator runs the gate, `rpi-checks.py --all` was not run. Not deployed, so no live proof of the new behaviour.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history, not on demand | logged 500s; live3 note; no live drill (owner decision) |
| Find the cause in the demo container logs | Proven | docs/reference/research/issue-2237-live-cause-and-fix-2026-11-23.md |
| Fix with a regression test | Proven | #2290 tests, live3 retry test, and the new malformed-date test for a second 500 class |
| Re-prove 200 live | Proven on 0000056 (live3, 56 of 56); new code not deployed, not live-proven | docs/reference/research/issue-2237-live3-2026-11-23/result-live3.json |
