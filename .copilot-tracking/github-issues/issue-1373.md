---
title: Issue 1373 creation record (resident session opacity test oracle)
description: Created test-oracle issue, scope and stacked dependency, separate from any authentication claim
ms.date: 2026-11-10
ms.topic: reference
---

## Created Issue

* Issue: #1373, https://github.com/jmservera/ama/issues/1373
* Created: 2026-11-10T09:19:01Z (state OPEN at the admission snapshot).
* Title: Fix random-signature false failure in resident session opacity test
* Template: generic; .github/ISSUE_TEMPLATE absent.
* Labels/assignees/type: none specified.
* Severity: Medium test-oracle defect. No product authentication defect and no Closed cases CSV regression is demonstrated.

## Initial Scope and Dependency

* Failing evidence: source CI run 42787438444, Core job 129732281167,
  `SessionTests.test_round_trip_and_handle_is_opaque`, `src/core/tests/test_resident_showcase.py:231`;
  2864 tests, 1 failure, 347 skips. The raw token is not copied into this record.
* Scope: `src/core/tests/test_resident_showcase.py` (the opacity method and a directly coupled
  deterministic regression) plus this RPI evidence. No production codec, authentication, RNG,
  encoding or permission change.
* Dependency: Refs #80, #189 and #462 and PR #1371. Stacked child of
  `feat/demo-closed-page-csv-80-1110` at `9e71736bc09984b07d77c122747483548b580c7d`; it targets that
  parent, not main. The child carries no closing keyword.
* Allowance: one initial bounded newly observed test-oracle repair is admitted. No legacy
  #189/#462/#80 corrective allowance is transferred or reset, and there is no automatic
  post-review extension. Historical balances remain UNKNOWN.
* Open criteria: deterministic red-before and green-after, preserved session behavior, affected
  and Core static checks, independent exact-head review and actual hosted checks. The issue body
  is the authoritative requirement text.
