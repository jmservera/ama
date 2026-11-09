<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refusal receipts initial plan critique
description: Single independent critique of the final prospective plan candidate, committed before any merge or source edit
ms.date: 2026-11-09
---

## Execution

* Critique executed once on the final candidate by an independent read-only `rubber-duck` subagent (harness default model, native), on the plan, details and research files, verifying against parent `e192bc74`. It is not repeated for this task. The independent exact-head review stays required later.
* Verdict returned: Revise (one blocking and two non-blocking findings). No user decision required. Dispositions below were applied to the plan and details in the same commit as this record.

## Findings and dispositions

* PC-001 (blocking, applied): the unstored payload (`{outcome, model_calls}`) disagreed with the plan wording of `tokens=None`, cost "Unknown". Disposition: reuse prior art exactly. The stored receipt is the full `_receipt(tid)` (tokens `None`, provider_outcome `not-called`, cost "Unknown"). The unstored receipt mirrors the existing `chat.turn.unstored` refusal payload `{outcome, model_calls: 0}`, which carries no token or cost field, so tokens stay unknown and nothing is fabricated. The plan, details and tests assert these two exact shapes.
* PC-002 (non-blocking, applied): the revocation control was ambiguous. Disposition: two controls. (a) A user refused before the stored-thread checks keeps the existing 403 and one `access-rejected` receipt (existing behaviour, unchanged). (b) A race after the thread checks passed but before the helper recheck is covered in core by a helper test with a refused user (no row), and described honestly: the HTTP 400 is preserved with no new receipt.
* PC-003 (non-blocking, applied): the plan excluded SQL while the core module runs SQLite tests. Disposition: no standalone disposable-SQL-Server suite is required because the audit seam is unchanged, but the full existing core and API test modules run as they are, and a focused helper persistence check uses the existing core fixture (`test_nested_store_lock_callers_preserve_json_and_sql_audits` style) to assert the audit row for both stores.
