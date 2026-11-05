---
title: Issue 96 r14 approval-reference open-issue changes
description: Changes and author Review for the published review's Medium diagnostic finding
ms.date: 2026-11-05
---

## Outcome

The static finding was reproduced on both JSON and SQLite stores at starting head
`4e78e2354f26f293eb07a50d534ae969da32172a`. A well-formed current-version approval
reference listing a field with an open issue (schema-invalid accepted value) was labelled
`Current`. It was not an approval bypass: no approval writer or reviewed export exists.

## RED and GREEN

* RED: `test_current_reference_to_a_field_with_an_open_issue_needs_review` failed at the
  start source (`'Current' != 'Review required'`). Log: `/tmp/g96-r14-red2.log`.
* GREEN: `test_form_dependencies`, `test_form_review`, `test_form_export` and
  `test_form_staging` together: 57 tests OK (`/tmp/g96-r14-green.log`).
* `ruff check`, `ruff format --check` and `mypy` from `src/core`: exit 0.
* Imports proved from this worktree; caches external; no ignored files.

## Changes

* `form_review.py`: `_report` passes the set of field ids that carry an issue into
  `_approvals` and `_bound_causes`. A listed field with an open issue, not already stale,
  adds cause `field-issue-open` and the field, so state is `Review required`. No new scans,
  reports, writes or approval semantics. The r12 missing-digest fix is untouched.
* `test_form_dependencies.py`: new regression (both stores, no mutation, unaffected-field
  Current control, plain Held kept). The existing approval-reference test now expects
  `field-issue-open` alongside `field-reviewed-after-approval` for the rejected `epc`
  field, whose rejection leaves a required-missing Unknown. This is an accurate extra cause.

## Deviations

* One `sed -i` line deletion was used on the test file instead of an edit tool. The diff
  was inspected afterwards.
* Test-fixture note: the first RED attempt failed on a positional assertion; the test was
  corrected to key by decision id before the authoritative RED.

## Self-review

* Scope is limited to the evaluator and its test. Stale fields keep `field-stale` only, to
  avoid duplicate causes. Unrelated drafts and Held references are unaffected.
* Remaining: a NEW FULL gate on the new head, independent exact-head review and hosted
  checks. Earlier receipts, including `/tmp/g96-r13-1105`, are historical for the prior
  head. C1, C5, residual C6 and parent #93 acceptance stay unproven. Refs #96.
