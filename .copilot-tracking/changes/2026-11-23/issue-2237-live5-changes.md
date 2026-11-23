---
title: Changes issue 2237 live5
ms.date: 2026-11-23
---

## Changes

* Modified: `approve_retention_deletion` in src/core/src/zava_forward/core/doc_controls.py. An unreadable retention trigger date now raises a plain ValueError (HTTP 400, "cannot be read, so nothing was deleted") instead of the raw parser message; nothing is deleted.
* Added: `test_approving_unreadable_trigger_date_is_refused_with_a_plain_message` in src/api/tests/test_document_controls.py (memory and SQL stores).

## Validation

test_document_controls 23 tests OK; ruff check clean; mypy in src/api clean (375 files). Tier: FULL applies (src change); the coordinator runs the gate; `rpi-checks.py --all` not run. Not deployed: registry `crcutovertestrzsrg` has public network access disabled, and live revision 0000058 (2026-11-23T19:20Z) predates both the live4 and live5 fixes.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history, not on demand | logged 500s; live3 note; no drills (owner decision) |
| Find the cause in the demo container logs | Proven | docs/reference/research/issue-2237-live-cause-and-fix-2026-11-23.md |
| Fix with a regression test | Proven | #2290 tests, live4 malformed-date test, and the new approval test |
| Re-prove 200 live | Proven on 0000056 (56 of 56, live3); the new code is unproven live | not deployable without changing registry network rules (estate change not authorised) |
