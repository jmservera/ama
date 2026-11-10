---
title: Issue 1388 creation record (delayed-companion route-delivery race)
description: Created checker-synchronization bug, initial scope and shared-file ordering, separate from 133 and 1384
ms.date: 2026-11-10
ms.topic: reference
---

## Created Issue

* Issue: #1388, https://github.com/jmservera/ama/issues/1388
* Created: 2026-11-10T13:24:00Z (state OPEN at the admission snapshot, no comments).
* Title: fix: synchronize delayed-companion browser checks with route delivery
* Template: generic bug; `.github/ISSUE_TEMPLATE` is absent.
* Labels: `bug`. Assignees/type: none specified.
* Severity: Medium checker-synchronization defect. No production loader defect is observed.

## Initial Scope and Dependency

* Defect: at main `65c2ab9d947d1498dafd37e24a377d1ff503e86f`,
  `src/api/checks/workspace_scripts_browser_check.py::delayed_companion` can see the retry script in
  the DOM before Playwright delivers the intercepted request to the Python route callback, so the
  exact `len(pending) == 1` assertion sees zero (a 2-6 ms gap in all three captured failures).
* Scope: only the delayed-companion synchronization in that checker and a focused regression test,
  plus this RPI evidence. No loader, app, roles/auth, retry count or delay, exhaustion parser,
  employee checker, aftercare or infrastructure change.
* Distinct initial main-based bug fix. It is not a correction-budget extension for #133 or #1384
  and has no dependency on held #132. #1384 owns the separate exhaustion-count oracle and stays
  unpublished until this fix reaches main and its own BOTH browser checks then pass.
* Shared-file ordering: this task owns only `delayed_companion` and its direct regression in the
  checker file; the frozen #1384 candidate owns the exhaustion/count/parser and employee checker
  changes. No overlapping implementation is authorized.
* Original reproduction and diagnosis: the coordinator's read-only diagnostic (main 65c failed
  1 of 12 sequential samples without controls, candidate 3f1fa48 failed 2 of 12 without controls
  and 0 of 12 with controls, isolated modes 0 of 12; every capture had DOM-ready before Python
  delivery). The small samples are not a failure-rate estimate. The raw bundle is not duplicated here.
* Open criteria: deterministic red-before and green-after through the real routine, zero and double
  pending controls, four real-browser variants, loader/checker tests and configured static checks,
  independent exact-head review and hosted checks. The issue body is the authoritative text.
