---
title: Issue 79 research, r25 stage-cleanup masking correction
ms.date: 2026-11-07
---

Task `issue-79-r25-stagecleanup`, parent `issue-79-r24-dirsync-audit`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Start: head `fd57f086d62f1446f8e1dbc3c7f8c89ca41a8c9b`, tree `e6e483dbf8a1806e64bc462302cd4fae70810aa1`, ignored-clean; `origin/main` `23b26a7f3a4693cd20dcf0447303d97491096cb3`. Preserve ref `preserve/issue-79-pre-stagecleanup`. Child 1231 (`4ec4c280...`) is read as Git objects only, not touched.
* Independent functional assessment ad3cab63 (`functional-findings.json`): parent standalone `request_changes`, one High. In parent `publish`, `finally: os.unlink(tmp)` runs after the final link. If the folder sync raised `DurabilityUnconfirmedError` and the unlink also fails (EROFS, PermissionError), the unlink error replaces it. Store then sees a plain `OSError`, writes no unconfirmed audit for the retained record, and the API may return 403 for a `PermissionError`. The same unlink in `finally` can also mask a link or write failure.
* Child 4ec4c280 fixes this with `_remove` (returns True only when the stage remains, never raises), `stage_retained` metadata on the typed error and result, and `_confirmed`. Parent-compatible minimum: reuse `_remove` and the `stage_retained` name.
* Out of scope, separate follow-ups: newly created archive ancestor fsync; existing file or dangling link schedule behaviour. No policy, schema or auth change.

## Conclusions

* Make the parent stage cleanup non-throwing in its `finally`, keep the original exception or committed outcome, and record a retained stage as metadata. Never delete another writer's stage and never present cleanup failure as rollback or confirmation.
