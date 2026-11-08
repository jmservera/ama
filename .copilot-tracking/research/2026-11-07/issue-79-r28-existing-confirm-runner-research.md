---
title: Issue 79 r28 research, existing-record durability confirmation and runner uncertainty outcome
ms.date: 2026-11-07
---

Research disposition: executed. Planning Readiness: Ready.

* Root `d99e6901e5fb7e4c8ea46ba3766ff23f31be0f7c`, tree `900c772c7c2b22b729b99eb0c37eb030d6261684`, ignored-clean; fetched `origin/main` is `f0afa8d76d7be13ec4278321e09e16e23eaeb37c`. Preserve ref `preserve/issue-79-pre-existingconfirm`. Child `61f3ebe1` is read only as Git objects.
* Independent functional report `review-ranking-61f3e-r29/functional-findings.json` (read by the coordinator; preserved, not replaced): ROOT request_changes (High: an existing record, retry or race loser returns `written: false` without a folder sync, so a retry after a failed sync is reported as published); CHILD and COMBINED approve_with_comments with a Medium runner contract finding.
* Root code: `publish` returns `_existing(...)` early for a pre-existing name and, after the r25 change, skips the folder sync on `FileExistsError`; the runner catches `(PublicationError, OSError)` into `publish_failed` refusal (status `refused`, exit 2), so a `DurabilityUnconfirmedError` (record linked) is reported like a no-write refusal.
* Child `61f3ebe1` `ranking_publication.py` has `_confirmed(outcome, archive_dir)`: sync the folder for every outcome (new, existing, race loser), raise `DurabilityUnconfirmedError` on failure with `stage_retained` carried over. Reusing that logic fits the root stage-prefix tests; the child private-stage metadata and `.ranking-*.tmp` naming are out of scope.
* Not in scope: #1258 ancestor durability, #1259 unusable archive window, the child Low stale-metadata snapshot, quota, policy.
