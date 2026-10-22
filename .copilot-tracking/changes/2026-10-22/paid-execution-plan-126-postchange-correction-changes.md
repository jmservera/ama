<!-- markdownlint-disable-file -->
# Changes: paid-execution-plan-126-postchange-correction

* Task ID: 126-postchange-correction
* Plan: .copilot-tracking/plans/2026-10-22/paid-execution-plan-126-postchange-correction-plan.md
* Declared scope: P01 implemented; P02 (gate, push, PR) recorded in the PR and external receipt.

## Evidence (read-only)

* Inventory about 14:53Z: 91 resources; no Front Door profile or WAF policy; demo API app minimum and running replicas 0; 61 cutover-test names remain.
* Cost read about 14:53Z identical to 14:00Z (242.36; 22 Oct partial 9.43). Subscription scope not retried. No Azure change made; no identifiers recorded.
* Start state: clean tree, head a4df6a04, origin/main 9e55a392 (no rebase needed: zero commits behind).

## Edits

* docs/case_study_48_addendum.md: relabelled the 14:00Z evidence, table rows, admissible-U limits and observed-versus-forecast text as a PRE-CHANGE scenario (credits no unmeasured saving, not an upper bound, not current); added a dated post-change note and a refresh gate; rewrote the retirement sentence to distinguish this proposal's non-authorization from the separately authorized, completed cutover-test deletion; withdrew "S0 is the only current baseline"; qualified T1 and the 403 statement; added a dated note to history row S1. Ceiling, thresholds and tranche bounds unchanged; history preserved.
* docs/reference/README.md: index row states the pre-change status.
* docs/reference/log.md: one appended entry superseding earlier wording; no earlier entry edited.

## Validation so far

* Arithmetic recomputed unchanged: 535.33, 164.67, 89.67.
* Remaining "no change" and "only current" hits are inside the dated history block.
* Identifier search over additions: none.
* New gate and receipt: pending; recorded in the PR.

## Divergences

* None. Critique PC-001 to PC-007 applied. Authorization of the cutover-test deletion rests on the coordinator's report, not a repository record.
