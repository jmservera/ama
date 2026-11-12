# Critique: issue 128 source-completeness paired dimension (single pass)

Executed once by an independent native rubber-duck agent on the plan and draft candidate (not before any code existed). Verdict: increment minimal and distinct; one High finding.

| Finding | Severity | Disposition |
| --- | --- | --- |
| A ranker that excludes the missing-source subject raised `StopIteration` in `_position` instead of reporting a detected defect | High | Applied directly: `_position` returns `None`, `_check_pair` records `excluded`; failing-first test `test_seeded_exclusion_is_detected_not_a_crash` (red: StopIteration error, then green) |
| Hash-change statement ambiguous | Low | Accepted: the record hash of any input changes because `DIMENSIONS` gains a key and an input lacking a source pair now blocks; no stored hash is consumed outside tests |

Other checks: no consumers of `paired_equity` or `DIMENSIONS` outside its tests; contrast covers `missing` only (stale and partial pairs are rejected as `wrong_contrast`, a documented fixture-local choice). Fairness and activation stay false.
