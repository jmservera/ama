# Issue 444 boundary threat model documentation: details

Date: 2026-10-25. Prospective.

## Content of the api README subsection "Threat model for the synthetic preview (#444)"

* Scope and non-goals: loopback-only synthetic read-only feedback preview. Not suitable for public hosting, not an authentication design, no password or session, not an approved resident design. A cloud showcase is separate issue 462, which needs its own cloud composition, identity and review and must not weaken this loopback guard.
* Assets: resident-visible fields (home, measures, progress, next step, appointments), the grant fixture, the synthetic dataset, staff-only data (notes, safeguarding, finance, staff identifiers, chat, memory, other homes) as the protected assets.
* Actors: the owner or reviewer running the process, a local user on the same host, a browser page on another origin, a malicious input in a dataset field.
* Trust boundaries: process start-up configuration (subject, dataset, fixture) is trusted and server-owned; HTTP requests are untrusted; the dataset text is untrusted for rendering.
* Threats and controls (table): impersonation by claimed subject; cross-case read; staff data leakage; stale or revoked grant; representative without current authority; offer shown as confirmed; unavailable action use; write or mutation; non-loopback or DNS-rebinding host; XSS and content injection; framing or cross-origin read; real or cloud data and credentials entering the process; outbound calls; normal data path read. Each row names the control and labels its evidence as test-proven (naming the exact existing test) or implementation-inspected only. Add no test claim for DNS rebinding, XSS from malicious dataset text, outbound traffic or generalised traversal (C1).
* Residuals (C2): fixture tampering by a same-host actor (grants re-read per request without integrity or ownership check); no concurrency, thread, rate or workload bound (ThreadingHTTPServer, grants JSON re-read per request); unexpected errors are not uniformly handled and may end the response or print diagnostics; dataset, case and representative-authority data load once so authority changes need a restart (grants re-read per request); local same-host users can reach the loopback port; no request audit log or rate limit; no TLS; the synthetic fixture is not evidence about real residents; no human review, screen-reader audit or conformance claim.
* Claims limits: documentation evidence, not a security certification or score promise.

## Files
Content change only in src/api/README.md and src/core/README.md (one link line). Tracking artifacts (research, plan, details, critique, changes, review, state) are separate and permitted (C5).

## Validation
Documentation review against code and tests; link check; Git diff; existing resident tests unchanged; full gate at exact head.

## Critique wording rules
* Write-method behaviour: known preview routes reject writes with 405, unavailable routes 403, unknown paths 404, disallowed Host 403 (C3).
* Outbound: say no configured external endpoints or third-party loads; the page makes a same-origin fetch; not egress-tested (C4).
* Binding to 127.0.0.1 or ::1 enforced by safe_start is the remote-exposure control; the Host check is an extra request guard, not authentication (C7).
* The two-cycle cap is operational only; every accuracy finding is fixed or recorded before the gate (C6).
