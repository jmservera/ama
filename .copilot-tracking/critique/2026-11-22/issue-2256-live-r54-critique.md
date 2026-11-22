# Critique (executed once)

Verdict: proceed verify-only; no src change.

* Risk: the issue has no checkbox list. Disposition: split the Expected paragraph into criteria A, B1, B2, C and say so.
* Risk: seeded offers lack due_at and a timezone, so due and wait cannot be shown. Disposition: record B2 as unproven for the demo; do not edit seed data (no production change).
* Risk: the image digest cannot be tied to a commit. Disposition: accepted as a stated limit; behaviour is the evidence.
* No conflict with owner decisions of 2026-11-18.
