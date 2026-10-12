---
title: Public Welcome and Entra Account Implementation Evidence
description: Current full-plan implementation and validation state
ms.date: 2026-10-12
---

## Scope and State

Task zava-workbench-entry-2026-10-12, full plan P01-P03.
Confirmed automatic; Implement active. Plan and details are ready after the
single critique and all five direct dispositions. Existing callback verified
using the owner's authorized isolated profile. No credentials collected.

## P01: Welcome and Account

P01-T01/P01-T02 source complete. Public welcome has no app script/data fetch.
/app is protected both by app routing and exact platform exemptions.
Validated-principal account metadata preserves stored synthetic staff and
contractor projections. Fixed own-photo proxy bounds bytes/type/timeout and
blocks redirects; explicit errors never include tokens/upstream bodies.
Native account menu provides initials, real-photo state, logout/switch,
Escape/outside closure and production-specific sign-in/error UI.
Targeted auth/photo tests pass. Full MVP suite: 284 tests, 26 existing skips.

## P02: Token Store

Source implemented; dedicated token-only account, scoped identity, private
endpoint/diagnostics, daily job, five-day HTTPS delegation and single-secret
writer. Four renewal tests pass. Bicep compiles after correcting placement.
Versionless Key Vault rotation is documented to refresh within 30 minutes;
the secret-ref environment trigger makes revision refresh explicit. No
credential is read by application code or output by renewal. Staged bootstrap
and real job execution remain pending.

## P03: Validation and Deployment

P03-T01 complete. MVP: 284 tests, 26 existing skips; initializer: 15 tests;
Bicep build clean and JavaScript syntax passes. ACR db3 succeeded, real image
welcome-20261012-01 digest
sha256:087f394f562e95a3b5e2f8a3a0ba1eeefc35c529d939a5c94d2c4b4fea69277d.
Playwright desktop/mobile welcome verified logo natural width 644, /sign-in
button and zero API resource requests; 375-pixel layout has no overflow.
Synthetic local account verifies name/initials, Escape focus return, Enter
reopening, outside closure, contained mobile panel and logout to welcome.
This local password session is not a live Entra photo acceptance claim.
Real registration User.Read merge and read-only recheck succeeded, retaining
callback/identity/roles/credentials. Bootstrap and activation succeeded.
Related infrastructure/MVP guides and knowledge-base routing updated.
Human photo/consent acceptance remains separately identified.

### Live bootstrap and activation

zava-welcome-bootstrap and zava-welcome-activation both Succeeded. Activation
reused the deployed module parameters and changed only tokenStoreReady,
avoiding a second unrelated foundation rollout. Actual job
job-forward-test-auth-renewal-18ee85o Succeeded and secret metadata reports
expiry 2026-10-17T16:43:34Z, without retrieving its value. Live role inventory
confirms exactly registry pull, account Delegator, auth-tokens-only Contributor
and single-secret Secrets Officer.
Actual shared keys/public blobs false; tags classify authentication secrets.
Auth token store true, private SAS setting name, delegated User.Read/
offline_access and select_account configured. API retains retrofit SQL,
standard model and existing registration/client-secret, plus versionless
rotation trigger. Anonymous root/logo/styles/health 200; data APIs and
non-browser /app 401. Revision 0000003 is now both latest and ready.
Live Playwright confirms public welcome/real logo, zero API resource requests,
no 375-pixel overflow, and provider redirect with User.Read/offline_access,
select_account and the correct callback. No OAuth state/token was returned.
Synthetic expiry browser check observes exactly one photo and refresh call,
visible initials/error, and zero password inputs for production role denial.
Two harness-only locator corrections were needed for hidden/native details
and duplicate alert roles; application behavior was already correct.

### Pending human gate

Fresh legitimate user sign-in is needed for delegated photo consent and
account-switch acceptance. Do not fabricate headers, save a photo/token or
treat the administrative CLI profile as a workbench browser session.

The acceptance form reported that the owner is unavailable and will review
later. Preserve that gate unchecked; no consent/photo acceptance is inferred.
All implementation/deployment is delivered. Review handoff is explicitly
bounded to source, deployment and synthetic behavior, with the human gate
routed as residual work rather than a conformant end-to-end outcome.
Current-head 80d4a47 technical CI, image/security scan, SQL parity, MVP
validation and prototype validation all succeeded. The source-only 15e8158
runs were superseded/cancelled by the record commit, not failed tests.
Rubric scoring remains running/pending and is not capstone readiness.

## Blockers and Remaining Work

P01/P02 and P03-T01 complete. P03-T02 implementation/deployment are complete,
but the legitimate user photo/consent/switch acceptance gate remains open.
P03-T03 published in 15e8158 on existing PR #65 with a completion-boundary
comment. Related link check reports eight existing missing targets, zero new
missing targets and zero changed-fragment failures. CI is triggered by the
source commit; final post-implementation Review remains pending human gate.
No implementation defect is presently known.
