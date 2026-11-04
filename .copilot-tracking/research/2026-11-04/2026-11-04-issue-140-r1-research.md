---
title: Issue 140 status research (2026-11-04, r1)
ms.date: 2026-11-04
---

## Scope

Check what merged PRs delivered for #140 (Azure IoT Hub Bicep module) and what remains.

## Evidence

* Merged PRs: #273 (module), #498 (private keyless transport), #557 (approved B1 reconciliation, publisher gating), #910 (offline fleet identity evidence, #110), #614 (closure audit).
* `infra/modules/iothub.bicep` exists with the hub, dedicated Event Hubs consumer, diagnostics to Log Analytics (AllMetrics only), private endpoints and a keyless API receiver role.
* `infra/README.md` (IoT Hub section) records B1, one unit, uksouth, one-day retention, USD10/month estimate, and the device provisioning approach: individual device identities, DPS deferred.
* The same section names Juan Manuel Servera as the exercise issue/rotate/revoke owner and states that no operational appointment exists.

## Findings

* Criteria 1 to 4 and 6 are delivered as engineering evidence (ticked in the issue).
* Criterion 5 (provisioning approach and named owner of credential issue and rotation) is partly recorded: approach and exercise owner are in README. An operational credential-owner appointment, rotation evidence and actual issuance (#185) are not done. These are human appointment and later implementation steps, not module work.
* ADR 0003 is still Proposed and BRD OD-43 is still open.

## Planning readiness

Ready for a docs-only record. No executable slice is unmet.
