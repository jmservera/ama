<!-- markdownlint-disable-file -->
# Critique: issue 1373 session-opacity test-oracle plan (one pass)

Executed 2026-11-10 before any source edit. The brief forbids nested agents, so this is a same-agent adversarial self-critique, not an independent critique. Independent exact-head review remains the Root's required gate. Verdict: proceed with amendments. The critique is not repeated for this task.

| Finding | Severity | Disposition |
| --- | --- | --- |
| Asserting `C-1` absent from the hex/digit structural parts is true by alphabet and gives little protection on its own | Non-blocking | Applied: the handle regex, equality with the keyed `handle("C-1")`, different-case and different-key separation carry the opacity claim; the substring check on structural parts stays as a cheap guard and is not presented as the primary property |
| The MAC-tamper step could pick a replacement equal to the current character | Non-blocking | Applied: choose a replacement character that differs from the last MAC character, then assert denial |
| Patching `rs.secrets` must not leak into other tests or the CSRF path | Non-blocking | Applied: patch only inside a `with` block around `issue`, replacing the module name, never `secrets.token_hex` globally |
| Frozen sid silently stops colliding if the key, clock or nonce constants drift | Non-blocking | Applied: the regression asserts the `C-1` substring in the MAC component and recomputes the MAC independently, so drift fails loudly |
| `token[:-2] + "xx"` tamper case in a neighboring test is vacuous if the MAC ends in `xx` | Non-blocking | Dispositioned as a residual: out of scope (no unrelated cleanup, one initial repair only); recorded in the changes and review records |

No finding conflicts with a confirmed owner decision. No significant or divergent issue needs a user decision.
