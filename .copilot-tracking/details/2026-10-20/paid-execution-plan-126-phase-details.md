---
title: Paid execution plan 126 phase details
description: Frozen content contract for the costed plan options
ms.date: 2026-10-20
---

## Cost Model (frozen)

* Currency USD; Azure CLI Cost Management ActualCost for RG `ama` only; retrieved 2026-10-20.
* Accrued 1-20 Oct 189.94, of which complete days 1-19 172.47 and partial 20 Oct 17.47.
* Run rate 30.245/day (18-19 Oct mean). S0 = 172.47 + 12 x 30.245 = 535.41; S1 (Front Door
  removed from 21 Oct, 20 Oct full burn) = 418.32; S2 (S1 plus SQL idle after 25 Oct at
  conservative 50% saving over 6.3 days) = 384.74.
* Tranche ceilings: T1 8, T2 10, T3 15, T4 0; billing-latency/unknown reserve 30.
  Projected month end S1 + 63 = 481.32; S2 + 63 = 447.74; S0 + 63 = 598.41 (blocked).
* Thresholds on projected month end (accrued complete + days left x run rate + unspent
  ceilings): review 400, pause new tranches 450, stop and clean up 475, never above 500.
* Inference worst case: per call 12,000 input characters treated as tokens plus 600 output
  tokens: mini 0.00576, gpt-4.1 0.0288; 300 mini + 100 gpt-4.1 = 4.61.

## Tranches (frozen)

* T0 prerequisite owner disposition: choose S1 or S2; separately name Front Door retirement
  (profile, endpoint, WAF policy; recreate via `infra/public-edge-existing.bicep`) and SQL
  idle (suspend the 5-minute orchestrator schedule after the window). Not executed here.
* T1 first deployment tranche: usable sign-in on the existing demo API; no new resources.
* T2 actual-model evaluation: two Foundry deployments, caps 300/100 calls, practice run only
  on existing non-held-out fixtures until the owner approves held-out manifest.
* T3 Azure validation: #358 vault preservation, #117 retention/scan simulation, #122
  restore drill; each uses existing scripts and temporary synthetic resources.
* T4 sizing: analysis only from E3/E5/E8; no allocation.

## Unresolved Blockers (frozen)

Private publisher capacity (known failures not retried), invalid client sentinel, tenant
registration/consent, private roster, in-VNet SQL executor, subscription-level charges,
held-out manifest approval, human review gates, legal/privacy terms, quota R9 Unknown.
