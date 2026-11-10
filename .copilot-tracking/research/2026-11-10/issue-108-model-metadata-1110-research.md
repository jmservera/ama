---
title: Issue 108 regional model metadata observation research
description: Prospective research for one bounded read-only Azure metadata observation of the demo model endpoint, deployment and regional quota limit
ms.date: 2026-11-10
---

## Task

Task `issue-108-model-metadata-1110`, under existing #108 (unticked criterion: model names, versions and quotas confirmed in the chosen region). Base `main` `4d8443d442fa8f1c47fa0749e5b8ba7c2bdd23ff`. Research disposition: executed.

## Evidence found

| Source | Finding |
| --- | --- |
| [AI Tokenomics, configured demo model section](../../../docs/reference/resources/ai-tokenomics.md#configured-demo-model-limits-and-evidence-gaps-2026-11-07-refs-108) | Existing synthesis for #108: 2026-11-07 readback of deployment `standard` on `aif-cutover-test-rzsrg` (`GlobalStandard`, capacity 10, `gpt-4.1-nano` `2025-04-14`, `NoAutoUpgrade`, `uksouth`). It lists "Live app environment" as not re-read and has no subscription quota limit (empty usage lists, only an availability figure). This is the fitting page to extend |
| [infra README, demo API and model settings](../../../infra/README.md) | Approved demo app is `ca-cutover-test-demo-api` in resource group `ama`; intended `AI_ENDPOINT` and `AI_DEPLOYMENT` values are documented but the live app had `AI_*` settings absent at 2026-10-28, so the live env value is unknown today |
| [Knowledge base index](../../../docs/reference/README.md) | No other page holds #108 model-region evidence; no new page is justified |

## Gaps this observation can close or record

* Whether the live demo app is configured with `AI_ENDPOINT` and `AI_DEPLOYMENT` (value, or absent, or secret reference).
* Whether the configured endpoint resolves to an account in `ama`, and that account's location, plus the configured deployment's model, version, SKU, capacity and provisioning state at the query time.
* The regional quota limit and provider-reported unit for that one model and SKU, if the usage API returns it. Unknown is not zero.

## Planned read-only queries (budget 8, one bounded transient retry inside it)

1. Container app env projected to `AI_ENDPOINT` and `AI_DEPLOYMENT` only (`name`, `value`, `secretRef`).
2. Account show for the account named by the endpoint host in `ama`: kind, location, SKU, endpoint (confirms identity).
3. Deployment show for the configured deployment name: SKU, capacity, model name and version, upgrade option, provisioning state.
4. Regional usage list for the account location, filtered to the single model and SKU entry and projected to name, limit and unit only (no current value).

Query 3 and 4 run only if the earlier identity checks are unambiguous. Stop rules: no secret resolution, no other group, no enumeration, no mutation, no inference, no tokens or keys, no `az login`.

## Semantics that bound any claim

* Configured version is not serving attestation; deployment name is an alias, not an immutable model; `GlobalStandard` resource location is not processing location.
* A quota limit is not reserved capacity, remaining budget or headroom. No TPM conversion is asserted.
* Denied or missing metadata is not proof a model is absent.

## Planning Readiness

Ready. Alternatives rejected: a new page (an existing synthesis fits); a subscription-wide quota listing (outside scope and exposes other workloads); a real call (no authority).
