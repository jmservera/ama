---
title: Issue 96 r16 export review-history research
description: Prospective research after release by the pinned ninth finance checkpoint and two owner answers
ms.date: 2026-11-05
---

## Identities

* Branch `feat/form-export-review-history-96`, head `f4e8c11befa46a06bf1feb8eca0cc7499b279c14`, clean including ignored files. Finance parent `0472fd5d5625bb610b5ac65ad177026953802830` (tree `268ead3a`), main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. No base movement. Eventual PR targets `feat/finance-integration-93`, `Refs #96`.
* The r15 records stay PAUSED and unchanged; this r16 continuation supersedes the pause only through the release below.

## Gate consumption (read from the pinned Git object)

* Governance commit `1faadaa3e75d3b4003319fde0491473fa1a87dee`, tree `678085a22e982a438fd275701f1e686bb212f258` (verified locally). Its `cutover-evidence-pack.md` line 3594 holds the ninth stabilization checkpoint for the finance parent held-export manifest contract. It recommends the required history key, rejects an optional key, and states legacy copies become Invalid with the regenerate-Held action and no backfill. It is a scoped recommendation, not an approval and not main acceptance. No governance code is taken.
* Owner answers (as supplied by the coordinator): old copies may become Invalid/regenerate; full history initially for synthetic test data only. Neither is DPO, Finance or Legal sign-off. Real data, reviewed packs and approvals stay unauthorized.

## Source re-confirmation

* `form_export.BODY_KEYS` has 11 keys without history; `_report` returns detached `history`; the freshness path turns a missing key into `Invalid`. Plan: add `history` to `BODY_KEYS` and to the body.
* Evidence visibility preflight already covers history sources, so no broader reads.
* No consumer outside core tests and README.

## Readiness

Ready to implement the bounded increment. Tier FULL, pending; light checks only now.
