---
title: Public Welcome and Entra Account Phase Details
description: Implementation boundaries and exact validation expectations
ms.date: 2026-10-12
---

## P01

Serve welcome.html at root, existing index at /app and legacy /index.html.
Inject only the known provider name into the workbench HTML. /sign-in uses
a fixed provider URL and /app return, or /app in local development. Exempt
only root, /welcome.html, /style.css, /zava-logo.png and /sign-in plus probes
in Container Apps globalValidation.excludedPaths as well as application
routing; data remains protected. No public script fetches user data.

Use native account details/summary with the current user picture, initials,
display name and explicit photo status. Ensure keyboard/outside closure.
Own account metadata is derived from the already-validated principal, not
trusted merely because a header exists. Contractor projection must still
withhold other staff/resident fields.

The photo client uses only fixed HTTPS Graph /me/photo/$value. The platform
token is never logged or returned. Block redirects, allow JPEG/PNG with valid
magic and maximum 2 MiB, timeout 10 seconds. Return explicit statuses for
missing token/photo, consent/expiry and network/type errors. Refresh through
the supported same-origin endpoint at most once; do not fall back silently.

Both logout actions retain CSRF/role enforcement. Their return URLs are fixed
root or /sign-in. Provider prompt=select_account is configured for fresh login.
Production errors never display the development shared-password form.

## P02

Create a separate private token-only storage account hosting auth-tokens with shared keys disabled,
HTTPS and existing public-development/private-production controls. Tag its
real authentication data accurately. Give a separate maintenance identity
Storage Blob Delegator at account scope and a new container-scoped Blob Data
Contributor role assignment on auth-tokens. Existing evidence-account
Contributor identities must not gain token access. Grant secret-writing only on entra-token-store-sas, not the API
identity or whole vault. Give the job registry pull access and existing
Container Apps network access.

The image renewal command uses ManagedIdentityCredential, bounded user
delegation and rwd HTTPS SAS, then authenticated Key Vault PUT. SAS expiry
five days, key bound below seven days, daily cron. Only expiry/success metadata
may be printed. Retry/error output must not contain a token or SAS.
Do not update the secret if delegation fails. Do not reset the secret with
a placeholder on redeployment.

Separate infrastructure provisioning from tokenStoreReady activation.
Bootstrap the first secret with the real job before turning on auth token
store and delegated User.Read/offline_access scopes. Use versionless Key Vault
reference for rotation; check actual platform refresh behavior before relying
on it. Confirm expiry and scheduled execution metadata without retrieving
secret values. Preserve existing auth secret, SQL, model parameters and data.

## P03

Run smallest relevant tests first, then existing MVP suite and Bicep build.
Use real ACR build/current data and guarded deploy parameters. Verify actual
anonymous landing/assets and protected entry/API on Azure; verify credential
job execution rather than a mocked success. Browser visuals may use a local
synthetic account for menu behavior, never claimed as live Entra acceptance.
Publish code/docs/evidence pointers to existing #65 with privacy-safe Git
identity. Update index and append-only log for durable instructions.

## Critique Boundary

One final-candidate critique; read plan/details/research and focused source as
needed, write only its critique. No source edits. All tests owned by parent,
no removals, at most 40 additions. Challenge SAS/bootstrap/redeploy and auth
boundary/claims assumptions, but do not propose broad Graph grants or another
login system when the documented platform flow supports the requirements.
