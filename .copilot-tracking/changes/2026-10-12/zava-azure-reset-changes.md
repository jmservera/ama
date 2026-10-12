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
