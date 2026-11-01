# Issue 521 live SQL window renewal: review (2026-11-01)

Review execution: once, self-review against the owner authorisation. Independent human review and CI remain required.
Outcome: live scope satisfied; no authorisation exceeded; no blocker hit.

## Verification (Playwright, resident test user; credentials never printed or stored)

| Check | Result |
|-------|--------|
| `/healthz` | 200, ready true (first request after idle took about 63 s cold start) |
| Unauthenticated `/demo/view` | 401 |
| Wrong credentials sign-in | stays signed out |
| Test user sign-in | login 200, session signed in, view 200 with expected sections |
| Forged session header; tampered session cookie | 409; 401 |
| Revision | `ca-resident-demo--0000005` Healthy, provisioning Succeeded, min 0 max 1, expiry 2027-01-31T23:59:59Z |
| Jobs and apps | 8 jobs Manual, 0 non-Manual; all apps min replicas 0 |

## Gaps and notes

* Cross-case denial is shown by session binding (forged header 409, tampered cookie 401, unauthenticated 401) and one case per view; no second resident account was used, so cross-account reads were not exercised live.
* The README step "renew one reviewed statement per row" was applied as one guarded transaction over the 522 rows sharing the single owner-approved provenance (interpretation of "approved, non-revoked").
* The ACR could not be read from this host; image post-#590 status is inferred from the revision commit and the accepted 2027 expiry.
* Credential rotation (README step) was not performed; not authorised. The AI tariff expiry (2026-11-01 in `resident_ai.reserve`) is unchanged, so the AI assistant stays unavailable by design.
* No billing/headroom was queried; the owner's explicit authorisation was relied on for the cost precondition.
* Issue #521 criteria: criterion 4 (live apply and verification) is evidenced here; other criteria are not re-proven, so this PR uses `Refs #521` only.
* The signed-in screenshot contains a synthetic address and was not retained.
