---
title: Issue 222 approval binding research
ms.date: 2026-11-03
---

## Disposition

Research executed (reused prior evidence plus code read). Planning Readiness: Ready.

## Already delivered (merged)

* #636: `core.cohort_eval` record (per-cohort counts, errors, Wilson interval, review burden, insufficient samples, unapproved thresholds, human disposition).
* #697: ranking-policy cohort run over 48 paired cases with seeded defects.
* #421: unapproved draft manifest and review pack.
* #504: release records bound to dependent policies (generic, not cohort thresholds).

## Gap found

`_thresholds_approved` accepted any two named owners. Approval was not bound to the manifest content (an edited manifest kept its approval), and OQ-018 lawful analysis fields had no named owner.

## Slice

Require a lawful-fields owner and a `manifest_digest` approval binding. Unapproved or stale approval stays fail closed and cannot be cleared by a human disposition.

## Unmet and out of scope

Criterion 1 (owner-approved manifest) and 6 (OQ-018 owner and DPO approval) need humans. AI-task cohort evaluation, #108 golden-set reporting and UI are later slices.
