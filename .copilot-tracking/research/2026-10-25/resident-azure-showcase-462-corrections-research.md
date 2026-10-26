# Research: limiter, stale-email and offline verifier corrections (issue 462)

Written 2026-10-25 (about 22:10Z) before the plan, critique and any code change. Refs #462. Prior work is preserved: local slice commit `b7bcf019` and its original review (Medium limiter, Low email), retrieval proposal commit `041e1995`.

## Owner direction (2026-10-25)

Option C approved: "Approve owner-held password and offline verifier tool", sharing "Only me". The owner chooses and keeps the password locally. Approval covers the offline verifier tool only: no real secret generation, read or write, no role, network or deployment action. The accepted ungated planning push is a process disposition only; technical gates remain.

## Facts

* Code: the limiter key is `self.client_address[0]` (`resident_demo/app.py`, `_login`); `LoginLimiter` has a per-source cap (5 per 600 s) and an overall cap (60 per 600 s). Behind an ingress the peer is the proxy, so every client shares one per-source bucket.
* `authorise(row, now, case_id)` checks only case id and `exclusion()`. The identity map holds email to case id from start-up, and `login` and `view_for` never compare the live row email with the map email. A database email edit therefore leaves the old map email signing in and an existing session valid until restart.
* Ingress, read-only management metadata (`az containerapp show`, `az containerapp env show`, 2026-10-25 22:07Z): the existing `ca-cutover-test-demo-api` uses external ingress, `allowInsecure` false, no IP restrictions, no client certificate mode, no sticky sessions, in `cae-cutover-test-demo` (not internal, public network access Enabled). This is a precedent only; no showcase app exists and nothing was created.
* Microsoft Learn, Ingress in Azure Container Apps, HTTP headers table (ms.date 2026-10-09, fetched 2026-10-25): `X-Forwarded-For`: "If specified in initial request, it is appended to. Only the rightmost IP is provided by Azure Container Apps. Any other values must be validated by the user to prevent IP spoofing." Therefore a client can pre-set earlier entries; only the rightmost is platform-added.
* A third-party search summary agreed but is not relied on.

## Trust boundary decision (hypothesis marked)

* Trusted: the rightmost `X-Forwarded-For` entry, only when the operator sets an explicit setting that says the process is directly behind Container Apps ingress. Default stays the TCP peer, which is right for loopback and tests.
* Not trusted: every other entry, `Forwarded`, `X-Real-IP`, `X-Client-IP` and any other header.
* Hypothesis, not proved: if another proxy (for example Front Door) were placed in front of the ingress, the rightmost entry would be that proxy and the per-source key would collapse again. The setting is documented as valid only for direct ingress, and a deployment change would need re-review.
* Fail closed on a bad header: with the setting on, a missing, unparsable or non-IP rightmost value falls back to the peer address (the shared bucket, stricter), never to a client-chosen value. The client cannot choose a key that evades the limit: appending is by the platform, and the attacker's visible address is the rightmost entry.
* Residual, stated not hidden: the overall cap (60 failures per 10 minutes) is deliberate because all residents share one password; a distributed attacker can still consume it and block sign-in for the window. This is accepted as a documented residual, not claimed solved. Per-source lockout of honest users behind a shared address (for example a corporate NAT) also remains.

## Stale email decision

Compare the stored row email with the email the identity map admitted for that case, on login and on every protected request. A mismatch denies. Login also requires the typed canonical email to equal the row email. The map is immutable for the process, so a DB change closes access and an addition still needs a restart.

## Offline verifier tool decision

* Pure function in core, reusing `make_verifier` and `PasswordVerifier`, and a policy check: at least 20 characters, at least 3 of 4 classes, no whitespace edges, a short denylist of obvious strings and no run of 4 identical characters; the reason is generic and never echoes the password.
* A small CLI in `tools/` uses `getpass` (hidden, no echo), prompts twice to confirm, prints only the verifier to stdout, and refuses a non-terminal stdin so a password cannot arrive from a pipe, argument or environment variable. It writes nothing to disk and never prints the password. Output is credential-derived sensitive material: the owner copies it to a secure local channel (a password manager or an access-controlled local file with owner-only permission), never to chat or git.
* Tests use clearly fake constants and a fake prompt function injected for the test only. The tool is never run with a real password here.

## Unknown or still open

Budget headroom; live synthetic equality and provenance; allowlist at most 25 rows; private SQL view and principal; the vault write principal and path; the full gate; hosted checks. The deleted raw cost JSON is not relied on.
