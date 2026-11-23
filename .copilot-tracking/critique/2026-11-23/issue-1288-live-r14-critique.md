---
title: Issue 1288 r14 critique
date: 2026-11-23
---

Executed once on the final candidate. Verdict: compatible, proceed.

* Downgrade only (fail-safe direction); no new autonomy. Accepted.
* Use cited keys only, so unrelated impossible rows do not suppress a valid flag. Accepted in P2.
* The test must mutate a cited row after the model result, not before capture, otherwise it duplicates r13. Applied in P1.
* Release admission (criteria 4, 8) cannot be advanced by this change and must stay recorded as unproven. Applied.
