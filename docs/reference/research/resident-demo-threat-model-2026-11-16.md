---
title: Resident Demo Threat Model (Issue #462)
description: Threat assessment of the public fake-email login, shared demo credential, session handling, cross-case access, database fields and deployment isolation of the synthetic resident showcase
ms.date: 2026-11-16
---

## Status and limits

Design-time threat assessment of the synthetic resident showcase as implemented on `main` at `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`. It is demonstration-only: the sign-in uses one shared password and does not prove who anyone is. It is not a penetration test, security acceptance, production resident identity assessment, accessibility acceptance, or Legal or Data Protection Officer approval, and it authorises no deployment or Azure spend. No real resident data is in scope. Live Azure resources, role assignments and the live SQL view were not inspected.

Evidence: the [prospective research](../../../.copilot-tracking/research/2026-11-16/resident-demo-local-gate-462-research.md) holds the full control references. Run results are in the [changes record](../../../.copilot-tracking/changes/2026-11-16/resident-demo-local-gate-462-changes.md). Implementation guide: [showcase runtime and access controls](../../../src/api/README.md#synthetic-resident-showcase-462).

## Assets and trust boundaries

* Assets: the synthetic home projection (address, town, postcode, stage, measures, documents, sensors); the scrypt verifier and session key held as Key Vault secrets; SQL availability; the Azure spend cap.
* Boundaries: internet to HTTPS ingress; app to Azure SQL through a user-assigned managed identity; app to Key Vault secret references; browser origin and cookie scope.

## Threats and controls

| ID | Surface | Threat | Control on main | Residual risk |
|----|---------|--------|-----------------|---------------|
| T1 | Public fake-email login | Anyone who knows a listed email and the shared password opens that synthetic case | Labelled demo sign-in; the lower-cased, trimmed email must match ASCII `@example.com` (Unicode case folding can map an input to an accepted value); server-owned identity map built from the allowlist view | Accepted by design. Synthetic data only |
| T2 | Email enumeration | Telling known from unknown emails | One scrypt run for every attempt; one generic denial for failures; same status | A holder of the shared password learns whether an email is listed (success versus denial). Timing equalised by work, not proven constant |
| T3 | Password guessing | Brute force; lockout abuse | 5 failures per source and 60 overall per 10 minutes, then 429; body cap 2 KiB; concurrency cap; rightmost ingress address, so forged forwarding headers do not pick the key | Counters are in memory (reset on restart) and checking and recording are separate steps, so concurrent attempts can overshoot. The 429 carries no `Retry-After`. Global limit can lock out legitimate demo users. Strong generated password is the main control; scrypt cost is configurable within bounds (default N=2^15) |
| T4 | Shared credential | Disclosure of the password | Only a scrypt verifier is configured; Key Vault references; no real password in the repository or tests | Owner retrieval and rotation are operational steps outside this assessment |
| T5 | Session handling | Theft, replay, fixation, CSRF | Signed token, 30 minute expiry capped by the authority end; `__Host-` cookie with `Secure`, `HttpOnly`, `SameSite=Strict`; double-submit CSRF plus an Origin check (the Origin authority must equal Host, with Sec-Fetch-Site same-origin); session id fence; `no-store`; logout; exact Host allowlist | Stateless tokens are not revocable by the server before expiry, except that logout revokes the token in memory, a process restart invalidates all tokens, and the session key can be rotated |
| T6 | Cross-case access | Reading another resident's case | Case id comes only from the signed session; identity map and a parameterised single-case read are re-checked per request; provenance, revoked, window, email-form and duplicate exclusions fail closed | Covered by two-resident, forged and expired session tests |
| T7 | Database fields | Staff, safeguarding, finance or unrelated data reaching the page | 17 named columns from one view; row key allowlist; sensor rows filtered to `SYNTHETIC` source in the view; SQL errors reduced to a type name | Case rows are not filtered by a synthetic flag in the view: synthetic provenance rests on the owner-approved allowlist rows and operator verification, and projected free-text fields (address, measures, documents) could carry sensitive content if the source row did. The view is the only boundary; a widened view would widen exposure, so any change needs review |
| T8 | Deployment isolation | Reaching employee systems, data or spend | Separate app, identity, image, secrets and Bicep; SQL principal denied on base tables and granted one view; forbidden employee, store and AI settings stop startup; non-root uid 10001; no data volume; ingress off is the rollback; expiry capped by the packaged authority date | Real Azure state and spend headroom are unverified and remain unmet issue criteria |
| T9 | Web surface | Script injection, framing, sniffing | Strict content security policy, no framing, `nosniff`, no referrer | No penetration test |
| T10 | AI and writes | Unintended action | The SQL case projection is read-only; assistant off by default; no consent, upload or download | An optionally configured local SQLite agenda supports synthetic callback bookings and cancellations, and an optional chat log stores question text. Both are off unless explicitly configured, must never be used for real residents, and are not covered by the SQL read-only boundary. Optional AI is separately gated |

## Accepted risks

* The shared credential and stateless sessions are accepted for a time-boxed synthetic demonstration.
* Any use with real residents, real consent or production identity needs a new assessment and the human approvals recorded elsewhere.
