# Critique: issue 2245 live plan (2026-11-22)

Executed once. Verdict: proceed with changes applied.

* Claiming "fixed" is not supported: the 500 is not reproduced and the lock holder is unknown. Plan states verify-not-fixed for that criterion. Applied.
* A 503 mapping for lock timeouts would change a shared handler and take the FULL tier for a hypothesis; rejected. Applied: test-only change.
* The test must fail if creation gains a write transaction; assertion bound of two is the measured baseline. Applied.
