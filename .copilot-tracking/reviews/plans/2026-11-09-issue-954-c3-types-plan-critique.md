# Plan critique: issue 954 C3 (2026-11-09)

Execution: one critique of the final candidate plan, before any merge, source edit or validation, by an independent read-only reviewer (rubber-duck agent; it ran nothing). Verdict: Revise, one finding applied, one rejected with a reason. Independent assessment of the final head is still required.

## Findings applied

* B1: the details used `Mapping[str, str]` without importing it, which would be a `name-defined` error. Applied: `Mapping` is imported from `collections.abc` (details updated before commit).

## Rejected

* B2 (replace `int(page.evaluate(...))` with a typed callable alias for `page.evaluate`): rejected. Aliasing a `-> Any` method to a narrower return type is an unchecked cast in disguise, which the coordinator forbids; `int()` is a real runtime conversion of a JavaScript array length and the `count == expected` assertion is unchanged for every valid value. The residual difference (a non-integer result raises instead of failing the comparison) is stricter, not weaker, and is disclosed in the research and the review. The fix remains proven by the unchanged 13 detector fixtures in the browser run.

No advice conflicts with a confirmed decision beyond B2. Product edits, config exclusions and CI changes remain rejected.
