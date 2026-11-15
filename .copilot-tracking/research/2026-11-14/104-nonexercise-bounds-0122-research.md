---
title: Issue 104 criterion 5 non-exercise bounds research
ms.date: 2026-11-14
---

## Objective

No AI capability is enabled beyond the exercise without owner-approved call, token and budget limits and an owned alert.

## Findings

* Disposition: executed. Planning Readiness: Ready.
* `ai_consumption.Consumption.authorize` accepted an authority on a billable (non-synthetic) price with zero call/token/money limits, a whitespace-only owner, and no alert identifier or alert owner. Zero limits fail closed at `reserve`, but unowned alerts did not: the alert owner fell back to the authority owner or `unassigned-owner-OD-51`.
* Exercise scope is expressed by price class: `price(synthetic=True)` and `Ai.is_live` (local nonbillable endpoint or `synthetic_price_capabilities`). A `live` reservation on a synthetic price is already held as `price-unknown`. Billable price therefore marks "beyond the exercise".
* Dispatch order in `ai.py` `_request`: `consumption.reserve` precedes `dispatch_check` and `urlopen`, so a reserve hold means zero provider calls.
* `rai_release.py` gates release records (named owner, approver, expiry) but holds no call/token/budget limits; no change needed.
* `infra/` already carries the `AI_LIMIT_BREACH` rule `alert-${prefix}-ai-limits` (disabled candidate); owners remain OD-51 pending. No infra change: activation and owner naming are human decisions.
* The ledger `_read` schema check required exact authority fields, so an optional extension needs an allow-list.

## Gap

Billable authorities could be recorded and used without an owned alert binding or with whitespace owners; legacy billable authorities lack any binding.

## Pointers

* `src/core/src/zava_forward/core/ai_consumption.py`, `ai.py`, `rai_release.py`, `infra/modules/operationalMonitoring.bicep`, `infra/monitoring-runbooks.md`
