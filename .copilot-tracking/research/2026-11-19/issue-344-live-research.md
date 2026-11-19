# Issue 344 live research, 2026-11-19

Task issue-344-live. Research disposition: executed (fresh read-only live pass, prior passes of 2026-11-18 reused as context).

## Finding

Criterion 1 (first unticked) is unmet for browsers: the anonymous protected API returns 401 to curl but 302 to Entra for requests with a browser User-Agent and `Accept: application/json`. Cause: Easy Auth `unauthenticatedClientAction` is `RedirectToLoginPage` on `ca-cutover-test-demo-api`. In `infra/modules/containerapps.bicep:302` the only 401 mode is the opt-in `entraBearerOnly`, which also removes the client secret and browser sign-in, so no existing switch satisfies both halves of the criterion.

## Tier

Any fix lies in Bicep or the Easy Auth platform setting (infrastructure, deployment, security control), or needs a platform change in production-like config the owner excluded. That requires the FULL tier. The brief says to stop and report. No source edit is made.

## Planning readiness

Blocked for code. Ready for evidence-only deliverable.
