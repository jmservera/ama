---
title: Issue 82 funding readers critique (follow-up RV01)
ms.date: 2026-11-12
task_id: funding-readers-82-2250
---

## Execution

Critique executed once, by an independent read-only reviewer agent (rubber-duck, default harness model) on the final candidate plan. Verdict as returned: needs changes. Verdict after applying compatible findings: conformant. No second critique is run for this task.

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| CR-01 | Blocking | `taskqueues.py:7` `MEMBERSHIP_REVISION` is part of the SQL queue fingerprint (`sqlstore.py:761-775`). Changing the funding expression without bumping it leaves persisted `queue_blocked` flags stale in existing databases, so cases with non-boolean funding stay out of the blocked queue until another change. | Applied directly. Bump `MEMBERSHIP_REVISION` from 2 to 3 in `taskqueues.py` (inside the write surface, existing mechanism and precedent `a86282c4b`). Add a regression in `test_sqlqueues.py` modelled on `test_old_certified_memberships_refresh_without_case_or_audit_writes`: a persisted revision-2 fingerprint and stale flag refresh to blocked on reopen. No scope exception needed. |
| CR-02 | Non-blocking | The home-case API test does not cover absent or non-boolean funding, which is the user-visible `KeyError` path. | Applied directly, kept minimal: one assertion in the existing `test_home_case_api.py` that an absent key returns 200 with `funding_confirmed` `False`. |
| CR-03 | Advice | Inline `is True` is acceptable versus a shared helper. | Accepted; no helper, matching the delivered store fix and the write-surface limit. |

No finding conflicts with a confirmed decision. No significant or divergent issue needed a user decision.
