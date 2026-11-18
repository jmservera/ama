---
title: Issue 164 / PR 1641 gate failure correction critique
date: 2026-11-17
---

Verdict: compatible, proceed record-only.

* Finding 1: editing `app.js` reset logic would be a guess; the handler is unchanged from main and the check passes in about 70 of 72 candidate runs. Disposition: rejected, no change.
* Finding 2: editing the browser check for a race that was never reproduced would alter evidence without proof. Disposition: rejected; reported for the coordinator.
* Finding 3: raising the Core timeout or sharding changes gate semantics. Disposition: not applied; reported with measurements.
