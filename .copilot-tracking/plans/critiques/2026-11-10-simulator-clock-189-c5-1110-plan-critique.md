<!-- markdownlint-disable-file -->
# Critique: issue 189 simulator-admin HTTP test-clock plan (one pass)

Executed 2026-11-10 before any source edit. The brief forbids nested agents, so this is a same-agent adversarial self-critique, not an independent critique. Independent exact-head review remains Root's required gate. Verdict: proceed with amendments. The critique is not repeated for this task.

| Finding | Severity | Disposition |
| --- | --- | --- |
| A datetime subclass whose `now` returns a plain `datetime` breaks the `Self` contract and mypy strict | Non-blocking | Applied: return `cls.fromtimestamp(...)` typed `Self`; whole-second instants are exact |
| Shared class-level clock state would leak between tests if one subclass were reused | Non-blocking | Applied: a per-test subclass from `scoped_clock`; `current` is never mutated on the shared base |
| Restoring the clock before the server stops could let a late request read the real clock | Non-blocking | Applied: register the clock restore before the thread, and join after `shutdown` and `server_close`; LIFO order is stated in the details |
| The server thread is currently never joined, so `join` must not hang if `shutdown` was skipped | Non-blocking | Applied: join is registered before `server_close` and `shutdown`, so it only runs after both; join uses a bounded timeout and the test asserts the thread is no longer alive |
| An inline `patch` in `setUp` cannot be neutralized by the external negative control without editing the test | Non-blocking | Applied: the installer is the single method `bind_clock`, called from `setUp`; the external runner replaces only that method. The method is the real code path, not a test-only hook with different behaviour |
| The new tests could pass if the clock were bound but the handler used a different time source | Non-blocking | Applied: the boundary test advances the scoped clock through real HTTP and asserts expiry GET and 400 refusal at exactly EXPIRES, which can only pass if the handler's time source is the scoped one |
| Status assertion before `started["changed"]` is diagnostic only | Non-blocking | Applied: stated as diagnostic; the repair is the clock binding, proven by the negative control |
| Other fixtures with absolute dates may be time-bombed | Non-blocking | Dispositioned: out of scope, not claimed; no unrelated cleanup; recorded as a follow-up |

No finding conflicts with a confirmed owner decision. No significant or divergent issue needs a user decision.
