# Plan critique: issue 954 C2 (2026-11-09)

Execution: one critique of the final candidate plan, before any source edit (self-critique; independent assessment of the final head is still required). Verdict: Revise, applied directly.

## Findings applied

* B1: a status-text sentinel can pass when a regression ignores the false response and the app self-heals by reloading (client flag true, `photoFailed` true). Applied: identity sentinel on `me.services` and `photoFailed = false` in the pre-state so an ignored false deterministically leaves the client flag true.
* B2: asserting the client flag right after the sentinel is sound only if the handler has finished; applied via the identity sentinel (the services replacement is synchronous with the merge).
* B3: the control must not inflate counts or the quiet receipts; applied: not appended to `results`, one control only.
* N1: the transient-toast timing note from the independent review stays a documented limitation; no new claim.

## Rejected

No advice conflicts with a confirmed decision. Product edits and blanket empty-dialog ignores remain rejected.
