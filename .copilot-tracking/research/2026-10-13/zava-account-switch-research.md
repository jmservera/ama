---
title: Account Switch and Failed Workflow Research
description: Focused evidence for deliberate Entra account selection and useful diagnostics
ms.date: 2026-10-13
---

## Research Brief and Opening State

Task zava-account-switch-2026-10-13, automatic child of tenant staff.
Owner confirms access and reports Use another account signs out but does not
switch. Inspect Azure logs, enable useful diagnostics if missing, and inspect
workflow 38319901482/job 115168811216 while respecting the owner's retry.
Focused convergence posture from named runtime symptom and workflow.
Scope: logout/login/chooser, safe logs and relevant CI failure. Non-goals:
directory identities/roles, global Microsoft logout or invented user sessions.

## Extensions and Participation

Repository branch/privacy/knowledge-base rules selected. RPI phase/state
contracts selected. Microsoft documentation/Context7 and Azure operations
selected for platform evidence; no specialist delegation needed for this
continuous short trace. Secrets/query strings and directory details remain
outside artifacts. Azure best-practice tool consulted. No new consent required.

## Questions and Prior Knowledge Gate

* Does switching reach an explicit account chooser or ordinary SSO login?
* Can existing Azure logs explain the observed flow without exposing tokens?
* Is the failed action a transient infrastructure fault or repository defect?
* What minimum change preserves normal sign-in/sign-out and fail-closed access?

Initial read-only evidence: existing switch response returns to /sign-in;
current sign-in redirects to ordinary Easy Auth login with no prompt parameter.
Console access works but selected replica contains only startup output.
Complete Wider, Deeper and Contrarian waves inline before readiness.

## Cycle 1: Wider

C1: mvp/zavaforward_mvp/auth.py:159-161 returns platform logout followed by
ordinary /sign-in for switching. C2: mvp/zavaforward_mvp/server.py:154-156
always uses ordinary Easy Auth login, without an account-choice prompt.
C3: mvp/zavaforward_mvp/server.py:118-119 disables access logs; successful
auth transitions have no app-level diagnostics.
Azure diagnostic routing already enables all environment log categories into
the existing workspace; no logging resource or permission is missing.
Actual resource-specific table is ContainerAppConsoleLogs, not legacy _CL.

## Cycle 1: Deeper

W1: https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
Retrieved 2026-10-13. prompt=select_account interrupts SSO and presents remembered
accounts plus another-account choice. Ordinary login can reuse the sole account.
W2: https://learn.microsoft.com/en-us/azure/app-service/configure-authentication-customize-sign-in-out
Retrieved via Microsoft Learn 2026-10-13. Easy Auth logout performs provider
sign-out; it is not itself an account-selection operation.
W3: Live HTTPS platform trace 2026-10-13 proves Easy Auth login with
prompt=select_account forwards that exact prompt to tenant-scoped Microsoft
authorize. Current /sign-in has no prompt. No tokens/state/cookies recorded.
W4: Existing Azure logs contain login/logout sidecar events, but no application
successful-flow markers. Four app denials last occurred before staff repair;
no evidence of a new role authorization failure. Only fixed event names/counts
were queried, not directory identities or token payloads.
W5: https://github.com/jmservera/ama/actions/runs/38319901482
Original job 115168811216 failed during Copilot provider authentication with
HTTP 403 after partial agent execution, and its internal retry failed similarly.
Owner's attempt 3 subsequently completed success. This is not the deployed
workbench's Entra failure; no workflow/secret change is justified by this result.

## Cycle 1: Contrarian and Alternatives

Adding prompt only after logout still depends on Microsoft end-session returning
to the application and needlessly signs out an existing identity-provider
session. Switching should go straight to a fixed local sign-in selection route
and Easy Auth with select_account; ordinary Sign out retains platform logout.
Do not automatically choose a different person: explicit user selection remains
required. Cancelling the chooser does not promise logout. No MSAL dependency,
new registration, consent, callback or auth exemption is required.
Do not enable generic request logging: callbacks/query strings/cookies contain
sensitive data. Add only constant app flow events for switch request, picker
start, normal sign-in/sign-out and authorized workbench arrival, collected by
the already enabled diagnostics. These markers cannot prove which account
was selected and must not be described as actual browser acceptance.

## Parent Synthesis and Readiness

Research disposition executed; one focused Wider/Deeper/Contrarian cycle.
Planning Readiness Ready. Select /sign-in?switch=1 with an exact parsed flag,
fixed /app destination and prompt=select_account only for explicit switching.
Reject global logout-first switching; retain ordinary sign-out unchanged.
Add privacy-safe fixed events and regression coverage; deploy existing app
image and verify live Microsoft prompt and ingestion. No need to change IaC
or rerun the already-successful owner workflow. Stop research: material
questions answered; remaining actual account replacement is owner-session
acceptance, not further code discovery.
