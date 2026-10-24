---
title: Independent plan critique, Entra-authoritative access (original outcome)
ms.date: 2026-10-24
---

Reviewer: independent rubber-duck agent, read-only, before any implementation. Verdict: REVISE (4 blocking, 2 non-blocking).

Blocking
1. Identity not byte-stable: tenant and oid must be parsed as UUIDs and canonicalised to lowercase before hashing.
2. Email and name remain authorization and snapshot-equality keys (bulk_edits, resident_decisions, redress). Authorization and distinct-person comparisons must use canonical tenant+OID or the derived code; email stays display/audit only.
3. RuleOwner cannot stay unbound while preserving named-approver and no-self-approval; author and approver identity are email strings in rulecards and server.
4. Trusted-header spoofing must be a release-gated invariant with direct-origin forged-header negative tests.

Non-blocking
5. setup-entra propagation wait verifies manifest appRoles only; the grant script must verify the ApplicationAdmin role id on the enterprise app.
6. Claim sanitisation underspecified; account() re-reads raw claims.

Dispositions (applied to the plan before implementation)
* 1, 6: UUID canonicalisation and one central sanitiser used by principal and account().
* 2: Entra principals get a derived, non-routable pseudonymous `email` (`<code>@entra.invalid`); claim name and email are stored only as `display_name` and `display_email`. No claim lands in an authorization or equality key.
* 3: Because the derived identity can never equal a named staff email, RuleOwner and AIRestart remain inoperable for unbound principals (fail closed). Named-person identity migration is routed as a follow-up, not weakened here. The admin is not granted these roles.
* 4: Phase 7 requires external anonymous and forged-header denial plus confirmation that ingress auth is enforced before the owner is told to sign in.
* 5: grant script waits for and verifies the role id.
