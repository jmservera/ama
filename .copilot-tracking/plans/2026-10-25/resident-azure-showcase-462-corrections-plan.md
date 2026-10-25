# Plan: limiter, stale-email and offline verifier corrections (issue 462)

Written 2026-10-25 after `research/2026-10-25/resident-azure-showcase-462-corrections-research.md`, before critique and code. Details: `details/2026-10-25/resident-azure-showcase-462-corrections-details.md`. Refs #462, no closing keyword.

## Authority and bounds

Local code, local focused tests, local commits. No push, PR, full gate, Azure write, secret operation, role, network, deployment, container or SQL workload. The loopback-only #444 guard and `resident_preview` are untouched. The resident_demo composition stays separate.

## Scope (three items, nothing else)

1. Client-address resolution for the limiter: setting `ZF_DEMO_CLIENT_ADDRESS` with values `peer` (default) and `ingress-rightmost`, unknown values stop start-up. Pure resolver in core; the app calls it.
2. Stale-email admission: `IdentityMap.email_for(case_id)`, `authorise(..., expected_email)`, used by login and every protected request.
3. Offline verifier tool: core `verifier_tool` policy plus `tools/resident_demo_verifier.py` hidden prompt CLI.

## Acceptance

* Tests that fail without each correction: limiter keys by rightmost entry under the ingress setting, ignores client-prefixed entries, falls back to the peer on a bad header, one client cannot lock another; default `peer` ignores every header; an edited DB email denies login and an existing session; the tool rejects weak passwords without echoing, never takes arguments or non-tty input, and prints only a verifier that verifies the fake password.
* ruff, mypy and focused tests clean. No heavy gate, no SQL tests.
* Docs state the residuals: shared overall cap, shared NAT, direct-ingress-only assumption.
* Changes artifact and one original independent review after implementation.

## Amendments after the one critique (2026-10-25, before implementation)

See `reviews/plans/2026-10-25/resident-azure-showcase-462-corrections-plan-critique.md`. Applied as governing text: (1) no swap or memory-safety claim, owner-controlled machine only; (2) `main(argv, stdin_isatty, stderr, prompt)` rejects any argument, requires a terminal, hides tracebacks, with subprocess tests; (3) limiter acceptance reads "a source blocked by the per-source limit does not block a distinct trusted source unless the shared overall cap is exhausted", with a test that the overall lockout remains; (4) tests for multiple header lines, IPv6, malformed or empty last entry, port or bracket values (fallback to peer) and client prefixes; (5) policy adds repeated-unit, minimum-distinct-character and common-substring rejection, and the tool recommends a password-manager random value; (6) stale-email tests cover old email, new email, existing session and unchanged success.
