# Plan: integrate #146 and #79 audit commits

* [ ] Phase 1: cherry-pick dd90536f then 45e821cc cleanly.
* [ ] Phase 2: check whether the TSV inventory needs regeneration; run test_cutover_audit and test_bicep_policy.
* [ ] Phase 3: link check on added lines, secret scrub, code-review-readiness review.
* [ ] Phase 4: commit locally with trailer, no push.
