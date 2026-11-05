---
title: Issue 96 r14 research, approval reference versus field issues
ms.date: 2026-11-05
---

Prospective, dated 2026-11-05. Refs #96, parent #93, PR #1223. Start head `4e78e2354f26f293eb07a50d534ae969da32172a`, base `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. Earlier records and the r13 receipt are preserved; r13 is historical for any new head.

## Claim under test

The independent review (`review-1223-4e78/review.md`, static trace only, not executed) says `_bound_causes` (`form_review.py` lines 276-308) checks membership, staleness and later history only. `_report` builds `issues` (Fail for a schema-invalid accepted value, Unknown for missing required input, Conflict) but `_approvals` receives only `impact` and `stale`, so a well-formed reference to a field with an open issue is labelled Current.

## Source read

Confirmed by reading `_report` and `_approvals`: issues are never passed to `_approvals`. Introduced by r6 in this PR (the evaluator is new). Reproduction by focused JSON and SQLite tests is the next step; if it does not fail, no source change is made.

## Intended minimal fix if reproduced

Pass the set of field ids that have an issue in the same report to `_approvals`/`_bound_causes`; a listed field with an open issue adds the cause `field-issue-open` and the field to `fields`, giving Review required. No new scans, reports, approval semantics or writes.
