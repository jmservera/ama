# Review: synthetic resident Azure showcase, local slice (issue 462)

Executed once on 2026-10-25 by an independent read-only code-review agent after the changes artifact was written. The agent's output is recorded unaltered below. Not repeated in this task.

Assessed boundary: the uncommitted local candidate on top of `4a72ac03`. Review execution: done. Outcome: Conformant with follow-ups. No High findings.

## Original reviewer output

**Outcome: Conformant with follow-ups.** The reviewer read the code only and ran nothing.

### Medium: login limiter collapses to one bucket behind the ingress
`src/api/src/zava_forward/api/resident_demo/app.py:244` keys `record_failure` and `retry_after` on the TCP peer (`client_address[0]`). Behind a proxy or Container Apps ingress all clients share one bucket of 5 failures per 10 minutes, so anyone can lock every demo resident out of sign-in for the window. The README says forwarded headers are never trusted but not this consequence. Fix: document the limitation, or add a trusted-proxy setting that reads the client-address header only when the peer is the known proxy.

### Low: stale identity map lets an old email keep signing in
`resident_showcase.py` (`authorise`, about line 170) and `app.py:96` (`login`). The email-to-case map is built at start-up; `authorise` re-reads the row but does not require `row.email` to equal the typed email, so an email changed in the database still opens the case until restart. This contradicts the README claim that every request re-checks admission. Fix: pass the canonical login email to `authorise` and require equality.

### Checked and found sound
Auth and cross-case access; SQL injection; positive-allowlist fields; user enumeration and timing; CSRF and `__Host-` cookies; fail-open config; secrets in code (none); #444 guard unchanged.

## Routing (later work, not fixed in this task)

* Follow-up 1 (Low, small, recommended first): require login email equality in `authorise`, with a test.
* Follow-up 2 (Medium, blocks cloud deployment): the proxy-aware limiter or an explicit documented lockout accepted by the owner before any ingress deployment.
* Blocked live criteria G1 to G4 and the coordinator full gate remain open.
