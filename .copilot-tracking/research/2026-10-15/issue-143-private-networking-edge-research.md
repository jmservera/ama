---
title: Issue 143 private networking and public edge research
date: 2026-10-15
---

## Scope

Issue #143 (parent #136): verify private-endpoint and DNS coverage, define Front Door Premium with WAF and Private Link origin (or record why not), manage custom domain/TLS/Entra callbacks, block development public access in production, and source private-network evidence from a production-profile deployment.

## Evidence

* `infra/modules/*.bicep`: sql, storage (blob, queue), keyvault, registry, foundry, iothub, monitoring and authTokenStore each switch `publicNetworkAccess` and call `privateEndpoint.bicep`; Container Apps environment is internal when `allowPublicNetworkAccess` is false. DNS zones in `network.bicep` include IoT Hub and Service Bus.
* `infra/modules/network.bicep` has an NSG rule for `AzureFrontDoor.Backend`; no Front Door resource exists.
* `infra/modules/guard.bicep` already rejects production profile plus `allowPublicNetworkAccess=true`.
* ADR 0001 section Edge and ADR 0002 decision 6 name Front Door Premium, WAF and Private Link as the intended edge; owner decision: Azure only, region uksouth.
* `create-api-app-registration.sh -u` registers `/.auth/login/aad/callback` URLs; EasyAuth has no forward-proxy setting yet.

## Findings and decision

* Coverage criterion: met by static check; add a test so new stores cannot omit endpoints.
* Edge: implement as an optional module (`enablePublicEdge`, default false) so private-only pilot stays default; guard to production profile only.
* Callbacks: output `entraRedirectUri`; set EasyAuth forward-proxy `Standard` behind the edge.

## Unverifiable here (open items)

* Production-profile deployment evidence (no deployment run).
* Front Door Private Link to Container Apps environments in uksouth and pricing; custom domain and DNS ownership; pilot edge go/no-go.

Planning Readiness: Ready. Research disposition: executed.

## Review-fix pass (2026-10-15)

Findings: (1) coverage test only used string assertions; (2) Private Link to `managedEnvironments` of an internal VNet-injected environment is unverified; (3) the route attaches the managed-certificate domain before DNS validation. Evidence: `infra/modules/network.bicep` (`dnsZones`, `zoneIds` output), module `privateEndpoint.bicep` calls, `infra/modules/edge.bicep`. Planning readiness: Ready.
