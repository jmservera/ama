---
title: Issue 130 nomination read-only view plan
description: Prospective plan for the read-only employee nomination section in the Resident tab (issue 130)
ms.date: 2026-11-10
---

## Task

Task `issue-130-nomination-view-1110`. Research: [issue-130-nomination-view-1110-research.md](../../research/2026-11-10/issue-130-nomination-view-1110-research.md). Details: [issue-130-nomination-view-1110-details.md](../../details/2026-11-10/issue-130-nomination-view-1110-details.md).

## Objective

Add a read-only "Nominations and self-referrals" section to the employee Resident tab that renders existing server-authorised `nomination_records` and `follow_up`. No backend, API, store, schema, mutation, model call, contact, eligibility, assignment, representative or decision-engine change.

## Phases

* [ ] Phase 1: add `nominationPanel(c)` to `panels.js` and compose it in the Resident tab at `app.js:1065`.
* [ ] Phase 2: node renderer test `tests/test_nomination_screen.py` over constructed states (original, correction with stale review, current review, legacy missing fields, empty list, role-denied absent key, escaping).
* [ ] Phase 3: loopback browser check `checks/nomination_browser_check.py` (keyboard, literal text, no resident POST or model call, role denial, reduced motion, axe scan, state unchanged).
* [ ] Phase 4: focused validation, changes record, Review.

## Success criteria

* Original and each correction are shown separately (supplied account, source, channel, recorder, time); the original is never overwritten in the display.
* Owner, next update with overdue state, route, acknowledgement reference and the literal words "Delivery unverified" are shown. Missing values read "Not recorded" or "Unknown".
* Identity, support and risk values display the server value; an unknown or absent value is never shown as "None".
* Each review is labelled "Current for version N" or "Stale: recorded for version N, record now at version M" in words, plus "Correction awaiting human re-review" and "No human review recorded".
* A role denied by the server (neither `challenge_targets` nor `nomination_records` supplied) sees no section; an authorised case with no records sees the empty state. Existing resident, call, draft and challenge paths are unchanged.
* The page makes no POST, PUT or PATCH while rendering and opening records, and no model call. Server case state is unchanged after the exercise.
* Existing Core resident-decisions and API resident tests, copy audit, accessibility baseline, design system and challenge browser check stay green.
* Declared overlap: new function in `panels.js` and a one-line edit at `app.js:1065` only. No backend file changes (proved by `git diff --stat` and an empty diff for `src/core`).

## Validation tier

FOCUSED/DEMO, not the complete local gate and not a `--changed` receipt. Checks: changed-JS `node --check`; ruff check and format for changed Python; mypy on API files including tests and checks; affected API tests; Core `test_resident_decisions`; API `test_resident_api`; copy and accessibility tests; the new owned loopback browser run and the existing `challenge_browser_check.py`, each under the heavy-resource lock. No SQL Server, MSSQL, Azure, model or real data. The existing `ResidentApi` synthetic SQLite fixture is used and is not SQL Server acceptance. No manifest hash update unless a registered recipe changes (verified not applicable in research).

## Human and authority limits

No human assistive-technology or WCAG acceptance is claimed. Fluent 2 tokens, plain-language standard, native semantics (`details`, `summary`, `dl`, headings), non-colour status text and reduced motion are preserved. The view does not approve anything; OD-41 and OD-42 stay open.

## Review plan

One post-implementation Review. Any source defect found is reported and frozen; no correction batch is authorised.
