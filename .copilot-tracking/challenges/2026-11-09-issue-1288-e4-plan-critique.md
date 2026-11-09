---
title: Plan critique - issue 1288 E4
---

# Plan critique (single final-candidate critique), issue 1288 E4

Executed once, by the RPI agent itself (not independent). Process disclosure: the lane, boundary change and tests were drafted and run green before this critique was written, so it challenges a drafted candidate rather than a blank plan. One test regex and the verifier wiring were corrected during the first run; no other change followed from a red result. No live, Azure, model or financial call was made.

## Challenges and dispositions

| Challenge | Finding | Disposition |
| --- | --- | --- |
| Whole-payload provenance | A reading-only seal would leave address, quality records, policy and prompt text open to private joins | The lane composes the entire evidence (fixture case, policy, control, persisted simulation readings) itself; `Ai.provider_body` is the only serializer, and the seal covers the SHA-256 of the exact serialized bytes. Test: a private payload under a valid fixture seal is refused with `payload-mismatch` before meter, token or socket |
| Source and credential isolation | The brief asks for a genuinely separate connection, schema and credential | Applied for SQLite: separate file, separate `SqlStore`, separate 0600 key file, refused when the paths overlap the working store or key is unsafe. Not applied for SQL Server: no separate SQL login or database exists. Recorded as an unmet criterion, with the route unavailable rather than faked. The provider credential is shared by design (existing token guards still apply) |
| Tamper | Altered body, forged mac, edited namespace or store claim | HMAC over namespace, store, nonce, digest and expiry; each refused with its own code. Tested |
| Replay | A valid seal reused | Nonce consumed atomically in the simulation store; second use refused `replayed`. Tested. A restored old store snapshot could re-open a nonce: expiry bounds it, disclosed |
| Cross namespace and cross store | A seal minted by another store or namespace | Store identity and namespace are inside the mac; `store` and `namespace` refusals tested |
| Caller free text | Caller-supplied boolean, unsigned digest or "synthetic" text | None is read as authority. Tested: boolean, unsigned digest and free-text claim all refused |
| Last-check suspension | Release or suspension could change between the hold check and the socket | Not solved atomically and not claimed. The hold is checked before dispatch and again after the response (output discarded if held). The private route stays off; the public lane does not relax it |
| Production composition | A test-only or mock path could pass while production differs | Tests run a real `Ai` client against a real loopback TLS peer with a counting meter and token; the peer's received bytes equal the composed bytes and the UI view. The route attaches the verifier to the real `Ai` lazily |
| In-process hostile code | Code that can read the key or replace the verifier could mint a seal | Out of scope: honour-system limit of an in-process seal, disclosed. A separate process or HSM-style signer is a candidate follow-up |
| Is this a working demo? | The simulation proposal works with a real client path; real captured-data grounding stays off | Recorded as an unmet criterion, not hidden |

## Applied amendments

* A1: the bytes received by the peer must be compared with the composed payload, not only the value matches. Applied (test asserts byte equality).
* A2: every refusal must be asserted before meter, token and socket, not only that an error is raised. Applied.
* A3: unavailable (no store, key, or unsafe key) must show the manual route, never success. Applied in the lane, API and UI.
* A4: record the architecture as CANDIDATE, not approved, with the SQL and process-signer gaps. Applied in the changes artifact and README.

## Not changed

No private route was enabled, no proxy, framework or schema rewrite was added, and no private data path was read.
