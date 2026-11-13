# Plan critique: 435 C1 call-site inventory (2058)

Executed once by `rubber-duck`. Verdict: Revise (1 non-blocking finding), compatible; applied directly.

* N1 scope the accounting claim: `own-accounting` holds for calls mediated by `heldout_batch.run_batch`; the provider returned by `make_provider` can be called directly and bypasses the runner accounting and the flag requirement. The inventory note states this. Accepted and applied in the details.
* Confirmed by the critic: `own-accounting` is accurate; an in-memory entry passed all six inventory tests, the cutover tests and 56 held-out tests; no other inventory or document needs change; the validation list is sufficient.
