---
title: Issue 462 hosted review correction 4 changes
ms.date: 2026-10-26
---

Bounded correction of five open hosted review findings on PR 463 (head f5ba4737), recorded 2026-10-26 after the work. Critique: an independent rubber-duck review of the diff ran after the first implementation, not before it; it found one high gap (public-role grants), which was then fixed. No gate, Azure write or secret read was done.

* `infra/scripts/resident_showcase_sql.py`: `--apply` now verifies an existing user (external type, SID equal to the resident client id, no role membership, only CONNECT and SELECT on the resident view, no user-object or schema grants to public) and refuses otherwise. It needs `--create-principal` or `--client-id`.
* `src/core/.../resident_showcase.py`: when the 4096-entry revocation store is full, `revoke` rotates the process nonce so every token, including the one logging out, stops verifying (fail closed; all sessions end).
* `infra/scripts/resident_demo_secrets.py`, `resident_demo_verifier.py`: `getpass.GetPassWarning` is an error before any input is accepted.
* `infra/scripts/resident_demo_deploy.py`: `--no-ingress` accepts an expired window (the 2026-11-01T00:00Z cap still applies); opening ingress still needs a future expiry.
* Tests added for each. Focused results: infra 42, core resident 68 (13 live-SQL skipped), api resident 49, all OK. Live SQL behaviour of the verification queries is untested.
