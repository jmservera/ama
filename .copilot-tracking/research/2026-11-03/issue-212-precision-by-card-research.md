---
title: Issue 212 research, per-card false-positive breakdown
description: Remaining criterion 7 gap after merged PRs and the smallest code slice
ms.date: 2026-11-03
---

Task: 212 / issue-212-precision-by-card. Research disposition: reused (2026-11-01 and 2026-11-03
research plus merged PRs). Planning Readiness: Ready.

## Delivered already (merged PRs)

* #328, #331, #389 engine, source monitoring and consultation controls; #630 and #835 per-home
  grouping (`address_key`, `stock_register`); #679 HTTP proof of grouped, ranked alerts and the
  `precision` block. Criteria 1 to 6, 8 and 9 are ticked.

## Remaining gap

* Criterion 7: no real staff precision trial; `precision` is only an aggregate, so a trial cannot
  show which card raises false positives.
* Not deliverable by code: the human staff trial, a verified dwelling identifier, hosted timer,
  workbench alert component.

## Decision

Add a deterministic per-card `by_card` breakdown to `precision`. No security, infrastructure, SQL
or deployment surface: focused tier. No model, no resident message, no approval change.
