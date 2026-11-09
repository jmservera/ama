# Plan critique: issue 954 composed-source browser validation (2026-11-09)

Execution: one critique of the final candidate plan, before the holder check and the run, by an independent read-only reviewer (rubber-duck agent; it ran nothing). Verdict: Revise, all four findings applied. Independent assessment of the final head is still required.

## Findings applied

* B1 (blocking): details said 13 detector PASS lines; the checker prints 14 in that group (13 fixtures plus `empty alert receipted`), 83 PASS in total. Applied: the criterion is exactly 83 PASS and exactly one expected control FAIL followed by `PASS negative control`, compared with the C2 labels, not context only.
* B2 (blocking): the checker does not create its observation directory. Applied: create `<evidence>/obs` before admission and inspect both status receipts.
* N3: `flock` and the checker can both exit 1. Applied: `flock -n -E 99`; 99 is unadmitted, other nonzero is a failed execution.
* N4: the runtime-equivalence wording could overclaim. Applied: the claim is that base `3a9767d5c` and main `2b6d80a25` have no runtime-source delta; the tested head is not claimed merged with `2b6d80a25`.

No advice conflicts with a confirmed decision; none rejected.
