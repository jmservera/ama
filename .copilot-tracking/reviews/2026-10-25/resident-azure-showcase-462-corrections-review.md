# Issue 462 corrections: original independent review (2026-10-25)

Reviewer: code-review agent, one execution after implementation, read-only. Outcome: Conformant,
no findings. Reviewed boundary: uncommitted working-tree diff against `041e1995` (limiter,
stale-email admission, offline verifier). Output below is unaltered.

---

No findings. All three items are conformant.

**Verdict: Conformant**

- **Login limiter:** `client_key` (`resident_showcase.py`) returns the peer unless the mode is `ingress-rightmost`. In that mode it takes the last entry of the joined `X-Forwarded-For` values and accepts it only if `ipaddress.ip_address` parses it. A missing, empty, trailing-comma, port-bearing or non-IP last entry falls back to the peer bucket, so a client-supplied earlier entry is never used. `ZF_DEMO_CLIENT_ADDRESS` is validated, with an invalid value raising `ShowcaseConfigError`. It is passed through `config.client_address` in `__main__.py` and `client_address=` in `app.py`. The login handler calls `client_key`.
- **Stale-email admission:** `authorise` denies unless `admitted_email` is non-None and equals `row.email`, and `exclusion` still runs. `IdentityMap.email_for` returns the canonical map key. Because `exclusion` already requires `canonical_email(row.email) == row.email`, the comparison is consistent. `app.py` calls it with `self.identity.email_for(case_id)` at both call sites: the login/session-issue path (line 120) and the protected-request path (line 135). A changed email therefore blocks login and live sessions.
- **Offline verifier:** `check_strength` and `build_verifier` return generic reasons that never include the password, and they use the existing `make_verifier`. `infra/scripts/resident_demo_verifier.py` rejects any argument and any non-tty stdin, uses `getpass` for a hidden prompt twice, and prints only the verifier to stdout. The prompt text goes to `/dev/tty` via `getpass`. The broad `except` blocks stop a traceback from carrying the password. The script sets `RLIMIT_CORE` to 0, and its docstring and the README say the plaintext briefly sits in process memory.
- **README claims:** They match the code. The NAT and distributed-attacker residuals and the untested other-proxy case are disclosed as such.
- **#444 loopback guard:** `git diff HEAD` has no changes to any `resident_preview*` file.
- **Tests:** The focused test run reported 44 tests, OK.

---

## Routing (added by the coordinator session, not part of the reviewer output)

* No review findings to route. Residuals already recorded in the changes artifact stay open: the
  distributed exhaustion of the overall cap, the untested extra-proxy case and the verifier memory
  exposure.
* Gates G1 to G4, the complete `tools/rpi-checks.py --all` gate, hosted checks and independent
  assessment remain open. The reviewer ran focused tests only; this review is not a gate.
