# Research: issue 216 live3 (evaluation gates, third live pass)

Task: issue-216-live3. Refs #216. Synthetic demo, desktop only. Live Azure authorised (rg ama, cap USD 700); no drills, no Key Vault rotation, no production change.

Research disposition: executed (opening record).

* One unticked criterion: citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set.
* Prior rounds (merged note eval-gates-live-216-2026-11-18.md): 7 of 7 model-path citations valid, refusals 10 of 10, but only 9 model calls reached the model and the raw container output was not retained.
* Plan for this pass: rerun the 30-prompt set in a throwaway server inside ca-cutover-test-demo-api with raw output retained locally, rescore, and rerun the gate unit tests. Stay within authorization.json limits where possible and record any overrun.
* The state file path given in the brief already exists from round 1 (tracked); it is overwritten for this pass and earlier content stays in git history.
