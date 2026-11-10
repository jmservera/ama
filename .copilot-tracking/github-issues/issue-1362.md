---
title: Match the current design version field in Atlas browser coverage
description: Issue metadata and status for #1362, a nonblocking assertion gap in the two-screen tension browser check
ms.date: 2026-11-10
ms.topic: reference
---

## Issue

* Issue: #1362, https://github.com/jmservera/ama/issues/1362 (OPEN, created 2026-11-10). Generic template; no labels, type or assignee when read.
* Refs: #233 and #149. Source candidate: branch `test/demo-tension-coverage-233-1110`, head `6725ba504beeef2d229eeae643a0b26289ea7ee4`.
* Origin: independent Functional assessment 709b5365-5029-49c7-92f7-1d7576b54718 (all 13 changed files, approve_with_comments, 0 Critical, High or Low, 1 nonblocking Medium).

## Finding

* `src/api/checks/atlas_tensions_browser_check.py` lines 407-413 test the expected current design version `1` as a substring of the whole Design version panel. The panel also holds the recorded timestamp `2026-10-20T09:00:00Z`, which contains `1`. A rendered current version of 2, Unknown or an omitted value could therefore still pass.
* Evidence class: a static counterexample. It is not a browser mutation run and not a product defect. Current-version coverage is PARTIAL; no claim that every new assertion is semantically correct.
* Suggested direction from the review (not applied): assert exact equality on the value under the Current design version label, and add a negative control where the version is 2 or Unknown while the timestamp still contains `1`.

## Status

* [ ] Exact-field assertion and negative control: NOT done. No fix, test or source change is made in this record.
* No repair or new allowance is granted. Earlier corrections are retained; the numeric correction balance is UNKNOWN and Root must reconcile finite authority before any code repair.
* Use Refs, never a closing keyword. This issue is not whole #233 or #149 acceptance, WCAG, assistive-technology, usability, real-data or live acceptance.
