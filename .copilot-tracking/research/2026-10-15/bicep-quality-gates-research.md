# Research: Bicep quality gates (issue #139, parent #136)

Disposition: executed. Planning Readiness: Ready.

## Evidence

* CI (`.github/workflows/mvp-validation.yml`) ran `az bicep build` and `az bicep lint` only; no `bicepconfig.json`, so lint warnings did not fail the build.
* `infra/tests` covered only Python initializers.
* Compiled `main.bicep` (az bicep available locally): all public access properties use `[if(parameters('allowPublicNetworkAccess'), 'Enabled', 'Disabled')]`; `publicAccess = isDev || allowPublicNetworkAccess`; SQL `azureADOnlyAuthentication: true`; storage shared key off; registry admin off; Foundry and App Insights local auth disabled; Key Vault purge protection follows `purgeProtection`; two immutability policies; private endpoints for sqlServer, blob, queue, vault, registry, account, azuremonitor.
* Gap: README said `allowPublicNetworkAccess=true` or `keyVaultPurgeProtection=false` could relax one control in the production profile, so production could be deployed with public access.
* Bicep has no assert; a module parameter with `@minLength(1)` fed by `cond ? 'ok' : ''` fails validation with the parameter name. Literal-typed `@allowed` fails type checking.

## Decisions and constraints

* Owner rules: Azure only, region uksouth, retention unlocked; no synthetic data change needed (infra only).
* Rejecting production plus public access changes documented behaviour; development profile remains the sanctioned route.

## Open items

* Live confirmation (`az deployment group validate`/`what-if`) of the guard message needs an Azure session.

## Review fix pass

* Finding 1: `guard` had no dependents, so ARM could deploy other modules in parallel. Finding 2: tests skip silently without `az`.
* Compiled template confirmed: only module output references created implicit dependencies; none on `parameter-guard`.
