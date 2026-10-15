---
title: Issue 173 Lifecycle Coverage Review
description: rpi-review of the existing diff against issue acceptance criteria
ms.date: 2026-10-15
---

## Review Execution

One review, run after the fact on commit 23cfd85 (retrospective).

## Findings

* AC1 each state seeded or deferred: met. Gap F1 (Low): README said grants
  seed a pending Opportunity proposal while DEFERRED lists Opportunity; the
  seeded state is Not recorded. Fixed by clarifying the README row.
* AC2 no invented outcomes: met; test asserts disjoint sets and unpayable
  invoices.
* F2 (Info): commitment Approved and invoice states are deferred in code but
  only partly itemised in the README table; acceptable.

## Outcome

Conformant after F1 fix. Open: owner decision on demo-only outcome fixtures
(sibling issues 90, 94, 95, 85, 86).
