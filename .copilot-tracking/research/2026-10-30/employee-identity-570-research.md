---
title: Employee acceptance identity research
description: Offline investigation of the recorded employee identity predicate
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

Task employee-identity-570-2026-10-30, slug employee-identity-570.
Refs #570. Determine whether the recorded failure is a runner expectation
defect or application projection defect, then prepare a bounded repair.
Audience: acceptance owner and maintainers. Output mode: convergence.
Inputs: original 1030c changes, review, runner and capture-free evidence;
API auth/me implementation and Entra-authoritative infra contract.

## Research Parameters

Focused posture, selected from the caller's named internal evidence.
No live sign-in, private test-user file, Azure change, deployment or push.
Read-only research except dated evidence and required workflow state.
No external research required. Existing failed evidence stays immutable.

## Extension Registry and Provenance

Repository instructions and RPI phase skills selected. Research specialists
skipped: one tightly coupled code/evidence trace. Web design skills not
applicable: no web implementation or design change intended.

## Direction Controls and Participation

Caller explicitly requests all four phases in order and a local Refs-only
commit. This is bounded full-loop authorization, not authorization for later
child work or live retries. No interaction required or available.

## Questions and Candidate Areas

1. What exactly does the runner compare, and which predicates failed?
2. What does auth/me guarantee under Entra-authoritative binding?
3. What offline regression can distinguish the defect from wrong-account admission?

## Research Cycle Log

Cycle 1, all inline in order:

1. Wider: inspected original changes and independent Review, both runners,
   tests, supplemental evidence and infra contract. The failure is specifically
   expectedIdentity=false, not rosterBound as an admission requirement.
   Reflection: inspect the account projection, not roster initialization.
2. Deeper: traced server /api/me to provider.account and identity.principal.
   Account email is display-only and blank unless exactly one email-like claim
   exists; user email is deliberately a derived pseudonym when unbound.
   Reflection: immutable tenant/object identity is already exposed and is the
   correct account-verification contract.
3. Contrarian: old predicate already trims returned email and lowercases both
   sides, never compares name and never gates on rosterBound. Missing, multiple,
   aliased or different-account display claims cannot be distinguished from the
   retained booleans. Existing tests explicitly allow rosterless staff and deny
   wrong tenant, malformed object id and absent/unmapped roles.
   Reflection: do not claim a particular raw claim or serving revision, weaken
   account verification to HTTP/role, or modify application authorization.

No additional cycle needed: code contract is established; actual historical
claim contents cannot be recovered within the permitted capture-free evidence.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | `.copilot-tracking/changes/2026-10-30/live-acceptance-1030c/acceptance.py:28-55` | expectedIdentity compares account.email to USERNAME; case folded already; rosterBound diagnostic only. |
| C2 | `.copilot-tracking/changes/2026-10-30/live-acceptance-1030c/second/evidence.json:26-51` | HTTP/schema/provider/role/not-view-only pass; email comparison fails; no raw identity retained. |
| C3 | `infra/README.md:1937-1947` | Verified tenant/object id and assigned app role suffice; roster metadata is optional, not login prerequisite. |
| C4 | `src/api/src/zava_forward/api/auth.py:29-30,158-184` | Email-like claims are optional display metadata; exactly-one selection is deliberately conservative, not identity authority. |
| C5 | `src/core/src/zava_forward/core/identity.py:1-5,57-92` | Tenant/object id define identity; unbound email/code are derived keys; display_email is separate. |
| C6 | `src/api/src/zava_forward/api/server.py:396-405` | /me projects authenticated user and separate provider account. |
| C7 | `src/api/tests/test_entra_authoritative.py:28-38,142-148,235-250` | Rosterless access and wrong-tenant/object/role denials are established test patterns. |
| C8 | `.copilot-tracking/reviews/logs/2026-10-30/live-acceptance-1030c-review.md:108-122` | Original failure proves missing acceptance, not a particular mapping bug; both employee slots consumed. |

## Findings, Alternatives and Decision State

Confirmed runner contract defect (C1/C3-C6): a display-email equality test
incorrectly stands in for verified immutable account identity. It can reject
the correct Entra account with absent/multiple/aliased display claims.
The evidence does NOT prove which such case occurred, whether the actual
session belonged to the requested person, or the deployed revision's parity.
No application mapping defect is demonstrated. Preserve that uncertainty.

Selected repair: reusable next-run browser predicate under src/api/checks,
verified against actual synthetic /api/me HTTP payloads in src/api/tests
(outside the installed package). Require owner/identity-admin independently
verified expected tenant/object IDs, provider, role, schema and view-only
checks. Email comparison and roster binding remain boolean diagnostics,
never alternative admission. No sign-in entry point or inferred expected IDs.
Historical runners and evidence remain byte-identical.

Rejected: roster provisioning (contradicts C3); display-name/case repair
(not the failing contract); selecting one of several email claims (changes
non-authoritative display semantics unnecessarily); accepting any role-bearing
200 response (would admit a wrong account).

## Current Decisions and Residual Uncertainty

No credentials, browser launch or live requests during research. No external
evidence or legal-currentness claims needed. Future live acceptance remains
owner-authorized work with fresh budget and independent expected IDs. Do not
replay either exhausted historical runner. Runner cleanup/visibility findings
from the old Review remain distinct, outside this identity-only repair.

## Planning Readiness

Ready. Research disposition: executed, complete. All three questions answered
within offline evidence limits. Parent action: Plan, one independent critique,
then implementation and one Review as explicitly requested.
