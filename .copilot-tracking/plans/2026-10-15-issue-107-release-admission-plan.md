---
title: Issue 107 release admission plan
description: Smallest coherent plan for RAI release admission on the existing assistants runtime
ms.date: 2026-10-15
---

## Phases

* [x] Add `assistant_release.py`: SQL `assistant_releases` table (portable DDL), record, suspend/revoke (terminal), admission check.
* [x] Wire `assistants.py`: runtime binding, `disabled()` admission (enqueue, claim), pre-dispatch recheck, completion recheck and serving-model attestation (quarantine and suspend), view/review/export reliance, registry exposure, record/change methods.
* [x] Gate retained legacy dispatch in `sqlstore.py` when AI is configured; add POST routes in `server.py`.
* [x] Tests: `test_assistant_release.py`, `release_support.py` fixtures; adapt existing tests.
* [x] README section; full suite.

Critique: executed once, verdict: compatible; applied directly (live provider needs an `actual` record; constructed fixtures never admit live Ai).

## PR 287 review-fix plan (2026-10-15)

* [x] Dialect-guard release DDL in test helper; add `_epoch_sql` dialect hook for `release_block`.
* [x] Pass the called deployment to the gate; add `ai_registry.legacy_binding` binding all versions.
* [x] Add legacy completion recheck that discards the result (`quarantined`).
* [x] Describe the serving-model check as a returned-model check, not attestation, in code, README and PR body.
* [x] Keep open items listed. Critique: one pass, compatible findings applied.
