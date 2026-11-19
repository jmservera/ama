---
title: Issue 118 hardened deployment live evidence
description: Read-only Azure probes and repository record for the unticked criterion "Azure Policy and Defender plans decided"
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, read-only Azure CLI with the existing login against subscription scope and resource group `ama` (uksouth). No Azure, source or infrastructure change was made. Subscription and tenant identifiers are omitted. Refs #118.

## Criterion result

| Criterion | Result | Evidence |
| --- | --- | --- |
| Azure Policy and Defender plans decided | Decision recorded (audit-only policy, Defender deferred); not independently shown to be adopted. The criterion stays unticked pending owner acceptance | See below |

The other four criteria are already ticked and were not re-audited.

## Recorded decision (repository)

[`infra/defender-decision.json`](../../../infra/defender-decision.json), recorded 2026-11-01 under owner Juan Manuel Servera:

* Policy: audit only (`enforcementMode=DoNotEnforce`) through [`infra/governance.bicep`](../../../infra/governance.bicep); no charge; a Deny stance stays an open owner decision.
* Defender: deferred. The plans StorageAccounts, SqlServers, KeyVaults and Containers are defined, `enableDefenderPlans=false`, cost approval pending and no price invented.
* Exceptions: [`infra/policy-exceptions.json`](../../../infra/policy-exceptions.json) EX-001 expires 2026-12-31.
* Summary table and open items: [infra README](../../../infra/README.md) governance section.

For the demo, billing reconciliation and cost approval are out of scope by owner decision 2026-11-18, so the deferral is a complete decision for the demo: audit-only policy, Defender plans not activated.

## Live probes (2026-11-18)

| Probe | Result (observed; raw output not retained) |
| --- | --- |
| `az policy assignment list` (subscription) | Empty list: the repository's `governance.bicep` assignments are not deployed at subscription scope |
| `az policy assignment list --disable-scope-strict-match` | Count 0 |
| `az policy state summarize -g ama` | 2 non-compliant policies, 6 non-compliant resources |
| Non-compliant states in `ama` | Assignments `MCAPSGovAuditPolicies` (SQL threat detection and auditing audit) and `Azure_Security_Baseline` (initiative controls on SQL, Event Hubs, virtual networks, Key Vault, Container Registry, Cognitive Services); both are platform-managed, not from this repository |
| `az group show -n ama` | Location uksouth; tags empty, so the required-tag policy would not pass if assigned |
| `az security pricing list` / `show` for the four plans | List empty; `show` returns AuthorizationFailed (Microsoft.Security read not granted to this identity). Plan tier cannot be read |

## Not proven

* That Defender plans are in the Free tier live: the identity lacks Microsoft.Security read, and granting it is a change outside this task.
* That the repository policy assignments are active: probes show none at subscription scope. This is consistent with the recorded "deployed separately by the subscription owner" boundary, and activation is not required for a documented audit-only decision.
* Production approval of Defender cost, a Deny stance and tag remediation remain open owner decisions, listed in the infra README.

## Adverse observations

The live compliance state shows platform audit findings on the demo resources. They are reported, not remediated, per the no-production-change rule.

## Evidence limits

* The six live probes were read-only Azure CLI calls. Their raw output was not retained, and subscription and tenant identifiers were not copied into this repository. The results above are transcribed observations, labelled "Observed; raw output not retained".
* The probe counts (2 non-compliant policies, 6 non-compliant resources, empty assignment list) can be regenerated only by repeating the calls against the live subscription.
* The recorded decision itself is a repository file (`infra/defender-decision.json`) and can be checked directly.
