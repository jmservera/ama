---
title: Issue 212 research, register-linked home grouping
description: Research for the remaining home identifier gap in criterion 7 of the deterministic rule engine
ms.date: 2026-11-03
---

Task: 212 / issue-212-stock-register-home. Research disposition: executed (reuses the 2026-11-01
home-grouping research). Planning Readiness: Ready.

## Delivered already (merged PRs)

* #328 engine and scoped step alerts; #331 offline source monitoring; #389 consultation controls.
* #630 grouped alerts per home across cases with a derived `address_key`; #679 HTTP proof of
  grouped, ranked alerts and false-positive tracking.
* Criteria 1 to 6, 8 and 9 are ticked on the issue. Criterion 7 is the only unticked one.

## Remaining gap in criterion 7

* `_home_key` in `src/core/src/zava_forward/core/rule_engine.py` knows `home_id`, then a derived
  `address_key`, then `case_only`.
* No case source writes `home_id`. Cases do carry `stock_link` (`status`, `stock_home_id`,
  `shared_anchor`), produced by `resolve_cases` in `synthetic/stock_fabric.py`. A linked stock
  reference is a stronger grouping key than address text, and shared anchors are exactly the
  several-cases-one-home situation.
* The README states a unique register reference is not verified dwelling identity, and that
  shared anchors never transfer consent, approvals or household identity. Alert grouping is staff
  triage only and transfers nothing.

## Not deliverable by code

* A real staff precision and false-positive trial needs human staff, so it stays unmet.
* Registered dwelling identifier from a real system, hosted timer and workbench alert component
  are outside this slice.

## Decision

Smallest coherent slice: add `stock_register` scope between `recorded_home` and `address_key`.
No security, infrastructure, SQL or deployment surface, so the focused validation tier applies.
