---
title: Zava Azure Reset Implementation Evidence
description: Destructive-scope preparation, deployment evidence and blockers
ms.date: 2026-10-12
---

## Intake and P01-T01 preparation

Owner-authorised full reset/redeploy/testing/review scope recorded in the plan.
Topic branch is clean and PR #65 is open. Fast-forwarded the recorded rubric
commit without changing its score. Original checkout local MCP/.env are untouched.

Inventory captured privately outside the repository. No resource locks exist.
Operator retains Owner access at resource-group scope and is the SQL Entra
administrator. The old four workload identities are Bicep-recreatable; Blob is
active and no SharePoint site is configured.

Both Azure CLI and M365 CLI still deny reading the API app registration.
Interactive callback/role updates remain blocked on tenant authority. Proceed
with the explicitly requested resource reset while preserving tenant resources
and authentication controls; never claim that this denial has been resolved.

Found a deployment gap to fix: the MVP implements real AI calls, but Bicep does
not configure its AI endpoint or grant the API identity model access. Placeholder
worker workloads do not provide application AI. This is within requested
redeployment fixes, not implementation of the unmerged Decision 1 experiment.

## P01-T01 dependency capture and reset start

Captured the existing auth credential and one staff object-id mapping in
mode-0600 temporary files, without output or tracked sensitive content.
The resource-only reset started from the saved inventory with scope guards,
dependency waves, explicit failures and no group/tenant deletion.

## P01-T03 cold-start and real-model fixes

Added an explicit dependency-only `deployApplications=false` bootstrap so the
real image, Key Vault secret and SQL seed exist before apps start. Incremental
bootstrap does not delete any existing apps. The full deployment defaults true.

Added opt-in `enableApiAi`: configure the MVP's existing model caller and grant
only its identity the existing model invocation roles. Default separate-runner
topology is unchanged. Managed-identity token requests now select the configured
user-assigned client id, with system identity behavior retained and regressions.
The explicit `entraRoleMap` override supports issued legacy role values until
an authorised owner updates the tenant. It does not conceal the callback blocker.

Validation: Bicep compiles; targeted auth/AI tests pass (43); complete MVP runs
272 tests with 26 existing skips using the pinned hash-locked dependencies.

## P01-T02 deletion dependency correction

Azure scheduled the old Container Apps environment for deletion; no apps or
jobs remain. Independent SQL/registry/vault/topic deletions proceeded while
the environment tears down. Foundry account deletion initially failed because
its project must be deleted first. Deleted the inventoried child project,
retried the account using the service CLI and confirmed success. This is a
reset ordering correction, not an authority or scope change.

Resource-group budgets are not included in the generic ARM resource listing.
A direct `Microsoft.Consumption/budgets` query found `budget-warm-test`; include
that existing, group-scoped resource in reset and emptiness verification. Do
not treat an empty generic list as complete reset evidence.

P01-T02: both indexes are now empty, including all four old workload identities.
The group and the external operator survive. The first reset report retained
one failed App Insights deletion; retrying after its private-link scope was
removed succeeded. The foundation wait correctly stopped on the initial
nonempty report. Reconcile that resolved failure and restart the guarded
foundation runner rather than bypassing its empty-group gate.

P01-T03: `zava-forward-foundation` and `zava-forward-applications` succeeded.
Built `crforwardtestrzsrg.azurecr.io/zava-forward-mvp:reset-20261012-9ab3c19`,
transferred the auth secret privately, recreated API/import contained users and
restored 980 cases with 443 open. The operator audit write survived SQL reopening.
Removed the credential, seed and staff-mapping temporary files after use.
Protected ingress is
`ca-forward-test-api.salmonplant-3b962c5f.uksouth.azurecontainerapps.io`.
The first health probe received 503 during cold image/auth-sidecar rollout;
the application subsequently logged its normal startup with no restarts.

## P02-T01 live acceptance boundary

Public health returned 200; the unauthenticated API returned 401; a browser
user-agent received a 302. Authentication stayed enabled. Direct checks in the
deployed API container used its own identity, confirmed 980 cases / 443 open,
appended SQL audit records and returned actual `source=ai`, validated results
from `standard` and `capable`. Restarted revision `ca-forward-test-api--5oigcb5`;
the subsequent identity-backed query found both model audit records and the SQL
write marker intact. The image's HTML contains both new names and no old brand.

The Container Apps exec CLI does not accept the quoted multiline `python -c`
diagnostic used initially. A transparent interactive Python program corrected
that test invocation; the harness rejects any traceback or missing result.
This was a diagnostic-command correction, not an application/auth workaround.

Live signed-in lists, map and login remain unverified: the authorised tenant
owner must add the new callback, preserve assignments/redirects and transition
the existing role values. Local lists/map/deck checks remain earlier evidence,
not a substitute for this unmet browser gate. Placeholder workers and planned
Decision 1 scoring are not claimed implemented.

## P02-T02 review readiness

The final active-name scan has no text/path replacement candidates; five
unchanged PPTX files are reported because the script refreshes their logo
branding when supplied a logo. No deck was reapplied or republished in this
reset. Reuse the existing five-deck/61-source render validation.
All 67 live generic resources have no old company/programme naming; the
separate budget is `budget-forward-test`. Final Markdown checks found no new
missing targets and no broken fragments in the changed guide/index/log.
Eight actual existing target defects remain after excluding code examples.
Migration regressions (21) and Bicep compilation passed.

Implementation is review-ready for the reset/rebuild and explicit acceptance
boundary. Tenant callback/role completion and authenticated browser acceptance
are unresolved, not conformant. Publication through the existing open #65
remains the final delivery action; the remote branch has no intervening commits.

P02-T02: the one review completed with outcome Residual work (RV-001, tenant
transition/authenticated browser acceptance). Published application/bootstrap
fix commit `9ab3c19` and reviewed rebuild evidence commit `fe68b88` to the
existing open #65. No merge, rebase or force-push. The source/image identity is
unchanged; final delivery tracking records publication and awaits PR checks.
