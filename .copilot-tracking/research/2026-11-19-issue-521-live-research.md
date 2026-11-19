---
title: Research for issue 521 live run (2026-11-19)
description: First unmet criterion of #521 and the evidence plan
---

## Scope

Refs #521. Synthetic demo, desktop only. Criteria 1 to 3 are ticked. Criterion 4 (live Azure change applied after owner confirmation, verified and recorded) is the first unmet one.
The [2026-11-18 note](../../docs/reference/research/resident-demo-authority-live-521-2026-11-18.md) left raw `az` output and test output unretained, the live SQL window unproven (private-only server) and the image-to-source link unproven.

## Selected criterion

Criterion 4. Planning Readiness: Ready. Research disposition: executed.

## Plan of evidence

Re-run read-only `az containerapp show` and a Playwright desktop sign-in, retaining raw output without secrets; re-run source tests. No src change is justified: the source already holds the 2028 boundary and the gap is live SQL access, which needs network access the demo does not have. Tier: FOCUSED (no src change).
