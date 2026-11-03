---
title: Issue 222 golden-set cohort reporting plan
ms.date: 2026-11-03
---

## Plan

* [x] Phase 1: add `cohort_report` to `agents.ai_eval` and a `cohorts` section in `run_eval` and the text output.
* [x] Phase 2: test that the section is blocked, synthetic, not fairness evidence, reconciles per dimension and marks AI-task cohorts not evaluated.
* [x] Phase 3: README note; ruff, format, mypy (cache /tmp/mypy-222), focused tests.

Details: see [phase details](../details/2026-11-03-issue-222-golden-cohort-report-details.md).

## Critique

Executed once, direct. Applied: report only counts and codes, no pass/fail averaging; `passed` is unchanged so the golden gate does not depend on approval; no approval is supplied. Not security, infrastructure, SQL or deployment: focused tier; gate not run.
