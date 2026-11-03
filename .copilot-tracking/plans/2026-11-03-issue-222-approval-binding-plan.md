---
title: Issue 222 approval binding plan
ms.date: 2026-11-03
---

## Plan

* [x] Phase 1: add `manifest_digest` and `approve` to `core.cohort_eval`; require `lawful_fields_owner` and a matching digest in `_thresholds_approved`.
* [x] Phase 2: update fixtures and the ranking run to approve after the manifest is final; add a test that incomplete or stale approval blocks and a disposition cannot clear it.
* [x] Phase 3: README note; ruff, format, mypy, focused tests.

Details: see [phase details](../details/2026-11-03-issue-222-approval-binding-details.md).

## Critique

Executed once, direct. Applied: digest excludes only the approval block so any case, cohort or threshold edit voids approval; unapproved remains non-disposable. Not security, infrastructure, SQL or deployment: focused tier.
