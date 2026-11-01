---
title: Issue 212 home grouping review
description: Single post-implementation review
ms.date: 2026-11-01
---

Review executed once. Outcome: Residual work (non-blocking). Boundary: the three changed files.

## Findings

* Passed: scope tight, no new code in mvp/ or prototype/, tests outside the package, no secrets,
  no model or resident-message path added, checkpoint keys unaffected.
* R1 (accepted): address matching may merge distinct dwellings with identical address text; it
  is labelled `address_key` and documented as not a registered identity.
* R2 (open, routed to later user-selected work): criterion 7 needs a real staff
  precision and false-positive trial and a registered home identifier. Criterion stays unticked, so
  the PR uses `Refs #212`.
* R3 (open): hosted CI is the gate evidence; no heavy local gate was run by instruction.

## Follow-ups

1. Source a registered home identifier into case facts (value: removes derived key).
2. Staff precision trial for false-positive tracking.
3. Workbench alert component and hosted timer.
