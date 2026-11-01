# Research: #142 Key Vault secret lifecycle (2026-11-01)

Disposition: executed (focused, source-only). Planning Readiness: Ready.

## Evidence
* infra/modules/keyvault.bicep: diagnostics to Log Analytics (AC4 ticked), expiry and denied-access alerts.
* infra/secret-inventory.json: two secrets only (entra-client-secret, entra-token-store-sas); owners are placeholders.
* infra/resident-demo.bicep and infra/scripts/credential_arm.py: two further vault secrets (resident-demo-password-verifier, resident-demo-session-key) with expiry capped by src/core resident-demo.json maximum_expiry_utc; absent from inventory.
* infra/scripts/secret_lifecycle.py: check, review (pending record), rotation-plan. Rotation is only a string-order assertion; review has no due/complete check.
* infra/README.md "Key Vault secret lifecycle"; closure audit 2026-10-31 lists C1-C3 unmet (placeholder owners, no live rotation, no executed review).

## Gaps closable offline
* G1 inventory incomplete (resident secrets) and owner placeholders.
* G2 no executable no-downtime model; delete-first outage not demonstrated.
* G3 no machine check that a review is complete, signed and not overdue.

## Not closable here (no live Azure, human approval)
* Live rotation exercise, executed signed review, alert evaluation in Azure Monitor, named-owner confirmation.

## Decision
Deliver G1-G3 plus docs; use "Refs #142" naming unmet criteria.
