<!-- markdownlint-disable-file -->
# Research: issue 948 accepted-proposal drops not counted as regressions

Disposition: executed. Planning Readiness: Ready.

## Prior delivery check

* Merged PR search for 948: none delivered. The grader came from the #909 slice (candidate comparison, issue 108); no later change touches regression counting.

## Evidence

* `candidate_comparison._verdict` flags a regression only when one of `critical_misses`, `unsupported_claims`, `overrides`, `reopened_cases` is higher than the baseline.
* Candidates must cover the same case ids as the baseline, so a candidate can set `accepted=False` on a case the baseline accepted. That lowers cost-per-accepted denominators in a misleading way (fewer accepted, same cost) or raises it, but was never a regression; a cheaper candidate that quietly loses accepted proposals could be reported "cheaper without a recorded regression".

## Smallest fix

* Add `dropped_accepted_proposals`: count of cases the baseline accepted that the candidate did not accept. Add it to `REGRESSIONS` (baseline value 0) so any drop makes the verdict `failure`. Candidates that accept more than the baseline are not penalised.
* Document in the module docstring and `src/agents/README.md`.
* Focused tier; pure offline grader, not security, infrastructure, SQL or deployment. No approval, price or model decision is implied.

## Acceptance criteria

* Dropping an accepted proposal increments the regression count: met (`dropped_accepted_proposals` counted and listed in `verdict.regressions`).
* A test covers the drop case: met.
